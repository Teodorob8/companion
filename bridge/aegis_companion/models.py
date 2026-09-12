from __future__ import annotations
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from pydantic import BaseModel, Field

class Mode(str, Enum):
    PAPER = "PAPER"
    REPLAY = "REPLAY"
    RESEARCH = "RESEARCH"

class Capability(str, Enum):
    READ_STATUS = "READ_STATUS"
    READ_EVENTS = "READ_EVENTS"
    RUN_DIAGNOSTIC = "RUN_DIAGNOSTIC"
    SAFE_REPAIR = "SAFE_REPAIR"
    PAPER_COMMAND = "PAPER_COMMAND"

class ErrorClass(str, Enum):
    SAFE_AUTO_FIX = "SAFE_AUTO_FIX"
    NEEDS_USER_DECISION = "NEEDS_USER_DECISION"
    SECURITY_BLOCKED = "SECURITY_BLOCKED"
    DATA_UNAVAILABLE = "DATA_UNAVAILABLE"
    DEPENDENCY_MISSING = "DEPENDENCY_MISSING"
    CONFIG_INVALID = "CONFIG_INVALID"
    SERVICE_DOWN = "SERVICE_DOWN"
    PERMISSION_DENIED = "PERMISSION_DENIED"
    UNKNOWN = "UNKNOWN"

class Command(BaseModel):
    command: str = Field(min_length=1, max_length=200)
    mode: Mode
    requested_capability: Capability
    correlation_id: str = Field(min_length=8)
    idempotency_key: str = Field(min_length=8)
    args: dict[str, Any] = Field(default_factory=dict)

class DiagnosticRecord(BaseModel):
    diagnostic_id: str
    classification: ErrorClass
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    component: str
    message: str
    correlation_id: str
    causation_id: str | None = None
    repair_attempted: bool = False
    repair_result: str | None = None
    evidence_path: str | None = None
