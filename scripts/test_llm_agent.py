import asyncio

from spade.message import Message
from vlagentic.agent.severity_agent import SeverityAgent


async def main():
    # Start the agent
    agent = SeverityAgent("severity@localhost", "password")
    await agent.start()
    print("SeverityAgent running...")

    # Send a test vulnerability description
    msg = Message(to="severity@localhost")
    msg.body = "The authentication module contains a buffer overflow vulnerability."
    await agent.send(msg)

    # Wait to receive reply
    await asyncio.sleep(10)

    # Stop agent
    await agent.stop()


asyncio.run(main())
