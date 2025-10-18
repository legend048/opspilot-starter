from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid

class InboundEvent(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    source: str
    payload: Dict[str, Any]
    received_at: datetime = Field(default_factory=datetime.utcnow)

class Classification(BaseModel):
    type: str  # invoice | complaint | anomaly | misc
    priority: str  # P0..P3
    owner_hint: str = "ops@company.com"
    next_action: str = "auto"

class ToolCall(BaseModel):
    name: str
    params_summary: str = ""
    status: str = "ok"  # ok | error
    latency_ms: int = 0
    error: Optional[str] = None
    at: datetime = Field(default_factory=datetime.utcnow)

class Run(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    event_id: str
    classification: Classification
    actions: List[str]
    tool_calls: List[ToolCall] = []
    status: str = "running"  # running | waiting_approval | done | failed
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    notes: Optional[str] = None
