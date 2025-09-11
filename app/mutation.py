import strawberry
from uuid import uuid4
from datetime import datetime
from strawberry.exceptions import GraphQLError

from .task import Task
from .database import TaskORM, SessionLocal


@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_task(self, title: str) -> Task:
        """
        Create a new task.

        Args:
            title: The title of the task.

        Returns:
            The newly created task.
        """
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
    def toggle_task(self, id: strawberry.ID) -> Task:
        """
        Toggle a task between completed and not completed.

        Args:
            id: The ID of the task to toggle.

        Returns:
            The updated task.
        """
        with SessionLocal() as db:
            task = db.query(TaskORM).filter(TaskORM.id == str(id)).first()
            if not task:
                raise GraphQLError(f"Task with ID \"{id}\" not found")
            task.completed = not task.completed
            task.updated_at = datetime.now()
            db.commit()
            db.refresh(task)
        return task

    @strawberry.mutation
    def delete_task(self, id: strawberry.ID) -> Task:
        """
        Delete a task, returning the deleted task.

        Args:
            id: The ID of the task to delete.

        Returns:
            The deleted task.
        """
        with SessionLocal() as db:
            task = db.query(TaskORM).filter(TaskORM.id == str(id)).first()
            if not task:
                raise GraphQLError(f"Task with ID \"{id}\" not found")
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
