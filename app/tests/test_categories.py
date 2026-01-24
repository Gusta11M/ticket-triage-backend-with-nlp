import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_category(client : AsyncClient):
    category_data = {
        "category_name": "Bug",
    }
    response = await client.post("/categories/", json=category_data)
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["category_name"] == category_data["category_name"]
    assert "id" in response_data
    assert "created_at" in response_data

@pytest.mark.asyncio
async def test_create_category_with_invalid_data(client : AsyncClient):
    invalid_category_data = {
        "category_name": "",  # Category name should not be empty
    }
    response = await client.post("/categories/", json=invalid_category_data)
    assert response.status_code == 422  # Unprocessable Entity
    response_data = response.json()
    assert "category_name" in response_data["detail"][0]["loc"]

@pytest.mark.asyncio
async def test_get_category(client : AsyncClient):
    category_data = {
        "category_name": "Feature Request",
    }

    create_response = await client.post("/categories/", json=category_data)
    category_id = create_response.json()["id"]

    response = await client.get(f"/categories/{category_id}")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == category_id
    assert response_data["category_name"] == category_data["category_name"]

@pytest.mark.asyncio
async def test_get_nonexistent_category(client : AsyncClient):
    nonexistent_category_id = 9999
    response = await client.get(f"/categories/{nonexistent_category_id}")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_list_categories(client : AsyncClient):
    categories_to_create = [
        {"category_name": "Support"},
        {"category_name": "Maintenance"},
    ]
    for category in categories_to_create:
        await client.post("/categories/", json=category)

    response = await client.get("/categories/")
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) >= len(categories_to_create)

@pytest.mark.asyncio
async def test_update_category(client : AsyncClient):
    category_data = {
        "category_name": "Initial Name",
    }
    create_response = await client.post("/categories/", json=category_data)
    category_id = create_response.json()["id"]

    updated_data = {
        "category_name": "Updated Name",
    }

    response = await client.put(f"/categories/{category_id}", json=updated_data)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == category_id
    assert response_data["category_name"] == updated_data["category_name"]

@pytest.mark.asyncio
async def test_delete_category(client : AsyncClient):
    category_data = {
        "category_name": "To Be Deleted",
    }

    create_response = await client.post("/categories/", json=category_data)
    category_id = create_response.json()["id"]

    response = await client.delete(f"/categories/{category_id}")
    assert response.status_code == 204

    get_response = await client.get(f"/categories/{category_id}")
    assert get_response.status_code == 404