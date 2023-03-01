def test_get_all_store(client):
    response = client.get("/store", )

    assert response.status_code == 200
    assert response.json == {
        "id": 1,
        "items": [
            {
                "category": "cat1",
                "expiry_time": "2023-12-12T11:07:10",
                "id": 1,
                "image": "Screenshot from 2023-01-05 11-59-56.png",
                "manufacturing_time": "2022-01-12T11:07:10",
                "name": "item1",
                "quantity": 3
            },
            {
                "category": "cat2",
                "expiry_time": "2023-12-12T11:07:10",
                "id": 2,
                "image": "Screenshot from 2023-01-05 11-59-56.png",
                "manufacturing_time": "2022-01-12T11:07:10",
                "name": "item2",
                "quantity": 3
            },
        ],
        "name": "store1"
    }


def test_get_all_store_if_not_any_exist(client):
    response = client.get("/store", )

    assert response.status_code == 200
    assert response.json == []


def test_get_store(client, store_id):
    response = client.get(f"/store/{store_id}", )

    assert response.status_code == 200
    assert response.json == {
        "id": 1,
        "items": [],
        "name": "store1"
    }


def test_get_store_not_found(client, store_id):
    response = client.get(f"/store/{store_id}", )

    assert response.status_code == 404
    assert response.json == {"code": 404, "status": "Not Found"}


def test_create_store(client):
    response = client.post("/store", json={"name": "Store1"}, )

    assert response.status_code == 201
    assert response.json["name"] == "Store1"


def test_create_already_exist_store(client):
    response = client.post("/store", json={"name": "Store1"}, )

    assert response.status_code == 409
    assert response.json == {"code": 409, "message": "A store with that name already exists.", "status": "Conflict"}


def test_delete_store(client, store_id):
    response = client.delete(f"/store/{store_id}")

    assert response.status_code == 200
    assert response.json == {"message": "Store deleted"}


def test_delete_store_doesnt_exist(client, store_id):
    response = client.delete(f"/store/{store_id}")

    assert response.status_code == 404
    assert response.json == {"code": 404, "status": "Not Found"}


def test_get_store_list_single(client):
    client.post("/store", json={"name": "Store1"}, )

    response = client.get("/store", )

    assert response.status_code == 200
    assert response.json == [{"id": 1, "name": "Store1", "items": []}]


def test_get_store_list_multiple(client):
    client.post("/store", json={"name": "Store1"}, )
    client.post("/store", json={"name": "Store2"}, )

    response = client.get("/store", )

    assert response.status_code == 200
    assert response.json == [
        {"id": 1, "name": "Store1", "items": []},
        {"id": 2, "name": "Store2", "items": []},
    ]


def test_update_store_name(client, store_id):
    response = client.post(f"/item/{store_id}", json={"name": "Store2"}, )

    assert response.status_code == 201
    assert response.json["name"] == "Store1"
