================
CODE SNIPPETS
================
TITLE: Run FastAPI Development Server
DESCRIPTION: To run any FastAPI example, copy the code to a file named `main.py` and start the development server. This command initiates the server, watches for file changes, and provides URLs for the application and its documentation.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/tutorial/index.md

LANGUAGE: Shell
CODE:
```
fastapi dev main.py
```

--------------------------------

TITLE: Install FastAPI with Standard Dependencies
DESCRIPTION: This command installs the FastAPI framework along with its standard dependencies, such as Uvicorn (an ASGI server) and Pydantic (for data validation). It is recommended to perform this installation within a virtual environment for project isolation.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/README.md

LANGUAGE: bash
CODE:
```
pip install "fastapi[standard]"
```

--------------------------------

TITLE: Run FastAPI application in development mode
DESCRIPTION: This console command `fastapi dev main.py` starts the FastAPI development server. It automatically detects the FastAPI app in `main.py` and uses Uvicorn, with auto-reload enabled for local development. The output shows server startup information, including serving addresses for the application and API docs.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/README.md

LANGUAGE: console
CODE:
```
$ fastapi dev main.py

 ╭────────── FastAPI CLI - Development mode ───────────╮
 │                                                     │
 │  Serving at: http://127.0.0.1:8000                  │
 │                                                     │
 │  API docs: http://127.0.0.1:8000/docs               │
 │                                                     │
 │  Running in development mode, for production use:   │
 │                                                     │
 │  fastapi run                                        │
 │                                                     │
 ╰─────────────────────────────────────────────────────╯

INFO:     Will watch for changes in these directories: ['/home/user/code/awesomeapp']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [2248755] using WatchFiles
INFO:     Started server process [2248757]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

--------------------------------

TITLE: Example JSON response from FastAPI endpoint
DESCRIPTION: This JSON snippet shows the expected output from accessing the `/items/5?q=somequery` endpoint of the FastAPI application. It confirms the correct parsing of both path parameters (`item_id`) and query parameters (`q`).

SOURCE: https://github.com/tiangolo/fastapi/blob/master/README.md

LANGUAGE: JSON
CODE:
```
{"item_id": 5, "q": "somequery"}
```

--------------------------------

TITLE: Define basic FastAPI GET endpoints (synchronous)
DESCRIPTION: This Python code defines a basic FastAPI application (`main.py`) with two synchronous GET endpoints: `/` returning 'Hello World' and `/items/{item_id}` handling path and query parameters. It uses `fastapi` and `typing.Union` for type hints.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/README.md

LANGUAGE: Python
CODE:
```
from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
```

--------------------------------

TITLE: Install and Run FastAPI CLI Development Server
DESCRIPTION: This snippet demonstrates how to install or upgrade the FastAPI package and then run a development server using the new FastAPI CLI. It uses `pip` for installation and `fastapi dev` to start a local development server, which automatically reloads on code changes and provides access to API documentation.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/release-notes.md

LANGUAGE: console
CODE:
```
$ pip install --upgrade fastapi

$ fastapi dev main.py
```

--------------------------------

TITLE: Install FastAPI with standard dependencies using pip
DESCRIPTION: Provides an example of installing the FastAPI framework along with its standard dependencies using `pip`. This command demonstrates the typical process of adding a new library, which by default, installs into the global Python environment.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/virtual-environments.md

LANGUAGE: console
CODE:
```
pip install "fastapi[standard]"
```

--------------------------------

TITLE: Install FastAPI with Standard Dependencies
DESCRIPTION: Install FastAPI using pip. It is recommended to create and activate a virtual environment first. The `fastapi[standard]` option includes common dependencies, such as `fastapi-cloud-cli`. Alternatively, `pip install fastapi` installs only the core, or `pip install "fastapi[standard-no-fastapi-cloud-cli]"` for standard dependencies without the cloud CLI.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/tutorial/index.md

LANGUAGE: Shell
CODE:
```
pip install "fastapi[standard]"
```

--------------------------------

TITLE: Define basic FastAPI GET endpoints (asynchronous)
DESCRIPTION: This Python code demonstrates defining a basic FastAPI application with asynchronous GET endpoints using `async def`. It mirrors the synchronous version but allows for non-blocking I/O operations, suitable for high-performance applications.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/README.md

LANGUAGE: Python
CODE:
```
from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
```

--------------------------------

TITLE: Basic FastAPI TestClient Setup and First Test
DESCRIPTION: Demonstrates how to initialize `TestClient` with a FastAPI application and write a simple `pytest` function to test a GET endpoint, verifying the status code and JSON response.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/em/docs/tutorial/testing.md

LANGUAGE: python
CODE:
```
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

@app.get("/")
async def read_main():
    return {"msg": "Hello World"}

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}
```

--------------------------------

TITLE: Install FastAPI Development Requirements
DESCRIPTION: Instructions for installing the necessary development dependencies for the FastAPI project. This can be done using either `pip` or `uv` to ensure all required packages are present for local development.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/contributing.md

LANGUAGE: shell
CODE:
```
pip install -r requirements.txt
```

LANGUAGE: shell
CODE:
```
uv pip install -r requirements.txt
```

--------------------------------

TITLE: Install Python Packages Directly with pip or uv
DESCRIPTION: These commands demonstrate how to install specific Python packages directly into your active virtual environment. Examples are provided for both 'pip' and 'uv' (an alternative package installer). This method is useful for quick installations but it's generally recommended to use a requirements file for project dependencies.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/virtual-environments.md

LANGUAGE: console
CODE:
```
$ pip install "fastapi[standard]"
```

LANGUAGE: console
CODE:
```
$ uv pip install "fastapi[standard]"
```

--------------------------------

TITLE: Extended FastAPI Application Example with Path Operations and Headers
DESCRIPTION: This comprehensive example showcases a more complex FastAPI application with multiple path operations (GET and POST) that include error handling and require an 'X-Token' header for authentication. It demonstrates how to define routes that can return different responses based on input or header values.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/tutorial/testing.md

LANGUAGE: python
CODE:
```
from typing import Annotated
from fastapi import FastAPI, Header, HTTPException

app = FastAPI()

@app.get("/items/")
async def read_items(x_token: Annotated[str | None, Header()] = None):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")
    return {"message": "Hello World"}

@app.post("/items/")
async def create_item(item: dict, x_token: Annotated[str | None, Header()] = None):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")
    if item.get("name") == "invalid":
        raise HTTPException(status_code=400, detail="Invalid item name")
    return {"item": item}
```

LANGUAGE: python
CODE:
```
from typing import Annotated, Optional
from fastapi import FastAPI, Header, HTTPException

app = FastAPI()

@app.get("/items/")
async def read_items(x_token: Annotated[Optional[str], Header()] = None):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")
    return {"message": "Hello World"}

@app.post("/items/")
async def create_item(item: dict, x_token: Annotated[Optional[str], Header()] = None):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")
    if item.get("name") == "invalid":
        raise HTTPException(status_code=400, detail="Invalid item name")
    return {"item": item}
```

LANGUAGE: python
CODE:
```
from typing import Annotated, Optional
from fastapi import FastAPI, Header, HTTPException

app = FastAPI()

@app.get("/items/")
async def read_items(x_token: Annotated[Optional[str], Header()] = None):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")
    return {"message": "Hello World"}

@app.post("/items/")
async def create_item(item: dict, x_token: Annotated[Optional[str], Header()] = None):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")
    if item.get("name") == "invalid":
        raise HTTPException(status_code=400, detail="Invalid item name")
    return {"item": item}
```

LANGUAGE: python
CODE:
```
from typing import Union
from fastapi import FastAPI, Header, HTTPException

app = FastAPI()

