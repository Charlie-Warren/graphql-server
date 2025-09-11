import strawberry
from schemas import Task


@strawberry.experimental.pydantic.type(model=Task, all_fields=True)
class TaskType:
    pass