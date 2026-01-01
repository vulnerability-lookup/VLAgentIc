import requests
from spade_llm import LLMTool


def get_weather(city: str) -> str:
    url = f"https://wttr.in/{city}?format=3"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text.strip()
    else:
        return f"Weather data not available for {city}"


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

if __name__ == "__main__":
    print(get_weather("Luxembourg"))
