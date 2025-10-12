================
CODE SNIPPETS
================
TITLE: Install Pydantic directly from GitHub repository using pip or uv
DESCRIPTION: These commands allow you to install Pydantic directly from its GitHub repository, useful for development, contributing, or accessing the latest unreleased versions. You can also specify optional dependencies using the 'egg' syntax for a complete setup.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/install.md

LANGUAGE: bash
CODE:
```
pip install 'git+https://github.com/pydantic/pydantic@main'
# or with `email` and `timezone` extras:
pip install 'git+https://github.com/pydantic/pydantic@main#egg=pydantic[email,timezone]'
```

LANGUAGE: bash
CODE:
```
uv add 'git+https://github.com/pydantic/pydantic@main'
# or with `email` and `timezone` extras:
uv add 'git+https://github.com/pydantic/pydantic@main#egg=pydantic[email,timezone]'
```

--------------------------------

TITLE: Install Pydantic core library using pip, uv, or conda
DESCRIPTION: These commands demonstrate how to install the Pydantic library using common Python package managers. Choose the command corresponding to your preferred package manager to get started with Pydantic's core features.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/install.md

LANGUAGE: bash
CODE:
```
pip install pydantic
```

LANGUAGE: bash
CODE:
```
uv add pydantic
```

LANGUAGE: bash
CODE:
```
conda install pydantic -c conda-forge
```

--------------------------------

TITLE: Install Pydantic with optional dependencies using pip or uv
DESCRIPTION: These commands show how to install Pydantic along with specific optional dependencies like 'email' for validation or 'timezone' for IANA time zone data. Use the bracket notation to include multiple extras, enhancing Pydantic's capabilities for specific use cases.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/install.md

LANGUAGE: bash
CODE:
```
pip install 'pydantic[email]'
# or with `email` and `timezone` extras:
pip install 'pydantic[email,timezone]'
```

LANGUAGE: bash
CODE:
```
uv add 'pydantic[email]'
# or with `email` and `timezone` extras:
uv add 'pydantic[email,timezone]'
```

--------------------------------

TITLE: Testing and Updating Pydantic Documentation Code Examples (Bash)
DESCRIPTION: Provides a Bash command to run tests specifically for documentation code examples and update their formatting and output. This ensures all examples within the documentation are correct and complete before deployment.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/contributing.md

LANGUAGE: bash
CODE:
```
# Run tests and update code examples
pytest tests/test_docs.py --update-examples
```

--------------------------------

TITLE: Clone Pydantic Fork and Install Development Tools (Bash)
DESCRIPTION: This sequence of commands clones a forked Pydantic repository, navigates into its directory, and then installs essential development tools like `uv` and `pre-commit` using `pipx`. These tools are necessary for managing dependencies and ensuring code quality during contribution.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/contributing.md

LANGUAGE: bash
CODE:
```
git clone git@github.com:<your username>/pydantic.git
cd pydantic

pipx install uv
pipx install pre-commit

make install
```

--------------------------------

TITLE: Install Pydantic V2 Migration Tool
DESCRIPTION: Installs the `bump-pydantic` tool from PyPI. This beta tool assists in migrating Pydantic V1 codebases to V2 by automating common changes.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/migration.md

LANGUAGE: bash
CODE:
```
pip install bump-pydantic
```

--------------------------------

TITLE: Install Pydantic V1
DESCRIPTION: Installs the latest version of Pydantic V1 from PyPI. Use this command if you specifically need to maintain a Pydantic V1 environment.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/migration.md

LANGUAGE: bash
CODE:
```
pip install "pydantic==1.*"
```

--------------------------------

TITLE: Install Pydantic V2
DESCRIPTION: Installs the latest stable version of Pydantic, which is V2, from PyPI. Use this command to upgrade or install Pydantic for new projects.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/migration.md

LANGUAGE: bash
CODE:
```
pip install -U pydantic
```

--------------------------------

TITLE: Install datamodel-code-generator library
DESCRIPTION: This command installs the `datamodel-code-generator` library using Python's package installer, `pip`. It ensures that the utility is available in your Python environment for generating Pydantic models.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/integrations/datamodel_code_generator.md

LANGUAGE: bash
CODE:
```
pip install datamodel-code-generator
```

--------------------------------

TITLE: Build Pydantic Documentation Locally (Bash)
DESCRIPTION: This command builds the project's documentation using `mkdocs-material`. Contributors should run this after making changes to documentation files or docstrings to ensure everything renders correctly and without errors.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/contributing.md

LANGUAGE: bash
CODE:
```
make docs
```

--------------------------------

TITLE: Configure Pydantic Mypy Plugins
DESCRIPTION: Provides examples for configuring Pydantic's Mypy plugins, including the optional V1 plugin, in both `mypy.ini` and `pyproject.toml` files. This ensures proper type checking for Pydantic models.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/migration.md

LANGUAGE: ini
CODE:
```
[mypy]
plugins = pydantic.mypy, pydantic.v1.mypy  # include `.v1.mypy` if required.
```

LANGUAGE: toml
CODE:
```
[tool.mypy]
plugins = [
    "pydantic.mypy",
    "pydantic.v1.mypy",  # include `.v1.mypy` if required.
]
```

--------------------------------

TITLE: Get Pydantic v1 Version Information (Bash)
DESCRIPTION: This command executes a Python script to print the version details of Pydantic. It is intended for Pydantic versions prior to 2.0 and should be included in bug reports and feature requests for context.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/contributing.md

LANGUAGE: bash
CODE:
```
python -c "import pydantic.utils; print(pydantic.utils.version_info())"
```

--------------------------------

TITLE: Install Pydantic with Pip for AWS Lambda Compatibility
DESCRIPTION: This `pip install` command ensures `pydantic` is installed correctly for an AWS Lambda environment. It specifies the target platform, Python version, and forces binary installations to prevent compatibility issues when deploying dependencies to Lambda.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/integrations/aws_lambda.md

LANGUAGE: bash
CODE:
```
pip install \
    --platform manylinux2014_x86_64 \
    --target=<your_package_dir> \
    --implementation cp \
    --python-version 3.10 \
    --only-binary=:all: \
    --upgrade pydantic
```

--------------------------------

TITLE: Get Pydantic v2 Version Information (Bash)
DESCRIPTION: This command executes a Python script to print the version details of Pydantic. It is specifically for Pydantic versions 2.0 and later, and should be included in bug reports and feature requests to provide context.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/contributing.md

LANGUAGE: bash
CODE:
```
python -c "import pydantic.version; print(pydantic.version.version_info())"
```

--------------------------------

TITLE: Customize Pydantic JSON Schema with Dictionary via json_schema_extra
DESCRIPTION: This example demonstrates how to use `json_schema_extra` with a dictionary to add static, extra information to the JSON schema generated for a Pydantic model. It shows how to include an 'examples' array within the schema, which is useful for documentation or client-side generation. The output displays the modified JSON schema with the added 'examples' property.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/json_schema.md

LANGUAGE: python
CODE:
```
import json

from pydantic import BaseModel, ConfigDict


class Model(BaseModel):
    a: str

    model_config = ConfigDict(json_schema_extra={'examples': [{'a': 'Foo'}]})


print(json.dumps(Model.model_json_schema(), indent=2))
```

--------------------------------

TITLE: Configure Pydantic `TypeAdapter` with `config` argument (Python)
DESCRIPTION: This code demonstrates how to apply configuration to a Pydantic `TypeAdapter` by passing a `ConfigDict` to its constructor. The example uses `coerce_numbers_to_str=True` to automatically convert numbers in a list to strings during validation.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/config.md

LANGUAGE: python
CODE:
```
from pydantic import ConfigDict, TypeAdapter

ta = TypeAdapter(list[str], config=ConfigDict(coerce_numbers_to_str=True))

print(ta.validate_python([1, 2]))
#> ['1', '2']
```

--------------------------------

TITLE: Documenting Pydantic Function Parameters and Returns with Google-style Docstrings (Python)
DESCRIPTION: Demonstrates how to document function parameters and return values using Google-style docstrings in Pydantic. It utilizes 'Args' for parameters and explicitly describes the return value, with types inferred from the function signature.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/contributing.md

LANGUAGE: python
CODE:
```
def bar(self, baz: int) -> str:
    """A function docstring.

    Args:
        baz: A description of `baz`.

    Returns:
        A description of the return value.
    """

    return 'bar'
```

--------------------------------

TITLE: Run Pydantic Tests and Linting Locally (Bash)
DESCRIPTION: This set of `make` commands automates code formatting, linting (using Ruff), and runs all tests to ensure code quality and functionality. It's crucial for contributors to run these checks before submitting a pull request to catch issues early.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/contributing.md

LANGUAGE: bash
CODE:
```
make format

make
```

--------------------------------

TITLE: Handle Incomplete JSON Lists with Pydantic Core
DESCRIPTION: This example demonstrates parsing an incomplete JSON list using `pydantic_core.from_json`. It shows how `allow_partial=False` (default) raises an error, while `allow_partial=True` successfully deserializes the available complete elements.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/json.md

LANGUAGE: python
CODE:
```
from pydantic_core import from_json

partial_json_data = '["aa", "bb", "c'  # (1)!

try:
    result = from_json(partial_json_data, allow_partial=False)
except ValueError as e:
    print(e)  # (2)!
    # > EOF while parsing a string at line 1 column 15

result = from_json(partial_json_data, allow_partial=True)
print(result)  # (3)!
# > ['aa', 'bb']
```

--------------------------------

TITLE: Sample JSON data for Pydantic validation
DESCRIPTION: This JSON object represents a single person's data, used as an example for validation with a Pydantic model.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/examples/files.md

LANGUAGE: json
CODE:
```json
{
    "name": "John Doe",
    "age": 30,
    "email": "john@example.com"
}
```

--------------------------------

TITLE: Pydantic Validation Error List Example (Python)
DESCRIPTION: This Python code snippet provides a list of dictionaries, each demonstrating a distinct Pydantic validation error structure. It includes examples for missing fields, value constraints (greater_than), type parsing failures (int_parsing, float_parsing), and generic value errors, illustrating how Pydantic categorizes and describes validation issues.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/errors/errors.md