@app.get("/items/")
async def read_items(x_token: Union[str, None] = Header(default=None)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")
    return {"message": "Hello World"}

@app.post("/items/")
async def create_item(item: dict, x_token: Union[str, None] = Header(default=None)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")
    if item.get("name") == "invalid":
        raise HTTPException(status_code=400, detail="Invalid item name")
    return {"item": item}
```

LANGUAGE: python
CODE:
```
from typing import Optional
from fastapi import FastAPI, Header, HTTPException

app = FastAPI()

@app.get("/items/")
async def read_items(x_token: Optional[str] = Header(None)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")
    return {"message": "Hello World"}

@app.post("/items/")
async def create_item(item: dict, x_token: Optional[str] = Header(None)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")
    if item.get("name") == "invalid":
        raise HTTPException(status_code=400, detail="Invalid item name")
    return {"item": item}
```

--------------------------------

TITLE: Run FastAPI Development Server via `fastapi dev`
DESCRIPTION: This console command starts a FastAPI application in development mode using the `fastapi dev` utility. It targets a specific Python file, running the application on `http://127.0.0.1:8000` by default. This setup ensures that local development does not conflict with documentation servers, which typically use a different port like `8008`.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/contributing.md

LANGUAGE: console
CODE:
```
$ fastapi dev tutorial001.py

INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

--------------------------------

TITLE: Basic FastAPI Application Testing with TestClient
DESCRIPTION: This example demonstrates the fundamental steps for testing a FastAPI application using `TestClient`. It shows how to import `TestClient`, instantiate it with your FastAPI app, define `pytest`-compatible test functions (starting with `test_`), and make synchronous requests to your application.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/tutorial/testing.md

LANGUAGE: python
CODE:
```
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

@app.get("/")
async def read_main():
    return {"msg": "Hello World"}

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}
```

--------------------------------

TITLE: Install httpx for FastAPI TestClient
DESCRIPTION: Before using FastAPI's TestClient, the 'httpx' library must be installed. This command demonstrates how to install it using pip within a virtual environment.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/tutorial/testing.md

LANGUAGE: console
CODE:
```
pip install httpx
```

--------------------------------

TITLE: Installing and Executing Pytest for FastAPI Tests
DESCRIPTION: Instructions for installing the `pytest` testing framework via pip and running tests from the command line, showing the typical output of a successful test run.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/em/docs/tutorial/testing.md

LANGUAGE: shell
CODE:
```
pip install pytest
```

LANGUAGE: shell
CODE:
```
pytest
```

--------------------------------

TITLE: Define a GET Path Operation in FastAPI with Python
DESCRIPTION: This example illustrates how to define a basic GET path operation in FastAPI using the `@app.get` decorator. It highlights FastAPI's intuitive routing system, designed to be as simple and direct as the `requests` library for defining API endpoints.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/alternatives.md

LANGUAGE: Python
CODE:
```
@app.get("/some/url")
def read_url():
    return {"message": "Hello World"}
```

--------------------------------

TITLE: Run FastAPI Development Server (Console)
DESCRIPTION: Execute this command in your terminal to start the FastAPI development server. It automatically reloads the application on code changes and provides the local URL for accessing your API and its documentation.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/tutorial/first-steps.md

LANGUAGE: console
CODE:
```
fastapi dev main.py
```

--------------------------------

TITLE: Run MkDocs Live Server Manually for Specific Language (Console)
DESCRIPTION: Manually start the MkDocs development server to preview the documentation for the current directory's language. This command serves the documentation on a specified address (127.0.0.1:8008) and is typically run from within a language-specific 'docs/' subdirectory.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/contributing.md

LANGUAGE: console
CODE:
```
mkdocs serve --dev-addr 127.0.0.1:8008
```

--------------------------------

TITLE: Example JSON Response from FastAPI (JSON)
DESCRIPTION: This JSON snippet illustrates the expected output when accessing the root endpoint (`/`) of the running FastAPI application. It confirms that the API is functioning correctly and returning the defined message.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/tutorial/first-steps.md

LANGUAGE: json
CODE:
```
{"message": "Hello World"}
```

--------------------------------

TITLE: Return Dictionary Response from FastAPI Endpoint
DESCRIPTION: Shows a typical return statement for a FastAPI endpoint, illustrating how to construct a dictionary response from processed input parameters. FastAPI automatically converts this dictionary into JSON for the client.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/README.md

LANGUAGE: Python
CODE:
```
    return {"item_name": item.name, "item_id": item_id}
```

--------------------------------

TITLE: Install FastAPI with Standard Dependencies
DESCRIPTION: This command installs the FastAPI library along with its recommended 'standard' dependencies. These typically include an ASGI server like Uvicorn for running the application and data validation libraries like Pydantic, ensuring a complete environment for developing FastAPI applications.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/index.md

LANGUAGE: bash
CODE:
```
pip install "fastapi[standard]"
```

--------------------------------

TITLE: Serve locally built FastAPI multi-language documentation
DESCRIPTION: After successfully running the `build-all` command, use this command to serve the combined multi-language documentation locally. This provides a simple server to preview the full site with translations, but it is not intended for active development.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/contributing.md

LANGUAGE: console
CODE:
```
python ./scripts/docs.py serve
```

--------------------------------

TITLE: Install python-multipart for FastAPI OAuth2
DESCRIPTION: Installs the `python-multipart` package, which is required by FastAPI for handling form data, specifically for OAuth2 password flow where username and password are sent as form data. It's automatically included with `fastapi[standard]` but needs manual installation if `fastapi` is installed alone.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/tutorial/security/first-steps.md

LANGUAGE: console
CODE:
```
$ pip install python-multipart
```

--------------------------------

TITLE: Example Path Operation within FastAPI APIRouter
DESCRIPTION: This small snippet provides an example of a path operation defined within an `APIRouter`. It shows how a GET request for an item by ID would be structured, inheriting the prefix and other configurations from its parent `APIRouter`.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/tutorial/bigger-applications.md

LANGUAGE: Python
CODE:
```
@router.get("/{item_id}")
async def read_item(item_id: str):
    ...
```

--------------------------------

TITLE: Run FastAPI Application with Uvicorn
DESCRIPTION: This command starts the FastAPI application using Uvicorn, a lightning-fast ASGI server. The `--reload` flag enables automatic reloading of the server when code changes are detected, which is useful for development. The `main:app` argument specifies that the `app` object from the `main.py` file should be used.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/em/docs/index.md

LANGUAGE: console
CODE:
```
uvicorn main:app --reload
```

LANGUAGE: console
CODE:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [28720]
INFO:     Started server process [28722]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

--------------------------------

TITLE: Install Pytest Testing Framework
DESCRIPTION: This command installs the `pytest` library, a popular testing framework for Python, using `pip`. It's recommended to perform this installation within a virtual environment.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/tutorial/testing.md

LANGUAGE: Shell
CODE:
```
pip install pytest
```

--------------------------------

TITLE: FastAPI Application with GET and PUT Endpoints
DESCRIPTION: This Python code defines a basic FastAPI application. It includes a root GET endpoint, a GET endpoint for items with path and query parameters, and a PUT endpoint for updating items. The `Item` class, inheriting from Pydantic's `BaseModel`, defines the data structure for the request body of the PUT endpoint, demonstrating data validation and serialization.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/em/docs/index.md

LANGUAGE: python
CODE:
```
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
```

--------------------------------

TITLE: Declare Single Body Example with FastAPI Body()
DESCRIPTION: Shows how to provide a single example for the request body using FastAPI's `Body()` dependency. This example will be included in the generated OpenAPI JSON Schema for the endpoint, improving clarity in API documentation.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/tutorial/schema-extra-example.md

LANGUAGE: Python
CODE:
```
from fastapi import FastAPI, Body
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Item = Body(
        examples=[
            {
                "name": "Foo",
                "description": "A very nice Item",
                "price": 42.0,
                "tax": 3.2
            }
        ]
    )
):
    results = {"item_id": item_id, "item": item}
    return results
```

--------------------------------

TITLE: Start Traefik Proxy Server
DESCRIPTION: This console command executes the Traefik binary, instructing it to load its configuration from the `traefik.toml` file. This initiates the proxy server, making it ready to handle incoming requests based on the defined rules.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/advanced/behind-a-proxy.md

LANGUAGE: console
CODE:
```
./traefik --configFile=traefik.toml
```

--------------------------------

TITLE: Install Uvicorn for FastAPI Applications
DESCRIPTION: This command installs the Uvicorn ASGI server, including recommended standard dependencies like `uvloop` for improved asynchronous performance. It's a crucial step for running FastAPI applications.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/deployment/manually.md

LANGUAGE: Shell
CODE:
```
$ pip install "uvicorn[standard]"
```

--------------------------------

TITLE: Run FastAPI Docs Live Server for a Specific Language (Python Script)
DESCRIPTION: Execute the FastAPI documentation live server for a specified language using the provided Python script. This command starts a development server, serving the documentation in the given language (e.g., Spanish 'es') and watches for changes, providing a quick way to preview translations.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/contributing.md

LANGUAGE: console
CODE:
```
python ./scripts/docs.py live es
```

--------------------------------

TITLE: Install Typer CLI Shell Completion
DESCRIPTION: Installs shell autocompletion for Typer CLI, which is used for some FastAPI scripts. This enhances productivity by providing command suggestions directly in the terminal.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/contributing.md

LANGUAGE: shell
CODE:
```
typer --install-completion
```

--------------------------------

TITLE: MkDocs YAML Inheritance Configuration for New Language
DESCRIPTION: Illustrates the 'mkdocs.yml' configuration for a new language, showing how it inherits settings from the main English documentation. This ensures consistency and reduces redundancy in configuration across different language versions, simplifying setup for new translations.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/contributing.md

LANGUAGE: yaml
CODE:
```
INHERIT: ../en/mkdocs.yml
```

--------------------------------

TITLE: Build all FastAPI documentation for multiple languages
DESCRIPTION: Use this command to compile the documentation for all supported languages. The `build-all` command processes each language's MkDocs site, combines them, and generates the final output in the `./site/` directory, preparing it for a comprehensive preview.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/contributing.md

LANGUAGE: console
CODE:
```
python ./scripts/docs.py build-all
```

--------------------------------

TITLE: Start FastAPI with Multiple Workers
DESCRIPTION: These examples demonstrate how to configure a FastAPI application to run with multiple worker processes, which can significantly improve concurrency and performance. You can achieve this using either the `fastapi` command-line tool or by directly invoking `uvicorn` with the `--workers` option.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/deployment/server-workers.md

LANGUAGE: console
CODE:
```
fastapi run --workers 4 main.py
```

LANGUAGE: console
CODE:
```
uvicorn main:app --host 0.0.0.0 --port 8080 --workers 4
```

--------------------------------

TITLE: FastAPI HTTP Basic Security Initial Setup
DESCRIPTION: This snippet demonstrates the initial setup for implementing HTTP Basic Authentication in a FastAPI application. It imports `HTTPBasic` and `HTTPBasicCredentials` from `fastapi.security`, defines an instance of `HTTPBasic` as a security dependency, and then applies this dependency to a path operation to automatically handle the initial authentication prompt.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/em/docs/advanced/security/http-basic-auth.md

LANGUAGE: python
CODE:
```
from fastapi import FastAPI, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()

security = HTTPBasic()

@app.get("/users/me")
def read_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    # In a real application, you would proceed to validate these credentials.
    # For this example, it just demonstrates receiving them.
    return {"message": "Credentials received", "username": credentials.username}
```

--------------------------------

TITLE: Declare Multiple Body Examples with FastAPI Body()
DESCRIPTION: Demonstrates how to define multiple examples for a request body using FastAPI's `Body()` dependency. While these examples are part of the internal JSON Schema, current Swagger UI versions may not display all of them directly, requiring alternative OpenAPI-specific example declarations for full UI support.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/tutorial/schema-extra-example.md

LANGUAGE: Python
CODE:
```
from fastapi import FastAPI, Body
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Item = Body(
        examples=[
            {
                "name": "Foo",
                "description": "A very nice Item",
                "price": 42.0,
                "tax": 3.2
            },
            {
                "name": "Bar",
                "description": "The bartenders",
                "price": 32.0,
                "tax": 2.2
            },
            {
                "name": "Baz",
                "description": "Empty",
                "price": 12.0,
                "tax": 0.0
            }
        ]
    )
):
    results = {"item_id": item_id, "item": item}
    return results
```

--------------------------------

TITLE: Example .env File Content
DESCRIPTION: Illustrates a typical `.env` file structure for defining environment variables, such as `ADMIN_EMAIL` and `APP_NAME`, which can be loaded by the application.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/advanced/settings.md

LANGUAGE: bash
CODE:
```
ADMIN_EMAIL="deadpool@example.com"
APP_NAME="ChimichangApp"
```

--------------------------------

TITLE: Run FastAPI development server for mounted applications
DESCRIPTION: Execute the `fastapi dev` command to start the main application, which includes mounted sub-applications, and observe the server's startup information.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/advanced/sub-applications.md

LANGUAGE: console
CODE:
```
$ fastapi dev main.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

--------------------------------

TITLE: Install Gunicorn and Uvicorn
DESCRIPTION: Installs Gunicorn and Uvicorn, including Uvicorn's 'standard' extra for better performance. These packages are necessary to run FastAPI with Gunicorn as a process manager.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/em/docs/deployment/server-workers.md

LANGUAGE: console
CODE:
```
pip install "uvicorn[standard]" gunicorn
```

--------------------------------

TITLE: Create a Dockerfile to Containerize a Python FastAPI App
DESCRIPTION: This Dockerfile outlines the steps to build a Docker image for a FastAPI application. It starts from a Python base image, sets the working directory, copies and installs dependencies, and then copies the application code into the container.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/deployment/docker.md

LANGUAGE: dockerfile
CODE:
```
FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app
```

--------------------------------

TITLE: Perform a GET Request using Python Requests Library
DESCRIPTION: This snippet demonstrates how to make a simple HTTP GET request using the `requests` library in Python. It showcases the library's straightforward and intuitive API for interacting with web services as a client.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/alternatives.md

LANGUAGE: Python
CODE:
```
response = requests.get("http://example.com/some/url")
```

--------------------------------

TITLE: Serve FastAPI Documentation Locally with Live Reload
DESCRIPTION: Commands to build and serve the FastAPI documentation locally, with live-reloading capabilities. This allows developers to see changes to documentation or source files reflected instantly in the browser at `http://127.0.0.1:8008`.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/contributing.md

LANGUAGE: shell
CODE:
```
python ./scripts/docs.py live
```

LANGUAGE: shell
CODE:
```
cd docs/en/
mkdocs serve --dev-addr 127.0.0.1:8008
```

--------------------------------

TITLE: Declare Examples using FastAPI Field Arguments
DESCRIPTION: Illustrates how to add example data directly to a Pydantic model field using FastAPI's `Field()` function. This allows for more granular control over example data for individual fields within a model, which is then reflected in the generated JSON Schema.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/tutorial/schema-extra-example.md

LANGUAGE: Python
CODE:
```
from pydantic import BaseModel, Field

class Item(BaseModel):
    name: str = Field(examples=["Foo"])
    description: str | None = Field(default=None, examples=["A very nice Item"])
    price: float = Field(examples=[42.0])
    tax: float | None = Field(default=None, examples=[3.2])
```

--------------------------------

TITLE: Example FastAPI Application Directory Structure
DESCRIPTION: Illustrates a common file and directory layout for a larger FastAPI project, showing how different components like main application, dependencies, and routers are organized into a package structure.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/em/docs/tutorial/bigger-applications.md

LANGUAGE: text
CODE:
```
.├── app│   ├── __init__.py│   ├── main.py│   ├── dependencies.py│   └── routers│   │   ├── __init__.py│   │   ├── items.py│   │   └── users.py│   └── internal│       ├── __init__.py│       └── admin.py
```

--------------------------------

TITLE: Run FastAPI Development Server
DESCRIPTION: Command to start the FastAPI application in development mode using `fastapi dev`. This makes the application accessible via a local URL, typically `http://127.0.0.1:8000`, and enables features like automatic code reloading.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/tutorial/security/first-steps.md

LANGUAGE: console
CODE:
```
$ fastapi dev main.py
```

--------------------------------

TITLE: Declare Path Parameter Type in FastAPI (int)
DESCRIPTION: Illustrates how to declare a simple integer type for a path parameter in FastAPI using standard Python type hints. This enables automatic validation and documentation for the parameter.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/README.md

LANGUAGE: Python
CODE:
```
item_id: int
```

--------------------------------

TITLE: Create Test Path Operation in FastAPI
DESCRIPTION: This code defines a simple GET path operation in FastAPI to serve as an endpoint for testing the custom documentation setup. It returns a basic JSON response, confirming the API is operational and accessible.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/how-to/custom-docs-ui-assets.md

LANGUAGE: Python
CODE:
```
@app.get("/items/")
async def read_items():
    return {"message": "Hello FastAPI!"}
```

--------------------------------

TITLE: Install PassLib with Bcrypt for secure password hashing
DESCRIPTION: This command installs the `passlib` library along with its `bcrypt` extension. PassLib is a comprehensive password hashing framework for Python, and Bcrypt is a recommended secure hashing algorithm for storing user passwords. This installation should also be performed within an activated virtual environment.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/tutorial/security/oauth2-jwt.md

LANGUAGE: Shell
CODE:
```
pip install "passlib[bcrypt]"
```

--------------------------------

TITLE: Run Uvicorn Server Directly for FastAPI Debugging (Python)
DESCRIPTION: This Python code demonstrates a common pattern for starting a FastAPI application using `uvicorn.run()` directly within the application's main file. This setup facilitates debugging by allowing the file to be executed as a standard Python script, enabling debuggers (e.g., VS Code, PyCharm) to attach and utilize breakpoints. The `if __name__ == "__main__":` block ensures the server initiates only when the file is run directly, preventing automatic startup when the file is imported as a module.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/tutorial/debugging.md

LANGUAGE: python
CODE:
```
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello FastAPI"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

--------------------------------

TITLE: Define a GET Path Operation Decorator in FastAPI
DESCRIPTION: FastAPI uses Python decorators to associate functions with specific URL paths and HTTP methods (operations). The `@app.get('/')` decorator, for example, registers the function below it to handle HTTP GET requests to the root path (`/`). This is the primary mechanism for defining API endpoints.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/tutorial/first-steps.md

LANGUAGE: Python
CODE:
```
@app.get("/")
async def read_root():
    return {"Hello": "World"}
```

--------------------------------

TITLE: Define and Use APIRouter for Modular Routes in FastAPI
DESCRIPTION: Shows how to import `APIRouter` and define path operations within a separate module (e.g., `app/routers/users.py`), allowing for modular organization of routes in a FastAPI application. It includes examples of basic GET requests and path parameters.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/em/docs/tutorial/bigger-applications.md

LANGUAGE: python
CODE:
```
from fastapi import APIRouter

router = APIRouter()

@router.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]

