================
CODE SNIPPETS
================
TITLE: Example HTTP GET Request with Authorization
DESCRIPTION: A complete example of an HTTP GET request to an MCP server, including the Host header and the Authorization header with a Bearer token.

SOURCE: https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization

LANGUAGE: http
CODE:
```
GET /mcp HTTP/1.1
Host: mcp.example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

--------------------------------

TITLE: Example GET Request with Authorization Header (HTTP)
DESCRIPTION: An example HTTP GET request demonstrating the correct usage of the Authorization header with a Bearer token. This illustrates how to authenticate requests to MCP resources.

SOURCE: https://modelcontextprotocol.io/specification/2025-03-26/basic/authorization

LANGUAGE: http
CODE:
```
GET /v1/contexts HTTP/1.1
Host: mcp.example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

--------------------------------

TITLE: Canonical Server URI Examples
DESCRIPTION: Examples of valid canonical URIs for MCP servers, adhering to RFC 8707. Implementations should use the most specific URI and may accept uppercase schemes and hosts for robustness.

SOURCE: https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization

LANGUAGE: text
CODE:
```
https://mcp.example.com/mcp
https://mcp.example.com
https://mcp.example.com:8443
https://mcp.example.com/server/mcp
```

--------------------------------

TITLE: Response for Getting a Prompt (JSON)
DESCRIPTION: The response to a 'prompts/get' request includes the prompt's description and a list of messages, typically containing user instructions and context.

SOURCE: https://modelcontextprotocol.io/specification/2025-03-26/server/prompts

LANGUAGE: json
CODE:
```
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "description": "Code review prompt",
    "messages": [
      {
        "role": "user",
        "content": {
          "type": "text",
          "text": "Please review this Python code:\ndef hello():\n    print('world')"
        }
      }
    ]
  }
}
```

--------------------------------

TITLE: JSON Data Type Examples
DESCRIPTION: Examples of different content types within a PromptMessage. This includes text, image (base64-encoded), audio (base64-encoded), and embedded resource definitions. Each type requires specific fields such as 'type', 'text'/'data'/'resource', and 'mimeType'.

SOURCE: https://modelcontextprotocol.io/specification/2025-03-26/server/prompts

LANGUAGE: json
CODE:
```
{
  "type": "text",
  "text": "The text content of the message"
}
```

LANGUAGE: json
CODE:
```
{
  "type": "image",
  "data": "base64-encoded-image-data",
  "mimeType": "image/png"
}
```

LANGUAGE: json
CODE:
```
{
  "type": "audio",
  "data": "base64-encoded-audio-data",
  "mimeType": "audio/wav"
}
```

LANGUAGE: json
CODE:
```
{
  "type": "resource",
  "resource": {
    "uri": "resource://example",
    "mimeType": "text/plain",
    "text": "Resource content"
  }
}
```

--------------------------------

TITLE: Example Initialization Error Response (JSON-RPC)
DESCRIPTION: This JSON object represents an example error response for an initialization request, specifically indicating a protocol version mismatch. It adheres to the JSON-RPC 2.0 specification and includes details about supported and requested protocol versions.

SOURCE: https://modelcontextprotocol.io/specification/2024-11-05/basic/lifecycle

LANGUAGE: json
CODE:
```
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32602,
    "message": "Unsupported protocol version",
    "data": {
      "supported": ["2024-11-05"],
      "requested": "1.0.0"
    }
  }
}
```

--------------------------------

TITLE: Error Handling
DESCRIPTION: Outlines common error cases that implementations should be prepared to handle, including protocol version mismatches, failed capability negotiation, and request timeouts. Provides an example of an initialization error response.

SOURCE: https://modelcontextprotocol.io/specification/2025-03-26/basic/lifecycle

LANGUAGE: APIDOC
CODE:
```
## Error Handling

Implementations **SHOULD** be prepared to handle these error cases:

* Protocol version mismatch
* Failure to negotiate required capabilities
* Request [timeouts](#timeouts)

Example initialization error:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32602,
    "message": "Unsupported protocol version",
    "data": {
      "supported": ["2024-11-05"],
      "requested": "1.0.0"
    }
  }
}
```
```

--------------------------------

TITLE: Elicitation Response Examples (JSON)
DESCRIPTION: These JSON snippets illustrate possible responses to an 'elicitation/create' request. The 'accept' action includes the user-provided 'content' matching the schema. 'decline' indicates the user refused to provide information, and 'cancel' signifies the user aborted the process.

SOURCE: https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation

LANGUAGE: json
CODE:
```
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "action": "accept",
    "content": {
      "name": "octocat"
    }
  }
}
```

LANGUAGE: json
CODE:
```
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "action": "decline"
  }
}
```

LANGUAGE: json
CODE:
```
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "action": "cancel"
  }
}
```

--------------------------------

TITLE: GET /prompts/get
DESCRIPTION: Retrieves a prompt from the server using its name and optional arguments for templating. This method is part of the ModelContextProtocol IO Specification.

SOURCE: https://modelcontextprotocol.io/specification/2025-06-18/schema

LANGUAGE: APIDOC
CODE:
```
## GET /prompts/get

