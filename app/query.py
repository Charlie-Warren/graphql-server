import strawberry

from .database import TaskORM, SessionLocal
from .task import Task


@strawberry.type
class Query:
    @strawberry.field
    def tasks(self) -> list[Task]:
        """
        Return a list of all tasks.

        Args:
            None

        Returns:
            A list of all tasks.
        """
        with SessionLocal() as db:
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
            return db.query(TaskORM).filter(TaskORM.id == str(id)).first()
