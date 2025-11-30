from fastapi.responses import RedirectResponse
from mcp.server.fastmcp import FastMCP
from uvicorn import Config, Server
from fastapi import FastAPI
import contextlib
import asyncio
import click

EXPOSE_URL = "http://localhost:8765"

mcp: FastMCP = FastMCP(name="send_message_service")


@mcp.tool()
def send_email(email: str, subject: str, body: str) -> str:
    """
    Send an email to the specified address with the given subject and body.
    """
    # Simulate sending an email
    return f"Email sent to {email} with subject '{subject}'"


@mcp.tool()
def send_sms(phone_number: str, message: str) -> str:
    """
    Send an SMS to the specified phone number with the given message.
    """
    # Simulate sending an SMS
    return f"SMS sent to {phone_number} with message '{message}'"


app: FastAPI = FastAPI()


# Create a combined lifespan to manage both session managers
@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    async with contextlib.AsyncExitStack() as stack:
        await stack.enter_async_context(mcp.session_manager.run())
        yield


app = FastAPI(lifespan=lifespan)
app.mount(f"/{mcp.name}", mcp.streamable_http_app())


@app.get("/", include_in_schema=False)
async def redirect_to_help():
    return RedirectResponse(url="/help")


@app.get("/help", include_in_schema=False)
async def help():
    return {
        "mcp_servers": [f"{EXPOSE_URL}/{mcp.name.replace(' ','_')}/mcp"],
        "client_example": "https://github.com/rb58853/fastchat-mcp",
    }


@click.command()
@click.option("--port", default=8765, help="Port to listen on")
@click.option("--host", default="0.0.0.0", help="Host to hosted on")
def main(port: int, host: str):
    async def run_server() -> None:
        config = Config(
            app,
            host=host,
            port=port,
            log_level="info",
        )
        server = Server(config)

        print(f"🚀 MCP Send Messages Httpstream Server running on http://{host}:{port}")
        await server.serve()
    asyncio.run(run_server())


if __name__ == "__main__":
    main()