### Description
Used by the client to get a prompt provided by the server. This endpoint allows fetching prompts by name and can utilize provided arguments for prompt templating.

### Method
GET

### Endpoint
/prompts/get

### Parameters
#### Query Parameters
- **name** (string) - Required - The name of the prompt or prompt template.
- **arguments** (object) - Optional - A key-value map of string arguments to use for templating the prompt. Example: `{"key": "value"}`.

### Request Example
```json
{
  "method": "prompts/get",
  "params": {
    "name": "examplePromptName",
    "arguments": {
      "user_input": "What is the weather today?"
    }
  }
}
```

### Response
#### Success Response (200)
- **prompt** (string) - The content of the prompt.
- **arguments** (object) - The arguments used for templating the prompt.

#### Response Example
```json
{
  "prompt": "The weather today is sunny.",
  "arguments": {
    "user_input": "What is the weather today?"
  }
}
```
```

--------------------------------

TITLE: JSON-RPC Error Response Example
DESCRIPTION: An example of a JSON-RPC error response a client might send if it does not support the roots capability, using code -32601 (Method not found).

SOURCE: https://modelcontextprotocol.io/specification/2024-11-05/client/roots

LANGUAGE: json
CODE:
```
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32601,
    "message": "Roots not supported",
    "data": {
      "reason": "Client does not have roots capability"
    }
  }
}
```

--------------------------------

TITLE: Get Prompt (prompts/get)
DESCRIPTION: Retrieves the content of a specific prompt, including its messages and arguments.

SOURCE: https://modelcontextprotocol.io/specification/2025-03-26/server/prompts

LANGUAGE: APIDOC
CODE:
```
## Get Prompt

### Description
Retrieves the details of a specific prompt by its name, including its messages and arguments. Arguments can be pre-filled.

### Method
`prompts/get`

### Parameters
#### Request Body
- **name** (string) - Required - The name of the prompt to retrieve.
- **arguments** (object) - Optional - Key-value pairs representing the arguments to be passed to the prompt.

### Request Example
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "prompts/get",
  "params": {
    "name": "code_review",
    "arguments": {
      "code": "def hello():\n    print('world')"
    }
  }
}
```

### Response
#### Success Response (200)
- **description** (string) - A description of the prompt.
- **messages** (array) - An array of message objects that form the prompt content.
  - **role** (string) - The role of the message sender (e.g., "user", "system").
  - **content** (object) - The content of the message.
    - **type** (string) - The type of content (e.g., "text").
    - **text** (string) - The text content of the message.

#### Response Example
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "description": "Code review prompt",
    "messages": [
      {
        "role": "user",
        "content": {
          "type": "text",
          "text": "Please review this Python code:\ndef hello():\n    print('world')"
        }
      }
    ]
  }
}
```
```

--------------------------------

TITLE: Tool Output Schema Definition (JSON)
DESCRIPTION: An example JSON object defining a tool's input and output schema. 'inputSchema' specifies the expected structure for tool inputs, while 'outputSchema' defines the structure for valid tool outputs, including types and required fields.

SOURCE: https://modelcontextprotocol.io/specification/2025-06-18/server/tools

LANGUAGE: json
CODE:
```
{
  "name": "get_weather_data",
  "title": "Weather Data Retriever",
  "description": "Get current weather data for a location",
  "inputSchema": {
    "type": "object",
    "properties": {
      "location": {
        "type": "string",
        "description": "City name or zip code"
      }
    },
    "required": ["location"]
  },
  "outputSchema": {
    "type": "object",
    "properties": {
      "temperature": {
        "type": "number",
        "description": "Temperature in celsius"
      },
      "conditions": {
        "type": "string",
        "description": "Weather conditions description"
      },
      "humidity": {
        "type": "number",
        "description": "Humidity percentage"
      }
    },
    "required": ["temperature", "conditions", "humidity"]
  }
}
```

--------------------------------

TITLE: Listening for Messages from the Server (GET /mcp)
DESCRIPTION: Clients can establish an SSE stream by issuing an HTTP GET request to the MCP endpoint, allowing the server to send messages proactively.

SOURCE: https://modelcontextprotocol.io/specification/2025-03-26/basic/transports

LANGUAGE: APIDOC
CODE:
```
## GET /mcp

### Description
Clients can establish an SSE stream by issuing an HTTP GET request to the MCP endpoint, allowing the server to send messages proactively.

### Method
GET

### Endpoint
/mcp

### Parameters
#### Headers
- **Accept** (string) - Required - Must include `text/event-stream`.

### Response
#### Success Response (200 OK)
- **Content-Type**: `text/event-stream`
- **Description**: Server initiates an SSE stream to send JSON-RPC requests and notifications to the client. Server MUST NOT send responses on this stream unless resuming.

#### Error Response (405 Method Not Allowed)
- **Status**: 405 Method Not Allowed
- **Description**: Indicates the server does not support SSE streams at this endpoint via GET.

