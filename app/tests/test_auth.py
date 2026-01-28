import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_register_success(client: AsyncClient):

    payload={
        "email": "user1@test.com",
        "password": "StrongPassword123",
        "role": "user"
    }

    response = await client.post("/auth/register", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_register_existing_user(client: AsyncClient):
    
    payload={
        "email": "user2@test.com",
        "password": "StrongPassword123",
        "role": "user"
    }

    await client.post("/auth/register", json=payload)
    response = await client.post("/auth/register", json=payload)

    assert response.status_code == 400
    assert response.json()["detail"] == "Utilizador já existe"

@pytest.mark.asyncio
async def test_register_invalid_email(client: AsyncClient):
    payload = {
        "email": "invalid-email",
        "password": "password",
        "role": "user"
    }

    response = await client.post("/auth/register", json=payload)

    assert response.status_code == 422
    assert "email" in response.json()["detail"][0]["loc"]


@pytest.mark.asyncio
async def test_register_missing_password(client: AsyncClient):
    payload = {
        "email": "user3@test.com",
        "role": "user"
    }

    response = await client.post("/auth/register", json=payload)

    assert response.status_code == 422

@pytest.mark.asyncio
async def test_login_success(client: AsyncClient):
    register_payload = {
        "email": "login@test.com",
        "password": "LoginPassword123",
        "role": "user"
    }

    await client.post("/auth/register", json=register_payload)

    login_payload = {
        "email": "login@test.com",
        "password": "LoginPassword123"
    }

    response = await client.post("/auth/login", json=login_payload)

    assert response.status_code == 200
    data = response.json()

    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient):
    register_payload = {
        "email": "wrongpass@test.com",
        "password": "CorrectPassword",
        "role": "user"
    }

    await client.post("/auth/register", json=register_payload)

    login_payload = {
        "email": "wrongpass@test.com",
        "password": "WrongPassword"
    }

    response = await client.post("/auth/login", json=login_payload)

    assert response.status_code == 401
    assert response.json()["detail"] == "Credenciais inválidas"


@pytest.mark.asyncio
async def test_login_nonexistent_user(client: AsyncClient):
    payload = {
        "email": "doesnotexist@test.com",
        "password": "password"
    }

    response = await client.post("/auth/login", json=payload)

    assert response.status_code == 401
    assert response.json()["detail"] == "Credenciais inválidas"

@pytest.mark.asyncio
async def test_refresh_token_success(client: AsyncClient):
    register_payload = {
        "email": "refresh@test.com",
        "password": "RefreshPassword123",
        "role": "user"
    }

    register_response = await client.post("/auth/register", json=register_payload)
    refresh_token = register_response.json()["refresh_token"]

    response = await client.post("/auth/refresh", json={
        "refresh_token": refresh_token
    })

    assert response.status_code == 200
    data = response.json()

    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_refresh_token_invalid(client: AsyncClient):
    response = await client.post("/auth/refresh", json={
        "refresh_token": "invalid.token.here"
    })

    assert response.status_code == 401
    assert response.json()["detail"] == "Token inválido"
