# Task ID: 64

**Title:** Define and Implement Database Configuration Object

**Status:** pending

**Dependencies:** None

**Priority:** high

**Description:** Create a `DatabaseConfig` class or data structure to encapsulate all database connection and configuration parameters, replacing direct usage of global variables like DATA_DIR and EMAILS_FILE.

**Details:**

Implement a `DatabaseConfig` Pydantic model or dataclass to hold database-related configuration. This object will replace global variables such as `DATA_DIR`, `EMAILS_FILE`, etc. Ensure properties are type-hinted and include validation logic (e.g., path existence, file format validation). This class will serve as the primary configuration source for `DatabaseManager` and its related components.

```python
from pathlib import Path
from pydantic import BaseModel, Field, ValidationError

class DatabaseConfig(BaseModel):
    data_dir: Path = Field(..., description="Root directory for database files")
    emails_file: Path = Field(..., description="Path to the emails data file")
    # Add other configuration parameters currently exposed as global variables
    # e.g., cache_enabled: bool = True

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def create_default_config(cls) -> 'DatabaseConfig':
        # Example of a factory method for default configuration
        return cls(data_dir=Path('./data'), emails_file=Path('./data/emails.json'))

def validate_config(config: DatabaseConfig):
    # Example of runtime validation beyond Pydantic's basic checks
    if not config.data_dir.is_dir():
        raise ValueError(f"Data directory does not exist: {config.data_dir}")
    # Further checks for emails_file existence, permissions, etc.
```

**Test Strategy:**

Create unit tests for `DatabaseConfig` to verify its instantiation with valid and invalid parameters. Test that configuration validation logic correctly identifies missing or incorrect paths. Ensure default configurations can be created and are valid.

## Subtasks

### 64.1. Design `DatabaseConfig` Pydantic model with core properties

**Status:** pending  
**Dependencies:** None  

Define the initial `DatabaseConfig` Pydantic model, including essential properties like `data_dir` and `emails_file`, ensuring proper type hinting and `Field` definitions.

**Details:**

Create the `DatabaseConfig` class inheriting from `pydantic.BaseModel`. Define `data_dir` as `Path` and `emails_file` as `Path`, adding descriptive `Field` comments as shown in the example. Include `arbitrary_types_allowed = True` in `Config`.

### 64.2. Implement Pydantic's built-in validation for `DatabaseConfig`

**Status:** pending  
**Dependencies:** 64.1  

Utilize Pydantic's native validation capabilities to ensure basic type correctness and enforce any constraints on fields within the `DatabaseConfig` model.

**Details:**

Ensure all fields in `DatabaseConfig` are correctly type-hinted so Pydantic handles type coercion and validation automatically. Verify that `Path` types are correctly handled.

### 64.3. Develop custom validation methods for `DatabaseConfig` paths

**Status:** pending  
**Dependencies:** 64.2  

Add custom validation logic to `DatabaseConfig` to verify the existence and type (e.g., directory vs. file) of specified paths.

**Details:**

Implement `@model_validator` or `@field_validator` methods within `DatabaseConfig` to check if `data_dir` is an existing directory and if `emails_file` is an existing file, raising `ValueError` for invalid paths.

### 64.4. Implement configuration loading from environment variables

**Status:** pending  
**Dependencies:** 64.3  

Create a class method `from_env()` within `DatabaseConfig` to populate its fields by reading values from environment variables.

**Details:**

Implement `DatabaseConfig.from_env()` using `os.getenv()` to retrieve configuration values. Provide sensible default values if environment variables are not set. Map environment variable names (e.g., `DB_DATA_DIR`) to model fields.

### 64.5. Develop configuration loading from JSON/YAML files

**Status:** pending  
**Dependencies:** 64.4  

Add methods to `DatabaseConfig` that enable loading configuration parameters from external JSON or YAML files.

**Details:**

Implement static or class methods like `from_json_file(filepath)` and `from_yaml_file(filepath)`. These methods should read the file, parse its content, and instantiate `DatabaseConfig` from the resulting dictionary. Use libraries like `json` and `pyyaml`.

### 64.6. Implement default value handling for all `DatabaseConfig` fields

**Status:** pending  
**Dependencies:** 64.5  

Ensure every field in `DatabaseConfig` has a clear default value or is explicitly marked as required, preventing configuration gaps.

**Details:**

