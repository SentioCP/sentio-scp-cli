import argparse
import json
import os
import sys
import re  # For regular expression matching
from openai import OpenAI  # OpenAI API client

# --- Constants ---
DATA_FILE = "sentiocp_data.json"
DEFAULT_AGENT_MODEL = "default_mock_v1"  # Placeholder for agent model type
OPENAI_MODEL = "gpt-4o"  # Default OpenAI model

# --- Data Management Functions ---
def load_data():
    default_structure = {"agents": {}, "active_agent": None}
    if not os.path.exists(DATA_FILE):
        return default_structure
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            content = f.read()
            if not content:
                return default_structure
            return json.loads(content)
    except json.JSONDecodeError:
        print(f"Error: {DATA_FILE} is corrupted or not valid JSON. ", end="")
        print("A new empty data structure will be used. Previous data may be lost if not backed up.")
        return default_structure
    except FileNotFoundError:
        return default_structure

def save_data(data):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except IOError as e:
        print(f"Error: Could not write to data file {DATA_FILE}: {e}")

# --- Helper Functions ---
def get_active_agent_name_or_exit(data):
    active_agent_name = data.get("active_agent")
    if not active_agent_name:
        print("Error: No active agent set. Use 'python sentiocp.py agent use <agent_name>' to set one.")
        sys.exit(1)
    if active_agent_name not in data.get("agents", {}):
        print(f"Error: Active agent '{active_agent_name}' is configured but not found.")
        print("The data file may be corrupted. Try setting an existing agent as active again.")
        sys.exit(1)
    return active_agent_name

def get_agent_or_exit(data, agent_name):
    agents_data = data.get("agents", {})
    if agent_name not in agents_data:
        print(f"Error: Agent '{agent_name}' not found.")
        sys.exit(1)
    return agents_data[agent_name]

# --- Agent Command Functions ---
def agent_create_cmd(args):
    data = load_data()
    agent_name = args.agent_name
    if agent_name in data.get("agents", {}):
        print(f"Error: Agent '{agent_name}' already exists.")
        return
    data["agents"][agent_name] = {
        "model": DEFAULT_AGENT_MODEL,
        "current_context_name": None,
        "contexts": {}
    }
    if not data.get("active_agent"):
        data["active_agent"] = agent_name
        print(f"Agent '{agent_name}' created and set as active.")
    else:
        print(f"Agent '{agent_name}' created.")
    save_data(data)

def agent_list_cmd(args):
    data = load_data()
    active_agent_name = data.get("active_agent")
    agents = data.get("agents", {})
    if not agents:
        print("No agents created yet. Use 'python sentiocp.py agent create <agent_name>'.")
        return
    print("Available Agents:")
    for name in sorted(agents.keys()):
        marker = " (*)" if name == active_agent_name else ""
        print(f"- {name}{marker}")
    if active_agent_name:
        print("\n(*) indicates the active agent.")

def agent_use_cmd(args):
    data = load_data()
    agent_name = args.agent_name
    if agent_name not in data.get("agents", {}):
        print(f"Error: Agent '{agent_name}' not found.")
        return
    data["active_agent"] = agent_name
    save_data(data)
    print(f"Agent '{agent_name}' is now active.")

def agent_delete_cmd(args):
    data = load_data()
    agent_name = args.agent_name
    if agent_name not in data.get("agents", {}):
        print(f"Error: Agent '{agent_name}' not found.")
        return
    del data["agents"][agent_name]
    print(f"Agent '{agent_name}' deleted.")
    if data.get("active_agent") == agent_name:
        data["active_agent"] = None
        print("The deleted agent was active. No agent is active now.")
        if data["agents"]:
            new_active = next(iter(data["agents"]))
            data["active_agent"] = new_active
            print(f"Agent '{new_active}' has been automatically set as active.")
    save_data(data)

# --- Context Command Functions ---
def context_add_cmd(args):
    data = load_data()
    active_agent = get_active_agent_name_or_exit(data)
    agent = data["agents"][active_agent]
    context_name, file_path = args.context_name, args.file
    if not os.path.isfile(file_path):
        print(f"Error: File '{file_path}' does not exist or is not a valid file.")
        return
    abs_path = os.path.abspath(file_path)
    agent["contexts"][context_name] = abs_path
    agent["current_context_name"] = context_name
    save_data(data)
    print(f"Context '{context_name}' from '{abs_path}' added and activated for agent '{active_agent}'.")

def context_use_cmd(args):
    data = load_data()
    active_agent = get_active_agent_name_or_exit(data)
    agent = data["agents"][active_agent]
    context_name = args.context_name
    if context_name not in agent.get("contexts", {}):
        print(f"Error: Context '{context_name}' not found for agent '{active_agent}'.")
        return
    agent["current_context_name"] = context_name
    save_data(data)
    print(f"Context '{context_name}' is now active for agent '{active_agent}'.")