LANGUAGE: python
CODE:
```python
            'url': 'https://errors.pydantic.dev/2/v/missing',
        },
        {
            'type': 'greater_than',
            'loc': ('gt_int',),
            'msg': 'Input should be greater than 42',
            'input': 21,
            'ctx': {'gt': 42},
            'url': 'https://errors.pydantic.dev/2/v/greater_than',
        },
        {
            'type': 'int_parsing',
            'loc': ('list_of_ints', 2),
            'msg': 'Input should be a valid integer, unable to parse string as an integer',
            'input': 'bad',
            'url': 'https://errors.pydantic.dev/2/v/int_parsing',
        },
        {
            'type': 'value_error',
            'loc': ('a_float',),
            'msg': 'Value error, Invalid float value',
            'input': 3.0,
            'ctx': {'error': ValueError('Invalid float value')},
            'url': 'https://errors.pydantic.dev/2/v/value_error',
        },
        {
            'type': 'float_parsing',
            'loc': ('recursive_model', 'lng'),
            'msg': 'Input should be a valid number, unable to parse string as a number',
            'input': 'New York',
            'url': 'https://errors.pydantic.dev/2/v/float_parsing',
        }
    ]
```

--------------------------------

TITLE: Create Pydantic Models Dynamically and Statically with Advanced Fields
DESCRIPTION: This example demonstrates creating a Pydantic model dynamically using `create_model` and its static class-based equivalent. It highlights advanced field definitions, including aliases with `Field`, descriptions with `Annotated`, and private attributes with `PrivateAttr`.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/models.md

LANGUAGE: python
CODE:
```python
from typing import Annotated

from pydantic import BaseModel, Field, PrivateAttr, create_model

DynamicModel = create_model(
    'DynamicModel',
    foo=(str, Field(alias='FOO')),
    bar=Annotated[str, Field(description='Bar field')],
    _private=(int, PrivateAttr(default=1)),
)


class StaticModel(BaseModel):
    foo: str = Field(alias='FOO')
    bar: Annotated[str, Field(description='Bar field')]
    _private: int = PrivateAttr(default=1)
```

--------------------------------

TITLE: Initialize Pydantic TypeAdapter with Deferred Schema Building
DESCRIPTION: This example shows how to initialize a `TypeAdapter` with `defer_build=True` in `ConfigDict` to postpone the creation of the core schema until it is first needed. This feature is beneficial for performance optimization, especially with complex types or forward references, as it avoids immediate schema analysis overhead.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/type_adapter.md

LANGUAGE: python
CODE:
```python
from pydantic import ConfigDict, TypeAdapter

ta = TypeAdapter('MyInt', config=ConfigDict(defer_build=True))
```

--------------------------------

TITLE: Configure `TypedDict` with `with_config` decorator (Python)
DESCRIPTION: This example uses the `with_config` decorator to apply Pydantic configuration to a `TypedDict`. This method helps avoid static type checking errors while setting configurations like `str_to_lower=True`.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/config.md

LANGUAGE: python
CODE:
```python
from typing_extensions import TypedDict

from pydantic import ConfigDict, with_config


@with_config(ConfigDict(str_to_lower=True))
class Model(TypedDict):
    x: str
```

--------------------------------

TITLE: Configure Pydantic Model with `model_config` attribute (Python)
DESCRIPTION: This example demonstrates how to set configuration for a Pydantic `BaseModel` using the `model_config` class attribute. It uses `str_max_length` to enforce a maximum string length, showcasing validation error handling.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/config.md

LANGUAGE: python
CODE:
```python
from pydantic import BaseModel, ConfigDict, ValidationError


class Model(BaseModel):
    model_config = ConfigDict(str_max_length=5)  # (1)!

    v: str


try:
    m = Model(v='abcdef')
except ValidationError as e:
    print(e)
    # """
    # 1 validation error for Model
    # v
    #   String should have at most 5 characters [type=string_too_long, input_value='abcdef', input_type=str]
    # """
```

--------------------------------

TITLE: Documenting Pydantic Class Attributes with Google-style Docstrings (Python)
DESCRIPTION: Illustrates how to document class attributes using Google-style docstrings in Pydantic, following PEP 257 guidelines. It shows the 'Attributes' section for documenting class variables with descriptions and default values.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/contributing.md

LANGUAGE: python
CODE:
```python
class Foo:
    """A class docstring.

    Attributes:
        bar: A description of bar. Defaults to "bar".
    """

    bar: str = 'bar'
```

--------------------------------

TITLE: Configure Sphinx Intersphinx for Pydantic API Documentation
DESCRIPTION: This Python code snippet demonstrates how to configure the `intersphinx_mapping` in a Sphinx `conf.py` file. It enables cross-referencing to Pydantic's official API documentation by mapping 'pydantic' to its documentation URL, allowing easy linking to Pydantic objects within Sphinx projects.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/integrations/documentation.md

LANGUAGE: python
CODE:
```python
intersphinx_mapping = {
    'pydantic': ('https://docs.pydantic.dev/latest', None)  # (1)!
}
```

--------------------------------

TITLE: Enable Pydantic Mypy Plugin in Configuration Files
DESCRIPTION: These examples show how to enable the Pydantic Mypy plugin in different Mypy configuration file formats. Adding `pydantic.mypy` to the `plugins` list in either `mypy.ini` or `pyproject.toml` activates the plugin, allowing Mypy to perform advanced type-checking for Pydantic models.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/integrations/mypy.md

LANGUAGE: ini
CODE:
```ini
[mypy]
plugins = pydantic.mypy
```

LANGUAGE: toml
CODE:
```toml
[tool.mypy]
plugins = ['pydantic.mypy']
```

--------------------------------

TITLE: Validate Partial JSON into Pydantic Model
DESCRIPTION: This example combines `pydantic_core.from_json` with a Pydantic `BaseModel` for validation. It demonstrates how to parse an incomplete JSON string into a dictionary and then validate that dictionary against a `Dog` model, leveraging `allow_partial=True` to handle truncation.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/json.md

LANGUAGE: python
CODE:
```python
from pydantic_core import from_json

from pydantic import BaseModel


class Dog(BaseModel):
    breed: str
    name: str
    friends: list


partial_dog_json = '{"breed": "lab", "name": "fluffy", "friends": ["buddy", "spot", "rufus"], "age'

dog = Dog.model_validate(from_json(partial_dog_json, allow_partial=True))
print(repr(dog))
# > Dog(breed='lab', name='fluffy', friends=['buddy', 'spot', 'rufus'])
```

--------------------------------

TITLE: Merge Pydantic Configurations in Subclasses (Python)
DESCRIPTION: This example shows how Pydantic merges configurations when a subclass defines its own `model_config` while inheriting from a parent with existing configuration. Subclass settings override or combine with parent settings.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/config.md

LANGUAGE: python
CODE:
```python
from pydantic import BaseModel, ConfigDict


class Parent(BaseModel):
    model_config = ConfigDict(extra='allow', str_to_lower=False)


class Model(Parent):
    model_config = ConfigDict(str_to_lower=True)

    x: str


m = Model(x='FOO', y='bar')
print(m.model_dump())
# > {'x': 'foo', 'y': 'bar'}
print(Model.model_config)
# > {'extra': 'allow', 'str_to_lower': True}
```

--------------------------------

TITLE: Validate YAML Configuration with Pydantic in Python
DESCRIPTION: This example demonstrates parsing a YAML file using the `PyYAML` library (`yaml.safe_load`) and validating the loaded data with a Pydantic `BaseModel`. It processes 'person.yaml' into a `Person` model instance, providing robust validation for configuration settings.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/examples/files.md

LANGUAGE: yaml
CODE:
```yaml
name: John Doe
age: 30
email: john@example.com
```

LANGUAGE: python
CODE:
```python
import yaml

from pydantic import BaseModel, EmailStr, PositiveInt


class Person(BaseModel):
    name: str
    age: PositiveInt
    email: EmailStr


with open('person.yaml') as f:
    data = yaml.safe_load(f)

person = Person.model_validate(data)
print(person)

```

--------------------------------

TITLE: Map validate_as to Pydantic Validators (Before, After, Wrap)
DESCRIPTION: This example illustrates how the experimental `validate_as` pipeline API provides a type-safe alternative to Pydantic's `BeforeValidator`, `AfterValidator`, and `WrapValidator`. It demonstrates stripping whitespace before parsing, transforming a value after parsing, and combining pre-processing, validation, and post-processing steps within a single `Annotated` type.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/experimental.md

LANGUAGE: python
CODE:
```python
from typing import Annotated

from pydantic.experimental.pipeline import transform, validate_as

# BeforeValidator
Annotated[int, validate_as(str).str_strip().validate_as(...)]  # (1)!
# AfterValidator
Annotated[int, transform(lambda x: x * 2)]  # (2)!
# WrapValidator
Annotated[
    int,
    validate_as(str)
    .str_strip()
    .validate_as(...)
    .transform(lambda x: x * 2),  # (3)!
]
```

--------------------------------

TITLE: Display Pydantic Badges in Documentation
DESCRIPTION: These snippets provide various ways to display Pydantic version 1 and version 2 badges in your project's documentation, linking to the official Pydantic website. You can choose the format that best suits your documentation system, such as Markdown, reStructuredText, or HTML.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/contributing.md

LANGUAGE: md
CODE:
```markdown
[![Pydantic v1](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v1.json)](https://pydantic.dev)

[![Pydantic v2](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v2.json)](https://pydantic.dev)
```

LANGUAGE: rst
CODE:
```rst
.. image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v1.json
    :target: https://pydantic.dev
    :alt: Pydantic

.. image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v2.json
    :target: https://pydantic.dev
    :alt: Pydantic
```

LANGUAGE: html
CODE:
```html
<a href="https://pydantic.dev"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v1.json" alt="Pydantic Version 1" style="max-width:100%;"></a>

<a href="https://pydantic.dev"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v2.json" alt="Pydantic Version 2" style="max-width:100%;"></a>
```

--------------------------------

TITLE: Configure Pydantic Model with Keyword Arguments
DESCRIPTION: This example shows how to configure a Pydantic model by passing configuration options, such as `frozen=True`, directly as keyword arguments during the class definition. This approach allows Pylance to provide enhanced type checking and error detection for immutable models.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/integrations/visual_studio_code.md

LANGUAGE: python
CODE:
```python
from pydantic import BaseModel


class Knight(BaseModel, frozen=True):
    title: str
    age: int
    color: str = 'blue'
```

--------------------------------

TITLE: Apply `validate_call` to Class Constructors (Python)
DESCRIPTION: This example illustrates that `validate_call` cannot be directly applied to a class definition to validate its construction. Instead, to validate a class's constructor, `validate_call` must be applied individually to the `__init__` or `__new__` methods within the class, as shown in the 'correct' examples.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/errors/usage_errors.md

