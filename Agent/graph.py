import os
import time
import random
import pathlib
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END
from google.api_core.exceptions import ResourceExhausted, GoogleAPICallError

from Agent.prompts import (
    planner_prompt,
    html_prompt,
    css_prompt,
    js_prompt,
)
from Agent.states import (
    AppState,
    Plan,
    HTMLCode,
    CSSCode,
    JSCode,
)
from Agent.tools import (
    write_file,
    read_file,
    set_project_root,
    get_project_root,
)

load_dotenv()

# ── Model list (Gemini models, best → fallback) ──────────────────────────────
# gemini-2.5-flash is the primary model for generating long, high-quality code.
# Lite/1.5 variants are used as fallback if rate limits are hit.
_MODELS = [
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-1.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-2.0-flash-lite",
]

_API_KEY = os.getenv("GOOGLE_GEMINI_API_KEY")

if not _API_KEY:
    raise RuntimeError(
        "Missing GOOGLE_GEMINI_API_KEY. Add it to your local .env file before running the app."
    )


def _make_llm(model: str) -> ChatGoogleGenerativeAI:
    return ChatGoogleGenerativeAI(
        model=model,
        temperature=0.3,
        google_api_key=_API_KEY,
        timeout=300,
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


# ── Node 1: Planner Agent ─────────────────────────────────────────────────────

def planner_agent(state: AppState) -> AppState:
    """Turn the user prompt into an exhaustive, structured Plan."""
    user_prompt: str = state["user_prompt"]
    plan: Plan = _invoke_with_fallback(
        chain_factory=lambda llm: llm.with_structured_output(Plan),
        prompt=planner_prompt(user_prompt),
        label="Planner",
    )
    set_project_root(plan.name)
    print(f"[Planner] Plan '{plan.name}' ready | {len(plan.features)} features planned.")
    return {"plan": plan}


# ── Node 2: HTML Architect Agent ──────────────────────────────────────────────

def html_agent(state: AppState) -> AppState:
    """Generate the complete, modern, semantic index.html markup."""
    user_prompt: str = state["user_prompt"]
    plan: Plan = state["plan"]

    print("[HTML Architect] Generating complete index.html...")
    result: HTMLCode = _invoke_with_fallback(
        chain_factory=lambda llm: llm.with_structured_output(HTMLCode),
        prompt=html_prompt(plan.model_dump_json(), user_prompt),
        label="HTML Architect",
    )
    html_code = result.code.strip()
    write_file.run({"path": "index.html", "content": html_code})
    print(f"[HTML Architect] index.html written ({len(html_code)} chars).")
    return {"html_code": html_code}


# ── Node 3: CSS Stylist Agent ─────────────────────────────────────────────────

def css_agent(state: AppState) -> AppState:
    """Generate the complete, stunning modern CSS design system."""
    plan: Plan = state["plan"]
    html_code: str = state["html_code"]

    print("[CSS Stylist] Generating complete style.css design system...")
    result: CSSCode = _invoke_with_fallback(
        chain_factory=lambda llm: llm.with_structured_output(CSSCode),
        prompt=css_prompt(plan.model_dump_json(), html_code),
        label="CSS Stylist",
    )
    css_code = result.code.strip()
    write_file.run({"path": "style.css", "content": css_code})
    print(f"[CSS Stylist] style.css written ({len(css_code)} chars).")
    return {"css_code": css_code}


# ── Node 4: JS Engineer Agent ─────────────────────────────────────────────────

def js_agent(state: AppState) -> AppState:
    """Generate complete, bug-free, fully implemented JavaScript logic."""
    plan: Plan = state["plan"]
    html_code: str = state["html_code"]
    css_code: str = state["css_code"]

    print("[JS Engineer] Generating complete script.js logic...")
    result: JSCode = _invoke_with_fallback(
        chain_factory=lambda llm: llm.with_structured_output(JSCode),
        prompt=js_prompt(plan.model_dump_json(), html_code, css_code),
        label="JS Engineer",
    )
    js_code = result.code.strip()
    write_file.run({"path": "script.js", "content": js_code})
    print(f"[JS Engineer] script.js written ({len(js_code)} chars).")
    return {"js_code": js_code}


# ── Node 5: Verifier Agent ────────────────────────────────────────────────────

def verifier_agent(state: AppState) -> AppState:
    """Verify all 3 files exist on disk and have rich content."""
    all_ok = True
    for fname in ("index.html", "style.css", "script.js"):
        content = read_file.run(fname)
        if not content or len(content.strip()) < 100:
            print(f"[Verifier] WARNING: '{fname}' is missing or too short ({len(content)} chars).")
            all_ok = False
        else:
            print(f"[Verifier] '{fname}' verified OK ({len(content)} chars).")

    return {"status": "DONE" if all_ok else "PARTIAL"}


# ── Graph Definition ──────────────────────────────────────────────────────────

graph = StateGraph(AppState)

graph.add_node("planner",      planner_agent)
graph.add_node("html_coder",   html_agent)
graph.add_node("css_coder",    css_agent)
graph.add_node("js_coder",     js_agent)
graph.add_node("verifier",     verifier_agent)

graph.add_edge(START,        "planner")
graph.add_edge("planner",    "html_coder")
graph.add_edge("html_coder", "css_coder")
graph.add_edge("css_coder",  "js_coder")
graph.add_edge("js_coder",   "verifier")
graph.add_edge("verifier",   END)

agent = graph.compile()