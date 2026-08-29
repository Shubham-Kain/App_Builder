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
            "Examples: 'study_planner', 'finance_dashboard', 'habit_tracker'."
        )
    )
    title: str = Field(
        default="Web Application",
        description="User-facing title of the app (e.g. 'Smart Study Planner & Productivity Dashboard')"
    )
    description: str = Field(
        description=(
            "2-3 sentences describing what the app does, its target audience, "
            "and core workflows."
        )
    )
    techstack: str = Field(
        default="HTML, CSS, JavaScript",
        description="Always 'HTML, CSS, JavaScript' for pure frontend apps. No frameworks."
    )
    complexity: Literal["simple", "moderate", "complex"] = Field(
        default="complex",
        description=(
            "App complexity level. "
            "'simple' = single-purpose tool. "
            "'moderate' = multi-feature utility. "
            "'complex' = multi-section dashboard with LocalStorage, charts, filters, modals, and comprehensive UI."
        )
    )
    features: list[str] = Field(
        description=(
            "Exhaustive, autonomous list of ALL features to implement. "
            "ALWAYS list 20-30 concrete, testable features regardless of how brief the user prompt is. "
            "Add standard domain features autonomously even if not mentioned by the user. "
            "Include CRUD, dashboard metrics, specialized tools, analytics, search/filters, "
            "gamification (streaks/scores), settings, CSV export, and countdown/deadline features."
        )
    )
    nav_tabs: list[str] = Field(
        default=[
            "Overview Dashboard",
            "Main Manager",
            "Specialized Tool",
            "Categories & Goals",
            "Analytics & Charts",
            "Timeline & Reports",
            "Settings & Export",
        ],
        description=(
            "Exactly 7 sidebar navigation tab names tailored to the specific app domain. "
            "Examples for Study: ['Overview Dashboard', 'Task Planner', 'Pomodoro Focus', "
            "'Subjects & Topics', 'Analytics & Charts', 'Exam Countdown', 'Settings & Export']. "
            "Examples for Finance: ['Overview Dashboard', 'Transaction Log', 'Budget Tracker', "
            "'Categories & Goals', 'Spending Analytics', 'Monthly Reports', 'Settings & Export']."
        )
    )
    data_models: list[str] = Field(
        default=["items", "categories", "sessions", "goals", "settings"],
        description=(
            "5-8 LocalStorage data model/entity names for the app. "
            "Examples for Study: ['tasks', 'subjects', 'pomodoro_sessions', 'exams', 'settings']. "
            "Examples for Finance: ['transactions', 'categories', 'budgets', 'goals', 'monthly_summaries', 'settings']. "
            "Each model name should be lowercase with underscores."
        )
    )
    files: list[File] = Field(
        default=[
            File(path="index.html", purpose="Complete semantic HTML — 7 tab panes, sidebar, topbar, 6 metric cards, 4+ modals, all interactive elements"),
            File(path="style.css", purpose="Full premium design system — dark/light theme, glassmorphism, animations, all components styled, 700+ lines"),
            File(path="script.js", purpose="Complete app logic — multi-model LocalStorage CRUD, charts, timers, filters, CSV export, 900+ lines"),
        ],
        description="Exactly 3 files: index.html, style.css, script.js."
    )


class HTMLCode(BaseModel):
    code: str = Field(
        description=(
            "The COMPLETE, exhaustive index.html file content. "
            "Must start with <!DOCTYPE html> and contain all layout sections, sidebar, header, tabs, metric cards, "
            "modals, buttons with IDs, and form elements. NEVER truncate."
        )
    )


class CSSCode(BaseModel):
    code: str = Field(
        description=(
            "The COMPLETE, exhaustive style.css file content. "
            "Must include full design system tokens, dark & light theme, glassmorphism, responsive grid, "
            "hover effects, animations, modal styling, and component styles for every HTML element. NEVER truncate."
        )
    )


class JSCode(BaseModel):
    code: str = Field(
        description=(
            "The COMPLETE, exhaustive script.js file content. "
            "Must include full LocalStorage CRUD, default initial sample data, timer engine, productivity score algorithm, "
            "streak counter, event handlers for every button/tab/form, CSV export, and toast notifications. NEVER truncate."
        )
    )


# ── LangGraph graph state ──────────────────────────────────────────────────────

class AppState(TypedDict, total=False):
    user_prompt: str
    plan: Optional[Plan]
    html_code: Optional[str]
    css_code: Optional[str]
    js_code: Optional[str]
    status: str