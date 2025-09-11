import strawberry
from datetime import datetime
from uuid import uuid4
from fastapi import Depends
from sqlalchemy.orm import Session

from strawb.tasktype import TaskType
from db.database import get_db
from db.models import TaskORM
from strawb.utils import orm_to_graphql


@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_task(self, title: str, db: Session = Depends(get_db)) -> TaskType:
        task = TaskORM(
            id=str(uuid4()),
            title=title,
            completed=False,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        return orm_to_graphql(task)

    @strawberry.mutation
    def toggle_task(self, id: strawberry.ID, db: Session = Depends(get_db)) -> TaskType | None:
        task = db.query(TaskORM).filter(TaskORM.id == str(id)).first()
        if not task:
            return None
        task.completed = not task.completed
        task.updated_at = datetime.now()
        db.commit()
        db.refresh(task)
        return orm_to_graphql(task)

    @strawberry.mutation
    def delete_task(self, id: strawberry.ID, db: Session = Depends(get_db)) -> TaskType | None:
        task = db.query(TaskORM).filter(TaskORM.id == str(id)).first()
        if not task:
            return None
        db.delete(task)
        db.commit()
        return orm_to_graphql(task)