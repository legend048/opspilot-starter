from pathlib import Path
import csv, datetime

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True, parents=True)
CSV_FILE = DATA_DIR / "sheets.csv"

def append_row(context: dict):
    run = context["run"]
    cl = run.classification
    row = [datetime.datetime.utcnow().isoformat(), run.id, cl.type, cl.priority, cl.owner_hint]
    write_header = not CSV_FILE.exists()
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if write_header:
            w.writerow(["timestamp", "run_id", "type", "priority", "owner"])
        w.writerow(row)