@router.get("/users/me", tags=["users"])
async def read_user_me():
    return {"username": "current user"}

@router.get("/users/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}
```

--------------------------------

TITLE: Admonition Syntax Example (English)
DESCRIPTION: This snippet demonstrates the standard syntax for an admonition block, specifically a 'tip', in the documentation. It shows how the keyword 'tip' is used to define the block type.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/management-tasks.md

LANGUAGE: Admonition Syntax
CODE:
```
///
tip

This is a tip.

///
```

--------------------------------

TITLE: Create a Simple FastAPI Application (Python)
DESCRIPTION: This snippet demonstrates how to create a basic FastAPI application. It initializes a FastAPI instance and defines a root endpoint that returns a 'Hello World' JSON response. Save this code as `main.py` to follow along with the tutorial.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/tutorial/first-steps.md

LANGUAGE: python
CODE:
```
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello World"}
```

--------------------------------

TITLE: Install python-multipart for File Uploads
DESCRIPTION: Before handling file uploads in FastAPI, the `python-multipart` library must be installed. This command installs the necessary dependency for processing form data, which is essential for receiving uploaded files.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/tutorial/request-files.md

LANGUAGE: console
CODE:
```
$ pip install python-multipart
```

--------------------------------

TITLE: Install pydantic-settings for FastAPI Configuration
DESCRIPTION: Instructions to install the `pydantic-settings` package, which is essential for managing application settings and environment variables with Pydantic's `BaseSettings` in FastAPI. It can be installed directly or as part of the `fastapi[all]` extra.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/advanced/settings.md

LANGUAGE: Shell
CODE:
```
pip install pydantic-settings
```

LANGUAGE: Shell
CODE:
```
pip install "fastapi[all]"
```

--------------------------------

TITLE: Example JSON response from a FastAPI GET endpoint
DESCRIPTION: This snippet shows the expected JSON output when accessing the `/items/{item_id}` endpoint with specific path and query parameters. It illustrates the structure of the data returned by the API, demonstrating how FastAPI serializes Python dictionaries to JSON.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/index.md

LANGUAGE: JSON
CODE:
```
{"item_id": 5, "q": "somequery"}
```

--------------------------------

TITLE: Start Traefik Proxy
DESCRIPTION: This command initiates the Traefik proxy, instructing it to load its primary configuration from the `traefik.toml` file. Traefik will then begin listening for incoming requests and applying the defined routing rules.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/em/docs/advanced/behind-a-proxy.md

LANGUAGE: console
CODE:
```
./traefik --configFile=traefik.toml

INFO[0000] Configuration loaded from file: /home/user/awesomeapi/traefik.toml
```

--------------------------------

TITLE: Install python-multipart for FastAPI Forms
DESCRIPTION: Before utilizing forms in FastAPI, the `python-multipart` library is required. This console command demonstrates how to install it using pip, typically within a virtual environment.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/tutorial/request-form-models.md

LANGUAGE: console
CODE:
```
$ pip install python-multipart
```

--------------------------------

TITLE: Verify FastAPI Endpoint JSON Response
DESCRIPTION: After starting the FastAPI application, this section demonstrates how to access a specific API endpoint (`/items/5?q=somequery`) in a web browser. It also shows the expected JSON response from the API, confirming that the endpoint correctly processes path parameters and query parameters.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/em/docs/index.md

LANGUAGE: json
CODE:
```
{"item_id": 5, "q": "somequery"}
```

--------------------------------

TITLE: Example FastAPI Application File Structure
DESCRIPTION: This snippet illustrates a recommended directory and file structure for a larger FastAPI application. It highlights the role of `__init__.py` files in defining Python packages and subpackages, enabling modular imports and organization.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/tutorial/bigger-applications.md

LANGUAGE: text
CODE:
```
.
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── dependencies.py
│   └── routers
│   │   ├── __init__.py
│   │   ├── items.py
│   │   └── users.py
│   └── internal
│       ├── __init__.py
│       └── admin.py
```

LANGUAGE: text
CODE:
```
.
├── app                  # "app" is a Python package
│   ├── __init__.py      # this file makes "app" a "Python package"
│   ├── main.py          # "main" module, e.g. import app.main
│   ├── dependencies.py  # "dependencies" module, e.g. import app.dependencies
│   └── routers          # "routers" is a "Python subpackage"
│   │   ├── __init__.py  # makes "routers" a "Python subpackage"
│   │   ├── items.py     # "items" submodule, e.g. import app.routers.items
│   │   └── users.py     # "users" submodule, e.g. import app.routers.users
│   └── internal         # "internal" is a "Python subpackage"
│       ├── __init__.py  # makes "internal" a "Python subpackage"
│       └── admin.py     # "admin" submodule, e.g. import app.internal.admin
```

--------------------------------

TITLE: Testing FastAPI Endpoints with Headers and Request Body
DESCRIPTION: Provides examples for testing FastAPI endpoints that require custom headers (`X-Token`) and handle different HTTP methods (GET, POST). It demonstrates how to pass headers and JSON request bodies using `TestClient` methods, including tests for invalid token scenarios.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/em/docs/tutorial/testing.md

LANGUAGE: python
CODE:
```
# app_b/main.py
from fastapi import FastAPI, Header, HTTPException

app = FastAPI()

@app.get("/items/")
async def read_items(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")
    return {"message": "Hello World from items"}

@app.post("/items/")
async def create_item(item: dict, x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")
    return {"item": item, "message": "Item created"}
```

LANGUAGE: python
CODE:
```
# app_b/test_main.py
from fastapi.testclient import TestClient
from app_b.main import app

client = TestClient(app)

def test_read_items():
    response = client.get("/items/", headers={"X-Token": "fake-super-secret-token"})
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World from items"}

def test_read_items_bad_token():
    response = client.get("/items/", headers={"X-Token": "bad-token"})
    assert response.status_code == 400
    assert response.json() == {"detail": "X-Token header invalid"}

def test_create_item():
    response = client.post(
        "/items/",
        headers={"X-Token": "fake-super-secret-token"},
        json={"name": "Foo", "description": "The Foo Fighters"},
    )
    assert response.status_code == 200
    assert response.json() == {"item": {"name": "Foo", "description": "The Foo Fighters"}, "message": "Item created"}

def test_create_item_bad_token():
    response = client.post(
        "/items/",
        headers={"X-Token": "bad-token"},
        json={"name": "Foo", "description": "The Foo Fighters"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "X-Token header invalid"}
```

--------------------------------

TITLE: Instantiate FastAPI Application in Python
DESCRIPTION: After importing the `FastAPI` class, you need to create an 'instance' of it. This instance, typically named `app`, serves as the main entry point for defining all your API's routes, operations, and configurations.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/tutorial/first-steps.md

LANGUAGE: Python
CODE:
```
app = FastAPI()
```

--------------------------------

TITLE: Install python-multipart for File and Form Handling
DESCRIPTION: To enable FastAPI to receive uploaded files and/or form data, the `python-multipart` library is required. This console command demonstrates how to install this dependency using pip, typically within a virtual environment, before running your FastAPI application.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/tutorial/request-forms-and-files.md

LANGUAGE: console
CODE:
```
$ pip install python-multipart
```

--------------------------------

TITLE: Activate Virtual Environment on Linux/macOS
DESCRIPTION: Command to activate the virtual environment on Linux and macOS systems. This ensures that any subsequent Python commands or package installations use the isolated environment's Python interpreter and installed packages, rather than global ones. This should be run every time a new terminal session is started for the project.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/virtual-environments.md

LANGUAGE: console
CODE:
```
$ source .venv/bin/activate
```

--------------------------------

TITLE: Install Python Packages from requirements.txt with pip or uv
DESCRIPTION: This section illustrates how to install all project dependencies listed in a 'requirements.txt' file. This is the recommended approach for managing project dependencies, ensuring consistent environments across different machines. Commands are provided for both 'pip' and 'uv'.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/virtual-environments.md

LANGUAGE: console
CODE:
```
$ pip install -r requirements.txt
```

LANGUAGE: console
CODE:
```
$ uv pip install -r requirements.txt
```

LANGUAGE: requirements.txt
CODE:
```
fastapi[standard]==0.113.0
pydantic==2.8.0
```

--------------------------------

TITLE: FastAPI: Returning Input Data Directly (Security Risk)
DESCRIPTION: This example demonstrates a FastAPI endpoint where the `UserIn` Pydantic model, containing a plaintext password, is used for both input and output (`response_model`). This configuration results in the password being returned in the API response, highlighting a significant security vulnerability if not handled with extreme caution. It also includes instructions for installing necessary dependencies like `email-validator`.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/tutorial/response-model.md

LANGUAGE: Python
CODE:
```
from typing import Union
from pydantic import BaseModel, EmailStr
from fastapi import FastAPI

class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: Union[str, None] = None

app = FastAPI()

@app.post("/user/", response_model=UserIn)
async def create_user(user: UserIn):
    return user
```

LANGUAGE: Shell
CODE:
```
$ pip install email-validator
```

LANGUAGE: Shell
CODE:
```
$ pip install "pydantic[email]"
```

--------------------------------

TITLE: Install python-multipart for FastAPI Forms
DESCRIPTION: Before using form data with FastAPI, the `python-multipart` library is required. This command demonstrates how to install it using pip, typically within a virtual environment.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/tutorial/request-forms.md

LANGUAGE: console
CODE:
```
pip install python-multipart
```

--------------------------------

TITLE: Install FastAPI without standard dependencies (Python pip)
DESCRIPTION: This command installs FastAPI without its standard dependencies. This is suitable for users who want to explicitly manage their dependencies or avoid unnecessary packages. It currently installs only the core FastAPI package. It requires a Python environment with pip installed.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/release-notes.md

LANGUAGE: shell
CODE:
```
pip install fastapi
```

--------------------------------

TITLE: Install Jinja2 for FastAPI templates
DESCRIPTION: Instructions to install the Jinja2 templating engine using pip, a common dependency for FastAPI applications requiring server-side rendering. It's recommended to do this within a virtual environment.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/advanced/templates.md

LANGUAGE: console
CODE:
```
pip install jinja2
```

--------------------------------

TITLE: Install SQLModel library for database integration
DESCRIPTION: Installs the `sqlmodel` Python package via `pip`. This library is essential for defining database models and interacting with SQL databases in a FastAPI application, building upon SQLAlchemy and Pydantic.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/tutorial/sql-databases.md

LANGUAGE: console
CODE:
```
pip install sqlmodel
```

--------------------------------

TITLE: Chain Sub-dependencies with yield in FastAPI
DESCRIPTION: This example demonstrates how FastAPI correctly handles a chain of sub-dependencies, where each dependency uses `yield`. FastAPI ensures that the 'exit code' (the `finally` block after `yield`) for each dependency is executed in the correct reverse order of their setup, guaranteeing proper resource cleanup across the entire dependency tree.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/tutorial/dependencies/dependencies-with-yield.md

LANGUAGE: python
CODE:
```
from typing import Generator
from fastapi import Depends, FastAPI

async def dependency_a() -> Generator:
    print("Running dependency_a setup")
    try:
        yield "value_a"
    finally:
        print("Cleaning up dependency_a") # Runs last in the chain

async def dependency_b(dep_a: str = Depends(dependency_a)) -> Generator:
    print(f"Running dependency_b setup, got {dep_a}")
    try:
        yield "value_b"
    finally:
        print("Cleaning up dependency_b") # Runs before dependency_a cleanup

async def dependency_c(dep_b: str = Depends(dependency_b)) -> Generator:
    print(f"Running dependency_c setup, got {dep_b}")
    try:
        yield "value_c"
    finally:
        print("Cleaning up dependency_c") # Runs first in the chain
```

--------------------------------

TITLE: Example PATH Variable on Windows
DESCRIPTION: Illustrates the typical structure of the `PATH` environment variable on Windows, showing semicolon-separated directories where the system searches for executables.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/environment-variables.md

LANGUAGE: plaintext
CODE:
```
C:\Program Files\Python312\Scripts;C:\Program Files\Python312;C:\Windows\System32
```

--------------------------------

TITLE: Run Uvicorn with Multiple Worker Processes
DESCRIPTION: This console command demonstrates how to start a Uvicorn application, `main:app`, binding it to `0.0.0.0:8080` and configuring it to use 4 worker processes. The output shows the Uvicorn server starting, indicating the parent process and the individual worker process IDs, confirming the successful launch of multiple concurrent application instances.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/em/docs/deployment/server-workers.md

LANGUAGE: console
CODE:
```
$ uvicorn main:app --host 0.0.0.0 --port 8080 --workers 4
```

--------------------------------

TITLE: Example Initial API Request and Body
DESCRIPTION: Provides an example of an initial HTTP request made to the FastAPI application. This request includes a query parameter for the external callback URL and a JSON body containing invoice details, which the API processes before initiating a callback.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/advanced/openapi-callbacks.md

LANGUAGE: HTTP
CODE:
```
https://yourapi.com/invoices/?callback_url=https://www.external.org/events
```

LANGUAGE: JSON
CODE:
```
{
    "id": "2expen51ve",
    "customer": "Mr. Richie Rich",
    "total": "9999"
}
```

--------------------------------

TITLE: Declare Pydantic Model Examples for JSON Schema (Pydantic v2 & v1)
DESCRIPTION: Demonstrates how to embed example data directly into a Pydantic model's JSON Schema definition. For Pydantic v2, `model_config` is used with `json_schema_extra`. For Pydantic v1, an internal `Config` class with `schema_extra` is used. This data appears in API documentation.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/tutorial/schema-extra-example.md

LANGUAGE: Python
CODE:
```
from typing import Literal
from pydantic import BaseModel, Field

class Item(BaseModel):
    name: str = Field(examples=["Foo"])
    description: str | None = Field(default=None, examples=["A very nice Item"])
    price: float = Field(examples=[42.0])
    tax: float | None = Field(default=None, examples=[3.2])
    category: Literal["electronics", "clothes"] = Field(examples=["electronics"])

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 42.0,
                    "tax": 3.2,
                    "category": "electronics"
                }
            ]
        }
    }
