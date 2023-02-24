from unittest import mock

from fastapi.testclient import TestClient
from starlette import status

from servers.http_server import JSON_ERROR_MSG, http_server_app, WS_ERROR_MSG

http_server_test_client = TestClient(http_server_app)


@mock.patch("websockets.connect.return_value.__aenter__.return_value.recv")
@mock.patch("websockets.connect")
def test_forward_ok(_, mocked_recv):
    test_data_in_json = '{"test":4}'

    mocked_recv.return_value = test_data_in_json
    response = http_server_test_client.post("/api/ui", content=test_data_in_json)
    assert response.status_code == 200
    assert response.text == test_data_in_json


def test_forward_with_invalid_json():
    response = http_server_test_client.post("/api/ui", content="{{invalid_json}")
    assert response.status_code == status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
    assert response.json()["detail"] == JSON_ERROR_MSG


def test_forward_without_websocket_server():
    response = http_server_test_client.post("/api/ui", content="{}")
    assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
    assert response.json()["detail"] == WS_ERROR_MSG
