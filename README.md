# AI App Builder

AI App Builder turns a plain-English prompt into a working frontend app. Give it a request such as "build me a calculator" and it generates the HTML, CSS, and JavaScript files for that app in a dedicated project folder.

## Overview

The project uses a multi-agent pipeline built with LangChain and LangGraph:

- Planner: turns the user prompt into a structured app plan
- Architect: produces full file contents for each planned file
- Coder: writes those files to disk
- Verifier: checks the generated files and repairs missing or empty output

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.13+ |
| Agent Framework | LangGraph, LangChain |
| LLM Provider | OpenRouter |
| Data Validation | Pydantic v2 |
| Config | python-dotenv |

## Setup

1. Create a local `.env` file from the example:

```powershell
Copy-Item .env.example .env
```

2. Open `.env` and set your OpenRouter key:

```env
OPENROUTER_API_KEY=your_real_key_here
```

3. Install dependencies:

```powershell
pip install -e .
```

4. Run the app:

```powershell
python main.py
```

## Security Notes

- `.env` is ignored by Git and must stay local
- Never commit real API keys
- If a key is exposed, rotate it immediately and replace it in your local `.env`

## Features

- Multi-agent generation pipeline
- Automatic file verification and repair
- Fallback model list for better resilience
- Browser-ready HTML, CSS, and JavaScript output
- Separate folder per generated app
- File write safeguards scoped to the project directory

## License

MIT