def context_show_cmd(args):
    data = load_data()
    active_agent = get_active_agent_name_or_exit(data)
    agent = data["agents"][active_agent]
    if args.all:
        contexts = agent.get("contexts", {})
        if not contexts:
            print(f"No contexts defined for agent '{active_agent}'.")
            return
        print(f"Contexts for agent '{active_agent}':")
        for name, path in sorted(contexts.items()):
            marker = " (*)" if name == agent.get("current_context_name") else ""
            print(f"- {name} (Path: {path}){marker}")
    else:
        current = agent.get("current_context_name")
        if not current:
            print(f"No active context for agent '{active_agent}'. Use '--all' to list contexts.")
            return
        path = agent["contexts"].get(current)
        print(f"Active context:\n  Name: {current}\n  Path: {path}")

def context_remove_cmd(args):
    data = load_data()
    active_agent = get_active_agent_name_or_exit(data)
    agent = data["agents"][active_agent]
    name = args.context_name
    if name not in agent.get("contexts", {}):
        print(f"Error: Context '{name}' not found.")
        return
    del agent["contexts"][name]
    if agent.get("current_context_name") == name:
        agent["current_context_name"] = None
        print("The removed context was active. No active context now.")
    save_data(data)
    print(f"Context '{name}' removed from agent '{active_agent}'.")

# --- Ask Command (OpenAI Integration) ---
def ask_cmd(args):
    data = load_data()
    active_agent = get_active_agent_name_or_exit(data)
    query = args.query

    context = None
    context_label = "no active context"
    agent = data["agents"][active_agent]
    context_name = agent.get("current_context_name")

    if context_name:
        context_path = agent["contexts"].get(context_name)
        if context_path and os.path.exists(context_path):
            with open(context_path, "r", encoding="utf-8") as f:
                context = f.read(10000)
            context_label = f"context '{context_name}'"

    system_msg = "You are a helpful assistant."
    prompt = f"Question: {query}"

    if context:
        system_msg = "Answer using only the provided context. If the answer is not present, say so."
        prompt = f"Context:\n---\n{context}\n---\n\nQuestion: {query}"

    print(f"\nQuerying OpenAI ({OPENAI_MODEL})...")

    try:
        if "OPENAI_API_KEY" not in os.environ:
            raise ValueError("OPENAI_API_KEY environment variable not set.")

        client = OpenAI()
        completion = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": prompt}
            ]
        )
        response = completion.choices[0].message.content
    except Exception as e:
        response = f"OpenAI API Error: {e}"

    print(
        f"Agent '{active_agent}' (using {context_label} via OpenAI):\n"
        f"  Query: \"{query}\"\n"
        f"  Answer: {response}"
    )

# --- Main Parser ---
def main():
    parser = argparse.ArgumentParser(
        prog="sentiocp",
        description="SentioCP AI CLI",
        epilog="Example: python sentiocp.py agent create my_agent"
    )
    subparsers = parser.add_subparsers(dest="command_group", required=True)

    agent_parser = subparsers.add_parser("agent", help="Agent management")
    agent_sub = agent_parser.add_subparsers(dest="agent_action", required=True)
    agent_sub.add_parser("list").set_defaults(func=agent_list_cmd)

    ap_create = agent_sub.add_parser("create")
    ap_create.add_argument("agent_name")
    ap_create.set_defaults(func=agent_create_cmd)

    ap_use = agent_sub.add_parser("use")
    ap_use.add_argument("agent_name")
    ap_use.set_defaults(func=agent_use_cmd)

    ap_delete = agent_sub.add_parser("delete")
    ap_delete.add_argument("agent_name")
    ap_delete.set_defaults(func=agent_delete_cmd)

    context_parser = subparsers.add_parser("context", help="Context management")
    context_sub = context_parser.add_subparsers(dest="context_action", required=True)

    cp_add = context_sub.add_parser("add")
    cp_add.add_argument("context_name")
    cp_add.add_argument("--file", required=True)
    cp_add.set_defaults(func=context_add_cmd)

    cp_use = context_sub.add_parser("use")
    cp_use.add_argument("context_name")
    cp_use.set_defaults(func=context_use_cmd)

    cp_show = context_sub.add_parser("show")
    cp_show.add_argument("--all", action="store_true")
    cp_show.set_defaults(func=context_show_cmd)

    cp_remove = context_sub.add_parser("remove")
    cp_remove.add_argument("context_name")
    cp_remove.set_defaults(func=context_remove_cmd)

    ask_parser = subparsers.add_parser("ask", help="Ask OpenAI")
    ask_parser.add_argument("query")
    ask_parser.set_defaults(func=ask_cmd)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
