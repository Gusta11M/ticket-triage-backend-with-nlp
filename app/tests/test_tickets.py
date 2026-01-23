import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_ticket(client: AsyncClient):
    ticket_data = {
        "title": "Test Ticket",
        "message": "This is a test ticket.",
    }
    response = await client.post("/tickets/", json=ticket_data)
    
    # DEBUG: Se falhar, vamos ver o porquê
    if response.status_code != 201:
        print(f"\nERRO DA API: {response.json()}")
        
    assert response.status_code == 201
    assert "id" in response.json()

@pytest.mark.asyncio
async def test_create_ticket_with_invalid_data(client : AsyncClient):
    invalid_ticket_data = {
        "title": "",  # Title should not be empty
        "message": "This is a test ticket with invalid data."
    }
    response = await client.post("/tickets/", json=invalid_ticket_data)
    assert response.status_code == 422  # Unprocessable Entity
    response_data = response.json()
    assert "title" in response_data["detail"][0]["loc"]


@pytest.mark.asyncio
async def test_get_ticket(client : AsyncClient):
    # First, create a ticket to retrieve
    ticket_data = {
        "title": "Get Ticket Test",
        "message": "This ticket is for testing retrieval."
    }

    create_response = await client.post("/tickets/", json=ticket_data)
    ticket_id = create_response.json()["id"]

    # Now, retrieve the ticket
    response = await client.get(f"/tickets/{ticket_id}")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == ticket_id
    assert response_data["title"] == ticket_data["title"]
    assert response_data["message"] == ticket_data["message"]

@pytest.mark.asyncio
async def test_get_nonexistent_ticket(client : AsyncClient):
    nonexistent_ticket_id = 9999  # Assuming this ID does not exist
    response = await client.get(f"/tickets/{nonexistent_ticket_id}")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_list_tickets(client : AsyncClient):
    # Create multiple tickets
    tickets_to_create = [
        {"title": "Ticket 1", "message": "First ticket."},
        {"title": "Ticket 2", "message": "Second ticket."},
    ]
    for ticket in tickets_to_create:
        await client.post("/tickets/", json=ticket)

    # Now, list all tickets
    response = await client.get("/tickets/")
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) >= len(tickets_to_create)


@pytest.mark.asyncio
async def test_list_tickets_with_pagination(client : AsyncClient):
    # Create multiple tickets
    for i in range(15):
        ticket_data = {
            "title": f"Ticket {i+1}",
            "message": f"This is ticket number {i+1}."
        }
        await client.post("/tickets/", json=ticket_data)

    # Now, list tickets with pagination
    response = await client.get("/tickets/?skip=5&limit=5")
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) == 5  # Should return 5 tickets

@pytest.mark.asyncio
async def test_list_tickets_with_no_tickets(client : AsyncClient):
    response = await client.get("/tickets/")
    assert response.status_code == 200
    response_data = response.json()
    assert isinstance(response_data, list)
    assert len(response_data) == 0 

@pytest.mark.asyncio
async def test_update_ticket(client : AsyncClient):
    # First, create a ticket to update
    ticket_data = {
        "title": "Update Ticket Test",
        "message": "This ticket is for testing updates."
    }

    create_response = await client.post("/tickets/", json=ticket_data)
    ticket_id = create_response.json()["id"]

    # Now, update the ticket
    updated_ticket_data = {
        "title": "Updated Ticket Title",
        "message": "This ticket has been updated."
    }
    response = await client.put(f"/tickets/{ticket_id}", json=updated_ticket_data)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == ticket_id
    assert response_data["title"] == updated_ticket_data["title"]
    assert response_data["message"] == updated_ticket_data["message"]

@pytest.mark.asyncio
async def test_update_nonexistent_ticket(client : AsyncClient):
    nonexistent_ticket_id = 9999  # Assuming this ID does not exist
    updated_ticket_data = {
        "title": "Updated Ticket Title",
        "message": "This ticket has been updated."
    }
    response = await client.put(f"/tickets/{nonexistent_ticket_id}", json=updated_ticket_data)
    assert response.status_code == 404