LANGUAGE: python
CODE:
```python
from pydantic import PydanticUserError, validate_call

# error
try:

    @validate_call
    class A1: ...

except PydanticUserError as exc_info:
    assert exc_info.code == 'validate-call-type'


# correct
class A2:
    @validate_call
    def __init__(self): ...

    @validate_call
    def __new__(cls): ...
```

--------------------------------

TITLE: Implement Custom Iteration and Item Access for Pydantic RootModel
DESCRIPTION: This example shows how to extend a `RootModel` by implementing Python's `__iter__` and `__getitem__` methods. This allows direct iteration and item access (like `pets[0]`) on the `RootModel` instance, providing a more intuitive interface for its underlying `root` data.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/models.md

LANGUAGE: python
CODE:
```python
from pydantic import RootModel


class Pets(RootModel):
    root: list[str]

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]


pets = Pets.model_validate(['dog', 'cat'])
print(pets[0])
# > dog
print([pet for pet in pets])
# > ['dog', 'cat']
```

--------------------------------

TITLE: Verify Pydantic-Core Compiled Library and Stubs (Python)
DESCRIPTION: This Python snippet helps debug the `no module named pydantic_core._pydantic_core` error by checking if the compiled library (e.g., .so or .pyd) and its type stubs (.pyi) are correctly installed within the `pydantic-core` package. It uses `importlib.metadata.files` to list package contents, which should ideally show two relevant files.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/integrations/aws_lambda.md

LANGUAGE: python
CODE:
```python
from importlib.metadata import files
print([file for file in files('pydantic-core') if file.name.startswith('_pydantic_core')])
```

--------------------------------

TITLE: Pydantic Data Validation with Redis Queue in Python
DESCRIPTION: This Python example demonstrates using Pydantic models to serialize data to JSON before pushing it to a Redis queue, and then deserialize and validate the data when it's retrieved. It requires the `redis` library and a running Redis server.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/examples/queues.md

LANGUAGE: python
CODE:
```python
import redis

from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: int
    name: str
    email: EmailStr


r = redis.Redis(host='localhost', port=6379, db=0)
QUEUE_NAME = 'user_queue'


def push_to_queue(user_data: User) -> None:
    serialized_data = user_data.model_dump_json()
    r.rpush(QUEUE_NAME, serialized_data)
    print(f'Added to queue: {serialized_data}')


user1 = User(id=1, name='John Doe', email='john@example.com')
user2 = User(id=2, name='Jane Doe', email='jane@example.com')

push_to_queue(user1)
# Added to queue: {"id":1,"name":"John Doe","email":"john@example.com"}

push_to_queue(user2)
# Added to queue: {"id":2,"name":"Jane Doe","email":"jane@example.com"}


def pop_from_queue() -> None:
    data = r.lpop(QUEUE_NAME)

    if data:
        user = User.model_validate_json(data)
        print(f'Validated user: {repr(user)}')
    else:
        print('Queue is empty')


pop_from_queue()
# Validated user: User(id=1, name='John Doe', email='john@example.com')

pop_from_queue()
# Validated user: User(id=2, name='Jane Doe', email='jane@example.com')

pop_from_queue()
# Queue is empty
```

--------------------------------

TITLE: Pydantic Model Signature with Custom __init__ (Python)
DESCRIPTION: This example shows that Pydantic's signature generation respects custom `__init__` methods defined within a `BaseModel`. The resulting signature accurately reflects the parameters of the custom constructor, merging them with model fields.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/models.md

LANGUAGE: python
CODE:
```python
import inspect

from pydantic import BaseModel


class MyModel(BaseModel):
    id: int
    info: str = 'Foo'

    def __init__(self, id: int = 1, *, bar: str, **data) -> None: 
        """My custom init!"""
        super().__init__(id=id, bar=bar, **data)


print(inspect.signature(MyModel))

```

--------------------------------

TITLE: Define and Use TypeVars in Pydantic Models
DESCRIPTION: This example demonstrates how Pydantic `BaseModel` supports `typing.TypeVar` in its fields. It shows unconstrained, bound, and constrained `TypeVar` declarations and how Pydantic handles type inference and validation when instantiating the model.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/api/standard_library_types.md

LANGUAGE: python
CODE:
```python
from typing import TypeVar

from pydantic import BaseModel

Foobar = TypeVar('Foobar')
BoundFloat = TypeVar('BoundFloat', bound=float)
IntStr = TypeVar('IntStr', int, str)


class Model(BaseModel):
    a: Foobar  # equivalent of ": Any"
    b: BoundFloat  # equivalent of ": float"
    c: IntStr  # equivalent of ": Union[int, str]"


print(Model(a=[1], b=4.2, c='x'))
# > a=[1] b=4.2 c='x'

# a may be None
print(Model(a=None, b=1, c=1))
# > a=None b=1.0 c=1
```

--------------------------------

TITLE: Correctly define Pydantic field validators
DESCRIPTION: This error occurs when a `@field_validator` is used without specifying any fields it should apply to. The first example shows the incorrect usage that triggers the `validator-no-fields` error, and the second example demonstrates the correct way to specify fields using string arguments.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/errors/usage_errors.md

LANGUAGE: python
CODE:
```python
from pydantic import BaseModel, PydanticUserError, field_validator

try:

    class Model(BaseModel):
        a: str

        @field_validator
        def checker(cls, v):
            return v

except PydanticUserError as exc_info:
    assert exc_info.code == 'validator-no-fields'
```

LANGUAGE: python
CODE:
```python
from pydantic import BaseModel, field_validator


class Model(BaseModel):
    a: str

    @field_validator('a')
    def checker(cls, v):
        return v
```

--------------------------------

TITLE: Validate INI Configuration with Pydantic in Python
DESCRIPTION: This example illustrates how to read an INI configuration file using Python's `configparser` and validate a specific section against a Pydantic `BaseModel`. It loads 'person.ini' and validates the 'PERSON' section, providing a robust way to handle INI-based configurations.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/examples/files.md

LANGUAGE: ini
CODE:
```ini
[PERSON]
name = John Doe
age = 30
email = john@example.com
```

LANGUAGE: python
CODE:
```python
import configparser

from pydantic import BaseModel, EmailStr, PositiveInt


class Person(BaseModel):
    name: str
    age: PositiveInt
    email: EmailStr


config = configparser.ConfigParser()
config.read('person.ini')
person = Person.model_validate(config['PERSON'])
print(person)

```

--------------------------------

TITLE: Define Pydantic Model with Dictionary Coercion Example
DESCRIPTION: This Python example demonstrates Pydantic's ability to automatically convert a dictionary into a nested `BaseModel` instance. Despite strict type checkers potentially flagging a `dict` for a `Knight` type as an error, Pydantic successfully coerces the input, showcasing its lenient data handling.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/integrations/visual_studio_code.md

LANGUAGE: python
CODE:
```python
from pydantic import BaseModel


class Knight(BaseModel):
    title: str
    age: int
    color: str = 'blue'


class Quest(BaseModel):
    title: str
    knight: Knight


quest = Quest(
    title='To seek the Holy Grail', knight={'title': 'Sir Lancelot', 'age': 23}
)
```

--------------------------------

TITLE: Sample JSON Lines data for Pydantic validation
DESCRIPTION: This example demonstrates data stored in JSON Lines format, where each line is a self-contained JSON object. This format is common for streaming or processing large datasets line by line.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/examples/files.md

LANGUAGE: json
CODE:
```json
{"name": "John Doe", "age": 30, "email": "john@example.com"}
{"name": "Jane Doe", "age": 25, "email": "jane@example.com"}
```

--------------------------------

TITLE: Create New Git Branch for Pydantic Contribution (Bash)
DESCRIPTION: This command creates a new Git branch, allowing contributors to isolate their changes from the main development line. It's a standard practice before implementing new features or bug fixes.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/contributing.md

LANGUAGE: bash
CODE:
```bash
git checkout -b my-new-feature-branch
```

--------------------------------

TITLE: Python Examples for Pydantic Partial Validation with TypeAdapter
DESCRIPTION: This comprehensive Python code illustrates various scenarios of Pydantic's experimental partial validation using `TypeAdapter`. It defines a `TypedDict` and applies `validate_json` and `validate_python` with `experimental_allow_partial` set to `True` or `'trailing-strings'`, showcasing how incomplete inputs are processed and validated according to the model's requirements.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/experimental.md

LANGUAGE: python
CODE:
```python
from typing import Annotated

from annotated_types import MinLen
from typing_extensions import NotRequired, TypedDict

from pydantic import TypeAdapter


class Foobar(TypedDict):  # (1)!
    a: int
    b: NotRequired[float]
    c: NotRequired[Annotated[str, MinLen(5)]]

ta = TypeAdapter(list[Foobar])

v = ta.validate_json('[{"a": 1, "b"', experimental_allow_partial=True)  # (2)!
print(v)
# > [{'a': 1}]

v = ta.validate_json(
    '[{"a": 1, "b": 1.0, "c": "abcd"', experimental_allow_partial=True  # (3)!
)
print(v)
# > [{'a': 1, 'b': 1.0}]

v = ta.validate_json(
    '[{"b": 1.0, "c": "abcde"', experimental_allow_partial=True  # (4)!
)
print(v)
# > []

v = ta.validate_json(
    '[{"a": 1, "b": 1.0, "c": "abcde"},{"a": ', experimental_allow_partial=True
)
print(v)
# > [{'a': 1, 'b': 1.0, 'c': 'abcde'}]

v = ta.validate_python([{'a': 1}], experimental_allow_partial=True)  # (5)!
print(v)
# > [{'a': 1}]

v = ta.validate_python(
    [{'a': 1, 'b': 1.0, 'c': 'abcd'}], experimental_allow_partial=True  # (6)!
)
print(v)
# > [{'a': 1, 'b': 1.0}]

v = ta.validate_json(
    '[{"a": 1, "b": 1.0, "c": "abcdefg"',
    experimental_allow_partial='trailing-strings',  # (7)!
)
print(v)
# > [{'a': 1, 'b': 1.0, 'c': 'abcdefg'}]
```

--------------------------------

TITLE: Pass multiple fields to Pydantic field validators
DESCRIPTION: This error is raised when a `@field_validator` is provided with non-string arguments, such as a list or tuple of field names. The first example demonstrates the incorrect usage that raises `validator-invalid-fields`, while the second example shows the correct method of passing multiple fields as separate string arguments.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/errors/usage_errors.md