```

LANGUAGE: Python
CODE:
```
from typing import Literal
from pydantic import BaseModel, Field

class Item(BaseModel):
    name: str = Field(examples=["Foo"])
    description: str | None = Field(default=None, examples=["A very nice Item"])
    price: float = Field(examples=[42.0])
    tax: float | None = Field(default=None, examples=[3.2])
    category: Literal["electronics", "clothes"] = Field(examples=["electronics"])

    class Config:
        schema_extra = {
            "examples": [
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 42.0,
                    "tax": 3.2,
                    "category": "electronics"
                }
            ]
        }

```

--------------------------------

TITLE: Define a Python function without type hints
DESCRIPTION: Illustrates a basic Python function for concatenating first and last names. This example demonstrates the lack of intelligent editor autocompletion and static analysis benefits when type hints are omitted, leading to a less guided development experience.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/python-types.md

LANGUAGE: Python
CODE:
```
def get_full_name(first_name, last_name):
    return f"{first_name.title()} {last_name.title()}"

# Example usage, producing 'John Doe'
print(get_full_name("john", "doe"))
```

--------------------------------

TITLE: Illustrate Python's Asynchronous `async with` Statement for Context Management
DESCRIPTION: This example shows how to use Python's `async with` statement with an asynchronous context manager. It's designed for managing asynchronous resources, ensuring that setup and teardown operations are performed correctly within an `await` context, similar to how `with` handles synchronous resources.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/advanced/events.md

LANGUAGE: Python
CODE:
```
async with lifespan(app):
    await do_stuff()