### Response Example (SSE Stream)
```
event: message
data: {"jsonrpc": "2.0", "method": "serverNotification", "params": {}}

```
```

--------------------------------

TITLE: Server Metadata Discovery Request
DESCRIPTION: Clients initiate server capability discovery by sending a GET request to the /.well-known/oauth-authorization-server endpoint. The server responds with metadata or a 404 if discovery is not supported, prompting fallback to default endpoints.

SOURCE: https://modelcontextprotocol.io/specification/2025-03-26/basic/authorization

LANGUAGE: http
CODE:
```
GET /.well-known/oauth-authorization-server HTTP/1.1
Host: api.example.com
MCP-Protocol-Version: 2024-11-05
```

--------------------------------

TITLE: Embedded Resource Example in JSON
DESCRIPTION: Details the format for referencing server-side resources within prompt messages. This includes a 'resource' object with a URI, name, title, MIME type, and either text content or base64-encoded blob data, enabling seamless integration of server-managed content.

SOURCE: https://modelcontextprotocol.io/specification/2025-06-18/server/prompts

LANGUAGE: json
CODE:
```
{
  "type": "resource",
  "resource": {
    "uri": "resource://example",
    "name": "example",
    "title": "My Example Resource",
    "mimeType": "text/plain",
    "text": "Resource content"
  }
}
```

--------------------------------

TITLE: MCP Protocol Version Header Example
DESCRIPTION: Illustrates the MCP-Protocol-Version header, which clients must include in HTTP requests to specify the protocol version for server compatibility.

SOURCE: https://modelcontextprotocol.io/specification/2025-06-18/basic/transports

LANGUAGE: http
CODE:
```
Request Header:
MCP-Protocol-Version: 2025-06-18
```

--------------------------------

TITLE: Get Prompt API
DESCRIPTION: Clients can retrieve the details and content of a specific prompt by sending a `prompts/get` request, optionally providing arguments to pre-fill the prompt.

SOURCE: https://modelcontextprotocol.io/specification/2025-06-18/server/prompts

LANGUAGE: APIDOC
CODE:
```
## Get Prompt (prompts/get)

### Description
Retrieves the details and messages for a specific prompt, potentially with pre-filled arguments.

### Method
`POST`

### Endpoint
`/` (Typically the root endpoint for JSON-RPC requests)

### Parameters
#### Request Body
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "prompts/get",
  "params": {
    "name": "code_review",
    "arguments": {
      "code": "def hello():\n    print('world')"
    }
  }
}
```

- **name** (string) - Required - The name of the prompt to retrieve.
- **arguments** (object) - Optional - Key-value pairs of arguments to pre-fill for the prompt.

### Response
#### Success Response (200 OK)
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "description": "Code review prompt",
    "messages": [
      {
        "role": "user",
        "content": {
          "type": "text",
          "text": "Please review this Python code:\ndef hello():\n    print('world')"
        }
      }
    ]
  }
}
```

- **description** (string) - A description of the prompt.
- **messages** (array) - An array of messages representing the prompt's content, suitable for sending to a language model.
  - **role** (string) - The role of the message sender (e.g., "user", "system").
  - **content** (object) - The content of the message.
    - **type** (string) - The type of content (e.g., "text").
    - **text** (string) - The text content of the message.
```

--------------------------------

TITLE: Model Preferences Interface
DESCRIPTION: Defines the structure for server preferences in model selection, guiding clients on prioritizing different aspects of model performance.

SOURCE: https://modelcontextprotocol.io/specification/2025-06-18/schema

LANGUAGE: APIDOC
CODE:
```
## ModelPreferences Interface

### Description
The server's preferences for model selection, requested of the client during sampling. These preferences are advisory and can be ignored by the client. The client is responsible for interpreting these preferences and balancing them against other considerations.

### Interface
`ModelPreferences`

### Properties
#### costPriority (Optional)
- **costPriority** (number) - Optional - How much to prioritize cost when selecting a model. A value of 0 means cost is not important, while a value of 1 means cost is the most important factor.

#### hints (Optional)
- **hints** (ModelHint[]) - Optional - Optional hints to use for model selection. If multiple hints are specified, the client MUST evaluate them in order. The client SHOULD prioritize these hints over the numeric priorities.

#### intelligencePriority (Optional)
- **intelligencePriority** (number) - Optional - How much to prioritize intelligence and capabilities when selecting a model. A value of 0 means intelligence is not important, while a value of 1 means intelligence is the most important factor.

#### speedPriority (Optional)
- **speedPriority** (number) - Optional - How much to prioritize speed when selecting a model. A value of 0 means speed is not important, while a value of 1 means speed is the most important factor.

### Example Request Body
```json
{
  "costPriority": 0.8,
  "intelligencePriority": 0.2,
  "speedPriority": 0.5,
  "hints": [
    {
      "type": "benchmark",
      "name": "fastest-model-benchmark"
    }
  ]
}
```

