# Trade Opportunities API (FastAPI) — Prototype

This project provides a prototype FastAPI service that analyzes market data and returns a markdown trade-opportunity report for a requested sector (India-focused).

## Files
- main.py : FastAPI app (single-file demo)
- requirements.txt

## Prerequisites
- Python 3.10+ recommended
- Optional: GEMINI_API_KEY environment variable (for Google Gemini integration). If not set, the app will use a heuristic fallback.

## Setup (venv)
```bash
python -m venv venv
# activate:
# Windows:
#   venv\Scripts\activate
# macOS / Linux:
#   source venv/bin/activate

pip install -r requirements.txt