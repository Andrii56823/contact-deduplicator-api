



def test_all_contacts_requires_auth(client):
    response = client.get("/contacts/all")
    assert response.status_code == 401