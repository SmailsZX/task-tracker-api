def test_register(client, test_user):
    """Регистрация нового пользователя."""
    response = client.post("/auth/register", json=test_user)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == test_user["email"]
    assert "id" in data
    assert "password" not in data  # пароль не возвращается


def test_register_duplicate_email(client, test_user):
    """Регистрация с существующим email — ошибка."""
    client.post("/auth/register", json=test_user)
    response = client.post("/auth/register", json=test_user)
    assert response.status_code == 400


def test_login_success(client, test_user):
    """Успешный логин — возвращает JWT."""
    client.post("/auth/register", json=test_user)
    response = client.post(
        "/auth/login",
        data={
            "username": test_user["email"],
            "password": test_user["password"],
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client, test_user):
    """Логин с неверным паролем — ошибка."""
    client.post("/auth/register", json=test_user)
    response = client.post(
        "/auth/login",
        data={
            "username": test_user["email"],
            "password": "wrongpassword",
        },
    )
    assert response.status_code == 401


def test_get_me(client, auth_client):
    """Получение информации о текущем пользователе."""
    response = auth_client.get("/auth/me")
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"


def test_get_me_unauthorized(client):
    """Без токена — 401."""
    response = client.get("/auth/me")
    assert response.status_code == 401