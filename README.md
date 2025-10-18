# OpsPilot Starter (FastAPI + Jinja2)

**What this is:** a self-contained, hackathon-friendly starter to demo an **AI Operations Command Center**:
- Ingest "events" (invoice emails, complaints, sheet alerts) via an API
- Classify → prioritize → choose a runbook
- Execute actions through a small ToolRouter (Slack/Sheets/Notion stubs)
- Human-in-the-loop approvals via the dashboard buttons or Slack links
- Everything runs locally. Zero external services required.

> Optional: set a `SLACK_WEBHOOK_URL` in `.env` to send real Slack messages. Otherwise actions are logged in `app/data/`.

---

## Quickstart (10 minutes)

1) Install Python 3.10+
2) Create a virtual env and install deps:
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```
3) Copy `.env.example` → `.env` and (optionally) paste a Slack webhook URL.
4) Run the server:
```bash
uvicorn app.main:app --reload --port 8000
```
5) In a new terminal, run the demo script to push sample events:
```bash
bash scripts/run_demo.sh
```
6) Open the dashboard: http://localhost:8000

- Approve/Reject any pending run right from the dashboard.
- All logs & state live in `app/data/`.

---

## Project structure
```
app/
  main.py                # FastAPI app + routes + dashboard
  models.py              # Pydantic models
  services/
    classifier.py        # Simple rule-based classifier (LLM-drop-in spot)
    runbooks.py          # Maps (type, priority) -> action plan
    toolrouter.py        # Executes tools & records tool call telemetry
  tools/
    slack.py             # Optional Slack webhook; else log file
    notion.py            # Stub: logs task creation
    sheets.py            # Stub: appends CSV
  templates/             # Jinja2 HTML templates for the dashboard
  data/                  # State + logs (JSON, CSV, log files)
demo_fixtures/           # Example events to ingest
scripts/
  run_demo.sh            # cURL a few fixtures
```

---

## Where to plug an LLM later
Replace the simple heuristics in `services/classifier.py` with an OpenAI call (or any LLM API) to produce:
```json
{ "type": "invoice|complaint|anomaly|misc", "priority": "P0..P3", "owner_hint": "ops@", "next_action": "..." }
```
Be sure to **do not** log secrets—`toolrouter` already redacts parameters in telemetry.

---

## Persisting to a DB (stretch)
For the hackathon demo, state is in `app/data/state.json`. If you later want Postgres, add SQLAlchemy models and replace the `load_state/save_state` helpers.

---

## Docker (optional)
```bash
# Build
docker build -t opspilot-starter .
# Run
docker run -p 8000:8000 --env-file .env opspilot-starter
```
