import spade

from vlagentic.agent.chat import init_chat_agent


async def main():
    xmpp_server = input("XMPP server domain (default: localhost): ") or "localhost"

    chat_agent = init_chat_agent(xmpp_server)

    try:

        await chat_agent.start()
        chat_agent.presence.set_available()
        chat_agent.presence.on_subscribe = lambda jid: chat_agent.presence.approve(jid)

        print("✅ Agent started!")
        print("🔧 Available tools:")
        print("• classify_severity")
        print("• classify_cwe")
        print("• get_current_time")
        print("• calculate_math")
        print("• get_weather")
        print("\n💡 Try these queries:")
        print("• 'What's the severity of the vulnerability described by ...?'")
        print("• 'What time is it?'")
        print("• 'Calculate 15 * 8 + 32'")
        print("• 'What's the weather in Luxembourg?'")

        # Start agent web interfaces
        # await chat_agent.web.start(hostname="127.0.0.1", port="10001")
        # print("Chat Agent Web Interface: http://127.0.0.1:10001/spade")

        # Run interactive chat
        await chat_agent.run_interactive(response_timeout=300)

    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
    finally:
        await chat_agent.stop()
        print("✅ Agent stopped successfully!")


if __name__ == "__main__":
    print("🚀 Prerequisites:")
    print("• XMPP server running")
    print()
    spade.run(main())
