# AI-Assisted URL Shortener Service

A production-grade, AI-assisted URL shortener built with Python 3.11, FastAPI, SQLite, and YAML configuration management[cite: 1].

## Architectural Overview
* **Web Engine:** FastAPI (ASGI framework)
* **Configuration Manager:** PyYAML + Pydantic Settings Schema (`config/config.yaml`)
* **Persistence:** SQLite with atomic link analytics tracking
* **CLI Tool:** `click` + `httpx` for terminal interactions
* **CI/CD Quality Gate:** GitHub Actions workflow running `flake8`, `mypy`, and `pytest` test coverage

---

## Quickstart Guide

### 1. Installation
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt

2. Run Application Server
Bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

3. Run CLI Interface
# Shorten a URL
python -m app.cli shorten [https://google.com](https://google.com) --custom mygoog

# Check Analytics
python -m app.cli analytics mygoog

4. Run Test Suite & Quality Gates
pytest --cov=app tests/

5. Run with Docker
docker-compose up --build

Execution Logs & AI Traceability

Greenfield Scenario Execution

[cite: 1]

Brownfield Scenario Execution

[cite: 1]

Ambiguous Scenario Execution

[cite: 1]
