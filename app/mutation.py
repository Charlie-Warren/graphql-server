import strawberry
from database import TaskORM, SessionLocal
from task import Task
from uuid import uuid4
from datetime import datetime


@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_task(self, title: str) -> Task:
        with SessionLocal() as db:
            task = TaskORM(
                id=str(uuid4()),
                title=title,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
            db.add(task)
            db.commit()
            db.refresh(task)
        return task

    @strawberry.mutation
    def toggle_task(self, id: strawberry.ID) -> Task | None:
        with SessionLocal() as db:
            task = db.query(TaskORM).filter(TaskORM.id == str(id)).first()
            if not task:
                return None
            task.completed = not task.completed
            task.updated_at = datetime.now()
            db.commit()
            db.refresh(task)
        return task

    @strawberry.mutation
    def delete_task(self, id: strawberry.ID) -> Task | None:
        with SessionLocal() as db:
            task = db.query(TaskORM).filter(TaskORM.id == str(id)).first()
            if not task:
                return None
            deleted_task_data = Task(
                id=task.id,
                title=task.title,
                completed=task.completed,
                created_at=task.created_at,
                updated_at=task.updated_at,
            )
            db.delete(task)
            db.commit()
        return deleted_task_data
