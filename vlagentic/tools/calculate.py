from spade_llm import LLMTool


def calculate_math(expression: str) -> str:
    try:
        allowed_names = {
            k: v
            for k, v in __builtins__.items()
            if k in ["abs", "round", "min", "max", "sum"]
        }
        result = eval(expression, {"__builtins__": allowed_names})
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"


math_tool = LLMTool(
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
)
