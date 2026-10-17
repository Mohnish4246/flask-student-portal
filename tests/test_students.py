def test_students_page(client):
    response = client.get(
        "/students"
    )
    assert response.status_code in [200,302]