```

--------------------------------

TITLE: Declare Body Model Type in FastAPI (Pydantic Model)
DESCRIPTION: Demonstrates declaring a more complex body parameter using a custom Pydantic model (e.g., 'Item') in FastAPI. This allows for automatic validation, serialization, and documentation of deeply nested JSON objects.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/README.md

LANGUAGE: Python
CODE:
```
item: Item
```

--------------------------------

TITLE: Add Summary and Description to FastAPI Path Operations
DESCRIPTION: This example demonstrates how to provide a concise `summary` and a more detailed `description` for a path operation directly within its decorator. These fields are crucial for generating informative and user-friendly API documentation in OpenAPI.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/tutorial/path-operation-configuration.md

LANGUAGE: Python
CODE:
```
from fastapi import FastAPI

app = FastAPI()

@app.post(
    "/items/",
    summary="Create an item",
    description="Create an item with all the information, name, description, price, and tax."
)
async def create_item(name: str):
    return {"name": name}
```

--------------------------------

TITLE: Full JSON Request Body Example with Optional Fields
DESCRIPTION: This JSON object represents a complete request body, including all fields (name, description, price, tax), where 'description' and 'tax' are optional and provided with values.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/tutorial/body.md

LANGUAGE: JSON
CODE:
```
{
    "name": "Foo",
    "description": "An optional description",
    "price": 45.2,
    "tax": 3.5
}
```

--------------------------------

TITLE: Example Output of Pydantic Model as Dictionary
DESCRIPTION: Provides an example of the dictionary structure obtained after converting a Pydantic `UserIn` model instance using `.dict()`, including all fields and their values.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/tutorial/extra-models.md

LANGUAGE: Python
CODE:
```
{
    'username': 'john',
    'password': 'secret',
    'email': 'john.doe@example.com',
    'full_name': None,
}
```

--------------------------------

TITLE: Run FastAPI Application with `fastapi run` Command
DESCRIPTION: This command starts a FastAPI application using the built-in `fastapi run` utility, which defaults to using Uvicorn. It automatically detects the application object (e.g., `app` from `main.py`) and serves it, providing server URLs for access and documentation. This is suitable for development, testing, or simple deployments.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/deployment/manually.md

LANGUAGE: console
CODE:
```
$ fastapi run main.py

  FastAPI   Starting production server 🚀

             Searching for package file structure from directories
             with __init__.py files
             Importing from /home/user/code/awesomeapp

   module   🐍 main.py

     code   Importing the FastAPI app object from the module with
             the following code:

             from main import app

      app   Using import string: main:app

   server   Server started at http://0.0.0.0:8000
   server   Documentation at http://0.0.0.0:8000/docs

             Logs:

     INFO   Started server process [2306215]
     INFO   Waiting for application startup.
     INFO   Application startup complete.
     INFO   Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C
             to quit)
```

--------------------------------

TITLE: Add Pydantic BaseModel and PUT endpoint to FastAPI
DESCRIPTION: This Python code extends the FastAPI application by introducing a Pydantic `BaseModel` for data validation (`Item`) and adding a `PUT` endpoint (`/items/{item_id}`). The `PUT` endpoint accepts an `item_id` and an `Item` object as the request body, showcasing data handling and validation capabilities. The server automatically reloads on file changes.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/README.md

LANGUAGE: Python
CODE:
```
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
```

--------------------------------

TITLE: Python Module Import Example
DESCRIPTION: Demonstrates a standard Python import statement, showing how one module (e.g., `app/main.py`) can import another module (e.g., `app/routers/items.py`) within the same package structure.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/em/docs/tutorial/bigger-applications.md

LANGUAGE: python
CODE:
```
from app.routers import items
```

--------------------------------

TITLE: Install PyJWT for JWT token generation and verification
DESCRIPTION: This command installs the `PyJWT` library, which is essential for creating, encoding, decoding, and verifying JSON Web Tokens (JWTs) in Python applications. It should be run within an activated virtual environment.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/tutorial/security/oauth2-jwt.md

LANGUAGE: Shell
CODE:
```
pip install pyjwt
```

--------------------------------

TITLE: Install Python Package Requirements using pip
DESCRIPTION: This console command demonstrates how to install all Python package dependencies listed in a `requirements.txt` file using the `pip` package installer, ensuring all project dependencies are met.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/deployment/docker.md

LANGUAGE: shell
CODE:
```
pip install -r requirements.txt
```

--------------------------------

TITLE: Run FastAPI Development Server
DESCRIPTION: This command starts the FastAPI application in development mode. It automatically reloads the server upon code changes and displays the local URL where the application is accessible.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/tutorial/sql-databases.md

LANGUAGE: console
CODE:
```
$ fastapi dev main.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

--------------------------------

TITLE: Define Application Settings with Pydantic BaseSettings
DESCRIPTION: This example demonstrates how to create a configuration class by inheriting from Pydantic's `BaseSettings`. It shows how to define settings fields with type hints, default values, and validation rules using `Field()`, allowing Pydantic to automatically load values from environment variables.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/em/docs/advanced/settings.md

LANGUAGE: python
CODE:
```
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Awesome API"
    admin_email: str
    items_per_user: int = Field(50, gt=0, lt=1000)
```

--------------------------------

TITLE: Install a specific Python package version globally
DESCRIPTION: Demonstrates how to install a specific version of a Python package (e.g., 'harry' version 1) using `pip`. This action, when performed in the global environment, highlights the potential for version conflicts with other projects.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/virtual-environments.md

LANGUAGE: console
CODE:
```
pip install "harry==1"
```

--------------------------------

