from spade_llm import LLMAgent

from vlagentic.agent.llm import get_llm_provider

from vlagentic.tools.current_time import current_time_tool
from vlagentic.tools.cwe import cwe_tool
from vlagentic.tools.calculate import math_tool
from vlagentic.tools.severity import severity_tool
from vlagentic.tools.weather import weather_tool

tools = [
    severity_tool,
    cwe_tool,
    weather_tool,
    current_time_tool,
    math_tool,
]


def init_llm_vlai_agent(xmpp_server):
    llm_agent = LLMAgent(
        jid=f"vlai_assistant@{xmpp_server}",
        password="password",
        provider=get_llm_provider(),
        system_prompt=(
            "You are a helpful assistant with access to tools: classify_severity, classify_cwe. "
            "Use these tools when appropriate to help users. "
            "You receive messages that may contain vulnerability descriptions.\n"
            "When appropriate, classify their severity or CWE using the available tools.\n"
            "Explain results clearly and concisely for a security audience.\n"
            "If classification is not relevant, respond directly."
        ),
        tools=[severity_tool, cwe_tool],
    )
    return llm_agent


def init_llm_tool_agent(xmpp_server):
    llm_agent = LLMAgent(
        jid=f"tool_assistant@{xmpp_server}",
        password="password",
        provider=get_llm_provider(),
        system_prompt=(
            "You are a helpful assistant with access to tools: get_current_time, calculate_math, and get_weather. "
            "Use these tools when appropriate to help users. "
            "You receive messages that may contain questions related to math, weather, time.\n"
        ),
        tools=[weather_tool, current_time_tool, math_tool],
    )
    return llm_agent
