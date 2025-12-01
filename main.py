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
def send_email(emails: list[str], subject: str, body: str) -> str:
    """
    Send an email to the specified list of email addresses with the given subject and body.

    Args:
        emails: List of email addresses to send to
        subject: Email subject line
        body: Email body content
    """
    # Simulate sending emails to all addresses
    sent_count = len(emails)
    return f"Emails sent to {sent_count} recipients ({', '.join(emails)}) with subject '{subject}'"


@mcp.tool()
def send_sms(phone_numbers: list[str], message: str) -> str:
    """
    Send an SMS to the specified list of phone numbers with the given message.

    Args:
        phone_numbers: List of phone numbers to send SMS to
        message: SMS message content
    """
    # Simulate sending SMS to all phone numbers
    sent_count = len(phone_numbers)
    return f"SMS sent to {sent_count} numbers ({', '.join(phone_numbers)}) with message '{message}'"


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
