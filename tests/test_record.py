import json


def test_createRecord(app, db, client, prepare_es):
    response = client.post('/records/', data=json.dumps({"title": "necooo"}), content_type='application/json')
    print(response.data)
    assert response.status_code == 201

