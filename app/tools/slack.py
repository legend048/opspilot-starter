import os, json
from dotenv import load_dotenv
import httpx
from ..models import Run
from pathlib import Path

load_dotenv()
WEBHOOK = os.getenv("SLACK_WEBHOOK_URL", "").strip()
PUBLIC_BASE = os.getenv("PUBLIC_BASE_URL", "").strip() or "http://localhost:8000"
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True, parents=True)
LOG_FILE = DATA_DIR / "slack.log"

def _post(payload: dict):
    if WEBHOOK:
        httpx.post(WEBHOOK, json=payload, timeout=10)
    else:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(payload) + "\n")

def send_approval_request(context: dict):
    run: Run = context["run"]
    approve = f"{PUBLIC_BASE}/approve/{run.id}?decision=approve"
    reject = f"{PUBLIC_BASE}/approve/{run.id}?decision=reject"
    text = f"Approval needed for run {run.id} (event {run.event_id}). Approve: {approve} | Reject: {reject}"
    _post({"text": text})

def send_summary(context: dict):
    run: Run = context["run"]
    cl = run.classification
    text = f"[{cl.priority}] {cl.type} handled. Run {run.id} for event {run.event_id} is {run.status}."
    _post({"text": text})
