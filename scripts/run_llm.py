import asyncio

import spade

from vlagentic.agent.llm import init_llm_agent


async def main():
    xmpp_server = input("XMPP server domain (default: localhost): ") or "localhost"
    llm_agent = init_llm_agent(xmpp_server)

    try:
        await llm_agent.start()

        llm_agent.presence.set_available()
        llm_agent.presence.on_subscribe = lambda jid: llm_agent.presence.approve(jid)

        # Start agent web interface
        await llm_agent.web.start(hostname="127.0.0.1", port="10000")
        print("LLM Agent Web Interface: http://127.0.0.1:10000/spade")

        print("Press Ctrl+C to exit.")

        # Keep agent alive
        while True:
            await asyncio.sleep(1)

    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
    finally:
        await llm_agent.stop()
        print("✅ Agent stopped successfully!")


if __name__ == "__main__":
    print("🚀 Prerequisites:")
    print("• Ollama running: ollama serve")
    print("• Model available: ollama pull qwen2.5:7b")
    print("• XMPP server running")
    print()
    spade.run(main())