### Example Success Response
```json
{
  "message": "Model preferences received successfully."
}
```
```

--------------------------------

TITLE: Root Data Type Example
DESCRIPTION: Defines the structure for a single filesystem root, including its mandatory 'uri' (a file:// URI) and an optional 'name' for display purposes.

SOURCE: https://modelcontextprotocol.io/specification/2024-11-05/client/roots

LANGUAGE: json
CODE:
```
{
  "uri": "file:///home/user/projects/myproject",
  "name": "My Project"
}
```

--------------------------------

TITLE: Log Levels
DESCRIPTION: Overview of the syslog severity levels used by the Model Context Protocol, including their descriptions and example use cases.

SOURCE: https://modelcontextprotocol.io/specification/2025-06-18/server/utilities/logging

LANGUAGE: APIDOC
CODE:
```
## Log Levels

### Description
The protocol follows the standard syslog severity levels specified in [RFC 5424](https://datatracker.ietf.org/doc/html/rfc5424#section-6.2.1).

### Levels Table

| Level     | Description                      | Example Use Case           |
| --------- | -------------------------------- | -------------------------- |
| debug     | Detailed debugging information   | Function entry/exit points |
| info      | General informational messages   | Operation progress updates |
| notice    | Normal but significant events    | Configuration changes      |
| warning   | Warning conditions               | Deprecated feature usage   |
| error     | Error conditions                 | Operation failures         |
| critical  | Critical conditions              | System component failures  |
| alert     | Action must be taken immediately | Data corruption detected   |
| emergency | System is unusable               | Complete system failure    |
```

--------------------------------

TITLE: HTTP Header Example for Session Management
DESCRIPTION: This example illustrates how a client should include the 'Mcp-Session-Id' header in subsequent HTTP requests after a session has been established by the server. This is crucial for maintaining stateful interactions.

SOURCE: https://modelcontextprotocol.io/specification/2025-03-26/basic/transports

LANGUAGE: http
CODE:
```
POST /mcp/endpoint HTTP/1.1
Host: example.com
Mcp-Session-Id: 1868a90c-1234-5678-90ab-abcdef123456
Content-Type: application/json

{
  "some": "request data"
}
```

--------------------------------

TITLE: Canonical Server URI
DESCRIPTION: Defines the structure and examples of valid and invalid canonical URIs for MCP servers, emphasizing adherence to RFC 8707 and RFC 9728.

SOURCE: https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization

LANGUAGE: APIDOC
CODE:
```
## Canonical Server URI

### Description
The canonical URI of an MCP server is defined as the resource identifier as specified in [RFC 8707 Section 2](https://www.rfc-editor.org/rfc/rfc8707.html#section-2) and aligns with the `resource` parameter in [RFC 9728](https://datatracker.ietf.org/doc/html/rfc9728).

MCP clients **SHOULD** provide the most specific URI that they can for the MCP server they intend to access, following the guidance in [RFC 8707](https://www.rfc-editor.org/rfc/rfc8707). While the canonical form uses lowercase scheme and host components, implementations **SHOULD** accept uppercase scheme and host components for robustness and interoperability.

### Examples

#### Valid Canonical URIs
- `https://mcp.example.com/mcp`
- `https://mcp.example.com`
- `https://mcp.example.com:8443`
- `https://mcp.example.com/server/mcp` (when path component is necessary to identify individual MCP server)

#### Invalid Canonical URIs
- `mcp.example.com` (missing scheme)
- `https://mcp.example.com#fragment` (contains fragment)

### Note on Trailing Slashes
While both `https://mcp.example.com/` (with trailing slash) and `https://mcp.example.com` (without trailing slash) are technically valid absolute URIs according to [RFC 3986](https://www.rfc-editor.org/rfc/rfc3986), implementations **SHOULD** consistently use the form without the trailing slash for better interoperability unless the trailing slash is semantically significant for the specific resource.

### Resource Parameter Example
For example, if accessing an MCP server at `https://mcp.example.com`, the authorization request would include:

```
&resource=https%3A%2F%2Fmcp.example.com
```

MCP clients **MUST** send this parameter regardless of whether authorization servers support it.
```

--------------------------------

TITLE: Model Selection Hints with Priorities
DESCRIPTION: This JSON structure defines model selection preferences for a client. It includes a list of 'hints' to suggest specific models or families, ordered by preference. It also specifies priorities for cost, speed, and intelligence to guide the model selection process when hints are not directly mappable or insufficient. Clients process these to choose an appropriate model.

SOURCE: https://modelcontextprotocol.io/specification/2025-03-26/client/sampling

LANGUAGE: json
CODE:
```
{
  "hints": [
    { "name": "claude-3-sonnet" }, // Prefer Sonnet-class models
    { "name": "claude" } // Fall back to any Claude model
  ],
  "costPriority": 0.3, // Cost is less important
  "speedPriority": 0.8, // Speed is very important
  "intelligencePriority": 0.5 // Moderate capability needs
}
```

--------------------------------

TITLE: Valid Tool Response with Structured Content (JSON)
DESCRIPTION: An example of a valid JSON-RPC response from a tool that returns structured content. It includes a 'result' object with 'content' (as text) and 'structuredContent' matching the defined output schema.

SOURCE: https://modelcontextprotocol.io/specification/2025-06-18/server/tools

LANGUAGE: json
CODE:
```
{
  "jsonrpc": "2.0",
  "id": 5,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "{\"temperature\": 22.5, \"conditions\": \"Partly cloudy\", \"humidity\": 65}"
      }
    ],
    "structuredContent": {
      "temperature": 22.5,
      "conditions": "Partly cloudy",
      "humidity": 65
    }
  }
}
```

--------------------------------

TITLE: Get Specific Prompt Request/Response (JSON)
DESCRIPTION: Clients use a 'prompts/get' request to retrieve a specific prompt by name, optionally providing arguments to customize it. The response includes the prompt's description and a structured list of messages for the language model.

SOURCE: https://modelcontextprotocol.io/specification/2024-11-05/server/prompts

LANGUAGE: json
CODE:
```
// Request:
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "prompts/get",
  "params": {
    "name": "code_review",
    "arguments": {
      "code": "def hello():\n    print('world')"
    }
  }
}

