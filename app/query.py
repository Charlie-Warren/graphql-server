import strawberry
from strawberry.exceptions import GraphQLError
from typing import Optional

from .database import TaskORM, SessionLocal
from .task import Task


@strawberry.type
class Query:
    @strawberry.field
    def tasks(self, search: Optional[str] = None) -> list[Task]:
        """
        Return a list of all tasks.

        Args:
            search (Optional): An optional search term to filter tasks by title.

        Returns:
            A list of all tasks (filtered by search term if provided).
        """
        with SessionLocal() as db:
            if search:
                return db.query(TaskORM).filter(TaskORM.title.contains(search)).all()
            return db.query(TaskORM).all()

    @strawberry.field
    def task(self, id: strawberry.ID) -> Task | None:
        """
        Get a particular Task by ID.

        Args:
            id: The ID of the task to retrieve.

        Returns:
            The task with the specified ID, or None if not found.
        """
        with SessionLocal() as db:
            task = db.query(TaskORM).filter(TaskORM.id == str(id)).first()
            if not task:
                raise GraphQLError(f"Task with ID \"{id}\" not found")
            return task
