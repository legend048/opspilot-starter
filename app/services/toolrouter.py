import time
from typing import List, Dict, Any
from ..models import ToolCall
from ..tools import slack, notion, sheets

REDACT_KEYS = {"token", "secret", "apikey", "api_key", "password", "webhook"}

def redact_params(params: Dict[str, Any]) -> str:
    safe = {}
    for k, v in params.items():
        key = k.lower()
        if any(s in key for s in REDACT_KEYS):
            safe[k] = "***"
        else:
            sv = str(v)
            safe[k] = sv if len(sv) <= 256 else sv[:256] + "..."
    # Compact summary
    items = [f"{k}={v}" for k, v in safe.items()]
    return ", ".join(items)[:500]

def run_actions(actions: List[str], context: Dict[str, Any]) -> List[ToolCall]:
    calls: List[ToolCall] = []
    for action in actions:
        t0 = time.time()
        status = "ok"
        error = None
        try:
            if action == "request_approval":
                slack.send_approval_request(context)
            elif action == "append_sheet":
                sheets.append_row(context)
            elif action == "open_notion":
                notion.create_task(context)
            elif action == "notify_slack":
                slack.send_summary(context)
            else:
                raise ValueError(f"Unknown action: {action}")
        except Exception as e:
            status = "error"
            error = str(e)
        dt = int((time.time() - t0) * 1000)
        calls.append(ToolCall(
            name=action,
            params_summary=redact_params({"context_keys": list(context.keys())}),
            status=status,
            latency_ms=dt,
            error=error
        ))
        if status == "error":
            break
    return calls
