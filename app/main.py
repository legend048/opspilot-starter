from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Dict, Any
from pathlib import Path
import json, time
from .models import InboundEvent, Run
from .services.classifier import classify
from .services.runbooks import plan_runbook
from .services.toolrouter import run_actions

app = FastAPI(title="OpsPilot Starter")
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))

STATE_FILE = Path(__file__).parent / "data" / "state.json"
STATE_FILE.parent.mkdir(parents=True, exist_ok=True)

def _load_state() -> Dict[str, Any]:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"events": [], "runs": []}

def _save_state(state: Dict[str, Any]):
    STATE_FILE.write_text(json.dumps(state, indent=2))

@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    state = _load_state()
    # Sort newest first
    events = sorted(state["events"], key=lambda e: e["received_at"], reverse=True)
    runs = sorted(state["runs"], key=lambda r: r["created_at"], reverse=True)
    return templates.TemplateResponse("index.html", {"request": request, "events": events, "runs": runs})

@app.post("/ingest")
def ingest(event: InboundEvent):
    state = _load_state()
    state["events"].append(json.loads(event.model_dump_json()))
    _save_state(state)

    cl = classify(event.payload, event.source)

    actions = plan_runbook(cl)

    run = Run(event_id=event.id, classification=cl, actions=actions)
    # If first action is human approval, pause
    if actions and actions[0] == "request_approval":
        run.status = "waiting_approval"
        ctx = {"event": event, "run": run.model_copy(deep=True)}
        tool_calls = run_actions(["request_approval"], ctx)
        run.tool_calls.extend(tool_calls)
    else:
        ctx = {"event": event, "run": run.model_copy(deep=True)}
        tool_calls = run_actions(actions, ctx)
        run.tool_calls.extend(tool_calls)
        run.status = "done" if all(tc.status == "ok" for tc in tool_calls) else "failed"

    state = _load_state()
    state["runs"].append(json.loads(run.model_dump_json()))
    _save_state(state)

    return JSONResponse({"event_id": event.id, "run_id": run.id, "status": run.status, "classification": cl.model_dump(), "actions": actions})

@app.get("/approve/{run_id}")
def approve(run_id: str, decision: str = Query("approve")):
    state = _load_state()
    run = next((r for r in state["runs"] if r["id"] == run_id), None)
    if not run:
        return JSONResponse({"error": "run not found"}, status_code=404)
    if run["status"] != "waiting_approval":
        return RedirectResponse(url="/", status_code=302)

    # Find original event
    ev = next((e for e in state["events"] if e["id"] == run["event_id"]), None)

    if decision == "approve":
        remaining = [a for a in run["actions"] if a != "request_approval"]
        from .models import InboundEvent as _Evt, Run as _Run, Classification as _Cl, ToolCall as _Tc
        ev_obj = _Evt(**ev)
        cl_obj = _Cl(**run["classification"])
        run_obj = _Run(**run)
        ctx = {"event": ev_obj, "run": run_obj.model_copy(deep=True)}
        calls = run_actions(remaining, ctx)
        run["tool_calls"].extend([json.loads(c.model_dump_json()) for c in calls])
        run["status"] = "done" if all(c.status == "ok" for c in calls) else "failed"
    else:
        run["status"] = "failed"
        run["notes"] = (run.get("notes") or "") + " Rejected by human."

    for i, r in enumerate(state["runs"]):
        if r["id"] == run_id:
            state["runs"][i] = run
            break
    _save_state(state)
    return RedirectResponse(url="/", status_code=302)
