# 🤖 AI App Builder

An AI-powered tool that converts a plain-English prompt into a fully working
web application. Type *"build me a calculator"* and it writes complete
**HTML + CSS + JavaScript** files and opens them in your browser automatically.

---

## 📌 Overview

AI App Builder is a multi-agent system built with LangChain and LangGraph.
It runs four AI agents in a pipeline — Planner, Architect, Coder, and Verifier —
each with a specific role, working together like a small software team.
The output is a ready-to-run web app saved in its own folder on your machine.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| Agent Framework | LangGraph, LangChain |
| LLM Provider | OpenRouter (free tier) |
| Data Validation | Pydantic v2 |
| Config | python-dotenv |

---

## ❓ Problem It Solves

Building even a small web app requires writing boilerplate HTML, styling it with
CSS, and wiring up JavaScript logic — repetitive work that takes time.
AI App Builder removes that entirely. You describe what you want in one sentence
and the system generates all three files, verifies they are correct, and opens
the result in your browser. No coding, no setup, no npm required.

---

## ✨ Features

- **Multi-agent pipeline** — four agents (Planner → Architect → Coder → Verifier) handle planning, coding, saving, and quality checking automatically
- **Self-healing output** — the Verifier node reads every file after writing and auto-repairs anything that is empty or missing
- **Fallback model chain** — tries 5 free LLM models in order so a rate-limited model never crashes the pipeline
- **Pure HTML/CSS/JS output** — generated apps open directly in any browser, no build tools needed
- **Dynamic project folders** — each app is saved in its own named folder (e.g. `calculator_app/`)
- **Path traversal protection** — all file writes are sandboxed to the project folder

---

## 🏁 Conclusion
AI App Builder is a practical example of how multi-agent AI systems can automate
real development tasks. By combining LangGraph's stateful pipeline with structured
LLM output and a self-healing Verifier node, the project goes beyond a simple
chatbot and acts like an autonomous mini development team.
Whether you are a beginner who wants to skip boilerplate or a developer exploring
agentic AI architecture, this project shows how to break a complex task into
smaller, reliable agent-driven steps — a pattern that scales to much larger
real-world problems.

## 📄 License

MIT — free to use and modify.