// Response:
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "description": "Code review prompt",
    "messages": [
      {
        "role": "user",
        "content": {
          "type": "text",
          "text": "Please review this Python code:\ndef hello():\n    print('world')"
        }
      }
    ]
  }
}
```

--------------------------------

TITLE: Multiple Roots Data Type Example
DESCRIPTION: Illustrates how multiple roots can be represented as an array of root objects, typically used when a client exposes several distinct directories or repositories.

SOURCE: https://modelcontextprotocol.io/specification/2024-11-05/client/roots

LANGUAGE: json
CODE:
```
[
  {
    "uri": "file:///home/user/repos/frontend",
    "name": "Frontend Repository"
  },
  {
    "uri": "file:///home/user/repos/backend",
    "name": "Backend Repository"
  }
]
```

--------------------------------

TITLE: Resource Data Type: With Annotations (JSON)
DESCRIPTION: An example of a resource definition that includes optional annotations. Annotations provide metadata such as intended audience, priority, and last modified timestamp, aiding clients in filtering and prioritization.

SOURCE: https://modelcontextprotocol.io/specification/2025-06-18/server/resources

LANGUAGE: json
CODE:
```
{
  "uri": "file:///project/README.md",
  "name": "README.md",
  "title": "Project Documentation",
  "mimeType": "text/markdown",
  "annotations": {
    "audience": ["user"],
    "priority": 0.8,
    "lastModified": "2025-01-12T15:00:58Z"
  }
}
```

--------------------------------

TITLE: TypeScript Interface for Root Object
DESCRIPTION: Defines the structure for a root object, representing a file or directory that the server can operate on. It includes optional metadata and name, and a mandatory URI which must start with 'file://'.

SOURCE: https://modelcontextprotocol.io/specification/2025-06-18/schema

LANGUAGE: typescript
CODE:
```
interface Root {
  _meta?: { [key: string]: unknown };
  name?: string;
  uri: string;
}
```

--------------------------------

TITLE: MCP Session ID Header Example
DESCRIPTION: Demonstrates the use of the Mcp-Session-Id header in HTTP requests and responses for managing stateful sessions in the MCP.

SOURCE: https://modelcontextprotocol.io/specification/2025-06-18/basic/transports

LANGUAGE: http
CODE:
```
Response Header:
Mcp-Session-Id: 1868a90c-11e7-4e32-a870-055188d83408

Request Header:
Mcp-Session-Id: 1868a90c-11e7-4e32-a870-055188d83408
```

--------------------------------

TITLE: Listening for Messages from the Server
DESCRIPTION: Details how clients can listen for messages from the server via an SSE stream using HTTP GET requests.

SOURCE: https://modelcontextprotocol.io/specification/2025-06-18/basic/transports

LANGUAGE: APIDOC
CODE:
```
## GET /mcp

### Description
Clients can initiate an SSE stream to receive JSON-RPC requests and notifications from the server without sending data first.

### Method
GET

### Endpoint
/mcp

### Headers
- **Accept** (string) - Required - Must include `text/event-stream`.

### Response
#### Success Response (200 OK)
- **Content-Type**: `text/event-stream`
- The stream may contain JSON-RPC requests, notifications, and responses.

#### Error Response (405 Method Not Allowed)
- Indicates the server does not offer an SSE stream at this endpoint.

### Response Example (SSE Stream)
```
id: 1
data: {"jsonrpc": "2.0", "method": "update", "params": ["someData"]}


id: 2
data: {"jsonrpc": "2.0", "method": "ping"}

```
```

--------------------------------

TITLE: Authorization Request Resource Parameter
DESCRIPTION: An example of how the MCP server's canonical URI is included as the 'resource' parameter in an authorization request, URL-encoded as per RFC 9728.

SOURCE: https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization

LANGUAGE: text
CODE:
```
&resource=https%3A%2F%2Fmcp.example.com
```

--------------------------------

TITLE: JSON-RPC Protocol Error Example
DESCRIPTION: Demonstrates a standard JSON-RPC error response, typically used for issues related to the RPC framework itself, such as invalid requests or internal server errors.

SOURCE: https://modelcontextprotocol.io/specification/2024-11-05/server/tools

LANGUAGE: json
CODE:
```
{
  "jsonrpc": "2.0",
  "id": 3,
  "error": {
    "code": -32602,
    "message": "Unknown tool: invalid_tool_name"
  }
}
```

--------------------------------

TITLE: POST /initialize
DESCRIPTION: Initializes the connection between the client and server. This request is sent by the client to begin the initialization process, providing information about its capabilities and supported protocol version.

SOURCE: https://modelcontextprotocol.io/specification/2025-06-18/schema

LANGUAGE: APIDOC
CODE:
```
## POST /initialize

