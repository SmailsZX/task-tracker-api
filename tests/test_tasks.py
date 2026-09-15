def test_create_task(auth_client):
    """Создание задачи."""
    response = auth_client.post(
        "/tasks",
        json={
            "title": "Тестовая задача",
            "description": "Описание",
            "priority": "high",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Тестовая задача"
    assert data["priority"] == "high"
    assert data["status"] == "todo"


def test_get_tasks(auth_client):
    """Получение списка задач."""
    auth_client.post("/tasks", json={"title": "Задача 1"})
    auth_client.post("/tasks", json={"title": "Задача 2"})
    response = auth_client.get("/tasks")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_filter_tasks(auth_client):
    """Фильтрация по статусу."""
    auth_client.post("/tasks", json={"title": "Задача 1", "status": "todo"})
    auth_client.post("/tasks", json={"title": "Задача 2", "status": "done"})
    response = auth_client.get("/tasks?status=done")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_update_task(auth_client):
    """Обновление задачи (PATCH)."""
    create = auth_client.post("/tasks", json={"title": "Старая"})
    task_id = create.json()["id"]
    response = auth_client.patch(
        f"/tasks/{task_id}",
        json={"title": "Новая", "status": "done"},
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Новая"
    assert response.json()["status"] == "done"


def test_delete_task(auth_client):
    """Удаление задачи."""
    create = auth_client.post("/tasks", json={"title": "Удалить"})
    task_id = create.json()["id"]
    response = auth_client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204
    # Проверяем, что задачи больше нет
    response = auth_client.get(f"/tasks/{task_id}")
    assert response.status_code == 404


def test_task_not_found(auth_client):
    """Задача не найдена — 404."""
    response = auth_client.get("/tasks/99999")
    assert response.status_code == 404


def test_unauthorized_tasks(client):
    """Без токена — 401."""
    response = client.get("/tasks")
    assert response.status_code == 401