TITLE: Run FastAPI with Root Path via Command Line
DESCRIPTION: Shows how to start a FastAPI application using the `fastapi run` command, specifying the `--root-path` option to inform the application about its effective base path when behind a proxy. The `--forwarded-allow-ips` option is also included for proxy compatibility.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/advanced/behind-a-proxy.md

LANGUAGE: Console
CODE:
```
fastapi run main.py --forwarded-allow-ips="*" --root-path /api/v1
```

--------------------------------

TITLE: Example PATH Variable on Linux/macOS
DESCRIPTION: Illustrates the typical structure of the `PATH` environment variable on Linux and macOS, showing colon-separated directories where the system searches for executables.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/environment-variables.md

LANGUAGE: plaintext
CODE:
```
/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin
```

--------------------------------

TITLE: Initialize New Language Documentation Directory (Python Script)
DESCRIPTION: Utilize the 'docs.py' script to create the necessary directory structure and initial files for a new documentation language. This command takes a 2-letter language code (e.g., 'la' for Latin) and sets up the basic configuration, including an 'mkdocs.yml' and 'index.md' file.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/contributing.md

LANGUAGE: console
CODE:
```
python ./scripts/docs.py new-lang la
```

--------------------------------

TITLE: Dockerfile: Installing Python Dependencies with Caching
DESCRIPTION: This Dockerfile command executes `pip install` to install Python dependencies from `requirements.txt`. By placing this instruction after copying `requirements.txt` alone, Docker can effectively cache this layer. If the `requirements.txt` file has not changed, this potentially time-consuming step will reuse the cached layer, significantly accelerating build times.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/deployment/docker.md

LANGUAGE: Dockerfile
CODE:
```
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
```

--------------------------------

TITLE: Translate Headings to German Infinite Verb Form Examples
DESCRIPTION: Illustrates the rule of translating English headings into German using the infinite verb form, while preserving the ID part. The code blocks show English sources, followed by the correct German translation, and then an incorrect German translation for each example.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/de/llm-prompt.md

LANGUAGE: markdown
CODE:
```
## Create a Project { #create-a-project }
```

LANGUAGE: markdown
CODE:
```
## Ein Projekt erstellen { #create-a-project }
```

LANGUAGE: markdown
CODE:
```
## Erstellen Sie ein Projekt { #create-a-project }
```

LANGUAGE: markdown
CODE:
```
# Install Packages { #install-packages }
```

LANGUAGE: markdown
CODE:
```
# Pakete installieren { #install-packages }
```

LANGUAGE: markdown
CODE:
```
# Installieren Sie Pakete { #install-packages }
```

LANGUAGE: markdown
CODE:
```
### Run Your Program { #run-your-program }
```

LANGUAGE: markdown
CODE:
```
### Ihr Programm ausführen { #run-your-program }
```

LANGUAGE: markdown
CODE:
```
### Führen Sie Ihr Programm aus { #run-your-program }
```

--------------------------------

TITLE: Minimal JSON Request Body Example with Only Required Fields
DESCRIPTION: This JSON object demonstrates a valid request body where only the required fields ('name' and 'price') are present. Optional fields ('description' and 'tax') are omitted, as allowed by the Pydantic model definition.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/tutorial/body.md

LANGUAGE: JSON
CODE:
```
{
    "name": "Foo",
    "price": 45.2
}
```

--------------------------------

TITLE: Instantiating a Python Class
DESCRIPTION: Shows a basic Python class definition with an `__init__` method and how to create an instance of that class. This example highlights that class instantiation uses a 'callable' syntax, making classes inherently suitable for use as dependencies in FastAPI.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/tutorial/dependencies/classes-as-dependencies.md

LANGUAGE: Python
CODE:
```
class Cat:
    def __init__(self, name: str):
        self.name = name


fluffy = Cat(name="Mr Fluffy")
```

--------------------------------

TITLE: Install a different version of a Python package globally
DESCRIPTION: Illustrates the conflict that arises when attempting to install a different version of an already installed package (e.g., 'harry' version 3) in the global Python environment. This often leads to the uninstallation of the previous version, breaking other projects.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/virtual-environments.md

LANGUAGE: console
CODE:
```
pip install "harry==3"
```

--------------------------------

TITLE: Separate Pydantic Settings into a config.py Module
DESCRIPTION: For better project structure and maintainability, this example shows how to define your Pydantic `BaseSettings` class in a dedicated `config.py` file. This modular approach keeps configuration logic separate from your main application code.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/em/docs/advanced/settings.md

LANGUAGE: python
CODE:
```
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Awesome API"
    admin_email: str
    items_per_user: int = Field(50, gt=0, lt=1000)
```

--------------------------------

TITLE: Run FastAPI Application with Uvicorn
DESCRIPTION: This command starts the Uvicorn server, serving the FastAPI application defined in `main.py` as `app`. It binds the server to all available network interfaces (`0.0.0.0`) on port `80`. The Python snippet clarifies how `main:app` refers to the module and application object.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/deployment/manually.md

LANGUAGE: Shell
CODE:
```
$ uvicorn main:app --host 0.0.0.0 --port 80
```

LANGUAGE: Python
CODE:
```
from main import app
```

--------------------------------

TITLE: Define Application Lifespan with Async Context Manager
DESCRIPTION: This Python code snippet demonstrates the recommended method for managing application lifespan events in FastAPI using an `asynccontextmanager`. It illustrates how to initialize resources (e.g., an ML model) during application startup and clean them up during shutdown, replacing the legacy `startup` and `shutdown` event handlers. The example sets up a fake ML model and exposes an endpoint to use it, ensuring resources are properly managed across the application's lifecycle.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/release-notes.md

LANGUAGE: python
CODE:
```
from contextlib import asynccontextmanager

from fastapi import FastAPI


def fake_answer_to_everything_ml_model(x: float):
    return x * 42


ml_models = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    ml_models["answer_to_everything"] = fake_answer_to_everything_ml_model
    yield
    # Clean up the ML models and release the resources
    ml_models.clear()


app = FastAPI(lifespan=lifespan)


@app.get("/predict")
async def predict(x: float):
    result = ml_models["answer_to_everything"](x)
    return {"result": result}
```

--------------------------------

TITLE: Test FastAPI lifespan events with TestClient
DESCRIPTION: This example demonstrates how to properly test FastAPI applications that use `lifespan` events. It shows the use of `TestClient` within a `with` statement to ensure the lifespan events (startup and shutdown) are correctly triggered and managed during tests, reflecting the recommended approach for modern FastAPI applications.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/advanced/testing-events.md

LANGUAGE: Python
CODE:
```
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI() # Line 9

@app.on_event("startup") # Line 10
async def startup_event(): # Line 11
    print("Application startup") # Line 12
    # Some setup logic # Line 13

@app.on_event("shutdown") # Line 14
async def shutdown_event(): # Line 15
    print("Application shutdown")
    # Some cleanup logic

@app.get("/") # Line 18
async def read_root():
    return {"message": "Hello World"}

def test_read_main():
    with TestClient(app) as client: # Line 27
        response = client.get("/") # Line 28
        assert response.status_code == 200 # Line 30
        assert response.json() == {"message": "Hello World"} # Line 31
        # More assertions # Line 32

# Some other code # Line 41
# More code # Line 42
# End of file # Line 43
```

--------------------------------

TITLE: Example of Importing FastAPI Application in Another Script (Python)
DESCRIPTION: This Python example shows a typical `importer.py` file that imports the `app` instance from `myapp.py`. This scenario is used to illustrate that when `myapp.py` is imported, its `__name__` variable will not be `"__main__"`, ensuring that the `uvicorn.run()` block within `myapp.py` does not execute automatically.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/tutorial/debugging.md

LANGUAGE: python
CODE:
```
from myapp import app

# Some more code
```

--------------------------------

TITLE: Updated PATH After Python Install on Windows
DESCRIPTION: Shows how a Python installer might modify the `PATH` environment variable on Windows by appending a new directory, allowing the system to find the newly installed Python executable.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/environment-variables.md

LANGUAGE: plaintext
CODE:
```
C:\Program Files\Python312\Scripts;C:\Program Files\Python312;C:\Windows\System32;C:\opt\custompython\bin
```

--------------------------------

TITLE: Define FastAPI Application Startup Command in Dockerfile
DESCRIPTION: This Dockerfile CMD instruction sets the entrypoint for running the FastAPI application using `fastapi run` with Uvicorn. It's crucial to use the exec form (list of strings) to ensure graceful shutdowns and proper triggering of lifespan events, which are essential for production deployments. This command executes from the working directory, typically `/code`.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/deployment/docker.md

LANGUAGE: Dockerfile
CODE:
```
CMD ["fastapi", "run", "app/main.py", "--port", "80"]
```

--------------------------------

TITLE: FastAPI: Define Global Dependencies During App Initialization
DESCRIPTION: This Python example demonstrates how to apply application-wide dependencies by passing a list of `Depends` objects to the `dependencies` parameter when initializing the `FastAPI` application. This ensures that a specified dependency, like `some_dependency`, is executed for all path operations within the application.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/release-notes.md

LANGUAGE: python
CODE:
```
from fastapi import FastAPI, Depends


async def some_dependency():
    return


app = FastAPI(dependencies=[Depends(some_dependency)])
```

--------------------------------

TITLE: Run FastAPI Tests with Coverage Report
DESCRIPTION: Runs all unit and integration tests for the FastAPI project and generates an HTML coverage report. The report allows developers to interactively explore code coverage and identify untested sections.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/contributing.md

LANGUAGE: shell
CODE:
```
bash scripts/test-cov-html.sh
```

--------------------------------

