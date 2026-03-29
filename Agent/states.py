from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, TypedDict


# ── Structured-output models (Pydantic) ───────────────────────────────────────

class File(BaseModel):
    path: str = Field(
        description=(
            "Relative file path inside the project folder. "
            "For web apps use ONLY: 'index.html', 'style.css', 'script.js'. "
            "Never use subdirectories or framework files."
        )
    )
    purpose: str = Field(description="One sentence: what this file does.")


class Plan(BaseModel):
    name: str = Field(
        description=(
            "Lowercase app name, underscores only, no spaces. "
            "Examples: 'calculator_app', 'todo_app', 'color_picker'."
        )
    )
    description: str = Field(description="One sentence describing the app.")
    techstack: str = Field(
        description="Always 'HTML, CSS, JavaScript' for frontend apps. No frameworks."
    )
    features: list[str] = Field(description="3-5 concrete, specific features.")
    files: list[File] = Field(
        description=(
            "Exactly 3 files for web apps: index.html, style.css, script.js. "
            "No more, no less."
        )
    )


class ImplementationTask(BaseModel):
    filepath: str = Field(
        description="Exact path — must match one of the paths in the Plan's files list."
    )
    task_description: str = Field(
        description=(
            "COMPLETE implementation spec: every HTML id/class, every CSS rule, "
            "every JS function signature and body logic. Must be long and detailed."
        )
    )
    full_code: str = Field(
        description=(
            "The COMPLETE, READY-TO-SAVE file content. "
            "This must be 100% working code — not pseudocode, not a skeleton. "
            "Include every tag, rule, and function."
        )
    )


class TaskPlan(BaseModel):
    implementation_steps: list[ImplementationTask] = Field(
        description=(
            "One task per file, ordered: index.html first, style.css second, script.js third."
        )
    )
    model_config = ConfigDict(extra="allow")


class CoderState(BaseModel):
    task_plan: TaskPlan
    current_step_idx: int = Field(0)
    model_config = ConfigDict(arbitrary_types_allowed=True)


# ── LangGraph graph state ──────────────────────────────────────────────────────

class AppState(TypedDict, total=False):
    user_prompt: str
    plan: Optional[Plan]
    task_plan: Optional[TaskPlan]
    coder_state: Optional[CoderState]
    status: str