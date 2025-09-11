from pydantic import BaseModel, Field
from datetime import datetime
from uuid import uuid4, UUID


class Task(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    title: str
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.now, frozen=True)
    updated_at: datetime = Field(default_factory=datetime.now)