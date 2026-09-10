from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import schemas
from app.deps import get_db, get_current_user
from app.models import Task, User, TaskStatus, TaskPriority

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("", response_model=list[schemas.TaskOut])
def list_tasks(
    status: TaskStatus | None = None,
    priority: TaskPriority | None = None,
    skip: int = 0,
    limit: int = Query(20, le=100),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    q = db.query(Task).filter(Task.owner_id == user.id)
    if status:
        q = q.filter(Task.status == status)
    if priority:
        q = q.filter(Task.priority == priority)
    return q.offset(skip).limit(limit).all()


@router.post("", response_model=schemas.TaskOut, status_code=201)
def create_task(
    data: schemas.TaskCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    task = Task(**data.model_dump(), owner_id=user.id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def _get_own_task(task_id: int, db: Session, user: User) -> Task:
    task = db.get(Task, task_id)
    if not task or task.owner_id != user.id:
        raise HTTPException(404, "Task not found")
    return task


@router.get("/{task_id}", response_model=schemas.TaskOut)
def get_task(task_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return _get_own_task(task_id, db, user)


@router.patch("/{task_id}", response_model=schemas.TaskOut)
def update_task(
    task_id: int,
    data: schemas.TaskUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    task = _get_own_task(task_id, db, user)
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(task, k, v)
    db.commit()
    db.refresh(task)
    return task


@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    db.delete(_get_own_task(task_id, db, user))
    db.commit()