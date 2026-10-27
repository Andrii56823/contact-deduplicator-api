


def test_all_contacts_requires_auth(client):
    response = client.get("/contacts/all")
    assert response.status_code == 401

def test_create_contact_requires_auth(client):
    response = client.post("/contacts/create", json={"name": "Test"})
    assert response.status_code == 401

def test_create_contact(client, auth_headers):
    response = client.post(
        "/contacts/create",
        json={"name": "Test", "email": "ivan@example.com"},                    
        headers=auth_headers,                  
    )
    assert response.status_code == 200  
    assert response.json()["name"] == "Test" 

def test_find_duplicates(client, auth_headers):
    names = ["John Smith", "Jon Smith", "Maria Kovalenko"]
    for name in names:
        client.post(
            "/contacts/create",
            json={"name": name, "email": "test@example.com"},
            headers=auth_headers,
        )

    response = client.get("/contacts/find-duplicates", headers=auth_headers)  
    assert response.status_code == 200                  
    assert len(response.json()) == 1                