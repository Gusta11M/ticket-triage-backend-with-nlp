import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_ticket(client: AsyncClient, user_headers: dict):
    """User normal pode criar tickets"""
    ticket_data = {
        "title": "Ticket de Teste Longo",
        "message": "Esta é uma mensagem de teste com tamanho suficiente.",
    }
    response = await client.post("/tickets/", json=ticket_data, headers=user_headers)
    
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["title"] == ticket_data["title"]

@pytest.mark.asyncio
async def test_create_ticket_with_invalid_data(client: AsyncClient, user_headers: dict):
    """Validação deve rejeitar dados inválidos"""
    invalid_ticket_data = {
        "title": "",  # Deve falhar
        "message": "Invalid"
    }
    response = await client.post("/tickets/", json=invalid_ticket_data, headers=user_headers)
    assert response.status_code == 422
    assert "title" in str(response.json()["detail"][0]["loc"])

@pytest.mark.asyncio
async def test_get_ticket_as_admin(client: AsyncClient, admin_headers: dict, user_headers: dict):
    """Admin consegue ler qualquer ticket"""
    ticket_data = {"title": "Título de Teste Get", "message": "Mensagem de teste para consulta."}
    create_res = await client.post("/tickets/", json=ticket_data, headers=user_headers)
    
    # Se falhar aqui, o assert vai mostrar o erro em vez de dar skip
    assert create_res.status_code == 201
    ticket_id = create_res.json()["id"]

    response = await client.get(f"/tickets/{ticket_id}", headers=admin_headers)
    assert response.status_code == 200
    assert response.json()["id"] == ticket_id

@pytest.mark.asyncio
async def test_get_ticket_forbidden_for_user(client: AsyncClient, user_headers: dict):
    """User normal não pode ler tickets (apenas admin)"""
    ticket_data = {"title": "Título de Teste Forbidden", "message": "Mensagem de teste."}
    create_res = await client.post("/tickets/", json=ticket_data, headers=user_headers)
    assert create_res.status_code == 201
    ticket_id = create_res.json()["id"]
    
    response = await client.get(f"/tickets/{ticket_id}", headers=user_headers)
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_get_nonexistent_ticket(client: AsyncClient, admin_headers: dict):
    """Deve retornar 404 para ticket inexistente"""
    response = await client.get("/tickets/9999", headers=admin_headers)
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_list_tickets_as_admin(client: AsyncClient, admin_headers: dict, user_headers: dict):
    """Admin lista todos os tickets"""
    # Criar tickets e forçar erro se falhar
    for i in range(2):
        res = await client.post(
            "/tickets/", 
            json={"title": f"Ticket Listagem {i+1}", "message": "Mensagem válida para lista."}, 
            headers=user_headers
        )
        assert res.status_code == 201 

    response = await client.get("/tickets/", headers=admin_headers)
    assert response.status_code == 200
    assert len(response.json()) >= 2

@pytest.mark.asyncio
async def test_list_tickets_with_pagination(client: AsyncClient, admin_headers: dict, user_headers: dict):
    """Paginação funciona corretamente"""
    for i in range(10):
        res = await client.post(
            "/tickets/", 
            json={"title": f"Ticket Pagina {i+1}", "message": "Mensagem válida para paginação."}, 
            headers=user_headers
        )
        assert res.status_code == 201

    response = await client.get("/tickets/?skip=0&limit=5", headers=admin_headers)
    assert response.status_code == 200
    assert len(response.json()) == 5

@pytest.mark.asyncio
async def test_update_ticket_as_admin(client: AsyncClient, admin_headers: dict, user_headers: dict):
    """Admin pode atualizar qualquer ticket"""
    create_res = await client.post(
        "/tickets/", 
        json={"title": "Antigo Titulo", "message": "Mensagem Antiga"}, 
        headers=user_headers
    )
    assert create_res.status_code == 201
    ticket_id = create_res.json()["id"]

    updated_data = {"title": "Novo Titulo Atualizado", "message": "Nova Mensagem Atualizada"}
    response = await client.put(f"/tickets/{ticket_id}", json=updated_data, headers=admin_headers)
    
    assert response.status_code == 200
    assert response.json()["title"] == "Novo Titulo Atualizado"

@pytest.mark.asyncio
async def test_update_ticket_forbidden_for_user(client: AsyncClient, user_headers: dict):
    """User normal não pode atualizar tickets"""
    ticket_data = {"title": "Titulo Teste", "message": "Mensagem Teste"}
    create_res = await client.post("/tickets/", json=ticket_data, headers=user_headers)
    assert create_res.status_code == 201
    ticket_id = create_res.json()["id"]
    
    response = await client.put(f"/tickets/{ticket_id}", json={"title": "Hacked Title"}, headers=user_headers)
    assert response.status_code == 403