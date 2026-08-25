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
| Language | Python 3.10+ |
| Web Framework | FastAPI, Uvicorn |
| Agent Framework | LangGraph, LangChain |
| LLM Provider | Google Gemini API |
| Data Validation | Pydantic v2 |
| Config | python-dotenv |

## Setup

1. Create a local `.env` file:

```env
GOOGLE_GEMINI_API_KEY=your_gemini_api_key_here
```

2. Install dependencies:

```bash
pip install -r Requirements.txt
```

3. Run the app:

```bash
python main.py
```

Open your browser at `http://localhost:8000` to start building apps!

## Deployment (Render)

- **Build Command**: `pip install -r Requirements.txt`
- **Start Command**: `python main.py`
- **Environment Variables**: Add `GOOGLE_GEMINI_API_KEY` in Render dashboard.

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
