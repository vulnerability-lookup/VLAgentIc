# VLAgentIc

The concept of an AI agent—combining models, tools, and orchestration logic—has become fairly standardized over the past year.  
Common patterns and frameworks for building such agents are also emerging.  

![VLAI is Agentic!](docs/VLAIgentIc.png)

While AI agents are becoming more common, **VLAgentIc** explores a unique approach in AI-assisted cybersecurity. Its agents communicate over XMPP, benefiting from behaviours for concurrent tasks, mailboxes for asynchronous messaging, and built-in presence and discovery support.


## Features

- Modular AI agents combining reasoning (LLM) and tools
- Tool orchestration with clear mental models
- XMPP-based communication between agents
- Integration with the Vulnerability-Lookup API and custom classifiers (e.g., CWE and severity classification)


## Architecture

```mermaid
graph LR
    Ch[Chat Agent] <--> A[LLMAgent]
    A --> C[ContextManager]
    A --> D[LLMProvider]
    A --> E[LLMTool]
    D --> F[OpenAI/Ollama/etc]
    E --> I[Human-in-the-Loop]
    E --> T1[VLAI Severity - Text Classification]
    E --> T2[VLAI CWE - Text Classification]
    E --> T3[Vulnerability-Lookup API]
    E --> J[MCP]
    J --> K[STDIO]
    J --> L[HTTP Streaming]
```

Human-in-the-loop is still in work and will be probably linked to the Vulnerability-Lookup API tool.  
The LLM provider can be configured in ``vlagentic.agent.llm:get_llm_provider()``. The default is ``qwen2.5:7b``.


**Component Overview:**


| Component          | Description                                                                        |
| ------------------ | ---------------------------------------------------------------------------------- |
| **ChatAgent**      | Entry point optionnaly with guardrails filtering.                                  |
| **LLMAgent**       | Core agent that reasons using a language model.                                    |
| **ContextManager** | Tracks conversation state and memory.                                              |
| **LLMProvider**    | Connects to models (OpenAI, Ollama, Qwen, etc.).                                   |
| **LLMTool**        | Performs actions such as classification, API queries, or human-in-the-loop checks. |
| **MCP**            | Multi-channel publisher for STDIO or HTTP streaming outputs.                       |

The **LLMAgent** (Qwen) leverages the
[VLAI Severity classification](https://huggingface.co/CIRCL/vulnerability-severity-classification-roberta-base) and
[VLAI CWE classification](https://huggingface.co/CIRCL/cwe-parent-vulnerability-classification-roberta-base) models as integrated tools, enabling automated vulnerability severity assessment and CWE categorization within its reasoning workflow.



## Agent Principle

```text
VLAgentIcAgent
 ├── Reasoning (LLM via spade-llm, Ollama or API)
 ├── Tools
 │    ├── SeverityClassifierTool (RoBERTa)
 │    ├── CVSS normalizer tool (planned)
 │    └── Other extensible tools
 └── Actions / Messages
 ```

```text
You: "What is the severity of the vulnerability described ..."
LLM: "This looks like a vulnerability description.
      I should classify severity."
→ calls severity_classifier tool
→ receives result
→ explains or forwards
```

Tools are assigned to an (LLM) agent. An agent can use one or multiple tools and should clearly explain their functionality.
Communications via XMPP/FIPA.


## Test



Install Ollama

```bash
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull llama3.1:8b
ollama pull qwen2.5:7b
ollama serve
```

```bash
# Check if default ports are already in use
netstat -an | grep 5222

# Try different ports if needed, or shutdown prosodyctl
spade run --client_port 6222 --server_port 6269
```

then use the Web interface to create the agent's password.


Alternatively (maybe even better, and it's what had been tested so far), use Prosody. In this
case create the agent's password:

```bash
$ sudo prosodyctl adduser severity_agent@localhost
Password: password
```

```bash
scripts/run_all.py
```

It will be registered to the registry and presence notification system.

Monitor incoming messages:

![alt text](docs/agent-monitoring.png)



