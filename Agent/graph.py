import os
import time
import random
import pathlib
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END
from google.api_core.exceptions import ResourceExhausted, GoogleAPICallError

from Agent.prompts import planner_prompt, architect_prompt, coder_system_prompt
from Agent.states import AppState, Plan, TaskPlan, CoderState
from Agent.tools import (
    write_file,
    read_file,
    get_current_directory,
    list_files,
    set_project_root,
    get_project_root,
)

load_dotenv()

# ── Model list (Gemini models, best → fallback) ──────────────────────────────
# gemini-2.5-flash is the most capable for generating complex, long code files.
# Lite variants are used as fallback when the primary hits rate limits.
_MODELS = [
    "gemini-3.1-flash-lite",
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-1.5-flash",
]

_API_KEY = os.getenv("GOOGLE_GEMINI_API_KEY")

if not _API_KEY:
    raise RuntimeError(
        "Missing GOOGLE_GEMINI_API_KEY. Add it to your local .env file before running the app."
    )


def _make_llm(model: str) -> ChatGoogleGenerativeAI:
    return ChatGoogleGenerativeAI(
        model=model,
        temperature=0.3,       # slightly higher creativity for richer code
        google_api_key=_API_KEY,
        timeout=300,           # complex apps need up to 5 minutes to generate
    )



try:
    from openai import RateLimitError, APIStatusError
except ImportError:
    RateLimitError = type("RateLimitError", (Exception,), {})
    APIStatusError = type("APIStatusError", (Exception,), {})


def _invoke_with_fallback(chain_factory, prompt: str, label: str = "LLM"):
    """
    Try _MODELS in order. For each model retry up to 3x on 429 with backoff.
    chain_factory: callable(llm) -> LangChain Runnable
    """
    last_exc = None
    for model in _MODELS:
        llm   = _make_llm(model)
        chain = chain_factory(llm)
        for attempt in range(1, 4):
            try:
                print(f"  [{label}] {model}  attempt={attempt}")
                result = chain.invoke(prompt)
                if result is not None:
                    return result
                print(f"  [{label}] got None from {model} -- next model")
                break
            except (RateLimitError, ResourceExhausted) as e:
                wait = 2 ** attempt + random.uniform(0, 1)
                print(f"  [{label}] 429 on {model} attempt {attempt}/3 -- wait {wait:.1f}s")
                last_exc = e
                if attempt < 3:
                    time.sleep(wait)
                else:
                    print(f"  [{label}] retries exhausted -- next model")
            except (APIStatusError, GoogleAPICallError, Exception) as e:
                err_str = str(e).lower()
                status_code = getattr(e, "status_code", None) or getattr(e, "code", None)
                if status_code in (404, 400) or "404" in err_str or "not found" in err_str or "not supported" in err_str or "invalid argument" in err_str:
                    print(f"  [{label}] {model} not available ({e}) -- next model")
                    last_exc = e
                    break
                elif "429" in err_str or "quota" in err_str or "resource_exhausted" in err_str:
                    wait = 2 ** attempt + random.uniform(0, 1)
                    print(f"  [{label}] 429/quota on {model} attempt {attempt}/3 -- wait {wait:.1f}s")
                    last_exc = e
                    if attempt < 3:
                        time.sleep(wait)
                    else:
                        print(f"  [{label}] retries exhausted -- next model")
                else:
                    print(f"  [{label}] error on {model}: {e} -- next model")
                    last_exc = e
                    break
    raise RuntimeError(f"[{label}] all models exhausted. Last: {last_exc}") from last_exc


# ── Node 1: Planner ───────────────────────────────────────────────────────────

def planner_agent(state: AppState) -> AppState:
    """Turn the user prompt into a structured Plan (name, files, features)."""
    user_prompt: str = state["user_prompt"]
    plan: Plan = _invoke_with_fallback(
        chain_factory=lambda llm: llm.with_structured_output(Plan),
        prompt=planner_prompt(user_prompt),
        label="Planner",
    )
    set_project_root(plan.name)
    print(f"[Planner] '{plan.name}' | files: {[f.path for f in plan.files]}")
    return {"plan": plan}


# ── Node 2: Architect ─────────────────────────────────────────────────────────

