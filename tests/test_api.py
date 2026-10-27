CUSTOMER = {"customer_id": "acme"}


async def test_empty_order_list(client):
    response = await client.get("/orders", params=CUSTOMER)
    assert response.status_code == 200
    assert response.json() == []


async def test_ingest_then_get_order(client, ingest, order_event):
    await ingest(order_event)
    response = await client.get("/orders/1001", params=CUSTOMER)
    assert response.status_code == 200
    assert response.json() == order_event


async def test_list_customer_orders(client, ingest, order_event):
    second = {**order_event, "order_id": 1002, "items": [{"sku": "NOTEBOOK-A5", "quantity": 3}]}
    other_customer = {**order_event, "order_id": 2001, "customer_id": "globex"}
    for event in (second, other_customer, order_event):
        await ingest(event)
    response = await client.get("/orders", params=CUSTOMER)
    assert response.status_code == 200
    assert sorted(response.json(), key=lambda order: order["order_id"]) == [order_event, second]


async def test_new_snapshot_updates_order(client, ingest, order_event):
    await ingest(order_event)
    updated = {**order_event, "status": "shipped"}
    await ingest(updated)
    response = await client.get("/orders/1001", params=CUSTOMER)
    assert response.status_code == 200
    assert response.json() == updated
    response = await client.get("/orders", params=CUSTOMER)
    assert response.status_code == 200
    assert response.json() == [updated]
