import strawberry
from fastapi import Depends
from sqlalchemy.orm import Session

from strawb.tasktype import TaskType
from db.database import get_db
from db.models import TaskORM
from strawb.utils import orm_to_graphql


@strawberry.type
class Query:
    @strawberry.field
    def tasks(self, db: Session = Depends(get_db)) -> list[TaskType]:
        tasks = db.query(TaskORM).all()
        return [orm_to_graphql(t) for t in tasks]

    @strawberry.field
    def task(self, id: strawberry.ID, db: Session = Depends(get_db)) -> TaskType | None:
        task = db.query(TaskORM).filter(TaskORM.id == str(id)).first()
        if not task:
            return None
        return orm_to_graphql(task)