def architect_agent(state: AppState) -> AppState:
    """
    Generate a TaskPlan where each task contains the COMPLETE source code
    for its file (in the full_code field).  This is the single LLM call
    that actually writes the code — the coder node just persists it to disk.
    """
    plan: Plan = state["plan"]
    task_plan: TaskPlan = _invoke_with_fallback(
        chain_factory=lambda llm: llm.with_structured_output(TaskPlan),
        prompt=architect_prompt(plan.model_dump_json()),
        label="Architect",
    )
    # Validate filepaths match the plan
    plan_paths = {f.path for f in plan.files}
    for step in task_plan.implementation_steps:
        if step.filepath not in plan_paths:
            # Best-effort fuzzy fix: use the closest plan path
            basename = pathlib.Path(step.filepath).name
            for p in plan_paths:
                if pathlib.Path(p).name == basename:
                    print(f"  [Architect] filepath fix: '{step.filepath}' → '{p}'")
                    step.filepath = p
                    break

    print(f"[Architect] {len(task_plan.implementation_steps)} file(s) planned.")
    return {"task_plan": task_plan}


# ── Node 3: Coder (deterministic — no LLM) ───────────────────────────────────

def coder_agent(state: AppState) -> AppState:
    """
    Write the next file to disk using the full_code from the architect's TaskPlan.
    No LLM is called here — this is pure Python I/O.

    Why: ReAct agents on free models frequently forget to call write_file,
    return truncated content, or respond with commentary instead of code.
    Separating code-generation (architect) from file I/O (coder) eliminates
    all of those failure modes.
    """
    coder_state: CoderState = state.get("coder_state")
    if coder_state is None:
        coder_state = CoderState(task_plan=state["task_plan"], current_step_idx=0)

    steps = coder_state.task_plan.implementation_steps
    idx   = coder_state.current_step_idx

    if idx >= len(steps):
        return {"coder_state": coder_state, "status": "DONE"}

    task = steps[idx]
    print(f"[Coder] Writing {idx + 1}/{len(steps)}: {task.filepath}")

    code = task.full_code.strip()
    if not code:
        print(f"  [Coder] WARNING: full_code is empty for {task.filepath} — skipping.")
    else:
        result = write_file.run({"path": task.filepath, "content": code})
        print(f"  [Coder] {result}")

    coder_state = CoderState(
        task_plan=coder_state.task_plan,
        current_step_idx=idx + 1,
    )
    return {"coder_state": coder_state}


# ── Node 4: Verifier ──────────────────────────────────────────────────────────

def verifier_agent(state: AppState) -> AppState:
    """
    Check every planned file exists and has non-trivial content.
    If a file is missing or empty, re-write it from the TaskPlan's full_code.
    This is the safety net that catches silent write failures.
    """
    plan: Plan          = state["plan"]
    task_plan: TaskPlan = state["task_plan"]

    code_by_path = {t.filepath: t.full_code for t in task_plan.implementation_steps}
    all_ok = True

    for file in plan.files:
        content = read_file.run(file.path)
        if not content or len(content.strip()) < 50:
            print(f"[Verifier] '{file.path}' missing or too short — re-writing.")
            code = code_by_path.get(file.path, "").strip()
            if code:
                result = write_file.run({"path": file.path, "content": code})
                print(f"  [Verifier] {result}")
            else:
                print(f"  [Verifier] No code available for '{file.path}' — cannot fix.")
                all_ok = False
        else:
            print(f"[Verifier] '{file.path}' OK ({len(content)} chars)")

    return {"status": "DONE" if all_ok else "PARTIAL"}


# ── Routing ───────────────────────────────────────────────────────────────────

def _coder_router(state: AppState) -> str:
    """Loop coder until all steps are done, then go to verifier."""
    if state.get("status") == "DONE":
        return "verifier"
    cs: CoderState = state.get("coder_state")
    if cs is None:
        return "coder"
    if cs.current_step_idx >= len(cs.task_plan.implementation_steps):
        return "verifier"
    return "coder"


# ── Graph ─────────────────────────────────────────────────────────────────────

graph = StateGraph(AppState)

graph.add_node("planner",   planner_agent)
graph.add_node("architect", architect_agent)
graph.add_node("coder",     coder_agent)
graph.add_node("verifier",  verifier_agent)

graph.add_edge(START,        "planner")
graph.add_edge("planner",    "architect")
graph.add_edge("architect",  "coder")
graph.add_conditional_edges("coder", _coder_router, {"coder": "coder", "verifier": "verifier"})
graph.add_edge("verifier",   END)

agent = graph.compile()