LANGUAGE: python
CODE:
```python
from pydantic import BaseModel, PydanticUserError, field_validator

try:

    class Model(BaseModel):
        a: str
        b: str

        @field_validator(['a', 'b'])
        def check_fields(cls, v):
            return v

except PydanticUserError as exc_info:
    assert exc_info.code == 'validator-invalid-fields'
```

LANGUAGE: python
CODE:
```python
from pydantic import BaseModel, field_validator


class Model(BaseModel):
    a: str
    b: str

    @field_validator('a', 'b')
    def check_fields(cls, v):
        return v
```

--------------------------------

TITLE: Configure Pydantic Dataclass with `config` argument (Python)
DESCRIPTION: This example illustrates configuring a Pydantic dataclass using the `config` argument in the `@dataclass` decorator. It sets `str_max_length` and `validate_assignment` to ensure data integrity upon assignment, with error handling for validation failures.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/config.md

LANGUAGE: python
CODE:
```python
from pydantic import ConfigDict, ValidationError
from pydantic.dataclasses import dataclass


@dataclass(config=ConfigDict(str_max_length=10, validate_assignment=True))
class User:
    name: str


user = User(name='John Doe')
try:
    user.name = 'x' * 20
except ValidationError as e:
    print(e)
    # """
    # 1 validation error for User
    # name
    #   String should have at most 10 characters [type=string_too_long, input_value='xxxxxxxxxxxxxxxxxxxx', input_type=str]
    # """
```

--------------------------------

TITLE: Define and validate a Pydantic data model in Python
DESCRIPTION: This example demonstrates how to define a data model using `pydantic.BaseModel` and validate external data against it. It showcases type hints for basic types, optional fields, and lists, and how Pydantic automatically performs type coercion and validation when instantiating the model.

SOURCE: https://github.com/pydantic/pydantic/blob/main/README.md

LANGUAGE: python
CODE:
```python
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str = 'John Doe'
    signup_ts: Optional[datetime] = None
    friends: list[int] = []

external_data = {'id': '123', 'signup_ts': '2017-06-01 12:22', 'friends': [1, '2', b'3']}
user = User(**external_data)
print(user)
# > User id=123 name='John Doe' signup_ts=datetime.datetime(2017, 6, 1, 12, 22) friends=[1, 2, 3]
print(user.id)
# > 123
```

--------------------------------

TITLE: Resolve Unevaluable Type Annotation Clashes in Pydantic Python
DESCRIPTION: This section explains how a field name clashing with a type annotation name can cause evaluation issues. The first example shows a problematic case where 'date' as a field name conflicts with 'date' from `datetime`. The second example provides a workaround by importing the module or aliasing the type to avoid the name collision.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/errors/usage_errors.md

LANGUAGE: python
CODE:
```python
from datetime import date

from pydantic import BaseModel, Field


class Model(BaseModel):
    date: date = Field(description='A date')
```

LANGUAGE: python
CODE:
```python
import datetime
# Or `from datetime import date as _date`

from pydantic import BaseModel, Field


class Model(BaseModel):
    date: datetime.date = Field(description='A date')
```

--------------------------------

TITLE: Illustrate stdlib type configuration propagation with Pydantic in Python
DESCRIPTION: This example shows how configuration propagates to standard library types (like dataclasses) when used within a Pydantic model. The `str_to_lower=True` from `Parent` model's config applies to `UserWithoutConfig`, but `UserWithConfig` explicitly overrides this behavior using `@with_config(str_to_lower=False)`, preventing the propagation.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/config.md

LANGUAGE: python
CODE:
```python
from dataclasses import dataclass

from pydantic import BaseModel, ConfigDict, with_config


@dataclass
class UserWithoutConfig:
    name: str


@dataclass
@with_config(str_to_lower=False)
class UserWithConfig:
    name: str


class Parent(BaseModel):
    user_1: UserWithoutConfig
    user_2: UserWithConfig

    model_config = ConfigDict(str_to_lower=True)


print(Parent(user_1={'name': 'JOHN'}, user_2={'name': 'JOHN'}))
# > user_1=UserWithoutConfig(name='john') user_2=UserWithConfig(name='JOHN')
```

--------------------------------

TITLE: Pydantic `MISSING` Sentinel Usage in Python
DESCRIPTION: This Python example illustrates the use of the `MISSING` sentinel within a Pydantic `BaseModel`. It demonstrates how to define a field with `MISSING` as a default, how such fields are excluded from `model_dump()` output and JSON Schema, and how to discriminate `MISSING` from other values.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/experimental.md

LANGUAGE: python
CODE:
```python
from typing import Union

from pydantic import BaseModel
from pydantic.experimental.missing_sentinel import MISSING


class Configuration(BaseModel):
    timeout: Union[int, None, MISSING] = MISSING


# configuration defaults, stored somewhere else:
defaults = {'timeout': 200}

conf = Configuration()

# `timeout` is excluded from the serialization output:
conf.model_dump()
# {}

# The `MISSING` value doesn't appear in the JSON Schema:
Configuration.model_json_schema()['properties']['timeout']
# > {'anyOf': [{'type': 'integer'}, {'type': 'null'}], 'title': 'Timeout'}}


# `is` can be used to discrimate between the sentinel and other values:
timeout = conf.timeout if conf.timeout is not MISSING else defaults['timeout']
```

--------------------------------

TITLE: Prepare Pydantic Release with uv
DESCRIPTION: Runs the semi-automated release preparation script. This command updates the version number in `version.py`, updates the dependency lock file, and adds a new section to `HISTORY.md`. Use the `--dry-run` flag to preview changes without applying them.

SOURCE: https://github.com/pydantic/pydantic/blob/main/release/README.md

LANGUAGE: shell
CODE:
```shell
uv run release/prepare.py {VERSION}
```

--------------------------------

TITLE: Demonstrate Pydantic Data Conversion for Model Fields
DESCRIPTION: This example illustrates how Pydantic automatically casts input data to match the declared field types, potentially leading to data transformation. It defines a BaseModel with integer, float, and string fields, then shows how different input types (float for int, string for float, bytes for string) are converted upon model instantiation and then dumped.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/models.md

LANGUAGE: python
CODE:
```python
from pydantic import BaseModel


class Model(BaseModel):
    a: int
    b: float
    c: str


print(Model(a=3.000, b='2.72', c=b'binary data').model_dump())
# > {'a': 3, 'b': 2.72, 'c': 'binary data'}
```

--------------------------------

TITLE: Configure Pydantic Model to Allow Extra Data
DESCRIPTION: This Python example shows how to configure a Pydantic model to explicitly 'allow' extra data using `ConfigDict(extra='allow')`. When allowed, extra fields are stored in the `__pydantic_extra__` attribute and are included in the output of `model_dump()`.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/models.md

LANGUAGE: python
CODE:
```python
from pydantic import BaseModel, ConfigDict


class Model(BaseModel):
    x: int

    model_config = ConfigDict(extra='allow')

m = Model(x=1, y='a')
assert m.model_dump() == {'x': 1, 'y': 'a'}
assert m.__pydantic_extra__ == {'y': 'a'}
```

--------------------------------

TITLE: Handle invalid field definitions in Pydantic `create_model`
DESCRIPTION: This error is raised when you provide an invalid number of arguments in the field definition tuple for `create_model()`. The example demonstrates how to trigger the `PydanticUserError` with code `create-model-field-definitions` by providing too many arguments.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/errors/usage_errors.md

LANGUAGE: python
CODE:
```python
from pydantic import PydanticUserError, create_model

try:
    create_model('FooModel', foo=(str, 'default value', 'more'))
except PydanticUserError as exc_info:
    assert exc_info.code == 'create-model-field-definitions'
```

--------------------------------

TITLE: Push Pydantic Release Changes with uv
DESCRIPTION: Runs the semi-automated script to push release-related changes to the repository. This typically involves creating a pull request with the prepared changes and opening a draft release on GitHub.

SOURCE: https://github.com/pydantic/pydantic/blob/main/release/README.md

LANGUAGE: shell
CODE:
```shell
uv run release/push.py
```

--------------------------------

TITLE: Address Invalid Annotated Type in Pydantic Python
DESCRIPTION: This example illustrates a `PydanticUserError` ('invalid-annotated-type') when a `typing.Annotated` type is used with an annotation that cannot apply to the base type, such as `FutureDate()` on a `str`. It highlights the importance of compatible annotations.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/errors/usage_errors.md

LANGUAGE: python
CODE:
```python
from typing import Annotated

from pydantic import BaseModel, FutureDate, PydanticUserError

try:

    class Model(BaseModel):
        foo: Annotated[str, FutureDate()]

except PydanticUserError as exc_info:
    assert exc_info.code == 'invalid-annotated-type'
```

--------------------------------

TITLE: Configure mkdocstrings for Pydantic API in MkDocs
DESCRIPTION: This YAML configuration snippet shows how to add Pydantic's object inventory to the `mkdocstrings` plugin within an MkDocs project's `mkdocs.yml` file. By specifying the import URL under the Python handler, `mkdocstrings` can resolve cross-references to Pydantic API elements within the documentation.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/integrations/documentation.md

LANGUAGE: yaml
CODE:
```yaml
plugins:
- mkdocstrings:
    handlers:
      python:
        import:
        - https://docs.pydantic.dev/latest/objects.inv  # (1)!
```

--------------------------------

TITLE: Define Pydantic Union Discriminator with Custom Logic
DESCRIPTION: This example illustrates using a `Discriminator` instance with a custom function for more flexible union discrimination. This approach is useful when the discriminator fields are not consistent across all models in the `Union`.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/fields.md

LANGUAGE: python
CODE:
```python
from typing import Annotated, Literal, Union

from pydantic import BaseModel, Discriminator, Field, Tag


class Cat(BaseModel):
    pet_type: Literal['cat']
    age: int


class Dog(BaseModel):
    pet_kind: Literal['dog']
    age: int


def pet_discriminator(v):
    if isinstance(v, dict):
        return v.get('pet_type', v.get('pet_kind'))
    return getattr(v, 'pet_type', getattr(v, 'pet_kind', None))


class Model(BaseModel):
    pet: Union[Annotated[Cat, Tag('cat')], Annotated[Dog, Tag('dog')]] = Field(
        discriminator=Discriminator(pet_discriminator)
    )


print(repr(Model.model_validate({'pet': {'pet_type': 'cat', 'age': 12}})))
# > Model(pet=Cat(pet_type='cat', age=12))

print(repr(Model.model_validate({'pet': {'pet_kind': 'dog', 'age': 12}})))
# > Model(pet=Dog(pet_kind='dog', age=12))
```

