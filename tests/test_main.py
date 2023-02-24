import asyncio
from multiprocessing import Process

import pytest
from fastapi.testclient import TestClient

from main import main
from servers.http_server import http_server_app


def run_server():
    asyncio.run(main())


@pytest.fixture
def server():
    proc = Process(target=run_server, args=(), daemon=True)
    proc.start()
    yield
    proc.kill()


def test_read_main(server):
    test_data_in_json = '{"test":4}'
    http_server_test_client = TestClient(http_server_app)

    response = http_server_test_client.post("/api/ui", content=test_data_in_json)
    assert response.status_code == 200
    assert response.text == test_data_in_json