### Description
Initializes the connection between the client and server. This request is sent by the client to begin the initialization process, providing information about its capabilities and supported protocol version.

### Method
POST

### Endpoint
/initialize

### Parameters
#### Request Body
- **method** (string) - Required - Must be 'initialize'.
- **params** (object) - Required - Contains initialization parameters.
  - **capabilities** (ClientCapabilities) - Required - The client's capabilities.
  - **clientInfo** (Implementation) - Required - Information about the client implementation.
  - **protocolVersion** (string) - Required - The latest version of the Model Context Protocol that the client supports.

### Request Example
```json
{
  "method": "initialize",
  "params": {
    "capabilities": { ... },
    "clientInfo": { ... },
    "protocolVersion": "1.0"
  }
}
```

### Response
#### Success Response (200)
(Response structure not detailed in the provided text)

#### Response Example
(No example provided)
```

--------------------------------

TITLE: Client Resuming Connection with Last-Event-ID Header
DESCRIPTION: This example demonstrates how a client, after a connection interruption, can request to resume the stream by sending an HTTP GET request to the MCP endpoint. The 'Last-Event-ID' header specifies the ID of the last successfully received event.

SOURCE: https://modelcontextprotocol.io/specification/2025-03-26/basic/transports

LANGUAGE: http
CODE:
```
GET /mcp/stream HTTP/1.1
Host: example.com
Last-Event-ID: 42


```

--------------------------------

TITLE: Listing Tools API
DESCRIPTION: Clients can discover available tools by sending a `tools/list` request. This operation supports pagination.

SOURCE: https://modelcontextprotocol.io/specification/2024-11-05/server/tools

LANGUAGE: APIDOC
CODE:
```
## Listing Tools

To discover available tools, clients send a `tools/list` request. This operation supports [pagination](/specification/2024-11-05/server/utilities/pagination).

### Method
POST

### Endpoint
/tools/list

### Parameters
#### Request Body
- **jsonrpc** (string) - Required - JSON RPC version, should be "2.0".
- **id** (integer) - Required - A unique identifier for the request.
- **method** (string) - Required - The method name, should be "tools/list".
- **params** (object) - Optional - Parameters for the method.
  - **cursor** (string) - Optional - A cursor for pagination, to fetch the next page of results.

### Request Example
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/list",
  "params": {
    "cursor": "optional-cursor-value"
  }
}
```

### Response
#### Success Response (200)
- **jsonrpc** (string) - JSON RPC version, should be "2.0".
- **id** (integer) - The identifier for the request.
- **result** (object) - The result of the method call.
  - **tools** (array) - A list of available tools.
    - **name** (string) - The unique identifier for the tool.
    - **description** (string) - A human-readable description of the tool's functionality.
    - **inputSchema** (object) - A JSON Schema defining the expected parameters for the tool.
  - **nextCursor** (string) - Optional - A cursor for fetching the next page of results.

#### Response Example
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "tools": [
      {
        "name": "get_weather",
        "description": "Get current weather information for a location",
        "inputSchema": {
          "type": "object",
          "properties": {
            "location": {
              "type": "string",
              "description": "City name or zip code"
            }
          },
          "required": ["location"]
        }
      }
    ],
    "nextCursor": "next-page-cursor"
  }
}
```
```

--------------------------------

TITLE: Resource Discovery and Access
DESCRIPTION: Covers the initial discovery of resources and reading their content.

SOURCE: https://modelcontextprotocol.io/specification/2025-03-26/server/resources

LANGUAGE: APIDOC
CODE:
```
## resources/list

### Description
Requests a list of all available resources from the server.

### Method
POST

### Endpoint
/

### Parameters
#### Request Body
- **jsonrpc** (string) - Required - Specifies the JSON-RPC version, should be "2.0".
- **id** (integer) - Required - A unique identifier for the request.
- **method** (string) - Required - The method to call, must be "resources/list".

### Request Example
```json
{
  "jsonrpc": "2.0",
  "id":. 
  "method": "resources/list"
}
```

### Response
#### Success Response (200)
- **jsonrpc** (string) - The JSON-RPC version.
- **id** (integer) - The identifier of the request.
- **result** (array) - A list of resource objects.
  - Each resource object contains:
    - **uri** (string) - Unique identifier for the resource.
    - **name** (string) - Human-readable name.
    - **description** (string) - Optional description.
    - **mimeType** (string) - Optional MIME type.
    - **size** (integer) - Optional size in bytes.

#### Response Example
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": [
    {
      "uri": "file:///project/README.md",
      "name": "Project README",
      "mimeType": "text/markdown",
      "size": 1024
    }
  ]
}
```
```