--------------------------------

TITLE: Apply String Constraints to Pydantic Model Fields
DESCRIPTION: This example demonstrates how to define string constraints in Pydantic models using `min_length`, `max_length`, and `pattern` with `Field`. This ensures that decimal values adhere to specified precision and scale requirements in the model.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/fields.md

LANGUAGE: python
CODE:
```python
from pydantic import BaseModel, Field


class Foo(BaseModel):
    short: str = Field(min_length=3)
    long: str = Field(max_length=10)
    regex: str = Field(pattern=r'^\d*$')  # (1)!


foo = Foo(short='foo', long='foobarbaz', regex='123')
print(foo)
# > short='foo' long='foobarbaz' regex='123'
```

LANGUAGE: json
CODE:
```json
{
  "title": "Foo",
  "type": "object",
  "properties": {
    "short": {
      "title": "Short",
      "type": "string",
      "minLength": 3
    },
    "long": {
      "title": "Long",
      "type": "string",
      "maxLength": 10
    },
    "regex": {
      "title": "Regex",
      "type": "string",
      "pattern": "^\\d*$"
    }
  },
  "required": [
    "short",
    "long",
    "regex"
  ]
}
```

--------------------------------

TITLE: Identifying Pydantic Dataclasses Programmatically
DESCRIPTION: This example demonstrates how to differentiate between a standard library dataclass and a Pydantic dataclass. While `dataclasses.is_dataclass()` returns `True` for both, `pydantic.dataclasses.is_pydantic_dataclass()` specifically identifies dataclasses that have been processed or created by Pydantic, providing a more precise check for Pydantic-specific features.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/dataclasses.md

LANGUAGE: python
CODE:
```python
import dataclasses

import pydantic


@dataclasses.dataclass
class StdLibDataclass:
    id: int

PydanticDataclass = pydantic.dataclasses.dataclass(StdLibDataclass)

print(dataclasses.is_dataclass(StdLibDataclass))
#嶼 True
print(pydantic.dataclasses.is_pydantic_dataclass(StdLibDataclass))
#嶼 False

print(dataclasses.is_dataclass(PydanticDataclass))
#嶼 True
print(pydantic.dataclasses.is_pydantic_dataclass(PydanticDataclass))
#嶼 True
```

--------------------------------

TITLE: Example JSON Schema definition for a Person object
DESCRIPTION: This JSON Schema defines the structure for a 'Person' object, specifying properties like first name, last name, age, and a collection of pets. It includes data types, descriptions, minimum value constraints, and marks certain fields as required, along with a nested 'Pet' definition.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/integrations/datamodel_code_generator.md

LANGUAGE: json
CODE:
```json
{
  "$id": "person.json",
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Person",
  "type": "object",
  "properties": {
    "first_name": {
      "type": "string",
      "description": "The person's first name."
    },
    "last_name": {
      "type": "string",
      "description": "The person's last name."
    },
    "age": {
      "description": "Age in years.",
      "type": "integer",
      "minimum": 0
    },
    "pets": {
      "type": "array",
      "items": [
        {
          "$ref": "#/definitions/Pet"
        }
      ]
    },
    "comment": {
      "type": "null"
    }
  },
  "required": [
      "first_name",
      "last_name"
  ],
  "definitions": {
    "Pet": {
      "properties": {
        "name": {
          "type": "string"
        },
        "age": {
          "type": "integer"
        }
      }
    }
  }
}
```

--------------------------------

TITLE: Apply Pydantic `model_serializer` to valid methods
DESCRIPTION: This error is raised when `@model_serializer` is applied incorrectly, either to an instance method without `self` as the first argument, or to a class method. Both examples demonstrate scenarios that trigger the `model-serializer-instance-method` error.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/errors/usage_errors.md

LANGUAGE: python
CODE:
```python
from pydantic import BaseModel, PydanticUserError, model_serializer

try:

    class MyModel(BaseModel):
        a: int

        @model_serializer
        def _serialize(slf, x, y, z):
            return slf

except PydanticUserError as exc_info:
    assert exc_info.code == 'model-serializer-instance-method'
```

LANGUAGE: python
CODE:
```python
from pydantic import BaseModel, PydanticUserError, model_serializer

try:

    class MyModel(BaseModel):
        a: int

        @model_serializer
        @classmethod
        def _serialize(self, x, y, z):
            return self

except PydanticUserError as exc_info:
    assert exc_info.code == 'model-serializer-instance-method'
```

--------------------------------

TITLE: Validate Pydantic Model by Alias at Runtime
DESCRIPTION: This example shows how to validate incoming data using the field's alias by passing `by_alias=True` to the `model_validate` method at runtime. The `validation_alias` specified in `Field` is used to match keys in the input dictionary.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/alias.md

LANGUAGE: python
CODE:
```python
from pydantic import BaseModel, Field


class Model(BaseModel):
    my_field: str = Field(validation_alias='my_alias')


m = Model.model_validate(
    {'my_alias': 'foo'},
    by_alias=True,
    by_name=False,
)
print(repr(m))
# > Model(my_field='foo')
```

--------------------------------

TITLE: Configure Pydantic Mypy Plugin and Strictness Settings
DESCRIPTION: This snippet demonstrates how to configure the Pydantic Mypy plugin and apply various strictness flags for both Mypy and the Pydantic plugin. It shows the configuration setup in both `mypy.ini` and `pyproject.toml` files, enabling features like `init_forbid_extra` and `init_typed` for stricter type checking and error detection related to Pydantic models.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/integrations/mypy.md

LANGUAGE: ini
CODE:
```ini
[mypy]
plugins = pydantic.mypy

follow_imports = silent
warn_redundant_casts = True
warn_unused_ignores = True
disallow_any_generics = True
no_implicit_reexport = True
disallow_untyped_defs = True

[pydantic-mypy]
init_forbid_extra = True
init_typed = True
warn_required_dynamic_aliases = True
```

LANGUAGE: toml
CODE:
```toml
[tool.mypy]
plugins = ["pydantic.mypy"]

follow_imports = "silent"
warn_redundant_casts = true
warn_unused_ignores = true
disallow_any_generics = true
no_implicit_reexport = true
disallow_untyped_defs = true

[tool.pydantic-mypy]
init_forbid_extra = true
init_typed = true
warn_required_dynamic_aliases = true
```

--------------------------------

TITLE: Define Decimal Constraints in Pydantic Models
DESCRIPTION: This Pydantic example illustrates how to apply constraints to `Decimal` fields using `max_digits` and `decimal_places` within `Field`. This ensures that decimal values adhere to specified precision and scale requirements in the model.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/fields.md

LANGUAGE: python
CODE:
```python
from decimal import Decimal

from pydantic import BaseModel, Field


class Foo(BaseModel):
    precise: Decimal = Field(max_digits=5, decimal_places=2)


foo = Foo(precise=Decimal('123.45'))
print(foo)
# > precise=Decimal('123.45')
```

--------------------------------

TITLE: Use Pydantic Field and Stdlib Dataclasses Field with Pydantic Dataclasses (Python)
DESCRIPTION: This example illustrates the flexibility of Pydantic dataclasses by showing how to combine both `pydantic.Field` and `dataclasses.field` for defining fields. It demonstrates setting default factories, metadata, and validation constraints (`ge`, `le`) using Pydantic's `Field` function.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/dataclasses.md

LANGUAGE: python
CODE:
```python
import dataclasses
from typing import Optional

from pydantic import Field
from pydantic.dataclasses import dataclass


@dataclass
class User:
    id: int
    name: str = 'John Doe'
    friends: list[int] = dataclasses.field(default_factory=lambda: [0])
    age: Optional[int] = dataclasses.field(
        default=None,
        metadata={'title': 'The age of the user', 'description': 'do not lie!'},
    )
    height: Optional[int] = Field(
        default=None, title='The height in cm', ge=50, le=300
    )


user = User(id='42', height='250')
print(user)
# > User(id=42, name='John Doe', friends=[0], age=None, height=250)
```

--------------------------------

TITLE: Create Generic Pydantic Models for Flexible Data Wrapping
DESCRIPTION: This example showcases how to define a generic Pydantic model, `Response`, to wrap varying data types. It provides two versions: one for Python 3.9+ using `TypeVar` and `typing.Generic`, and another for Python 3.12+ leveraging the new type parameter syntax. The snippets illustrate model instantiation with different data types (int, str, custom BaseModel), `model_dump()` usage, and error handling for type mismatches.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/models.md

LANGUAGE: python
CODE:
```python
from typing import Generic, TypeVar

from pydantic import BaseModel, ValidationError

DataT = TypeVar('DataT')  # (1)!


class DataModel(BaseModel):
    number: int


class Response(BaseModel, Generic[DataT]):  # (2)!
    data: DataT  # (3)!


print(Response[int](data=1))
# > data=1
print(Response[str](data='value'))
# > data='value'
print(Response[str](data='value').model_dump())
# > {'data': 'value'}

data = DataModel(number=1)
print(Response[DataModel](data=data).model_dump())
# > {'data': {'number': 1}}
try:
    Response[int](data='value')
except ValidationError as e:
    print(e)
    # """
    # 1 validation error for Response[int]
    # data
    #   Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='value', input_type=str]
    # """
```

LANGUAGE: python
CODE:
```python
from pydantic import BaseModel, ValidationError


class DataModel(BaseModel):
    number: int


class Response[DataT](BaseModel):  # (1)!
    data: DataT  # (2)!


print(Response[int](data=1))
# > data=1
print(Response[str](data='value'))
# > data='value'
print(Response[str](data='value').model_dump())
# > {'data': 'value'}

data = DataModel(number=1)
print(Response[DataModel](data=data).model_dump())
# > {'data': {'number': 1}}
try:
    Response[int](data='value')
except ValidationError as e:
    print(e)
    # """
    # 1 validation error for Response[int]
    # data
    #   Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='value', input_type=str]
    # """
```

--------------------------------

TITLE: Pydantic Model Validation from SQLAlchemy ORM Instances
DESCRIPTION: This example demonstrates how to configure a Pydantic `BaseModel` to validate and instantiate from an arbitrary class instance, specifically a SQLAlchemy ORM object. It shows defining an ORM model and a corresponding Pydantic model with `ConfigDict(from_attributes=True)` for seamless data transfer, reading attributes from the ORM instance.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/models.md

