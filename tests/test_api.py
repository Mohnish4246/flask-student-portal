def test_api_without_token(client):
    response = client.get(
        "/api/students"
    )

    assert response.status_code == 401