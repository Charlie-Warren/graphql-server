import strawberry
from datetime import datetime


@strawberry.type
class Task:
    id: strawberry.ID
    title: str
    completed: bool
    created_at: datetime
    updated_at: datetime
