import asyncio
import logging

import uvicorn

from configs.servers_config_reader import ConfigReader


async def create_webserver(file_name: str, host: str, port: int):
    server_config = uvicorn.Config(f"servers.{file_name}:{file_name}_app", host=host, port=port, log_level="info")
    server = uvicorn.Server(server_config)
    await server.serve()


async def main():
    servers_config = ConfigReader()
    await asyncio.wait([
        asyncio.create_task(create_webserver("http_server", servers_config.http_host, servers_config.http_port)),
        asyncio.create_task(create_webserver("websocket_server", servers_config.ws_host, servers_config.ws_port))
    ])


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
