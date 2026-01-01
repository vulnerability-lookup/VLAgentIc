import getpass

from spade_llm import LLMAgent, LLMProvider

from vlagentic.tools.current_time import current_time_tool
from vlagentic.tools.cwe import cwe_classify_tool, vulnerability_per_cwe_tool
from vlagentic.tools.calculate import math_tool
from vlagentic.tools.severity import severity_tool
from vlagentic.tools.weather import weather_tool


def get_llm_provider(model="qwen2.5:7b", temperature=0.7):
    """
    Returns an LLMProvider configured for Ollama.
    (qwen2.5:7b, llama3.1:8b)
    """
    return LLMProvider.create_ollama(
        model=model, base_url="http://localhost:11434/v1", temperature=temperature
    )


tools = [
    severity_tool,
    cwe_classify_tool,
    vulnerability_per_cwe_tool,
    weather_tool,
    current_time_tool,
    math_tool,
]


system_prompt = (
    "You are a security-focused assistant with access to specialized tools.\n\n"
    "You can use the following tools when appropriate:\n"
    "- classify_cwe: classify a vulnerability description into CWE categories\n"
    "- classify_severity: classify a vulnerability severity\n"
    "- vulnerability_info_by_cwe: retrieve recent vulnerabilities for a given CWE ID\n"
    "- get_current_time, calculate_math, get_weather for general assistance\n\n"
    "Tool usage guidelines:\n"
    "- If the user provides a vulnerability description and asks for classification, "
    "use classify_cwe and/or classify_severity.\n"
    "- If the user asks for recent or known vulnerabilities for a specific CWE "
    "(e.g. 'recent vulnerabilities for CWE-119'), "
    "use vulnerability_info_by_cwe.\n"
    "- Do NOT invent vulnerability data; always use tools for factual vulnerability information.\n\n"
    "Response style:\n"
    "- Be concise and factual.\n"
    "- Assume the audience has security knowledge.\n"
    "- Summarize vulnerabilities briefly (title, short description, affected vendor/product, link).\n"
    "- Avoid unnecessary verbosity or speculation.\n\n"
    "If no tool is relevant, respond directly in plain text."
)


def init_llm_agent(xmpp_server):
    llm_agent = LLMAgent(
        jid=f"tool_assistant@{xmpp_server}",
        password=getpass.getpass("LLM agent password: "),
        provider=get_llm_provider(),
        system_prompt=system_prompt,
        tools=tools,
    )
    return llm_agent
