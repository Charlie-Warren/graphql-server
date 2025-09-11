import strawberry
from database import TaskORM, SessionLocal
from task import Task


@strawberry.type
class Query:
    @strawberry.field
    def tasks(self) -> list[Task]:
        """
        Return a list of all tasks.
        """
        with SessionLocal() as db:
            return db.query(TaskORM).all()

    @strawberry.field
    def task(self, id: strawberry.ID) -> Task | None:
        """
        Get a particular Task by ID.
        """
        with SessionLocal() as db:
            return db.query(TaskORM).filter(TaskORM.id == str(id)).first()