Review all `DatabaseConfig` properties. For optional fields, assign default values directly or using `Field(default=...)`. For required fields, ensure they are specified without defaults or marked as `Field(...)`.

### 64.7. Create configuration factory functions for common scenarios

**Status:** pending  
**Dependencies:** 64.6  

Develop dedicated factory functions or class methods within `DatabaseConfig` to provide predefined configurations for development, testing, or production environments.

**Details:**

Implement methods such as `create_default_config()` or `for_testing()`, which return a `DatabaseConfig` instance with pre-set values suitable for specific use cases.

### 64.8. Configure `DatabaseConfig` for immutability

**Status:** pending  
**Dependencies:** 64.7  

Modify the `DatabaseConfig` Pydantic model to be immutable, preventing runtime modifications after instantiation.

**Details:**

Set `frozen = True` in the inner `Config` class of `DatabaseConfig`. This ensures that once an instance is created, its attributes cannot be changed.

### 64.9. Implement configuration serialization to dictionary/JSON

**Status:** pending  
**Dependencies:** 64.8  

Add methods to `DatabaseConfig` to serialize its instance into a standard Python dictionary or a JSON string.

**Details:**

Utilize Pydantic's `model_dump()` method to get a dictionary representation and `model_dump_json()` to get a JSON string. Ensure `Path` objects are correctly converted to strings for serialization.

### 64.10. Implement configuration deserialization from dictionary/JSON

**Status:** pending  
**Dependencies:** 64.9  

Enable `DatabaseConfig` to be instantiated directly from a Python dictionary or a JSON string.

**Details:**

Leverage Pydantic's ability to directly instantiate from a dictionary (`DatabaseConfig(**data_dict)`) or from a JSON string (`DatabaseConfig.model_validate_json(json_string)`). Ensure string paths are correctly parsed back into `Path` objects.

### 64.11. Refine `DatabaseConfig` schema for comprehensive type validation

**Status:** pending  
**Dependencies:** 64.10  

Review and enhance the `DatabaseConfig` Pydantic schema to include all necessary fields, their precise types, and any specific constraints beyond basic type hinting.

**Details:**

Inspect all global variables and configuration parameters currently in use for database management. Add them as fields to `DatabaseConfig`, ensuring correct type hints (e.g., `int`, `bool`, `str`, `Path`), and use `Field` for more specific validation like `min_length`, `pattern`, or custom `validator` decorators.

### 64.12. Implement robust error handling and reporting for `DatabaseConfig`

**Status:** pending  
**Dependencies:** 64.11  

Establish a consistent strategy for handling and reporting validation and loading errors related to `DatabaseConfig` to provide clear user feedback.

**Details:**

Wrap `DatabaseConfig` instantiation and loading methods in `try-except ValidationError` blocks. Implement custom exception types or use logging to provide detailed, actionable error messages for invalid configurations. Consider mapping Pydantic errors to more user-friendly messages.

### 64.13. Create unit tests for `DatabaseConfig` utilities

**Status:** pending  
**Dependencies:** 64.12  

Develop comprehensive unit tests to cover all aspects of `DatabaseConfig`, including its factory methods, serialization/deserialization, and error handling.

**Details:**

Consolidate and expand the unit tests created in previous subtasks into a dedicated test module for `DatabaseConfig`. Ensure full coverage of all public methods and properties, covering both valid and invalid scenarios.

### 64.14. Integrate `DatabaseConfig` object with `DatabaseManager` and related components

**Status:** pending  
**Dependencies:** 64.13  

Modify the `DatabaseManager` class and any other components that previously used global variables to accept and utilize the new `DatabaseConfig` object.

**Details:**

Update the `__init__` method of `DatabaseManager` to take a `DatabaseConfig` instance as an argument. Replace all direct references to global variables (e.g., `DATA_DIR`, `EMAILS_FILE`) with attributes from the passed `DatabaseConfig` object. Adapt other modules that depend on these globals.

### 64.15. Document `DatabaseConfig` usage patterns and maintenance procedures

**Status:** pending  
**Dependencies:** 64.14  

Create detailed documentation for `DatabaseConfig`, including examples of its usage, configuration loading, and guidelines for future maintenance and extension.

**Details:**

Add comprehensive docstrings to the `DatabaseConfig` class and its methods. Update the project's README or create a dedicated configuration documentation file outlining how to configure the application using environment variables, config files, and factory methods. Include guidelines for adding new configuration parameters.
