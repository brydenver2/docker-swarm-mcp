#!/usr/bin/env python3
import json
import sys
from pathlib import Path


def count_tokens(text: str) -> int:
    return len(text) // 4


def parse_yaml_tools(content: str) -> list:
    """
    Parse a simple YAML-like string describing tools into a list of tool dictionaries.
    
    Parses `content` for top-level tool entries that start with `- name:` and collects subsequent `key: value` pairs into the current tool. Blank lines and lines beginning with `#` are ignored. The literal value `null` is converted to Python `None`; keys with empty values are omitted.
    
    Parameters:
        content (str): YAML-like text containing one or more tool entries.
    
    Returns:
        list: A list of dictionaries where each dictionary represents a tool (contains a `name` key and any additional keys with string values or `None`).
    """
    tools = []
    current_tool = {}
    indent_stack = []

    lines = content.split('\n')
    for line in lines:
        stripped = line.lstrip()
        if not stripped or stripped.startswith('#'):
            continue

        indent = len(line) - len(stripped)

        if stripped.startswith('- name:'):
            if current_tool:
                tools.append(current_tool)
            current_tool = {'name': stripped.split(':', 1)[1].strip()}
        elif ':' in stripped and current_tool:
            key, value = stripped.split(':', 1)
            key = key.strip().lstrip('- ')
            value = value.strip()

            if value == 'null':
                current_tool[key] = None
            elif value:
                current_tool[key] = value

    if current_tool:
        tools.append(current_tool)

    return tools


def load_tools(tools_path: Path) -> dict:
    """
    Load and parse a tools file from disk into a Python dictionary.
    
    Supports JSON when the file suffix is ".json". For other suffixes it attempts to parse as YAML using PyYAML; if PyYAML is not available it falls back to a simple line-based parser and returns a dictionary with a top-level "tools" key. On any I/O or parsing error the function prints an error message to stderr and exits the process with status 1.
    
    Parameters:
        tools_path (Path): Path to the tools file to load.
    
    Returns:
        dict: Parsed representation of the tools file.
    """
    try:
        with open(tools_path) as f:
            content = f.read()

        if tools_path.suffix == '.json':
            return json.loads(content)
        else:
            try:
                import yaml
                return yaml.safe_load(content)
            except ImportError:
                tools = parse_yaml_tools(content)
                return {"tools": tools}
    except Exception as e:
        print(f"Error loading tools file: {e}", file=sys.stderr)
        sys.exit(1)


def serialize_tools(tools: list) -> str:
    return json.dumps({"tools": tools}, indent=2)


def validate_context_size(tools_path: Path, hard_limit: int = 7600, warn_threshold: int = 5000):
    """
    Validate the serialized tools context size against configured thresholds and report the result.
    
    Loads tools from the given file path, serializes them, estimates the token count, prints summary information, and enforces limits: exits the process with status 1 if the estimated token count exceeds `hard_limit`, prints a warning if it exceeds `warn_threshold`, otherwise prints a pass message.
    
    Parameters:
        tools_path (Path): Path to the tools file to load.
        hard_limit (int): Absolute maximum allowed token count; exceeding this causes process exit.
        warn_threshold (int): Token count threshold that triggers a warning when exceeded.
    
    Returns:
        int: The estimated token count for the serialized tools.
    """
    tools_data = load_tools(tools_path)
    tools = tools_data.get('tools', [])

    serialized = serialize_tools(tools)
    token_count = count_tokens(serialized)

    print(f"Tool count: {len(tools)}")
    print(f"Serialized size: {len(serialized)} chars")
    print(f"Estimated tokens: {token_count}")

    if token_count > hard_limit:
        print(f"❌ FAIL: Context size {token_count} exceeds hard limit {hard_limit}", file=sys.stderr)
        sys.exit(1)

    if token_count > warn_threshold:
        print(f"⚠️  WARNING: Context size {token_count} exceeds recommended threshold {warn_threshold}")
    else:
        print("✅ PASS: Context size within limits")

    return token_count


if __name__ == "__main__":
    repo_root = Path(__file__).parent.parent
    tools_path = repo_root / "tools.yaml"

    if not tools_path.exists():
        print(f"Error: {tools_path} not found", file=sys.stderr)
        sys.exit(1)

    validate_context_size(tools_path)