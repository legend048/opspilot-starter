from pathlib import Path
import json, datetime

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True, parents=True)
LOG_FILE = DATA_DIR / "notion.log"

def create_task(context: dict):
    run = context["run"]
    cl = run.classification
    record = {
        "at": datetime.datetime.utcnow().isoformat(),
        "run_id": run.id,
        "title": f"{cl.type.upper()} | Owner: {cl.owner_hint} | Priority: {cl.priority}",
        "notes": run.notes or ""
    }
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")
