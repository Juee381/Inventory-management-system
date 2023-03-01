def test_create_item_in_store(client):
    response = client.post("/item", json={"name": "item1",
                                          "category": "cat1",
                                          "expiry_time": "2023-12-12 22:37:10",
                                          "quantity": 3,
                                          "manufacturing_time": "2022-1-12 22:37:10",
                                          "image": "Screenshot from 2023-01-05 11-59-56.png",
                                          "store_id": 1},
                           )

    assert response.status_code == 201
    assert response.json == {"category": "cat1", "expiry_time": "2023-12-12T11:07:10", "id": 1,
                             "image": "Screenshot from 2023-01-05 11-59-56.png",
                             "manufacturing_time": "2022-01-12T11:07:10", "name": "item1", "quantity": 3,
                             "store": {"id": 1, "name": "Store1"}
                             }
    assert response.json["name"] == "item1"
    assert response.json["category"] == "cat1"
    assert response.json["store"] == {"id": 1, "name": "Store1"}


def test_create_item_with_store_id_not_found(client):
    response = client.post("/item", json={"name": "item1",
                                          "category": "cat1",
                                          "expiry_time": "2023-12-12 22:37:10",
                                          "quantity": 3,
                                          "manufacturing_time": "2022-1-12 22:37:10",
                                          "image": "Screenshot from 2023-01-05 11-59-56.png",
                                          "store_id": 2},
                           )

    assert response.status_code == 201
    assert response.json == {
        "code": 400,
        "message": "Store does not exist with given store id",
        "status": "Bad Request"
    }


def test_create_item_with_unknown_data(client):
    response = client.post("/item", json={
        "name": "item5",
        "category": "cat1",
        "expiry_time": "2023-12-12 22:37:10",
        "quantity": 3,
        "manufacturing_time": "2022-1-12 22:37:10",
        "image": "Screenshot from 2023-01-05 11-59-56.png",
        "store_id": 1,
        "image_type": ".png"
    }, )

    assert response.status_code == 422
    assert response.json == {
        "code": 422,
        "errors": {
            "json": {
                "image_type": ["Unknown field."]
            }
        },
        "status": "Unprocessable Entity"
    }


def test_get_all_items(client):
    client.post("/item", json={
        "name": "item1",
        "category": "cat1",
        "expiry_time": "2023-12-12 22:37:10",
        "quantity": 3,
        "manufacturing_time": "2022-1-12 22:37:10",
        "image": "Screenshot from 2023-01-05 11-59-56.png",
        "store_id": 1,
    },
                )

    response = client.get("/item", )

    assert response.status_code == 200

    assert response.json == {
        "category": "cat1",
        "expiry_time": "2023-12-12T11:07:10",
        "id": 1,
        "manufacturing_time": "2022-01-12T11:07:10",
        "name": "item3",
        "quantity": 3,
        "store": {
            "id": 1,
            "name": "store1"
        }
    }


def test_get_all_items_empty(client):
    response = client.get("/item", )

    assert response.status_code == 200
    assert len(response.json) == 0
    assert response.json == []


def test_get_specific_item_details(client, item_id):
    client.post("/item", json={
        "name": "item1",
        "category": "cat1",
        "expiry_time": "2023-12-12 22:37:10",
        "quantity": 3,
        "manufacturing_time": "2022-1-12 22:37:10",
        "image": "Screenshot from 2023-01-05 11-59-56.png",
        "store_id": 1,
    },
                )

    response = client.get(f"/item/{item_id}", )

    assert response.status_code == 200
    assert response.json["name"] == "item1"
    assert response.json == {
        "category": "cat1",
        "expiry_time": "2023-12-12T11:07:10",
        "id": 1,
        "image": "Screenshot from 2023-01-05 11-59-56.png",
        "manufacturing_time": "2022-01-12T11:07:10",
        "name": "item5",
        "quantity": 3,
        "store": {
            "id": 1,
            "name": "Store1"
        }
    }


def test_get_item_detail_not_found(client):
    response = client.get("/item/10", )

    assert response.status_code == 404
    assert response.json == {"code": 404, "status": "Not Found"}


def test_delete_item(client, item_id):
    response = client.delete(f"/item/{item_id}", )

    assert response.status_code == 200
    assert response.json["message"] == "Item deleted."


def test_delete_item_detail_not_found(client):
    response = client.get("/item/10", )

    assert response.status_code == 404
    assert response.json == {"code": 404, "status": "Not Found"}


def test_delete_list_of_items(client):
    response = client.post("/del_item", json={
        "del_items": [1, 2]
    },
                           )

    assert response.json == {
        "message": "Deleted list of item"
    }


def test_delete_list_of_items_not_found(client):
    response = client.post("/del_item", json={
        "del_items": [1, 2]
    },
                           )

    assert response.status_code == 404
    assert response.json == {
        "code": 404,
        "message": "item not found.",
        "status": "Not Found"
    }
