import argparse
import os
import sys
import traceback
import webbrowser

from Agent.graph import agent
from Agent.states import Plan


def main() -> None:
    parser = argparse.ArgumentParser(description="App Builder — generate web apps with AI")
    parser.add_argument(
        "--recursion-limit", "-r",
        type=int, default=50,
        help="LangGraph recursion limit (default: 50).",
    )
    args = parser.parse_args()

    try:
        user_prompt = input("Enter your project prompt: ").strip()
        if not user_prompt:
            print("No prompt provided.")
            sys.exit(1)

        print("\n═══ Starting App Builder ═══\n")
        result = agent.invoke(
            {"user_prompt": user_prompt},
            {"recursion_limit": args.recursion_limit},
        )

        plan: Plan | None = result.get("plan")
        status = result.get("status", "unknown")
        print(f"\n═══ Pipeline finished — status: {status} ═══\n")

        if plan:
            project_folder = os.path.join(os.getcwd(), plan.name)
            index_html     = os.path.join(project_folder, "index.html")
            if os.path.exists(index_html):
                print(f"Opening {index_html} …")
                webbrowser.open(f"file:///{os.path.abspath(index_html)}")
            else:
                print(f"index.html not found in {project_folder}")
                print("Files present:")
                for f in os.listdir(project_folder):
                    print(f"  {f}")

    except KeyboardInterrupt:
        print("\nCancelled.")
        sys.exit(0)
    except Exception:
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()