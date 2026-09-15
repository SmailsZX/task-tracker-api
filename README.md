# Task Tracker API

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-D71F00?logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/)
[![Docker](https://img.shields.io/badge/Docker-compose-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![JWT](https://img.shields.io/badge/Auth-JWT-000000?logo=jsonwebtokens&logoColor=white)](https://jwt.io/)
[![Tests](https://github.com/SmailsZX/task-tracker-api/actions/workflows/tests.yml/badge.svg)](https://github.com/SmailsZX/task-tracker-api/actions/workflows/tests.yml)

REST API для управления задачами с JWT-авторизацией. Учебный пет-проект: написан за один вечер, чтобы показать уверенное владение FastAPI, SQLAlchemy 2.0, PostgreSQL и Docker.

---

## ✨ Возможности

- 🔐 **JWT-авторизация** — регистрация, логин, защищённые эндпоинты
- 👤 **Привязка задач к пользователю** — каждый видит только свои задачи
- 📝 **Полный CRUD** — создание, чтение, обновление, удаление задач
- 🔍 **Фильтры и пагинация** — по статусу, приоритету, `skip`/`limit`
- 🗄 **PostgreSQL 16** через SQLAlchemy 2.0 (typed Mapped API)
- 🐳 **Docker + docker-compose** — запуск одной командой
- 📖 **Автогенерируемая документация** — Swagger UI из коробки
- 🧪 **13 тестов (pytest)** — авторизация и CRUD

---

## 🛠 Стек

| Слой | Технология |
|------|-----------|
| Web-фреймворк | FastAPI 0.115 |
| ORM | SQLAlchemy 2.0 |
| База данных | PostgreSQL 16 |
| Валидация | Pydantic v2 + pydantic-settings |
| Аутентификация | JWT (python-jose) + bcrypt (passlib) |
| ASGI-сервер | Uvicorn |
| Тестирование | pytest 8.3 + httpx |
| Контейнеризация | Docker + docker-compose |

---

## 🚀 Быстрый старт

### Требования
- Docker Desktop
- Git

### Запуск

```bash
git clone https://github.com/SmailsZX/task-tracker-api.git
cd task-tracker-api
cp .env.example .env
docker compose up --build
```

Через 1–2 минуты API будет доступен:

- 📖 **Swagger UI** — http://localhost:8000/docs
- 📄 **ReDoc** — http://localhost:8000/redoc
- ❤️ **Healthcheck** — http://localhost:8000/health

---

## 🧪 Тесты

Проект покрыт тестами (pytest) — **13 тестов**.

### Запуск

```bash
pytest tests/ -v
```

### Что покрыто

**Авторизация (`tests/test_auth.py`):**
- ✅ Регистрация пользователя
- ✅ Регистрация с дублирующимся email
- ✅ Успешный логин (JWT)
- ✅ Логин с неверным паролем
- ✅ Получение текущего пользователя (`/auth/me`)
- ✅ Доступ без токена (401)

**Задачи (`tests/test_tasks.py`):**
- ✅ Создание задачи
- ✅ Получение списка задач
- ✅ Фильтрация по статусу
- ✅ Обновление задачи (PATCH)
- ✅ Удаление задачи
- ✅ Задача не найдена (404)
- ✅ Доступ без токена (401)

### Как устроены тесты

- **SQLite в памяти** — тесты не зависят от PostgreSQL.
- **Фикстуры** (`conftest.py`):
  - `client` — тестовый клиент с чистой БД для каждого теста.
  - `auth_client` — клиент с JWT-токеном.
- **Изоляция** — каждый тест получает чистую БД.

### Пример

```python
def test_create_task(auth_client):
    response = auth_client.post(
        "/tasks",
        json={"title": "Тестовая задача", "priority": "high"},
    )
    assert response.status_code == 201
    assert response.json()["title"] == "Тестовая задача"
```

---

## 📸 Скриншоты

### Регистрация

![Register 1](docs/01-register.png)
![Register 2](docs/02-register.png)

### Логин и получение JWT

![Login 1](docs/01-login.png)
![Login 2](docs/02-login.png)

### Создание задачи (защищённый эндпоинт)

![Create Task 1](docs/01-create-task.png)
![Create Task 2](docs/02-create-task.png)

---

## 🌐 API Endpoints

### Auth

| Метод | Путь | Описание | Auth |
|-------|------|----------|:----:|
| `POST` | `/auth/register` | Регистрация нового пользователя | ❌ |
| `POST` | `/auth/login` | Получить JWT-токен | ❌ |
| `GET` | `/auth/me` | Информация о текущем пользователе | 🔒 |

### Tasks

| Метод | Путь | Описание | Auth |
|-------|------|----------|:----:|
| `GET` | `/tasks` | Список задач (фильтры, пагинация) | 🔒 |
| `POST` | `/tasks` | Создать задачу | 🔒 |
| `GET` | `/tasks/{id}` | Получить задачу по ID | 🔒 |
| `PATCH` | `/tasks/{id}` | Обновить задачу | 🔒 |
| `DELETE` | `/tasks/{id}` | Удалить задачу | 🔒 |

### Meta

| Метод | Путь | Описание |
|-------|------|----------|
| `GET` | `/health` | Healthcheck |

**Параметры фильтрации `GET /tasks`:**

- `status` — `todo` / `in_progress` / `done`
- `priority` — `low` / `medium` / `high`
- `skip` — пропустить N записей (по умолчанию 0)
- `limit` — вернуть N записей (по умолчанию 20, максимум 100)

---

## 🧪 Примеры запросов

### Регистрация

```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"secret123"}'
```

### Логин

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=secret123"
```

Ответ:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Создание задачи

```bash
TOKEN="вставь access_token сюда"

curl -X POST http://localhost:8000/tasks \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Сделать апгрейд","description":"FastAPI + JWT + Docker","priority":"high"}'
```

### Список задач с фильтром

```bash
curl "http://localhost:8000/tasks?status=todo&priority=high&limit=10" \
  -H "Authorization: Bearer $TOKEN"
```

---

## 🏗 Структура проекта

```
task-tracker-api/
├── app/
│   ├── main.py              # Точка входа FastAPI
│   ├── config.py            # Настройки через pydantic-settings
│   ├── database.py          # Engine, SessionLocal, Base
│   ├── models.py            # SQLAlchemy-модели (User, Task)
│   ├── schemas.py           # Pydantic-схемы (валидация + сериализация)
│   ├── security.py          # bcrypt + JWT-хелперы
│   ├── deps.py              # Зависимости (get_db, get_current_user)
│   └── routers/
│       ├── auth.py          # /auth/* — регистрация и логин
│       └── tasks.py         # /tasks/* — CRUD задач
├── tests/                   # Тесты (pytest)
│   ├── conftest.py          # Фикстуры
│   ├── test_auth.py         # Тесты авторизации
│   └── test_tasks.py        # Тесты задач
├── docs/                    # Скриншоты Swagger UI
├── Dockerfile               # Образ приложения
├── docker-compose.yml       # api + postgres
├── requirements.txt         # Python-зависимости
├── .env.example             # Шаблон переменных окружения
└── README.md
```

---

## 🔒 Безопасность

- Пароли хешируются **bcrypt** (не sha256 — медленный + salt из коробки)
- JWT содержит `sub` (email) и `exp` (60 минут по умолчанию)
- `SECRET_KEY` вынесен в переменные окружения (`.env` в `.gitignore`)
- Все защищённые эндпоинты требуют `Authorization: Bearer <token>`
- Пользователь видит и редактирует **только свои** задачи (`owner_id == current_user.id`)

---

## 🔮 Roadmap

- [x] **pytest + httpx** — тесты на auth и CRUD (13 тестов)
- [x] **GitHub Actions** — CI: pytest на каждый push
- [ ] **Alembic** — миграции вместо `Base.metadata.create_all`
- [ ] **Пагинация с total** — `{items: [...], total: N}`
- [ ] **Rate limit** на `/auth/login` через slowapi
- [ ] **Refresh-токены** — длинные сессии без релогина

---

## 📝 Заметки

- **Почему `bcrypt==4.0.1`?** `passlib 1.7.4` несовместим с `bcrypt 4.1+` — падает на внутреннем тесте с `ValueError: password cannot be longer than 72 bytes`. Пин версии — самое простое решение. В проде лучше взять `argon2` или валидировать длину пароля в Pydantic-схеме.

---

## 📄 Лицензия

MIT — используй свободно.