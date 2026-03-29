import pathlib
import subprocess
from typing import Optional
from langchain_core.tools import tool

_project_root: Optional[pathlib.Path] = None


def set_project_root(name: str) -> str:
    """Set the output folder from the plan name. Called by planner_agent."""
    global _project_root
    safe = name.strip().replace(" ", "_").lstrip("./\\")
    _project_root = (pathlib.Path.cwd() / safe).resolve()
    _project_root.mkdir(parents=True, exist_ok=True)
    print(f"[Tools] Project root → {_project_root}")
    return str(_project_root)


def get_project_root() -> pathlib.Path:
    if _project_root is None:
        raise RuntimeError("Project root not set. Call set_project_root() first.")
    return _project_root


def _safe_path(path: str) -> pathlib.Path:
    root     = get_project_root()
    resolved = (root / path).resolve()
    if not str(resolved).startswith(str(root)):
        raise ValueError(f"Path '{path}' escapes the project root.")
    return resolved


# ── File tools exposed to the LLM ─────────────────────────────────────────────

@tool
def write_file(path: str, content: str) -> str:
    """
    Write 'content' to 'path' inside the project folder.
    'content' must be the COMPLETE file text — every line.
    Creates parent directories automatically.
    Returns confirmation with the number of bytes written.
    """
    if not content or not content.strip():
        return "ERROR: content is empty — nothing written."
    p = _safe_path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    size = p.stat().st_size
    return f"OK: wrote {size} bytes to {path}"


@tool
def read_file(path: str) -> str:
    """
    Read and return the content of 'path' inside the project folder.
    Returns an empty string if the file does not exist yet.
    """
    p = _safe_path(path)
    if not p.exists():
        return ""
    return p.read_text(encoding="utf-8")


@tool
def get_current_directory() -> str:
    """Return the absolute path of the project folder."""
    return str(get_project_root())


@tool
def list_files(directory: str = ".") -> str:
    """List all files inside the project folder (recursively)."""
    p = _safe_path(directory)
    if not p.is_dir():
        return f"ERROR: '{directory}' is not a directory."
    files = sorted(str(f.relative_to(get_project_root())) for f in p.rglob("*") if f.is_file())
    return "\n".join(files) if files else "No files found."


@tool
def run_cmd(cmd: str, cwd: str = ".", timeout: int = 30) -> str:
    """Run a shell command inside the project folder."""
    cwd_path = _safe_path(cwd)
    try:
        result = subprocess.run(
            cmd, shell=True, cwd=str(cwd_path),
            capture_output=True, text=True, timeout=timeout,
        )
        return f"rc={result.returncode}\nstdout:{result.stdout}\nstderr:{result.stderr}"
    except subprocess.TimeoutExpired:
        return f"ERROR: timed out after {timeout}s"
    except Exception as exc:
        return f"ERROR: {exc}"