LANGUAGE: APIDOC
CODE:
```
## resources/read

### Description
Reads the content of a specified resource.

### Method
POST

### Endpoint
/

### Parameters
#### Request Body
- **jsonrpc** (string) - Required - Specifies the JSON-RPC version, should be "2.0".
- **id** (integer) - Required - A unique identifier for the request.
- **method** (string) - Required - The method to call, must be "resources/read".
- **params** (object) - Required - Parameters for reading the resource.
  - **uri** (string) - Required - The URI of the resource to read.

### Request Example
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "resources/read",
  "params": {
    "uri": "file:///project/src/main.rs"
  }
}
```

### Response
#### Success Response (200)
- **jsonrpc** (string) - The JSON-RPC version.
- **id** (integer) - The identifier of the request.
- **result** (object) - Contains the resource content.
  - **uri** (string) - The URI of the resource.
  - **mimeType** (string) - The MIME type of the resource.
  - **text** (string) - Resource content as text (if applicable).
  - **blob** (string) - Resource content as base64-encoded binary data (if applicable).

#### Response Example (Text Content)
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "uri": "file:///example.txt",
    "mimeType": "text/plain",
    "text": "Resource content"
  }
}
```

#### Response Example (Binary Content)
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "uri": "file:///example.png",
    "mimeType": "image/png",
    "blob": "base64-encoded-data"
  }
}
```
```

--------------------------------

TITLE: Listing Tools API
DESCRIPTION: Clients can discover available tools by sending a `tools/list` request. This operation supports pagination.

SOURCE: https://modelcontextprotocol.io/specification/2025-06-18/server/tools

LANGUAGE: APIDOC
CODE:
```
## List Tools

### Method
`tools/list`

### Description
Retrieves a list of available tools that can be invoked by the language model. Supports pagination.

### Request Body
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/list",
  "params": {
    "cursor": "optional-cursor-value"
  }
}
```

**Parameters:**
* **`cursor`** (string) - Optional - A cursor value for paginating through the list of tools.

### Response Body (Success - 200)
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "tools": [
      {
        "name": "get_weather",
        "title": "Weather Information Provider",
        "description": "Get current weather information for a location",
        "inputSchema": {
          "type": "object",
          "properties": {
            "location": {
              "type": "string",
              "description": "City name or zip code"
            }
          },
          "required": ["location"]
        }
      }
    ],
    "nextCursor": "next-page-cursor"
  }
}
```

**Response Fields:**
* **`tools`** (array) - A list of available tool definitions.
  * Each tool object contains:
    * **`name`** (string) - Unique identifier for the tool.
    * **`title`** (string) - Optional human-readable name of the tool.
    * **`description`** (string) - Human-readable description of the tool's functionality.
    * **`inputSchema`** (object) - JSON Schema defining the expected input parameters.
    * **`outputSchema`** (object) - Optional JSON Schema defining the expected output structure.
    * **`annotations`** (object) - Optional properties describing tool behavior.
* **`nextCursor`** (string) - Optional - A cursor for fetching the next page of results.
```

--------------------------------

TITLE: Request to Get a Specific Prompt (JSON)
DESCRIPTION: Clients send a 'prompts/get' request to retrieve a specific prompt by name, optionally providing arguments for customization. Argument auto-completion is possible via the completion API.

SOURCE: https://modelcontextprotocol.io/specification/2025-03-26/server/prompts

LANGUAGE: json
CODE:
```
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "prompts/get",
  "params": {
    "name": "code_review",
    "arguments": {
      "code": "def hello():\n    print('world')"
    }
  }
}
```

--------------------------------

TITLE: Prompts API Overview
DESCRIPTION: The Model Context Protocol (MCP) provides a standardized way for servers to expose prompt templates to clients. Prompts allow servers to provide structured messages and instructions for interacting with language models. Clients can discover available prompts, retrieve their contents, and provide arguments to customize them. Servers supporting prompts must declare the `prompts` capability during initialization.

SOURCE: https://modelcontextprotocol.io/specification/2025-03-26/server/prompts

LANGUAGE: APIDOC
CODE:
```
## Prompts API Overview

### Description
The Model Context Protocol (MCP) enables servers to expose prompt templates to clients, facilitating structured interactions with language models. Clients can discover, retrieve, and customize these prompts.

### Capabilities
Servers must declare the `prompts` capability during initialization:

```json
{
  "capabilities": {
    "prompts": {
      "listChanged": true
    }
  }
}
```

`listChanged` indicates if notifications will be sent when the prompt list changes.
```

--------------------------------

TITLE: Streamable HTTP Transport
DESCRIPTION: A transport mechanism using HTTP POST and GET requests. Servers can optionally use Server-Sent Events (SSE) for streaming multiple messages. Requires a single MCP endpoint supporting both POST and GET.

SOURCE: https://modelcontextprotocol.io/specification/2025-03-26/basic/transports

LANGUAGE: APIDOC
CODE:
```
## Streamable HTTP Transport

### Description
This transport utilizes HTTP POST and GET requests for client-server communication. Servers can optionally leverage Server-Sent Events (SSE) to stream multiple messages, enabling support for notifications and server-to-client requests. A single HTTP endpoint path must support both POST and GET methods.

### Method
POST, GET

