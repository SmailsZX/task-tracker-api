from fastapi import FastAPI

from app.database import Base, engine
from app.routers import auth, tasks

app = FastAPI(title="Task Tracker API")

app.include_router(auth.router)
app.include_router(tasks.router)


@app.get("/health")
def health():
    return {"status": "ok"}


# Создание таблиц — ТОЛЬКО при запуске приложения, не при импорте
# Лучше вынести в отдельный скрипт или startup-событие