LANGUAGE: python
CODE:
```python
from typing import Annotated

from sqlalchemy import ARRAY, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from pydantic import BaseModel, ConfigDict, StringConstraints


class Base(DeclarativeBase):
    pass


class CompanyOrm(Base):
    __tablename__ = 'companies'

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    public_key: Mapped[str] = mapped_column(
        String(20), index=True, nullable=False, unique=True
    )
    domains: Mapped[list[str]] = mapped_column(ARRAY(String(255)))


class CompanyModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    public_key: Annotated[str, StringConstraints(max_length=20)]
    domains: list[Annotated[str, StringConstraints(max_length=255)]]


co_orm = CompanyOrm(
    id=123,
    public_key='foobar',
    domains=['example.com', 'foobar.com'],
)
print(co_orm)
#
co_model = CompanyModel.model_validate(co_orm)
print(co_model)
```

--------------------------------

TITLE: Validate Pydantic Model by Alias and Name at Runtime
DESCRIPTION: This example demonstrates validating a Pydantic model where both the field's alias and its attribute name are accepted as input keys. This flexibility is achieved by setting both `by_alias=True` and `by_name=True` during the `model_validate` call.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/alias.md

LANGUAGE: python
CODE:
```python
from pydantic import BaseModel, Field


class Model(BaseModel):
    my_field: str = Field(validation_alias='my_alias')


m = Model.model_validate(
    {'my_alias': 'foo'},
    by_alias=True,
    by_name=True,
)
print(repr(m))
# > Model(my_field='foo')

m = Model.model_validate(
    {'my_field': 'foo'},
    by_alias=True,
    by_name=True,
)
print(repr(m))
# > Model(my_field='foo')
```

--------------------------------

TITLE: Define Pydantic Model with Experimental Pipeline API (validate_as)
DESCRIPTION: This example demonstrates the experimental Pydantic pipeline API using `validate_as` within `Annotated` types to define a sequence of validation, transformation, and constraint steps for model fields. It showcases various operations like lowercasing strings, applying numeric constraints, regex matching, custom transformations, and combining steps with logical OR (`|`). This API aims for more type-safe and composable data processing.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/experimental.md

LANGUAGE: python
CODE:
```python
from __future__ import annotations

from datetime import datetime
from typing import Annotated

from pydantic import BaseModel
from pydantic.experimental.pipeline import validate_as


class User(BaseModel):
    name: Annotated[str, validate_as(str).str_lower()]  # (1)!
    age: Annotated[int, validate_as(int).gt(0)]  # (2)!
    username: Annotated[str, validate_as(str).str_pattern(r'[a-z]+')]  # (3)!
    password: Annotated[
        str,
        validate_as(str)
        .transform(str.lower)
        .predicate(lambda x: x != 'password'),  # (4)!
    ]
    favorite_number: Annotated[  # (5)!
        int,
        (validate_as(int) | validate_as(str).str_strip().validate_as(int)).gt(
            0
        ),
    ]
    friends: Annotated[list[User], validate_as(...).len(0, 100)]  # (6)!
    bio: Annotated[
        datetime,
        validate_as(int)
        .transform(lambda x: x / 1_000_000)
        .validate_as(...),  # (8)!
    ]
```

--------------------------------

TITLE: Example Pydantic model causing Mypy error (Python)
DESCRIPTION: This Python snippet defines a Pydantic BaseModel and then attempts to instantiate it with an unexpected keyword argument ('b'). This code serves as the input for a Mypy test, designed to trigger a type checking error.

SOURCE: https://github.com/pydantic/pydantic/blob/main/tests/mypy/README.md

LANGUAGE: python
CODE:
```python
from pydantic import BaseModel


class Model(BaseModel):
    a: int


model = Model(a=1, b=2)
```

--------------------------------

TITLE: Validate and Generate Schema for List of Integers with Pydantic TypeAdapter
DESCRIPTION: This Python example demonstrates using Pydantic's `TypeAdapter` to validate a list of string representations of numbers into a list of integers and then generate its corresponding JSON schema. The `TypeAdapter` provides a unified interface for handling validation, serialization, and schema generation for arbitrary types, serving as a replacement for older Pydantic V1 utilities.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/migration.md

LANGUAGE: python
CODE:
```python
from pydantic import TypeAdapter

adapter = TypeAdapter(list[int])
assert adapter.validate_python(['1', '2', '3']) == [1, 2, 3]
print(adapter.json_schema())
# > {'items': {'type': 'integer'}, 'type': 'array'}
```

--------------------------------

TITLE: Handle Mutually Exclusive Dataclass Init and Init_Var Fields in Pydantic Python
DESCRIPTION: This example highlights a `PydanticUserError` caused by attempting to set both `init=False` and `init_var=True` for a field in a Pydantic dataclass. These two field settings are mutually exclusive, as `init_var=True` implies initialization, contradicting `init=False`.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/errors/usage_errors.md

LANGUAGE: python
CODE:
```python
from pydantic import Field
from pydantic.dataclasses import dataclass


@dataclass
class Foo:
    bar: str = Field(init=False, init_var=True)
```

--------------------------------

TITLE: Dynamically Creating Pydantic Models with `create_model`
DESCRIPTION: This Python snippet demonstrates how to dynamically generate Pydantic `BaseModel` classes at runtime using the `create_model` function. This feature is particularly useful when model schemas need to be constructed programmatically based on runtime data or configurations. The example defines a model with a string field and an integer field with a default value.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/models.md

LANGUAGE: python
CODE:
```python
from pydantic import BaseModel, create_model

DynamicFoobarModel = create_model('DynamicFoobarModel', foo=str, bar=(int, 123))
```

--------------------------------

TITLE: Pydantic Field Validator with `json_schema_input_type`
DESCRIPTION: This example expands on the `before` mode validator by introducing the `json_schema_input_type` argument. It specifies that the field can accept `Union[int, str]`, ensuring that the generated JSON schema accurately reflects the allowed input types for the validated field.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/validators.md

LANGUAGE: python
CODE:
```python
from typing import Any, Union

from pydantic import BaseModel, field_validator


class Model(BaseModel):
    value: str

    @field_validator(
        'value',
        mode='before',
        json_schema_input_type=Union[int, str]
    )
    @classmethod
    def cast_ints(cls, value: Any) -> Any:
        if isinstance(value, int):
            return str(value)
        else:
            return value


print(Model.model_json_schema()['properties']['value'])
# > {'anyOf': [{'type': 'integer'}, {'type': 'string'}], 'title': 'Value'}
```

--------------------------------

TITLE: Handle Pydantic Unrecognized Model Serializer Signature Error
DESCRIPTION: This Python example shows a `PydanticUserError` caused by a `model_serializer` with an incorrect signature (e.g., having extraneous parameters like `x`, `y`, `z`). It defines a `BaseModel` and a misconfigured `model_serializer` to illustrate the 'model-serializer-signature' error.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/errors/usage_errors.md

LANGUAGE: python
CODE:
```python
from pydantic import BaseModel, PydanticUserError, model_serializer

try:

    class MyModel(BaseModel):
        a: int

        @model_serializer
        def _serialize(self, x, y, z):
            return self

except PydanticUserError as exc_info:
    assert exc_info.code == 'model-serializer-signature'
```

--------------------------------

TITLE: Pydantic Datetime Validation with pytz Timezones
DESCRIPTION: Demonstrates validating `datetime` objects with `pytz` timezones using Pydantic. It includes an example of a timezone that might cause validation issues or specific outputs, highlighting how `ValidationError` exceptions are handled and their error details can be pretty-printed.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/examples/custom_validators.md

LANGUAGE: python
CODE:
```python
ta.validate_python(dt.datetime(2023, 1, 1, 0, 0, tzinfo=pytz.timezone(LA)))

LONDON = 'Europe/London'
try:
    print(
        ta.validate_python(
            dt.datetime(2023, 1, 1, 0, 0, tzinfo=pytz.timezone(LONDON))
        )
    )
except ValidationError as e:
    pprint(e.errors(), width=100)
```

--------------------------------

TITLE: Pydantic V1 vs V2 JSON Serialization of None Keys
DESCRIPTION: This Python example demonstrates the difference in JSON serialization when using `None` as a dictionary key between Pydantic V1 and V2. Pydantic V1's `json()` method serializes `None` to the string 'null', while Pydantic V2's `model_dump_json()` serializes it to the string 'None'.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/migration.md

LANGUAGE: python
CODE:
```python
from typing import Optional

from pydantic import BaseModel as V2BaseModel
from pydantic.v1 import BaseModel as V1BaseModel


class V1Model(V1BaseModel):
    a: dict[Optional[str], int]


class V2Model(V2BaseModel):
    a: dict[Optional[str], int]


v1_model = V1Model(a={None: 123})
v2_model = V2Model(a={None: 123})

# V1
print(v1_model.json())
# > {"a": {"null": 123}}

# V2
print(v2_model.model_dump_json())
# > {"a":{"None":123}}
```

--------------------------------

TITLE: Add Validators to Dynamically Created Pydantic Model
DESCRIPTION: This example demonstrates how to integrate custom field validators into a dynamically generated Pydantic model using `create_model` and the `__validators__` argument. It includes a custom `alphanum` validator and shows error handling with `ValidationError`.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/models.md

LANGUAGE: python
CODE:
```python
from pydantic import ValidationError, create_model, field_validator


def alphanum(cls, v):
    assert v.isalnum(), 'must be alphanumeric'
    return v


validators = {
    'username_validator': field_validator('username')(alphanum)  # (1)!
}

UserModel = create_model(
    'UserModel', username=(str, ...), __validators__=validators
)

user = UserModel(username='scolvin')
print(user)
# > username='scolvin'

try:
    UserModel(username='scolvi%n')
excep ValidationErr`or as e:
    print(e)
    # """
    # 1 validation error for UserModel
    # username
    #   Assertion failed, must be alphanumeric [type=assertion_error, input_value='scolvi%n', input_type=str]
    # """
```

--------------------------------

TITLE: Skip Callable Arguments in Pydantic Schema Validation
DESCRIPTION: This example demonstrates using a `parameters_callback` with `generate_arguments_schema` to selectively skip validation for certain parameters of a callable. The provided callback skips the first parameter (`p`) based on its index. This allows for flexible control over which arguments are included in the validation process when using `SchemaValidator`.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/experimental.md

LANGUAGE: python
CODE:
```python
from typing import Any