### Endpoint
`[HTTP Endpoint URL]/mcp` (e.g., `https://example.com/mcp`)

### Parameters
#### Path Parameters
None

#### Query Parameters
None

#### Request Body
- **message** (JSON-RPC Object or Array) - Required (for POST) - A valid JSON-RPC message or batch sent via HTTP POST.

### Request Example
**POST Request Body:**
```json
{
  "jsonrpc": "2.0",
  "method": "anotherMethod",
  "params": {"key": "value"},
  "id": 2
}
```

**GET Request (for SSE stream initiation or polling):**
(Details on GET request parameters for SSE would typically be in a more detailed spec, but often involve headers or query params to establish/maintain the stream.)

### Response
#### Success Response (200)
- **response** (JSON-RPC Object or Array) - The JSON-RPC response to a request.
- **Server-Sent Events (SSE)** - For streaming multiple messages, including notifications and server-to-client requests.

#### Response Example
**Standard Response Body:**
```json
{
  "jsonrpc": "2.0",
  "result": 42,
  "id": 2
}
```

**SSE Event Example:**
```
event: mcp-notification
data: {"jsonrpc": "2.0", "method": "serverNotification", "params": ["data"]}

```

### Security Warning
- Servers **MUST** validate the `Origin` header.
- Servers **SHOULD** bind only to localhost (127.0.0.1) when running locally.
- Servers **SHOULD** implement proper authentication.
```

--------------------------------

TITLE: POST /api/prompts/list
DESCRIPTION: Requests a list of prompts and prompt templates from the server. Supports pagination using a cursor.

SOURCE: https://modelcontextprotocol.io/specification/2025-06-18/schema

LANGUAGE: APIDOC
CODE:
```
## POST /api/prompts/list

### Description
Sends a request to list prompts and prompt templates. Supports pagination by providing a cursor.

### Method
POST

### Endpoint
/api/prompts/list

### Parameters
#### Request Body
- **method** (string) - Required - Must be "prompts/list"
- **params** (object) - Optional - Parameters for pagination.
  - **cursor** (string) - Optional - An opaque token representing the current pagination position. If provided, the server should return results starting after this cursor.

### Request Example
```json
{
  "method": "prompts/list",
  "params": {
    "cursor": "some_opaque_cursor_token"
  }
}
```

### Response
#### Success Response (200)
- **prompts** (array) - A list of prompt objects.
- **next_cursor** (string) - An opaque token for fetching the next page of results, or null if there are no more results.

#### Response Example
```json
{
  "prompts": [
    {
      "id": "prompt_123",
      "name": "Example Prompt",
      "template": "This is a template for {{variable}}."
    }
  ],
  "next_cursor": "another_opaque_cursor_token"
}
```

#### Error Response (e.g., 400, 500)
- **error** (string) - A message describing the error.

#### Error Response Example
```json
{
  "error": "Invalid cursor provided."
}
```
```

--------------------------------

TITLE: List Resource Templates Request and Response (JSON RPC)
DESCRIPTION: Demonstrates the JSON RPC request to list available resource templates and the corresponding server response, which includes details about each template like URI template, name, title, description, and MIME type.

SOURCE: https://modelcontextprotocol.io/specification/2025-06-18/server/resources

LANGUAGE: json
CODE:
```
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "resources/templates/list"
}
```

LANGUAGE: json
CODE:
```
{
  "jsonrpc": "2.0",
  "id": 3,
  "result": {
    "resourceTemplates": [
      {
        "uriTemplate": "file:///{path}",
        "name": "Project Files",
        "title": "📁 Project Files",
        "description": "Access files in the project directory",
        "mimeType": "application/octet-stream"
      }
    ]
  }
}
```

--------------------------------

TITLE: Log Message Notification Example (JSON)
DESCRIPTION: Servers send log messages to clients via 'notifications/message' JSON-RPC notifications. This includes the message severity level, an optional logger name, and arbitrary JSON-serializable data containing log details.

SOURCE: https://modelcontextprotocol.io/specification/2024-11-05/server/utilities/logging

LANGUAGE: json
CODE:
```
{
  "jsonrpc": "2.0",
  "method": "notifications/message",
  "params": {
    "level": "error",
    "logger": "database",
    "data": {
      "error": "Connection failed",
      "details": {
        "host": "localhost",
        "port": 5432
      }
    }
  }
}
```

--------------------------------

TITLE: MCP JSON-RPC Response for Listing Tools
DESCRIPTION: This JSON snippet represents a server's response to a 'tools/list' request. It contains a list of available tools, each with a `name`, `title`, `description`, and `inputSchema`. The `nextCursor` field is used for paginating through the list of tools.

SOURCE: https://modelcontextprotocol.io/specification/2025-06-18/server/tools

LANGUAGE: json
CODE:
```
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "tools": [
      {
        "name": "get_weather",
        "title": "Weather Information Provider",
        "description": "Get current weather information for a location",
        "inputSchema": {
          "type": "object",
          "properties": {
            "location": {
              "type": "string",
              "description": "City name or zip code"
            }
          },
          "required": ["location"]
        }
      }
    ],
    "nextCursor": "next-page-cursor"
  }
}
```