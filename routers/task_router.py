from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from sqlmodel import Session, select
from database import get_session
from models.task import Task, TaskStatus, TaskPriority
from schemas.task import TaskCreate, TaskUpdate, TaskResponse

router = APIRouter(prefix="/tasks", tags=["Tasks"])

# --- Create Task ---
@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate, session: Session = Depends(get_session)):
    db_task = Task.model_validate(task)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

# --- Get All Tasks (with optional filtering, search, pagination) ---
@router.get("/", response_model=List[TaskResponse])
def list_tasks(
    skip: int = 0,
    limit: int = 10,
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    search: Optional[str] = None,
    session: Session = Depends(get_session),
):
    query = select(Task)
    if status:
        query = query.where(Task.status == status)
    if priority:
        query = query.where(Task.priority == priority)
    if search:
        pattern = f"%{search.lower()}%"
        query = query.where(
            Task.title.ilike(pattern) | Task.description.ilike(pattern)
        )
    query = query.offset(skip).limit(limit)
    return session.exec(query).all()

# --- Get Task by ID ---
@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# --- Update Task ---
@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_data: TaskUpdate, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in task_data.dict(exclude_unset=True).items():
        setattr(task, key, value)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

# --- Delete Task ---
@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    session.delete(task)
    session.commit()
    return

# --- Get Tasks by Status ---
@router.get("/status/{status}", response_model=List[TaskResponse])
def get_by_status(status: TaskStatus, session: Session = Depends(get_session)):
    tasks = session.exec(select(Task).where(Task.status == status)).all()
    return tasks

# --- Get Tasks by Priority ---
@router.get("/priority/{priority}", response_model=List[TaskResponse])
def get_by_priority(priority: TaskPriority, session: Session = Depends(get_session)):
    tasks = session.exec(select(Task).where(Task.priority == priority)).all()
    return tasks

@router.post("/filter", response_model=List[TaskResponse])
def filter_tasks(filter: TaskFilterRequest, session: Session = Depends(get_session)):
    query = select(Task)

    if filter.status:
        query = query.where(Task.status == filter.status)
    if filter.priority:
        query = query.where(Task.priority == filter.priority)
    if filter.assigned_to:
        query = query.where(Task.assigned_to == filter.assigned_to)

    if filter.search:
        pattern = f"%{filter.search.lower()}%"
        query = query.where(
            Task.title.ilike(pattern) | Task.description.ilike(pattern)
        )

    # Validate sort field
    valid_sort_fields = Task.__fields__.keys()
    if filter.sort_by not in valid_sort_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sort field: {filter.sort_by}")

    sort_column = getattr(Task, filter.sort_by)
    if filter.order == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    return session.exec(query).all()