from pydantic_core import SchemaValidator

from pydantic.experimental.arguments_schema import generate_arguments_schema


def func(p: bool, *args: str, **kwargs: int) -> None: ...


def skip_first_parameter(index: int, name: str, annotation: Any) -> Any:
    if index == 0:
        return 'skip'


arguments_schema = generate_arguments_schema(
    func=func,
    parameters_callback=skip_first_parameter,
)

val = SchemaValidator(arguments_schema)

args, kwargs = val.validate_json('{"args": ["arg1"], "kwargs": {"extra": 1}}')
print(args, kwargs)
# > ('arg1',) {'extra': 1}
```

--------------------------------

TITLE: Mark Pydantic computed_field as deprecated
DESCRIPTION: This example shows how to mark a `computed_field` as deprecated using the `@deprecated` decorator from `typing_extensions`. Similar to regular fields, this allows developers to signal that a computed property is no longer recommended for use.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/fields.md

LANGUAGE: python
CODE:
```python
from typing_extensions import deprecated

from pydantic import BaseModel, computed_field


class Box(BaseModel):
    width: float
    height: float
    depth: float

    @computed_field
    @property
    @deprecated("'volume' is deprecated")
    def volume(self) -> float:
        return self.width * self.height * self.depth
```

--------------------------------

TITLE: Pydantic Model Validation with Nested Arbitrary Class Instances
DESCRIPTION: This example illustrates how Pydantic models can validate and create instances from arbitrary classes containing nested arbitrary class instances. It defines `PetCls` and `PersonCls` as standard Python classes and corresponding Pydantic models `Pet` and `Person`, demonstrating deep attribute parsing when `from_attributes=True` is enabled.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/models.md

LANGUAGE: python
CODE:
```python
from pydantic import BaseModel, ConfigDict


class PetCls:
    def __init__(self, *, name: str, species: str):
        self.name = name
        self.species = species


class PersonCls:
    def __init__(self, *, name: str, age: float = None, pets: list[PetCls]):
        self.name = name
        self.age = age
        self.pets = pets