TITLE: Updated PATH After Python Install on Linux/macOS
DESCRIPTION: Shows how a Python installer might modify the `PATH` environment variable on Linux/macOS by appending a new directory, allowing the system to find the newly installed Python executable.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/environment-variables.md

LANGUAGE: plaintext
CODE:
```
/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/custompython/bin
```

--------------------------------

TITLE: Implement Custom Validation for FastAPI Path Parameters with Pydantic AfterValidator
DESCRIPTION: This example demonstrates applying custom validation logic to FastAPI path parameters using Pydantic's `AfterValidator` within `Annotated`. It defines a validator function to ensure an item ID starts with 'isbn-' or 'imdb-', providing a flexible mechanism for enforcing specific data formats beyond standard type validations in your API.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/tutorial/query-params-str-validations.md

LANGUAGE: python
CODE:
```
from typing import Annotated
from fastapi import FastAPI
from pydantic import AfterValidator

app = FastAPI()

def validate_item_id(value: str):
    # This function checks if the item ID starts with "isbn-" or "imdb-"
    if not value.startswith(("isbn-", "imdb-")):
        raise ValueError("Item ID must start with 'isbn-' or 'imdb-'")
    return value

# Define a type alias using Annotated and AfterValidator
ValidatedItemId = Annotated[str, AfterValidator(validate_item_id)]

@app.get("/items/{item_id}")
async def read_item(item_id: ValidatedItemId):
    return {"item_id": item_id}
```

--------------------------------

TITLE: Run FastAPI Development Server
DESCRIPTION: This command initiates the FastAPI development server, typically using Uvicorn, to run the application specified by 'main.py'. It's used for local development and testing, providing real-time feedback on code changes.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/tutorial/sql-databases.md

