#!/usr/bin/env python3
"""
Build-time validator to cross-check tools.yaml schemas against Pydantic models.
Run this script before deployment to ensure schema consistency.
"""

import sys
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, ValidationError

# Add parent directory to path to import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.schemas import containers, networks, services, stacks, system, volumes

# Mapping of tool names to their Pydantic schema models
TOOL_SCHEMA_MAPPING = {
    # System
    "ping": (None, system.PingResponse),
    "info": (None, system.SystemInfo),
    # Containers
    "list-containers": (None, list),  # List of ContainerResponse
    "create-container": (containers.ContainerCreateRequest, containers.ContainerResponse),
    "start-container": (None, dict),
    "stop-container": (None, dict),
    "remove-container": (None, dict),
    "get-logs": (None, str),
    # Stacks
    "deploy-compose": (stacks.ComposeDeployRequest, stacks.ComposeDeployResponse),
    "list-stacks": (None, list),  # List of StackSummary entries
    "remove-compose": (None, dict),
    # Services
    "list-services": (None, list),  # List of ServiceResponse
    "scale-service": (services.ServiceScaleRequest, services.ServiceResponse),
    "remove-service": (None, dict),
    # Networks
    "list-networks": (None, list),  # List of NetworkResponse
    "create-network": (networks.NetworkCreateRequest, networks.NetworkResponse),
    "remove-network": (None, dict),
    # Volumes
    "list-volumes": (None, list),  # List of VolumeResponse
    "create-volume": (volumes.VolumeCreateRequest, volumes.VolumeResponse),
    "remove-volume": (None, dict),
}


def json_schema_to_pydantic_sample(schema: dict[str, Any]) -> Any:
    """Generate a sample value from a JSON schema for validation"""
    schema_type = schema.get("type", "object")

    if schema_type == "object":
        sample = {}
        properties = schema.get("properties", {})
        required = schema.get("required", [])

        for prop, prop_schema in properties.items():
            if prop in required:
                sample[prop] = json_schema_to_pydantic_sample(prop_schema)
            elif "default" in prop_schema:
                sample[prop] = prop_schema["default"]

        return sample

    elif schema_type == "array":
        items_schema = schema.get("items", {"type": "object"})
        return [json_schema_to_pydantic_sample(items_schema)]

    elif schema_type == "string":
        return schema.get("default", "test_value")

    elif schema_type == "integer":
        return schema.get("default", 1)

    elif schema_type == "number":
        return schema.get("default", 1.0)

    elif schema_type == "boolean":
        return schema.get("default", True)

    else:
        return None


def validate_tool_schemas() -> tuple[list[str], list[str]]:
    """
    Validate tools.yaml schemas against Pydantic models

    Returns:
        Tuple of (errors, warnings)
    """
    tools_yaml_path = Path(__file__).parent.parent / "tools.yaml"

    if not tools_yaml_path.exists():
        return [f"tools.yaml not found at {tools_yaml_path}"], []

    with open(tools_yaml_path) as f:
        tools_data = yaml.safe_load(f)

    tools = tools_data.get("tools", [])
    errors = []
    warnings = []

    for tool in tools:
        tool_name = tool.get("name")

        if not tool_name:
            errors.append("Tool missing 'name' field")
            continue

        # Check if tool has a schema mapping
        if tool_name not in TOOL_SCHEMA_MAPPING:
            warnings.append(f"Tool '{tool_name}' not in TOOL_SCHEMA_MAPPING - skipping validation")
            continue

        request_model, response_model = TOOL_SCHEMA_MAPPING[tool_name]

        # Validate request schema
        request_schema = tool.get("request_schema")
        if request_schema and request_model:
            try:
                # Generate sample data from JSON schema
                sample_request = json_schema_to_pydantic_sample(request_schema)

                # Validate against Pydantic model
                if isinstance(request_model, type) and issubclass(request_model, BaseModel):
                    try:
                        request_model(**sample_request)
                    except ValidationError as e:
                        errors.append(
                            f"Tool '{tool_name}' request_schema doesn't match Pydantic model: {e}"
                        )
            except Exception as e:
                warnings.append(f"Tool '{tool_name}' request_schema validation skipped: {e}")

        # Validate response schema
        response_schema = tool.get("response_schema")
        if response_schema and response_model:
            try:
                # For simple types, just check the schema type
                if response_model in (str, int, bool, float, list, dict):
                    expected_type = {
                        str: "string",
                        int: "integer",
                        bool: "boolean",
                        float: "number",
                        list: "array",
                        dict: "object",
                    }[response_model]

                    if response_schema.get("type") != expected_type:
                        errors.append(
                            f"Tool '{tool_name}' response_schema type '{response_schema.get('type')}' "
                            f"doesn't match expected type '{expected_type}'"
                        )
                # For Pydantic models, validate sample data
                elif isinstance(response_model, type) and issubclass(response_model, BaseModel):
                    sample_response = json_schema_to_pydantic_sample(response_schema)
                    try:
                        response_model(**sample_response)
                    except ValidationError as e:
                        errors.append(
                            f"Tool '{tool_name}' response_schema doesn't match Pydantic model: {e}"
                        )
            except Exception as e:
                warnings.append(f"Tool '{tool_name}' response_schema validation skipped: {e}")

    return errors, warnings


def main() -> int:
    """Run validation and return exit code"""
    print("🔍 Validating tools.yaml schemas against Pydantic models...")

    errors, warnings = validate_tool_schemas()

    if warnings:
        print(f"\n⚠️  {len(warnings)} warnings:")
        for warning in warnings:
            print(f"  - {warning}")

    if errors:
        print(f"\n❌ {len(errors)} errors:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print("\n✅ All tools.yaml schemas validated successfully!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
