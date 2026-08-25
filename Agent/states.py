from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, TypedDict, Literal


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
            "Examples: 'finance_dashboard', 'study_planner', 'calculator_app'."
        )
    )
    description: str = Field(
        description=(
            "2-3 sentences describing what the app does, its main purpose, "
            "and who it is for."
        )
    )
    techstack: str = Field(
        description="Always 'HTML, CSS, JavaScript' for frontend apps. No frameworks."
    )
    complexity: Literal["simple", "moderate", "complex"] = Field(
        default="moderate",
        description=(
            "App complexity level. "
            "'simple' = single-purpose tool (calculator, timer, converter). "
            "'moderate' = multi-feature utility (todo+categories, quiz app). "
            "'complex' = multi-section dashboard or productivity system with "
            "LocalStorage, charts, filters, themes, and 10+ features."
        )
    )
    features: list[str] = Field(
        description=(
            "Exhaustive list of ALL features the app must have. "
            "For simple apps: 5-8 features. "
            "For moderate apps: 8-12 features. "
            "For complex/dashboard apps: 12-20 features. "
            "Each feature must be concrete and testable — describe what the user "
            "can do, not how it looks. Include every feature the user mentioned, "
            "plus obvious supporting features needed for completeness."
        )
    )
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
            "every JS function signature and body logic. Must be long and detailed. "
            "For complex apps this should be 3-5 paragraphs."
        )
    )
    full_code: str = Field(
        description=(
            "The COMPLETE, READY-TO-SAVE file content. "
            "This must be 100% working code — not pseudocode, not a skeleton. "
            "Include every tag, rule, and function. "
            "For complex apps, script.js will naturally be 500-1500+ lines — "
            "that is expected and correct. Never truncate or abbreviate."
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