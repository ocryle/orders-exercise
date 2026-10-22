from app.consumer import handle_order_event


async def test_handler_persists_order(sessions, client, order_event):
    async with sessions.begin() as session:
        await handle_order_event(order_event, session)

    response = await client.get(f"/orders/{order_event['order_id']}", params={"customer_id": order_event["customer_id"]})
    assert response.status_code == 200
    assert response.json() == order_event
