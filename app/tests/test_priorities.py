
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_priority(client : AsyncClient):
    priority_data = {
        "priority_name": "High",
        "level": 4
    }

    response = await client.post("/priorities/", json=priority_data)
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["priority_name"] == priority_data["priority_name"]
    assert response_data["level"] == priority_data["level"]
    assert "id" in response_data
    assert "created_at" in response_data

@pytest.mark.asyncio
async def test_create_priority_with_invalid_data(client : AsyncClient):
    invalid_priority_data = {
        "priority_name": "",  # Priority name should not be empty
        "level": 6           # Level should be between 1 and 5
    }

    response = await client.post("/priorities/", json=invalid_priority_data)
    assert response.status_code == 422  # Unprocessable Entity
    response_data = response.json()
    assert "priority_name" in response_data["detail"][0]["loc"]
    assert "level" in response_data["detail"][1]["loc"]

@pytest.mark.asyncio
async def test_get_priority(client : AsyncClient):
    priority_data = {
        "priority_name": "Medium",
        "level": 3
    }

    create_response = await client.post("/priorities/", json=priority_data)
    priority_id = create_response.json()["id"]

    response = await client.get(f"/priorities/{priority_id}")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == priority_id
    assert response_data["priority_name"] == priority_data["priority_name"]
    assert response_data["level"] == priority_data["level"]

@pytest.mark.asyncio
async def test_get_nonexistent_priority(client : AsyncClient):
    nonexistent_priority_id = 9999
    response = await client.get(f"/priorities/{nonexistent_priority_id}")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_list_priorities(client : AsyncClient):
    priorities_to_create = [
        {"priority_name": "Low", "level": 1},
        {"priority_name": "Critical", "level": 5},
    ]
    for priority in priorities_to_create:
        await client.post("/priorities/", json=priority)

    response = await client.get("/priorities/")
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) >= len(priorities_to_create)

@pytest.mark.asyncio
async def test_update_priority(client : AsyncClient):
    priority_data = {
        "priority_name": "Urgent",
        "level": 4
    }

    create_response = await client.post("/priorities/", json=priority_data)
    priority_id = create_response.json()["id"]

    updated_priority_data = {
        "priority_name": "Very Urgent",
        "level": 5
    }

    response = await client.put(f"/priorities/{priority_id}", json=updated_priority_data)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == priority_id
    assert response_data["priority_name"] == updated_priority_data["priority_name"]
    assert response_data["level"] == updated_priority_data["level"]

@pytest.mark.asyncio
async def test_delete_priority(client : AsyncClient):
    priority_data = {
        "priority_name": "To Be Deleted",
        "level": 2
    }

    create_response = await client.post("/priorities/", json=priority_data)
    priority_id = create_response.json()["id"]

    response = await client.delete(f"/priorities/{priority_id}")
    assert response.status_code == 204