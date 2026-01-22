# SentioCP AI – Command-Line Interface Demo (MVP)
## 🚀 Welcome to the SentioCP CLI Experience

This command-line application is a **Minimum Viable Product (MVP)** designed to demonstrate the core ideas behind the **SentioCP AI** platform within a lightweight, local setup.

## The SentioCP Vision
SentioCP enables intelligent AI agents that reason effectively while operating within rich, evolving context. Built with modularity, privacy-first principles, and full user control at its core, SentioCP places meaningful intelligence directly in the hands of developers and users.

This CLI illustrates how SentioCP coordinates three fundamental architectural layers:

1. 🧠 **AI Reasoning Layer** – The agent’s cognitive and decision-making core  
2. 🎯 **Intent Understanding Layer** – Determining and interpreting user objectives  
3. 🔗 **Context Connection Layer** – Supplying relevant, secure contextual data  

The purpose of this demo is to provide a hands-on view of how these layers work together, and how developers can experiment within SentioCP’s decentralized, modular, and trust-minimized AI framework.

---

## Core Ideas Demonstrated in This MVP

- **Context-Sensitive AI Agents**  
  Create distinct agents that reference isolated local data sources to tailor their responses.

- **Modular Command Execution**  
  Manage agents, curate contextual data, and perform natural-language queries through independent CLI commands.

- **Privacy-First Architecture**  
  All contextual information remains local. Only explicitly approved prompts are sent to the OpenAI API (when configured). No file uploads, background transfers, or hidden data sharing occur.

- **Simulated Intelligence Layer**  
  When enabled, OpenAI’s API is used to generate responses. The broader SentioCP architectural model remains intact and is demonstrated through the CLI’s orchestration of context, agents, and workflows.

---

# 📋 Requirements

- Python 3.7 or newer  
- OpenAI Python SDK → pip install openai  
- An OpenAI API key (OPENAI_API_KEY)  

---

# ⚙️ Getting Started Quickly

## 1. Save the CLI script
Place the `sentiocp.py` file into your project directory (for example: `sentiocp-cli-mvp`).

## 2. Navigate to the project directory

    cd path/to/sentiocp-cli-mvp

## 3. (Optional but recommended) Create a virtual environment

    python -m venv venv
    source venv/bin/activate   # macOS/Linux
    venv\Scripts\activate      # Windows

## 4. Install dependencies

    pip install openai

## 5. Configure your OpenAI API key

### macOS / Linux

    export OPENAI_API_KEY='your_key_here'

### Windows CMD

    set OPENAI_API_KEY=your_key_here

### PowerShell

    $env:OPENAI_API_KEY="your_key_here"

---

# 🛠️ Simulated SentioCP Architecture

## 1. 🔗 Context Connection Layer (Simulated)

In a full SentioCP deployment, agents retrieve data from decentralized and secure storage systems. In this MVP, that behavior is simulated using local files.

- Assign files to agents using named contexts  
- Organize multiple datasets per agent  
- Maintain complete user control over what context is included in each query  

Only explicitly selected context is passed along with OpenAI requests. No other data is stored or transmitted externally.

### CLI Commands

    python sentiocp.py context add <name> --file <path>
    python sentiocp.py context use <name>
    python sentiocp.py context show

---

## 2. 🎯 Intent Understanding Layer (Simulated)

This layer analyzes user input and determines intent. In the CLI, this is represented by:

- The ask "<query>" command  
- Optional OpenAI-powered interpretation and response generation  
- Minimal prompt structuring to ensure relevance and correct context usage  

### CLI Command

    python sentiocp.py ask "Your question here"

---

## 3. 🧠 AI Reasoning Layer (Simulated)

This layer represents the agent’s reasoning engine. In this MVP, responses are generated using OpenAI’s gpt-3.5-turbo.

- Agent responses depend entirely on the active context  
- The DEFAULT_AGENT_MODEL variable acts as a placeholder  
- Future SentioCP agents will support multiple models and fine-tuned configurations  

---

## 🤖 Agents in the SentioCP CLI

An **agent** is a named configuration that includes its own context space and behavioral scope.

### Create an agent

    python sentiocp.py agent create <name>

### Switch between agents

    python sentiocp.py agent use <name>

- Each agent maintains isolated contexts  
- All agent data is stored locally in `sentiocp_data.json`  

---

## ⌨️ Command Reference

### 🧩 Agent Operations

    python sentiocp.py agent create <agent_name>
    python sentiocp.py agent use <agent_name>
    python sentiocp.py agent list
    python sentiocp.py agent delete <agent_name>

### 📂 Context Operations (per agent)

    python sentiocp.py context add <context_name> --file <path>
    python sentiocp.py context use <context_name>
    python sentiocp.py context show [--all]
    python sentiocp.py context remove <context_name>

### 🧠 Ask a Question

    python sentiocp.py ask "Your question"

---

## 📊 Example Usage

### Step 1: Create an agent

    python sentiocp.py agent create researcher

### Step 2: Add contextual data

Create a file named `quantum_notes.txt` with content such as:

    Quantum entanglement refers to non-local correlations between particles.
    Einstein famously described it as “spooky action at a distance.”

Then run:

    python sentiocp.py context add entanglement --file ./quantum_notes.txt

### Step 3: Ask a question

    python sentiocp.py ask "What phrase did Einstein use to describe quantum entanglement?"

The response will be generated using your local context and OpenAI.

---

## 💡 The Road Ahead for SentioCP

This CLI is only an early preview. Future developments include:

- Encrypted, decentralized context storage  
- Advanced and programmable intent engines  
- Support for self-hosted and multi-model AI  
- Comprehensive developer SDKs and tooling  
- Transparent, verifiable agent behavior and auditing  

This MVP offers a glimpse into how **SentioCP** aims to reshape agent-based AI for decentralized, privacy-conscious systems.
