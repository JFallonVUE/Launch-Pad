from sqlmodel import SQLModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
import uuid

class Intake(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    mode: str  # "lighting" | "deep_dive"
    answers: Dict[str, Any]
    signals: Dict[str, Any]
    stacks: Dict[str, Any]  # three stacks + rationales
    biases: Dict[str, Any]  # top 3 bias mini-plans
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ExportJob(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    intake_id: str
    chosen_tier: str
    chosen_bias_key: str
    status: str = "pending"  # pending|done|error
    file_path: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
