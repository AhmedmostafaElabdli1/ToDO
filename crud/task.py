from sqlmodel import Session, select, asc, desc
from models.task import Task
from schemas.task import TaskCreate, TaskUpdate
from typing import List, Optional

def create_task(session: Session, task_data: TaskCreate) -> Task:
    task = Task.from_orm(task_data)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

def get_task(session: Session, task_id: int) -> Optional[Task]:
    return session.get(Task, task_id)

def get_all_tasks(session: Session, skip=0, limit=10) -> List[Task]:
    return session.exec(select(Task).offset(skip).limit(limit)).all()

def update_task(session: Session, task_id: int, task_data: TaskUpdate) -> Optional[Task]:
    task = session.get(Task, task_id)
    if not task:
        return None
    for key, value in task_data.dict(exclude_unset=True).items():
        setattr(task, key, value)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

def delete_task(session: Session, task_id: int) -> bool:
    task = session.get(Task, task_id)
    if not task:
        return False
    session.delete(task)
    session.commit()
    return True

def filter_tasks(
    session: Session,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    skip: int = 0,
    limit: int = 10,
    sort_by: str = "created_at",
    order: str = "asc"
) -> List[Task]:
    query = select(Task)

    if status:
        query = query.where(Task.status == status)
    if priority:
        query = query.where(Task.priority == priority)

    sort_column = getattr(Task, sort_by, None)
    if sort_column is not None:
        query = query.order_by(asc(sort_column) if order == "asc" else desc(sort_column))

    return session.exec(query.offset(skip).limit(limit)).all()
