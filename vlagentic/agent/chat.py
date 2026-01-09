import getpass
import json

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from spade_llm import ChatAgent

console = Console()


def display_response(message: str, sender: str = "Tool Assistant", **metadata):
    """
    Display agent messages in rich panels, with optional metadata.
    Confidence values are color-coded.
    """

    # Header with sender
    header = Text(f"🗨️  {sender}", style="bold cyan")

    # Main message
    message_text = Text(message, style="white")

    # Metadata panel
    metadata_panel = None
    if metadata:
        # Use a proper Table instead of Table.grid
        table = Table(show_header=False, box=box.SIMPLE, expand=True)
        table.add_column("Key", style="bold magenta", justify="right")
        table.add_column("Value", style="white", justify="left")

        for key, value in metadata.items():
            # Pretty-print JSON structures
            if isinstance(value, dict):
                value = json.dumps(value, indent=2)

            # Color confidence values
            if "confidence" in key.lower():
                try:
                    conf = float(value)
                    if conf >= 0.6:
                        style = "bold green"
                    elif conf >= 0.3:
                        style = "bold yellow"
                    else:
                        style = "bold red"
                    value = Text(f"{conf:.3f}", style=style)
                except Exception:
                    pass

            # Add to table
            table.add_row(str(key), value if isinstance(value, Text) else str(value))

        metadata_panel = Panel(table, title="📌 Metadata", box=box.ROUNDED, style="dim")

    # Compose full panel
    if metadata_panel:
        console.print(
            Panel.fit(
                Panel(message_text, title=header, box=box.ROUNDED, style="green"),
                metadata_panel,
                box=box.SQUARE,
            )
        )
    else:
        console.print(Panel(message_text, title=header, box=box.ROUNDED, style="green"))


def init_chat_agent(xmpp_server, agent_name="chat_agent"):
    agent_name = input("Agent name (default: chat_agent): ") or agent_name

    chat_agent = ChatAgent(
        jid=f"{agent_name}@{xmpp_server}",
        password=getpass.getpass("Chat agent password: "),
        target_agent_jid=f"tool_assistant@{xmpp_server}",
        display_callback=display_response,
    )

    return chat_agent
