# MCP Send Message Simulation

## Use the project

This repository contains a FastAPI server that exposes a simple MCP service called `send_message_service` with two simulated tools: `send_email` and `send_sms`.  
The main MCP endpoint is mounted at:

- <http://localhost:8765/send_message_service/mcp>

There is also a help route:

- <http://localhost:8765/help>

## Ways to run the server

### Run locally with Python

- Create a virtual environment and install dependencies:

    ```shell
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

- Start the server:

    ```shell
    python3 main.py --host 0.0.0.0 --port 8765
    ```

### Use Docker (image and container)

``` shell
docker compose -f docker-compose.yml up -d --build
```

## Client

As an MCP client, you can use [Fastchat-MCP](https://github.com/rb58853/fastchat-mcp) and pass the following configuration:

```json
{
    "messages_simulation": {
        "protocol": "httpstream",
            "httpstream-url": "http://localhost:8765/send_message_service/mcp",
            "name": "send_message_service",
            "description": "This server specializes in send messages as simulation."
        }
}
```
