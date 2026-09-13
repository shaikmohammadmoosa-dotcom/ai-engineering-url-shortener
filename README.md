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

## Execution Logs & AI Traceability

### Greenfield Scenario Execution
* **Intent:** Build core FastAPI URL shortener with Base62 short code generation, SQLite persistence, and Pydantic validation.
* **Prompt Strategy:** Structured prompt requesting async endpoint handlers, schema definitions, and atomic database creation.
* **AI Output & Validation:** Generated initial FastAPI boilerplate and SQLite connection setup. Validated via local curl requests and manual database checks.

### Brownfield Scenario Execution
* **Intent:** Integrate CLI tool (`click` + `httpx`) and Click Analytics endpoint into the existing codebase without breaking existing shortener endpoints.
* **Prompt Strategy:** Context-aware prompts providing existing `app/main.py` models to generate non-destructive schema additions for click counters.
* **AI Output & Validation:** Generated CLI commands in `app/cli.py` and modified DB schema to include UTC creation timestamps and atomic click counters. Tested using `pytest`.

### Ambiguous Scenario Execution
* **Intent:** Resolve non-deterministic CI failures caused by Python pathing (`ModuleNotFoundError`) and timezone deprecation in Python 3.11+.
* **Prompt Strategy:** Provided raw GitHub Actions runtime logs and asked for root-cause analysis and structural fixes.
* **AI Output & Validation:** 
  * Replaced deprecated `datetime.utcnow()` with `datetime.now(timezone.utc)`.
  * Configured `PYTHONPATH: .` inside `.github/workflows/ci.yml`.
  * Added `--max-line-length=120` to `flake8` execution in CI runner.
  ### Automated Testing & Reporting
* **Test Suite:** Pytest coverage across all core endpoints (`/shorten`, `/{short_code}`, `/analytics/{short_code}`).
* **Visual Artifacts:** Every CI run automatically generates and uploads an interactive **HTML Test & Coverage Report** (`report.html`), accessible directly under the GitHub Actions run summary.
