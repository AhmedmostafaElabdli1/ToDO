from fastapi import FastAPI
from sqlmodel import SQLModel, Session, select
from sqlalchemy import text  # ✅ Needed for raw SQL
from datetime import datetime, timedelta

from routers import task_router
from database import engine
from models.task import Task, TaskPriority, TaskStatus

app = FastAPI(
    title="Task Management API",
    description="FastAPI-based Task Management Backend",
    version="1.0.0",
)

@app.on_event("startup")
def startup():
    # ✅ Create DB & tables
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        # ✅ Fix: Use text() to run raw SQL
        session.exec(text("DELETE FROM tasks"))
        session.commit()

        now = datetime.utcnow()
        tasks = [
            Task(title="Fix login bug", priority=TaskPriority.high, status=TaskStatus.in_progress, due_date=now + timedelta(days=2), assigned_to="Alice"),
            Task(title="Write user docs", priority=TaskPriority.medium, status=TaskStatus.pending, due_date=now + timedelta(days=5), assigned_to="Bob"),
            Task(title="Deploy to staging", priority=TaskPriority.urgent, status=TaskStatus.pending, due_date=now + timedelta(days=1), assigned_to="Charlie"),
            Task(title="Refactor payment module", priority=TaskPriority.low, status=TaskStatus.completed, due_date=now + timedelta(days=2), assigned_to="Dana"),
            Task(title="Design dashboard UI", priority=TaskPriority.medium, status=TaskStatus.in_progress, assigned_to="Eve"),
            Task(title="Team meeting prep", priority=TaskPriority.low, status=TaskStatus.pending),
            Task(title="Client follow-up", priority=TaskPriority.high, status=TaskStatus.cancelled),
            Task(title="Update SSL cert", priority=TaskPriority.urgent, status=TaskStatus.pending),
            Task(title="Optimize DB queries", priority=TaskPriority.medium, status=TaskStatus.in_progress, assigned_to="Alice"),
            Task(title="Test notification system", priority=TaskPriority.low, status=TaskStatus.completed, due_date=now + timedelta(days=10)),
        ]

        session.add_all(tasks)
        session.commit()
        print("✅ Sample data inserted.")

@app.get("/")
def root():
    return {
        "message": "Welcome to the Task Management API",
        "endpoints": [
            "/tasks", "/tasks/{id}", "/tasks/status/{status}",
            "/tasks/priority/{priority}", "/tasks/filter"
        ]
    }

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(task_router.router)
