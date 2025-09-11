import strawberry
from database import TaskORM, SessionLocal
from task import Task


@strawberry.type
class Query:
    @strawberry.field
    def tasks(self) -> list[Task]:
        with SessionLocal() as db:
            return db.query(TaskORM).all()

    @strawberry.field
    def task(self, id: strawberry.ID) -> Task | None:
        with SessionLocal() as db:
            return db.query(TaskORM).filter(TaskORM.id == str(id)).first()
