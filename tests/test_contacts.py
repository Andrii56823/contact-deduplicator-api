


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

def test_merge_contacts(client, auth_headers):
    keep = client.post(
        "/contacts/create",
        json={"name": "John Smith", "email": "john@example.com"},
        headers=auth_headers,
    ).json()
    remove = client.post(
        "/contacts/create",
        json={"name": "Jon Smith", "email": "jon@example.com", "phone": "123456"},
        headers=auth_headers,
    ).json()

    response = client.post(
        f"/contacts/merge/{keep['id']}/{remove['id']}",
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["phone"] == "123456"

    contacts = client.get("/contacts/all", headers=auth_headers).json()
    assert len(contacts) == 1  

def test_merge_contact_with_itself(client, auth_headers):
    contact = client.post(
        "/contacts/create",
        json={"name": "John Smith", "email": "john@example.com"},
        headers=auth_headers,
    ).json()

    response = client.post(
        f"/contacts/merge/{contact['id']}/{contact['id']}",
        headers=auth_headers,
    )
    assert response.status_code == 400

    contacts = client.get("/contacts/all", headers=auth_headers).json()
    assert len(contacts) == 1            