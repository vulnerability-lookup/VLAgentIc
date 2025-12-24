import asyncio
import getpass

import spade
from spade_llm import ChatAgent, LLMProvider, LLMAgent

from vlagentic.agent.severity_agent import SeverityAgent
from vlagentic.agent.severity_agent import severity_tool, weather_tool


async def main():
    # severity_agent = SeverityAgent("severity_agent@localhost", "password")

    provider = LLMProvider.create_ollama(
        model="qwen2.5:7b",  # Or any model that supports function calling
        base_url="http://localhost:11434/v1",
        temperature=0.7,
    )
    llm_agent = LLMAgent(
        jid="severity_agent@localhost",
        password=getpass.getpass("LLM agent password: "),
        provider=provider,
        system_prompt="You are a helpful assistant with access to tools: get_current_time, calculate_math, and get_weather. Use these tools when appropriate to help users.",
        tools=[severity_tool, weather_tool],  # Pass tools to the agent
    )

    # Create chat interface
    def display_response(message: str, sender: str):
        print(f"\n🤖 Multi-Tool Agent: {message}")
        print("-" * 60)

    chat_agent = ChatAgent(
        jid=f"ChatAgent@localhost",
        password=getpass.getpass("Chat agent password: "),
        target_agent_jid=f"tool_assistant@localhost",
        display_callback=display_response,
    )

    try:

        # await severity_agent.start()
        await llm_agent.start()
        await chat_agent.start()

        print("VLAgentIc running")

        # Run interactive chat
        await chat_agent.run_interactive()

        # await severity_agent.web.start(hostname="127.0.0.1", port="10000")
        # print("Web Graphical Interface available at:")
        # print("  http://127.0.0.1:10000/spade")
        # print("Wait until user interrupts with ctrl+C")
        # while True:  # not agent.CollectingBehav.is_killed():
        #     try:
        #         await asyncio.sleep(1)
        #     except KeyboardInterrupt:
        #         break
        # assert severity_agent.CollectingBehav.exit_code == 10

    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
    finally:
        severity_agent.stop()
        chat_agent.stop()
        print("✅ Agents stopped successfully!")


if __name__ == "__main__":
    spade.run(main())
