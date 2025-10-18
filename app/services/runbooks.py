from typing import Tuple, List
from ..models import Classification

def plan_runbook(cl: Classification) -> List[str]:
    key: Tuple[str, str] = (cl.type, cl.priority)

    table = {
        ("invoice", "P1"): ["request_approval", "append_sheet", "open_notion", "notify_slack"],
        ("complaint", "P1"): ["open_notion", "notify_slack"],
        ("anomaly", "P0"): ["open_notion", "notify_slack"],
        ("misc", "P3"): ["notify_slack"],
    }
    return table.get(key, ["notify_slack"])
