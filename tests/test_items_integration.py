def test_create_and_list_item(client):
    create_response = client.post(
        "/items",
        json={
            "name": "integration-item",
            "description": "created through the API",
        },
    )

    assert create_response.status_code == 201
    created = create_response.json()
    assert created["name"] == "integration-item"
    assert created["id"] > 0

    list_response = client.get("/items")

    assert list_response.status_code == 200
    assert any(item["id"] == created["id"] for item in list_response.json())
