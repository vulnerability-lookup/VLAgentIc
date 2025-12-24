import spade
import getpass
from datetime import datetime
from spade_llm import LLMAgent, ChatAgent, LLMProvider, LLMTool

from vlagentic.agent.severity_agent import severity_tool


# Simple tool functions
def get_current_time() -> str:
    """Get the current date and time."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def calculate_math(expression: str) -> str:
    """Safely evaluate a mathematical expression."""
    try:
        # Only allow basic math operations for safety
        allowed_names = {
            k: v
            for k, v in __builtins__.items()
            if k in ["abs", "round", "min", "max", "sum"]
        }
        result = eval(expression, {"__builtins__": allowed_names})
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"


def get_weather(city: str) -> str:
    """Get simulated weather for a city."""
    weather_data = {
        "madrid": "22°C, sunny",
        "london": "15°C, cloudy",
        "new york": "18°C, rainy",
        "tokyo": "25°C, clear",
        "paris": "19°C, partly cloudy",
        "barcelona": "24°C, sunny",
        "luxembourg": "2.3°C, cloudy"
    }
    return weather_data.get(city.lower(), f"No weather data available for {city}")


async def main():
    print("🔧 Custom Tools Tutorial: Basic Tool Creation")

    # Configuration
    xmpp_server = input("XMPP server domain (default: localhost): ") or "localhost"

    # Create provider (using Ollama as in the example)
    provider = LLMProvider.create_ollama(
        model="qwen2.5:7b",  # Or any model that supports function calling
        base_url="http://localhost:11434/v1",
        temperature=0.7,
    )

    # Create tools with proper schema definitions
    tools = [
        severity_tool,
        LLMTool(
            name="get_current_time",
            description="Get the current date and time",
            parameters={"type": "object", "properties": {}, "required": []},
            func=get_current_time,
        ),
        LLMTool(
            name="calculate_math",
            description="Safely evaluate a mathematical expression",
            parameters={
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Mathematical expression to evaluate (e.g., '2 + 3 * 4')",
                    }
                },
                "required": ["expression"],
            },
            func=calculate_math,
        ),
        LLMTool(
            name="get_weather",
            description="Get weather information for a city",
            parameters={
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "City name (e.g., 'Madrid', 'London')",
                    }
                },
                "required": ["city"],
            },
            func=get_weather,
        ),
    ]

    # Create LLM agent with tools
    llm_agent = LLMAgent(
        jid=f"tool_assistant@{xmpp_server}",
        password=getpass.getpass("LLM agent password: "),
        provider=provider,
        system_prompt="You are a helpful assistant with access to tools: classify_severity, get_current_time, calculate_math, and get_weather. Use these tools when appropriate to help users."
        "You receive messages that may contain vulnerability descriptions.\n"
        "When appropriate, classify their severity using the available tools.\n"
        "Explain results clearly and concisely for a security audience.\n"
        "If classification is not relevant, respond directly.",
        tools=tools,  # Pass tools to the agent
    )

    # Create chat interface
    def display_response(message: str, sender: str):
        print(f"\n🤖 Tool Assistant: {message}")
        print("-" * 50)

    chat_agent = ChatAgent(
        jid=f"user@{xmpp_server}",
        password=getpass.getpass("Chat agent password: "),
        target_agent_jid=f"tool_assistant@{xmpp_server}",
        display_callback=display_response,
    )

    try:
        # Start agents
        await llm_agent.start()
        await chat_agent.start()

        print("✅ Tool assistant started!")
        print("🔧 Available tools:")
        print("• classify_severity - Get severity classification of a vulnerability based on its description")
        print("• get_current_time - Get current date and time")
        print("• calculate_math - Perform mathematical calculations")
        print("• get_weather - Get weather for major cities")
        print("\n💡 Try these queries:")
        print("• 'What time is it?'")
        print("• 'Calculate 15 * 8 + 32'")
        print("• 'What's the weather in Madrid?'")
        print("• 'What's the severity of the vulnerability described by ...?'")
        print("Type 'exit' to quit\n")

        # Run interactive chat
        await chat_agent.run_interactive()

    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
    finally:
        await chat_agent.stop()
        await llm_agent.stop()
        print("✅ Agents stopped successfully!")


if __name__ == "__main__":
    print("🚀 Prerequisites:")
    print("• Ollama running: ollama serve")
    print("• Model available: ollama pull qwen2.5:7b")
    print("• XMPP server running")
    print()

    spade.run(main())
