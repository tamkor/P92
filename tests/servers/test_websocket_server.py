from fastapi.testclient import TestClient

from servers.websocket_server import websocket_server_app


def test_websocket_endpoint_response_is_the_same():
    websocket_test_client = TestClient(websocket_server_app)
    test_data_in_json = {"test": 4}

    with websocket_test_client.websocket_connect("/") as websocket:
        websocket.send_json(test_data_in_json)
        response = websocket.receive_json()
        assert response == test_data_in_json
