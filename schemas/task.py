from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime
from models.task import TaskStatus, TaskPriority

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[TaskStatus] = TaskStatus.pending
    priority: Optional[TaskPriority] = TaskPriority.medium
    due_date: Optional[datetime] = None
    assigned_to: Optional[str] = None

    @validator("title")
    def title_must_not_be_empty(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("Title cannot be empty or whitespace.")
        return v

    @validator("due_date")
    def due_date_must_be_future(cls, v):
        if v and v < datetime.utcnow():
            raise ValueError("Due date must be in the future.")
        return v

class TaskUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    status: Optional[TaskStatus]
    priority: Optional[TaskPriority]
    due_date: Optional[datetime]
    assigned_to: Optional[str]

class TaskResponse(TaskCreate):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
