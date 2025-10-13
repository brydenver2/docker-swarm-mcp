#!/usr/bin/env python3
import json
import sys
from pathlib import Path


def count_tokens(text: str) -> int:
    return len(text) // 4


def parse_yaml_tools(content: str) -> list:
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
