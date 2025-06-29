from pydantic import BaseModel
from typing import Optional
from models.task import TaskStatus, TaskPriority

class TaskFilterRequest(BaseModel):
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    assigned_to: Optional[str] = None
    sort_by: Optional[str] = "created_at"
    order: Optional[str] = "asc"
    search: Optional[str] = None
