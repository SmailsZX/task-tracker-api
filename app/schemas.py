from datetime import datetime

from pydantic import BaseModel, EmailStr, ConfigDict

from app.models import TaskStatus, TaskPriority


# ---------- USER ----------
class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    created_at: datetime


# ---------- AUTH ----------
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ---------- TASK ----------
class TaskBase(BaseModel):
    title: str
    description: str | None = None
    status: TaskStatus = TaskStatus.todo
    priority: TaskPriority = TaskPriority.medium


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: TaskStatus | None = None
    priority: TaskPriority | None = None


class TaskOut(TaskBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_id: int
    created_at: datetime