LANGUAGE: console
CODE:
```
fastapi dev main.py
<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

--------------------------------

TITLE: Combine Request Body and Path Parameters in FastAPI
DESCRIPTION: This example illustrates how to declare both path parameters and a request body (defined by a Pydantic model) simultaneously in a FastAPI endpoint. FastAPI intelligently distinguishes and extracts data from the correct sources based on parameter types.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/tutorial/body.md

LANGUAGE: Python
CODE:
```
Code from file: ../../docs_src/body/tutorial003_py310.py hl[15:16]
```

--------------------------------

TITLE: Format FastAPI Project Code
DESCRIPTION: Executes a shell script to automatically format the FastAPI project's codebase. This script ensures consistent code style and auto-sorts imports across the project.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/contributing.md

LANGUAGE: shell
CODE:
```
bash scripts/format.sh
```

--------------------------------

TITLE: Import BaseSettings from pydantic-settings
DESCRIPTION: To utilize Pydantic's settings management functionality in FastAPI applications, import `BaseSettings` from the `pydantic_settings` package. This package is now an additional optional dependency, included when installing `fastapi[all]`.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/release-notes.md

LANGUAGE: python
CODE:
```
from pydantic_settings import BaseSettings
```

--------------------------------

TITLE: View Raw OpenAPI JSON Schema for FastAPI Application
DESCRIPTION: FastAPI automatically generates an OpenAPI schema for your API, providing a machine-readable description of all endpoints, data models, and operations. This snippet shows an example of the initial structure of the `openapi.json` file, which can be accessed directly from your running FastAPI application.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/tutorial/first-steps.md

LANGUAGE: JSON
CODE:
```
{
    "openapi": "3.1.0",
    "info": {
        "title": "FastAPI",
        "version": "0.1.0"
    },
    "paths": {
        "/items/": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {



...

```

--------------------------------

TITLE: Set Custom HTTP Status Code in FastAPI Endpoint
DESCRIPTION: Illustrates how to apply a specific HTTP status code to a FastAPI GET endpoint using `status.HTTP_418_IM_A_TEAPOT`. This example defines a simple API route `/items/` that returns a list of items with the specified custom status code.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/reference/status.md

LANGUAGE: python
CODE:
```
from fastapi import FastAPI, status

app = FastAPI()


@app.get("/items/", status_code=status.HTTP_418_IM_A_TEAPOT)
def read_items():
    return [{"name": "Plumbus"}, {"name": "Portal Gun"}]
```

--------------------------------

TITLE: FastAPI Application File for Separated Tests
DESCRIPTION: This snippet shows a simple FastAPI application defined in a 'main.py' file. This setup is typical when organizing a larger application where the FastAPI instance is imported and tested from a separate test file.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/tutorial/testing.md

LANGUAGE: python
CODE:
```
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_main():
    return {"msg": "Hello World"}
```

--------------------------------

TITLE: Example of an Actual Callback HTTP Request
DESCRIPTION: This code snippet illustrates a simple example of how an actual HTTP callback request might be implemented within your application. It shows sending a POST request to a `callback_url` with a JSON payload, typically after an event (like an invoice being paid) occurs. This is the operational part of a callback, distinct from its documentation.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/advanced/openapi-callbacks.md

LANGUAGE: Python
CODE:
```
callback_url = "https://example.com/api/v1/invoices/events/"
httpx.post(callback_url, json={"description": "Invoice paid", "paid": True})
```

--------------------------------

TITLE: GET /heroes
DESCRIPTION: Retrieves a list of heroes from the database. Supports pagination using optional `limit` and `offset` query parameters.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/tutorial/sql-databases.md

LANGUAGE: APIDOC
CODE:
```
## GET /heroes

### Description
Retrieves a list of heroes from the database. Results can be paginated to control the number of returned items and their starting point.

### Method
GET

### Endpoint
/heroes

### Parameters
#### Path Parameters
(None)

#### Query Parameters
- **offset** (integer) - Optional - Default: 0 - The number of hero entries to skip from the beginning of the result set.
- **limit** (integer) - Optional - Default: 100 - The maximum number of hero entries to return.

#### Request Body
(None)

### Request Example
(None)

### Response
#### Success Response (200)
An array of hero objects, each with the following structure:
- **id** (integer) - The unique identifier of the hero.
- **name** (string) - The hero's name.
- **secret_name** (string) - The hero's secret identity name.
- **age** (integer) - The hero's age.

#### Response Example
```json
[
  {
    "id": 1,
    "name": "Deadpond",
    "secret_name": "Dive Wilson",
    "age": 30
  },
  {
    "id": 2,
    "name": "Spider-Boy",
    "secret_name": "Pedro Parqueador",
    "age": null
  }
]
```
```

--------------------------------

TITLE: Navigate to Language Documentation Directory (Console)
DESCRIPTION: Change the current directory to the specific language's documentation folder within the project structure (e.g., 'docs/es/'). This is a preparatory step before manually running the documentation server for that particular language.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/contributing.md

LANGUAGE: console
CODE:
```
cd docs/es/
```

--------------------------------

TITLE: Build a Docker Image for a FastAPI Application
DESCRIPTION: This Dockerfile provides a standard way to containerize a FastAPI application. It uses a Python base image, sets up a working directory, copies and installs dependencies, then copies the application code, and defines the command to run the FastAPI server. An optional comment indicates how to add proxy headers if running behind a reverse proxy.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/deployment/docker.md

LANGUAGE: Dockerfile
CODE:
```
FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["fastapi", "run", "app/main.py", "--port", "80"]

# If running behind a proxy like Nginx or Traefik add --proxy-headers
# CMD ["fastapi", "run", "app/main.py", "--port", "80", "--proxy-headers"]
```

--------------------------------

TITLE: Run FastAPI application in development mode with auto-reload
DESCRIPTION: This command starts the FastAPI development server using `fastapi dev`. It automatically detects the FastAPI app in `main.py` and enables auto-reloading for local development, powered by Uvicorn. The output shows server details and watch directories.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/index.md

LANGUAGE: console
CODE:
```
$ fastapi dev main.py

 ╭────────── FastAPI CLI - Development mode ───────────╮
 │                                                     │
 │  Serving at: http://127.0.0.1:8000                  │
 │                                                     │
 │  API docs: http://127.0.0.1:8000/docs               │
 │                                                     │
 │  Running in development mode, for production use:   │
 │                                                     │
 │  fastapi run                                        │
 │                                                     │
 ╰─────────────────────────────────────────────────────╯

INFO:     Will watch for changes in these directories: ['/home/user/code/awesomeapp']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [2248755] using WatchFiles
INFO:     Started server process [2248757]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

--------------------------------

TITLE: Understand JavaScript-only Swagger UI Settings
DESCRIPTION: Explains that some Swagger UI configurations are JavaScript-only objects (like functions or presets) and cannot be passed directly from Python. It provides an example of a JavaScript `presets` configuration that would need to be handled separately.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/how-to/configure-swagger-ui.md

LANGUAGE: JavaScript
CODE:
```
presets: [
    SwaggerUIBundle.presets.apis,
    SwaggerUIBundle.SwaggerUIStandalonePreset
]
```

--------------------------------

TITLE: Importing the FastAPI Class
DESCRIPTION: This code snippet demonstrates the standard way to import the `FastAPI` class from the `fastapi` library. The `FastAPI` class is the main entry point for creating web applications and APIs, providing core functionalities like defining HTTP routes (e.g., `get`, `post`), managing middleware, handling events, and integrating with OpenAPI specifications.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/reference/fastapi.md

LANGUAGE: Python
CODE:
```
from fastapi import FastAPI
```

--------------------------------

TITLE: Testing File for Separated FastAPI Application
DESCRIPTION: This example demonstrates how to create a separate test file ('test_main.py') within the same Python package as the FastAPI application. It uses a relative import to access the 'app' object from 'main.py' and then proceeds with standard TestClient usage.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/tutorial/testing.md

LANGUAGE: python
CODE:
```
from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}
```

--------------------------------

TITLE: Create a basic FastAPI application with synchronous endpoints
DESCRIPTION: This snippet demonstrates how to define a simple FastAPI application with two GET endpoints: a root endpoint and an item endpoint with path and query parameters. It uses standard Python `def` for synchronous functions, suitable for CPU-bound operations.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/index.md

LANGUAGE: Python
CODE:
```
from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
```

--------------------------------

TITLE: Example JSON for a Nested FastAPI Model
DESCRIPTION: Provides a concrete JSON example demonstrating the expected structure of a request body when using nested Pydantic models in FastAPI. It shows how a submodel translates into a nested JSON object.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/tutorial/body-nested-models.md

LANGUAGE: json
CODE:
```
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2,
    "tags": ["rock", "metal", "bar"],
    "image": {
        "url": "http://example.com/baz.jpg",
        "name": "The Foo live"
    }
}
```

--------------------------------

TITLE: Illustrate Python Relative Import Syntax
DESCRIPTION: These examples clarify the different forms of relative imports in Python. They show how single (`.`), double (`..`), and triple (`...`) dots are used to navigate the package hierarchy to import modules or objects from sibling or parent directories.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/em/docs/tutorial/bigger-applications.md

LANGUAGE: Python
CODE:
```
from .dependencies import get_token_header
```

LANGUAGE: Python
CODE:
```
from ..dependencies import get_token_header
```

LANGUAGE: Python
CODE:
```
from ...dependencies import get_token_header
```

--------------------------------

TITLE: Example JSON Response with Enum Value
DESCRIPTION: This is an example of the JSON output received by a client when a FastAPI path operation returns an `Enum` member. It demonstrates that the enum member is serialized into its underlying string value in the final JSON response.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/tutorial/path-params.md

LANGUAGE: json
CODE:
```
{
  "model_name": "alexnet",
  "message": "Deep Learning FTW!"
}
```

--------------------------------

TITLE: Create Project Directory Structure
DESCRIPTION: Commands to set up a new project directory, typically under a 'code' directory in the user's home, preparing for a new Python project. This sequence navigates to the home directory, creates a 'code' directory, enters it, creates a project-specific directory, and then enters that project directory.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/virtual-environments.md

LANGUAGE: console
CODE:
```
$ cd
$ mkdir code
$ cd code
$ mkdir awesome-project
$ cd awesome-project
```

--------------------------------

TITLE: Run FastAPI Application with Uvicorn and Root Path
DESCRIPTION: This command starts the Uvicorn server for the FastAPI application. The `--root-path /api/v1` argument is crucial for informing FastAPI that it will be served behind a proxy at this specific sub-path, ensuring correct URL generation and routing.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/em/docs/advanced/behind-a-proxy.md

LANGUAGE: console
CODE:
```
uvicorn main:app --root-path /api/v1

INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

--------------------------------

TITLE: Run FastAPI with Gunicorn and Uvicorn Workers
DESCRIPTION: Executes the FastAPI application using Gunicorn, configured to use Uvicorn workers. This command specifies the application entry point (`main:app`), the number of workers (`--workers 4`), the worker class (`uvicorn.workers.UvicornWorker`), and the binding address and port (`--bind 0.0.0.0:80`). The output demonstrates Gunicorn starting and managing multiple Uvicorn worker processes.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/em/docs/deployment/server-workers.md

LANGUAGE: console
CODE:
```
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:80

[19499] [INFO] Starting gunicorn 20.1.0
[19499] [INFO] Listening at: http://0.0.0.0:80 (19499)
[19499] [INFO] Using worker: uvicorn.workers.UvicornWorker
[19511] [INFO] Booting worker with pid: 19511
[19513] [INFO] Booting worker with pid: 19513
[19514] [INFO] Booting worker with pid: 19514
[19515] [INFO] Booting worker with pid: 19515
[19511] [INFO] Started server process [19511]
[19511] [INFO] Waiting for application startup.
[19511] [INFO] Application startup complete.
[19513] [INFO] Started server process [19513]
[19513] [INFO] Waiting for application startup.
[19513] [INFO] Application startup complete.
[19514] [INFO] Started server process [19514]
[19514] [INFO] Waiting for application startup.
[19514] [INFO] Application startup complete.
[19515] [INFO] Started server process [19515]
[19515] [INFO] Waiting for application startup.
[19515] [INFO] Application startup complete.
```

--------------------------------

TITLE: Example JSON Request Body for Item Model
DESCRIPTION: Illustrates the structure of a JSON request body that fully conforms to the `Item` Pydantic model, showing both required and optional fields with values.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/em/docs/tutorial/body.md

LANGUAGE: json
CODE:
```
{
    "name": "Foo",
    "description": "An optional description",
    "price": 45.2,
    "tax": 3.5
}
```

--------------------------------

TITLE: Run FastAPI Application with Uvicorn in Docker
DESCRIPTION: This Dockerfile `CMD` instruction starts the Uvicorn server to serve a FastAPI application. It specifies the main application entry point (`main:app`), binds to all network interfaces (`0.0.0.0`), and listens on port 80. This is a common way to run a FastAPI application within a Docker container.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/em/docs/deployment/docker.md

LANGUAGE: Dockerfile
CODE:
```
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
```

--------------------------------

TITLE: Provide Pydantic Settings as a FastAPI Dependency
DESCRIPTION: This example shows how to create a simple dependency function (`get_settings`) that returns an instance of your Pydantic `Settings` class. This pattern is crucial for integrating settings with FastAPI's dependency injection system, allowing settings to be easily provided to path operations and other dependencies.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/em/docs/advanced/settings.md

LANGUAGE: python
CODE:
```
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Awesome API"
    admin_email: str
    items_per_user: int = Field(50, gt=0, lt=1000)


def get_settings():
    return Settings()
```

--------------------------------

TITLE: Create and Use Environment Variables in Shell
DESCRIPTION: Demonstrates how to define and utilize environment variables directly within the terminal. Examples are provided for both Linux/macOS/Windows Bash and Windows PowerShell, showing how to set a variable and then access its value using `echo`.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/environment-variables.md

LANGUAGE: bash
CODE:
```
export MY_NAME="Wade Wilson"

echo "Hello $MY_NAME"
```

LANGUAGE: powershell
CODE:
```
$Env:MY_NAME = "Wade Wilson"

echo "Hello $Env:MY_NAME"
```

--------------------------------

TITLE: FastAPI Application Directory Structure with Explanations
DESCRIPTION: Provides a detailed breakdown of a FastAPI project's file structure, explaining the role of `__init__.py` files in defining Python packages and subpackages, and how modules within them are referenced.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/em/docs/tutorial/bigger-applications.md

LANGUAGE: text
CODE:
```
.├── app                  # "app" is a Python package│   ├── __init__.py      # this file makes "app" a "Python package"│   ├── main.py          # "main" module, e.g. import app.main│   ├── dependencies.py  # "dependencies" module, e.g. import app.dependencies│   └── routers          # "routers" is a "Python subpackage"│   │   ├── __init__.py  # makes "routers" a "Python subpackage"│   │   ├── items.py     # "items" submodule, e.g. import app.routers.items│   │   └── users.py     # "users" submodule, e.g. import app.routers.users│   └── internal         # "internal" is a "Python subpackage"│       ├── __init__.py  # makes "internal" a "Python subpackage"│       └── admin.py     # "admin" submodule, e.g. import app.internal.admin
```

--------------------------------

TITLE: Run FastAPI Application and Access API Docs
DESCRIPTION: Provides console commands to run the FastAPI application using `fastapi dev` and instructions to access the automatically generated interactive API documentation (Swagger UI) at the `/docs` endpoint.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/tutorial/bigger-applications.md

LANGUAGE: Console
CODE:
```
$ fastapi dev app/main.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

--------------------------------

TITLE: Run Python Program within Virtual Environment
DESCRIPTION: After activating your virtual environment, use this command to execute your Python program. Running your script this way ensures that it utilizes the Python interpreter and packages installed within your isolated virtual environment, preventing conflicts with system-wide installations.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/virtual-environments.md

LANGUAGE: console
CODE:
```
$ python main.py
```

--------------------------------

TITLE: Source Path for English Documentation Page
DESCRIPTION: Specifies the file path of an English documentation page (e.g., 'features.md') within the 'docs/en/docs/' directory. This path indicates the source file that should be copied and subsequently translated into another language.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/contributing.md

LANGUAGE: text
CODE:
```
docs/en/docs/features.md
```

--------------------------------

TITLE: Example JSON Data with Values Matching Defaults
DESCRIPTION: Shows a JSON data structure where some fields have values identical to their defaults. FastAPI (via Pydantic) intelligently includes these fields in the response because they were explicitly set, rather than being derived from defaults.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/tutorial/response-model.md

LANGUAGE: JSON
CODE:
```
{
    "name": "Baz",
    "description": null,
    "price": 50.2,
    "tax": 10.5,
    "tags": []
}
```

--------------------------------

TITLE: Handle Exceptions in FastAPI Dependencies with Yield (Python)
DESCRIPTION: This Python code illustrates how to manage exceptions within `async` dependencies that use `yield` in FastAPI. The first example shows catching `HTTPException` to perform a session rollback before re-raising. The second example demonstrates using a `try...finally` block to ensure cleanup operations run irrespective of exceptions occurring after `yield`, highlighting the `finally` block's guarantee.

SOURCE: https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/release-notes.md

LANGUAGE: Python
CODE:
```
async def get_database():
    with Session() as session:
        try:
            yield session
        except HTTPException:
            session.rollback()
            raise
        finally:
            session.close()
```

LANGUAGE: Python
CODE:
```
async def do_something():
    try:
        yield something
    finally:
        some_cleanup()
```