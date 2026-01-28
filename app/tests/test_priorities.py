import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_priority(client: AsyncClient, admin_headers: dict):
    priority_data = {
        "priority_name": "High",
        "level": 4
    }
    # Apenas Admin pode criar
    response = await client.post("/priorities/", json=priority_data, headers=admin_headers)
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["priority_name"] == priority_data["priority_name"]
    assert response_data["level"] == priority_data["level"]
    assert "id" in response_data

@pytest.mark.asyncio
async def test_create_priority_forbidden_for_user(client: AsyncClient, user_headers: dict):
    priority_data = {"priority_name": "Should Fail", "level": 1}
    # User comum não tem permissão
    response = await client.post("/priorities/", json=priority_data, headers=user_headers)
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_create_priority_with_invalid_data(client: AsyncClient, admin_headers: dict):
    invalid_priority_data = {
        "priority_name": "", 
        "level": 6           
    }
    response = await client.post("/priorities/", json=invalid_priority_data, headers=admin_headers)
    assert response.status_code == 422 
    response_data = response.json()
    # Pydantic costuma retornar os erros de validação aqui
    assert any("priority_name" in err["loc"] for err in response_data["detail"])
    assert any("level" in err["loc"] for err in response_data["detail"])

@pytest.mark.asyncio
async def test_get_priority(client: AsyncClient, admin_headers: dict, user_headers: dict):
    priority_data = {"priority_name": "Medium", "level": 3}
    
    # Admin cria
    create_response = await client.post("/priorities/", json=priority_data, headers=admin_headers)
    priority_id = create_response.json()["id"]

    # User consulta
    response = await client.get(f"/priorities/{priority_id}", headers=user_headers)
    assert response.status_code == 200
    assert response.json()["id"] == priority_id

@pytest.mark.asyncio
async def test_get_nonexistent_priority(client: AsyncClient, user_headers: dict):
    response = await client.get("/priorities/9999", headers=user_headers)
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_list_priorities(client: AsyncClient, admin_headers: dict, user_headers: dict):
    priorities_to_create = [
        {"priority_name": "Low", "level": 1},
        {"priority_name": "Critical", "level": 5},
    ]
    for priority in priorities_to_create:
        await client.post("/priorities/", json=priority, headers=admin_headers)

    response = await client.get("/priorities/", headers=user_headers)
    assert response.status_code == 200
    assert len(response.json()) >= 2

@pytest.mark.asyncio
async def test_update_priority(client: AsyncClient, admin_headers: dict):
    # Criar
    create_res = await client.post("/priorities/", json={"priority_name": "Urgent", "level": 4}, headers=admin_headers)
    priority_id = create_res.json()["id"]

    # Atualizar (Admin)
    updated_data = {"priority_name": "Very Urgent", "level": 5}
    response = await client.put(f"/priorities/{priority_id}", json=updated_data, headers=admin_headers)
    
    assert response.status_code == 200
    assert response.json()["priority_name"] == "Very Urgent"
    assert response.json()["level"] == 5

@pytest.mark.asyncio
async def test_delete_priority(client: AsyncClient, admin_headers: dict):
    # Criar
    create_res = await client.post("/priorities/", json={"priority_name": "To Delete", "level": 2}, headers=admin_headers)
    priority_id = create_res.json()["id"]

    # Remover (Admin)
    response = await client.delete(f"/priorities/{priority_id}", headers=admin_headers)
    assert response.status_code == 204

    # Verificar ausência
    get_res = await client.get(f"/priorities/{priority_id}", headers=admin_headers)
    assert get_res.status_code == 404