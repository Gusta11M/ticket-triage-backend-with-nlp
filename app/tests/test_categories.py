import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_category(client: AsyncClient, admin_headers: dict):
    category_data = {"category_name": "Bug"}
    # Apenas Admin pode criar
    response = await client.post("/categories/", json=category_data, headers=admin_headers)
    
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["category_name"] == category_data["category_name"]
    assert "id" in response_data

@pytest.mark.asyncio
async def test_create_category_forbidden_for_user(client: AsyncClient, user_headers: dict):
    category_data = {"category_name": "Should Fail"}
    # Utilizador comum recebe 403
    response = await client.post("/categories/", json=category_data, headers=user_headers)
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_create_category_with_invalid_data(client: AsyncClient, admin_headers: dict):
    invalid_data = {"category_name": ""}
    response = await client.post("/categories/", json=invalid_data, headers=admin_headers)
    
    assert response.status_code == 422
    assert "category_name" in response.json()["detail"][0]["loc"]

@pytest.mark.asyncio
async def test_get_category(client: AsyncClient, admin_headers: dict, user_headers: dict):
    # Admin cria
    create_res = await client.post("/categories/", json={"category_name": "Feature Request"}, headers=admin_headers)
    category_id = create_res.json()["id"]

    # User consegue ler
    response = await client.get(f"/categories/{category_id}", headers=user_headers)
    assert response.status_code == 200
    assert response.json()["id"] == category_id

@pytest.mark.asyncio
async def test_get_nonexistent_category(client: AsyncClient, user_headers: dict):
    response = await client.get("/categories/9999", headers=user_headers)
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_list_categories(client: AsyncClient, admin_headers: dict, user_headers: dict):
    # Criar algumas categorias
    await client.post("/categories/", json={"category_name": "Support"}, headers=admin_headers)
    await client.post("/categories/", json={"category_name": "Maintenance"}, headers=admin_headers)

    # Listar
    response = await client.get("/categories/", headers=user_headers)
    assert response.status_code == 200
    assert len(response.json()) >= 2

@pytest.mark.asyncio
async def test_update_category(client: AsyncClient, admin_headers: dict):
    # Criar
    create_res = await client.post("/categories/", json={"category_name": "Initial"}, headers=admin_headers)
    category_id = create_res.json()["id"]

    # Atualizar (Admin)
    updated_data = {"category_name": "Updated Name"}
    response = await client.put(f"/categories/{category_id}", json=updated_data, headers=admin_headers)
    
    assert response.status_code == 200
    assert response.json()["category_name"] == "Updated Name"

@pytest.mark.asyncio
async def test_delete_category(client: AsyncClient, admin_headers: dict):
    # Criar
    create_res = await client.post("/categories/", json={"category_name": "To Delete"}, headers=admin_headers)
    category_id = create_res.json()["id"]

    # Remover (Admin)
    response = await client.delete(f"/categories/{category_id}", headers=admin_headers)
    assert response.status_code == 204

    # Verificar que sumiu
    get_res = await client.get(f"/categories/{category_id}", headers=admin_headers)
    assert get_res.status_code == 404