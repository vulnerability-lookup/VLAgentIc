from spade_llm import LLMAgent, LLMTool

from vlagentic.tools.severity_classifier import SeverityClassifierTool
from vlagentic.agent.llm import get_llm_provider


# ---------------------------------------------------------------------------
# Tool definition (agentic-style)
# ---------------------------------------------------------------------------

_classifier = SeverityClassifierTool(
    model_name="CIRCL/vulnerability-severity-classification-roberta-base"
)

async def classify_severity(text: str) -> dict:
    """
    Tool wrapper used by the LLM.
    """
    return _classifier(text)

def get_weather(city: str) -> str:
    """Get weather information for major cities."""
    weather_data = {
        "madrid": "22°C, sunny with light clouds",
        "london": "15°C, cloudy with occasional rain",
        "new york": "18°C, rainy with strong winds",
        "tokyo": "25°C, clear skies",
        "paris": "19°C, partly cloudy",
        "barcelona": "24°C, sunny and warm",
        "berlin": "16°C, overcast",
        "rome": "26°C, sunny",
    }
    return weather_data.get(city.lower(), f"Weather data not available for {city}")


severity_tool = LLMTool(
    name="classify_severity",
    description=(
        "Classify the severity of a vulnerability description using "
        "the VLAI RoBERTa-based model. Returns severity label and confidence."
    ),
    parameters={
        "type": "object",
        "properties": {
            "text": {
                "type": "string",
                "description": "Vulnerability description to classify"
            }
        },
        "required": ["text"]
    },
    func=classify_severity,
)

weather_tool = LLMTool(
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
)



# ---------------------------------------------------------------------------
# Agent definition
# ---------------------------------------------------------------------------

class SeverityAgent(LLMAgent):
    def __init__(self, jid: str, password: str):
        super().__init__(
            jid=jid,
            password=password,
            provider=get_llm_provider(),
            system_prompt=(
                "You are a security analysis agent with access to tools: classify_severity, get_weather.  Use these tools when appropriate to help users.\n\n"
                "You receive messages that may contain vulnerability descriptions.\n"
                "When appropriate, classify their severity using the available tools.\n"
                "Explain results clearly and concisely for a security audience.\n"
                "If classification is not relevant, respond directly."
            ),
            tools=[severity_tool, weather_tool],
        )