class Pet(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    species: str


class Person(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    age: float = None
    pets: list[Pet]


bones = PetCls(name='Bones', species='dog')
orion = PetCls(name='Orion', species='cat')
anna = PersonCls(name='Anna', age=20, pets=[bones, orion])
anna_model = Person.model_validate(anna)
print(anna_model)
```

--------------------------------

TITLE: Instantiate Pydantic Parametrized Generic Class
DESCRIPTION: Demonstrates how to instantiate a Pydantic `BaseModel` that has been parametrized with specific types, showing the resulting representation of the model with the applied types.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/models.md

LANGUAGE: python
CODE:
```python
print(ChildClass[str, int](x='1', y='y', z='3'))
```

--------------------------------

TITLE: Validate and Serialize TypedDict Lists with Pydantic TypeAdapter
DESCRIPTION: This example demonstrates how to use Pydantic's `TypeAdapter` to validate and serialize a list of `TypedDict` instances. It includes input validation, error handling for invalid types, and serialization of the validated data to JSON bytes.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/type_adapter.md

LANGUAGE: python
CODE:
```python
from typing_extensions import TypedDict

from pydantic import TypeAdapter, ValidationError


class User(TypedDict):
    name: str
    id: int


user_list_adapter = TypeAdapter(list[User])
user_list = user_list_adapter.validate_python([{'name': 'Fred', 'id': '3'}])
print(repr(user_list))
# > [{'name': 'Fred', 'id': 3}]

try:
    user_list_adapter.validate_python(
        [{'name': 'Fred', 'id': 'wrong', 'other': 'no'}]
    )
except ValidationError as e:
    print(e)
    # """
    # 1 validation error for list[User]
    # 0.id
    #   Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='wrong', input_type=str]
    # """

print(repr(user_list_adapter.dump_json(user_list)))
# > b'[{"name":"Fred","id":3}]'
```

--------------------------------

TITLE: Serialize and deserialize Pydantic models with pickle in Python
DESCRIPTION: Pydantic models natively support Python's `pickle` module for efficient serialization (pickling) and deserialization (unpickling). This example demonstrates how to store a model instance as a byte stream and then reconstruct it back into an identical model object, including its data types.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/serialization.md

LANGUAGE: python
CODE:
```python
import pickle

from pydantic import BaseModel


class FooBarModel(BaseModel):
    a: str
    b: int


m = FooBarModel(a='hello', b=123)
print(m)
# > a='hello' b=123
data = pickle.dumps(m)
print(data[:20])
# > b'\x80\x04\x95\x95\x00\x00\x00\x00\x00\x00\x00\x8c\x08__main_'
m2 = pickle.loads(data)
print(m2)
# > a='hello' b=123
```

--------------------------------

TITLE: Define Pydantic Union Discriminator by Field Name
DESCRIPTION: This example demonstrates using the `discriminator` parameter with a field name to specify how Pydantic should distinguish between models within a `Union`. It simplifies validation when a common field exists across all union members.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/fields.md

LANGUAGE: python
CODE:
```python
from typing import Literal, Union

from pydantic import BaseModel, Field


class Cat(BaseModel):
    pet_type: Literal['cat']
    age: int


class Dog(BaseModel):
    pet_type: Literal['dog']
    age: int


class Model(BaseModel):
    pet: Union[Cat, Dog] = Field(discriminator='pet_type')


print(Model.model_validate({'pet': {'pet_type': 'cat', 'age': 12}})) # (1)!
# > pet=Cat(pet_type='cat', age=12)
```

--------------------------------

TITLE: Authenticate GitHub CLI
DESCRIPTION: Authenticates the GitHub CLI tool with your GitHub account. This step is a prerequisite for making API calls required during the release process, such as creating pull requests or draft releases.

SOURCE: https://github.com/pydantic/pydantic/blob/main/release/README.md

LANGUAGE: shell
CODE:
```shell
gh auth login
```

--------------------------------

TITLE: Pydantic V2: Accessing ValidationInfo in @field_validator for Config and Field Details
DESCRIPTION: This Python example showcases how to use the new `@field_validator` in Pydantic V2 to access validation metadata. It demonstrates how to retrieve configuration details via `info.config` and field information using `cls.model_fields[info.field_name]`, which replaces the deprecated `config` and `field` arguments from Pydantic V1's `@validator`.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/migration.md

LANGUAGE: python
CODE:
```python
from pydantic import BaseModel, ValidationInfo, field_validator


class Model(BaseModel):
    x: int

    @field_validator('x')
    def val_x(cls, v: int, info: ValidationInfo) -> int:
        assert info.config is not None
        print(info.config.get('title'))
        # > Model
        print(cls.model_fields[info.field_name].is_required())
        # > True
        return v


Model(x=1)
```

--------------------------------

TITLE: Mypy output with type error for Pydantic model (Python)
DESCRIPTION: This Python snippet shows the expected output from Mypy after processing the previous Pydantic model example. It includes the original code along with an inline Mypy error comment indicating an 'Unexpected keyword argument "b" for "Model"'.

SOURCE: https://github.com/pydantic/pydantic/blob/main/tests/mypy/README.md

LANGUAGE: python
CODE:
```python
from pydantic import BaseModel


class Model(BaseModel):
    a: int


model = Model(a=1, b=2)
# MYPY: error: Unexpected keyword argument "b" for "Model"  [call-arg]
```

--------------------------------

TITLE: Handle Pydantic Unrecognized Field Validator Signature Error
DESCRIPTION: This Python example illustrates a `PydanticUserError` triggered by a `field_validator` with an incorrect signature (e.g., missing expected parameters like `value`). It defines a model with a `field_validator` that only takes `cls` and catches the 'validator-signature' error.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/errors/usage_errors.md

LANGUAGE: python
CODE:
```python
from pydantic import BaseModel, PydanticUserError, field_validator

try:

    class Model(BaseModel):
        a: str

        @field_validator('a')
        @classmethod
        def check_a(cls):
            return 'a'

except PydanticUserError as exc_info:
    assert exc_info.code == 'validator-signature'
```

--------------------------------

TITLE: Validate Partial Python Lists with Pydantic TypeAdapter
DESCRIPTION: This example illustrates how Pydantic's `TypeAdapter` handles validation of Python lists with `experimental_allow_partial=True`. It demonstrates that errors occurring in the last element of the list are ignored, allowing the validated prefix of the list to be returned. This applies to both type validation and constraint validation (e.g., `Ge` for greater than or equal to).

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/experimental.md

LANGUAGE: python
CODE:
```python
from typing import Annotated

from annotated_types import Ge

from pydantic import TypeAdapter

ta = TypeAdapter(list[Annotated[int, Ge(10)]])
v = ta.validate_python([20, 30, 4], experimental_allow_partial=True)  # (1)!
print(v)
# > [20, 30]

ta = TypeAdapter(list[int])

v = ta.validate_python([1, 2, 'wrong'], experimental_allow_partial=True)  # (2)!
print(v)
# > [1, 2]
```

--------------------------------

TITLE: Structural Pattern Matching with Pydantic Models (Python)
DESCRIPTION: Illustrates how to use Python 3.10's structural pattern matching with Pydantic `BaseModel` instances. It demonstrates matching on field values and declaring new variables from matched attributes, providing a concise way to handle different model states.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/models.md

LANGUAGE: python
CODE:
```python
from pydantic import BaseModel


class Pet(BaseModel):
    name: str
    species: str


a = Pet(name='Bones', species='dog')

match a:
    # match `species` to 'dog', declare and initialize `dog_name`
    case Pet(species='dog', name=dog_name):
        print(f'{dog_name} is a dog')
    # default case
    case _:
        print('No dog matched')

```

--------------------------------

TITLE: Validate and serialize TypedDict with Pydantic TypeAdapter
DESCRIPTION: This Python example demonstrates how to use Pydantic's TypeAdapter to validate and serialize a TypedDict. It shows validating a dictionary against a Meeting TypedDict, serializing the validated object, and generating its JSON schema. The TypedDict uses datetime, bytes, and NotRequired from typing_extensions.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/why.md

LANGUAGE: python
CODE:
```python
from datetime import datetime

from typing_extensions import NotRequired, TypedDict

from pydantic import TypeAdapter


class Meeting(TypedDict):
    when: datetime
    where: bytes
    why: NotRequired[str]


meeting_adapter = TypeAdapter(Meeting)
m = meeting_adapter.validate_python(  # (1)!
    {'when': '2020-01-01T12:00', 'where': 'home'}
)
print(m)
# > {'when': datetime.datetime(2020, 1, 1, 12, 0), 'where': b'home'}
meeting_adapter.dump_python(m, exclude={'where'})  # (2)!

print(meeting_adapter.json_schema())  # (3)!
"""
{
    'properties': {
        'when': {'format': 'date-time', 'title': 'When', 'type': 'string'},
        'where': {'format': 'binary', 'title': 'Where', 'type': 'string'},
        'why': {'title': 'Why', 'type': 'string'},
    },
    'required': ['when', 'where'],
    'title': 'Meeting',
    'type': 'object',
}
"""
```

--------------------------------

TITLE: Compare Pydantic Performance with Pure Python for JSON and URL Validation
DESCRIPTION: This Python example benchmarks Pydantic's data validation performance against a hand-written pure Python implementation. It fetches JSON data from a GitHub API, then measures the execution time for both approaches to parse the JSON and validate URLs, demonstrating Pydantic's significantly faster processing (over 300% quicker) due to its Rust-optimized core validation logic.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/why.md

LANGUAGE: python
CODE:
```python
import json
import timeit
from urllib.parse import urlparse

import requests

from pydantic import HttpUrl, TypeAdapter

reps = 7
number = 100
r = requests.get('https://api.github.com/emojis')
r.raise_for_status()
emojis_json = r.content


def emojis_pure_python(raw_data):
    data = json.loads(raw_data)
    output = {}
    for key, value in data.items():
        assert isinstance(key, str)
        url = urlparse(value)
        assert url.scheme in ('https', 'http')
        output[key] = url


emojis_pure_python_times = timeit.repeat(
    'emojis_pure_python(emojis_json)',
    globals={
        'emojis_pure_python': emojis_pure_python,
        'emojis_json': emojis_json,
    },
    repeat=reps,
    number=number,
)
print(f'pure python: {min(emojis_pure_python_times) / number * 1000:0.2f}ms')
#|> pure python: 5.32ms

type_adapter = TypeAdapter(dict[str, HttpUrl])
emojis_pydantic_times = timeit.repeat(
    'type_adapter.validate_json(emojis_json)',
    globals={
        'type_adapter': type_adapter,
        'HttpUrl': HttpUrl,
        'emojis_json': emojis_json,
    },
    repeat=reps,
    number=number,
)
print(f'pydantic: {min(emojis_pydantic_times) / number * 1000:0.2f}ms')
#|> pydantic: 1.54ms

print(
    f'Pydantic {min(emojis_pure_python_times) / min(emojis_pydantic_times):0.2f}x faster'
)
#|> Pydantic 3.45x faster
```

--------------------------------

TITLE: Define Valid Pydantic Field Serializer Signatures
DESCRIPTION: This Python code provides various examples of correctly structured `field_serializer` signatures in Pydantic. It covers instance methods and static methods for both 'plain' and 'wrap' modes, demonstrating how to include or omit `self`, `value`, `info`, and `SerializerFunctionWrapHandler` parameters.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/errors/usage_errors.md

LANGUAGE: python
CODE:
```python
from pydantic import FieldSerializationInfo, SerializerFunctionWrapHandler, field_serializer

# an instance method with the default mode or `mode='plain'`
@field_serializer('x')  # or @field_serializer('x', mode='plain')
def ser_x(self, value: Any, info: FieldSerializationInfo): ...

# a static method or function with the default mode or `mode='plain'`
@field_serializer('x')  # or @field_serializer('x', mode='plain')
@staticmethod
def ser_x(value: Any, info: FieldSerializationInfo): ...

# equivalent to
def ser_x(value: Any, info: FieldSerializationInfo): ...
serializer('x')(ser_x)

# an instance method with `mode='wrap'`
@field_serializer('x', mode='wrap')
def ser_x(self, value: Any, nxt: SerializerFunctionWrapHandler, info: FieldSerializationInfo): ...

# a static method or function with `mode='wrap'`
@field_serializer('x', mode='wrap')
@staticmethod
def ser_x(value: Any, nxt: SerializerFunctionWrapHandler, info: FieldSerializationInfo): ...

# equivalent to
def ser_x(value: Any, nxt: SerializerFunctionWrapHandler, info: FieldSerializationInfo): ...
serializer('x')(ser_x)

# For all of these, you can also choose to omit the `info` argument, for example:
@field_serializer('x')
def ser_x(self, value: Any): ...

@field_serializer('x', mode='wrap')
def ser_x(self, value: Any, handler: SerializerFunctionWrapHandler): ...
```

--------------------------------

TITLE: Validate single user data with Pydantic BaseModel and HTTPX
DESCRIPTION: This example demonstrates fetching a single user's data from a public API using the `httpx` client, defining a Pydantic `BaseModel` to specify the expected data structure, and then validating the JSON response against this model. It showcases basic data validation for individual objects retrieved via HTTP.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/examples/requests.md

LANGUAGE: python
CODE:
```python
import httpx

from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: int
    name: str
    email: EmailStr


url = 'https://jsonplaceholder.typicode.com/users/1'

response = httpx.get(url)
response.raise_for_status()

user = User.model_validate(response.json())
print(repr(user))
# > User(id=1, name='Leanne Graham', email='Sincere@april.biz')
```

--------------------------------

TITLE: Catch Pydantic `schema-for-unknown-type` error in Python
DESCRIPTION: This example demonstrates how Pydantic raises a `PydanticUserError` when it encounters a type that it cannot generate a `CoreSchema` for, such as a literal integer used as a type annotation. The `try-except` block captures the `schema-for-unknown-type` error during model definition, indicating an unsupported type annotation.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/errors/usage_errors.md

LANGUAGE: python
CODE:
```python
from pydantic import BaseModel, PydanticUserError

try:

    class Model(BaseModel):
        x: 43 = 123

except PydanticUserError as exc_info:
    assert exc_info.code == 'schema-for-unknown-type'
```

--------------------------------

TITLE: Rebuilding Pydantic Model with Resolved Forward Reference
DESCRIPTION: This example demonstrates how to resolve the forward reference `MyType` by defining it as an integer type. Subsequently, calling `Foo.model_rebuild()` processes the newly defined type. After the rebuild, `Foo.__pydantic_core_schema__` correctly reflects the model's structure, showing a fully resolved schema.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/internals/resolving_annotations.md

LANGUAGE: python
CODE:
```python
type MyType = int

Foo.model_rebuild()
Foo.__pydantic_core_schema__
```

--------------------------------

TITLE: Handling Pydantic `ValidationError` Exceptions
DESCRIPTION: This example demonstrates how Pydantic raises a `ValidationError` exception when data fails validation against a `BaseModel` schema. It defines a model with a list of integers and a float, then attempts to validate invalid input data, catching and printing the detailed validation error message that includes information about all detected errors.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/models.md

LANGUAGE: python
CODE:
```python
from pydantic import BaseModel, ValidationError


class Model(BaseModel):
    list_of_ints: list[int]
    a_float: float


data = dict(
    list_of_ints=['1', 2, 'bad'],
    a_float='not a float',
)

try:
    Model(**data)
except ValidationError as e:
    print(e)
```

--------------------------------

TITLE: Bypass Pydantic validation using `Any` in Python
DESCRIPTION: This Python example demonstrates how to use `typing.Any` within a Pydantic `BaseModel` to explicitly instruct Pydantic to skip validation for a specific field. When a field is typed as `Any`, Pydantic will accept any value for that field without performing any validation checks, which can be useful for performance if validation is not needed.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/performance.md

LANGUAGE: python
CODE:
```python
from typing import Any

from pydantic import BaseModel


class Model(BaseModel):
    a: Any


model = Model(a=1)
```

--------------------------------

TITLE: Define Pydantic BaseModel with a Strict Boolean Field (Python)
DESCRIPTION: This Python example demonstrates defining a Pydantic `BaseModel` with a boolean field `foo` set to strict validation. The `Field(strict=True)` annotation influences how the corresponding core schema for this field will be generated.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/internals/architecture.md

LANGUAGE: python
CODE:
```python
from pydantic import BaseModel, Field


class Model(BaseModel):
    foo: bool = Field(strict=True)
```

--------------------------------

TITLE: Customize Pydantic JSON schema using __get_pydantic_json_schema__ in Python
DESCRIPTION: This snippet demonstrates the correct way to customize Pydantic's JSON schema in V2 using the `__get_pydantic_json_schema__` class method. It receives a `CoreSchema` and a `handler`, allowing for modification of the generated JSON schema, such as adding examples, and then printing the resulting schema.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/errors/usage_errors.md

LANGUAGE: python
CODE:
```python
from typing import Any

from pydantic_core import CoreSchema

from pydantic import BaseModel, GetJsonSchemaHandler


class Model(BaseModel):
    @classmethod
    def __get_pydantic_json_schema__(
        cls,
        core_schema: CoreSchema,
        handler: GetJsonSchemaHandler
    ) -> dict[str, Any]:
        json_schema = super().__get_pydantic_json_schema__(core_schema, handler)
        json_schema = handler.resolve_ref_schema(json_schema)
        json_schema.update(examples=['example'])
        return json_schema


print(Model.model_json_schema())
"""
{'examples': ['example'], 'properties': {}, 'title': 'Model', 'type': 'object'}
"""
```

--------------------------------

TITLE: Run Pydantic V2 Migration Tool on a Package
DESCRIPTION: Executes the `bump-pydantic` tool on a specified Python package within your repository. This command automatically applies migration fixes to the source files in `my_package`.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/migration.md

LANGUAGE: bash
CODE:
```bash
bump-pydantic my_package
```

--------------------------------

TITLE: Validate CSV Data with Pydantic in Python
DESCRIPTION: This example shows how to parse a CSV file using Python's `csv` module and validate each row against a Pydantic `BaseModel`. It demonstrates reading structured data from 'people.csv' and converting rows into `Person` model instances, ensuring type safety and data integrity.

SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/examples/files.md

LANGUAGE: csv
CODE:
```csv
name,age,email
John Doe,30,john@example.com
Jane Doe,25,jane@example.com
```

LANGUAGE: python
CODE:
```python
import csv

from pydantic import BaseModel, EmailStr, PositiveInt


class Person(BaseModel):
    name: str
    age: PositiveInt
    email: EmailStr


with open('people.csv') as f:
    reader = csv.DictReader(f)
    people = [Person.model_validate(row) for row in reader]

print(people)

```