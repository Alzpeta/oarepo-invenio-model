import json

#todo elasticsearch UnsupportedProductError
def test_createRecord(app, db, client):
    response = client.post('/records/', data=json.dumps({"title": "necooo"}), content_type='application/json')
    print(response.data)
    assert response.status_code == 201
