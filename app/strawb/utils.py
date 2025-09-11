from db.models import TaskORM
from strawb.tasktype import TaskType

def orm_to_graphql(task: TaskORM) -> TaskType:
    return TaskType(
        id=task.id,
        title=task.title,
        completed=task.completed,
        created_at=task.created_at,
        updated_at=task.updated_at,
    )
