from typing import Dict, Any
from ..models import Classification

KEYWORDS_INVOICE = ["invoice", "total", "due", "receipt"]
KEYWORDS_COMPLAINT = ["complaint", "unhappy", "delay", "poor", "angry", "escalate"]
def classify(payload: Dict[str, Any], source: str) -> Classification:
    text_blob = " ".join([str(payload.get("subject","")), str(payload.get("body","")), str(payload)]).lower()
    if any(k in text_blob for k in KEYWORDS_INVOICE):
        # request a human approval for money flows
        return Classification(type="invoice", priority="P1", owner_hint="finance@company.com", next_action="request_approval")
    if any(k in text_blob for k in KEYWORDS_COMPLAINT):
        return Classification(type="complaint", priority="P1", owner_hint="support@company.com", next_action="auto")
    if source == "sheets" and "threshold" in payload:
        return Classification(type="anomaly", priority="P0", owner_hint="ops@company.com", next_action="auto")
    return Classification(type="misc", priority="P3", owner_hint="ops@company.com", next_action="auto")
