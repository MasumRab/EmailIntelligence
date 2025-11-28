# Task ID: 33

**Title:** Add Deprecation Shims for Context Control Static Methods

**Status:** pending

**Dependencies:** 28

**Priority:** medium

**Description:** Implement backward compatibility shims for removed `context_control` static methods by providing deprecated static wrappers that instantiate and call their new instance-based alternatives, issuing a `DeprecationWarning` for each.

**Details:**

This task involves creating backward-compatible static methods within the `src/backend/context_control/context_control.py` module (or the relevant file where these classes are defined) that will wrap the corresponding new instance methods. This is crucial for smooth migration and to guide developers away from outdated static method usage.

1.  **Identify Target Methods and Their Instance Equivalents:**
    *   `BranchMatcher.find_profile_for_branch()` -> wraps `BranchMatcher(branch_name).find_profile_for_branch_instance()`
    *   `EnvironmentTypeDetector.determine_environment_type()` -> wraps `EnvironmentTypeDetector(env_vars).determine_environment_type_instance()`
    *   `ContextFileResolver.resolve_accessible_files()` -> wraps `ContextFileResolver(base_path).resolve_accessible_files_instance(patterns)`
    *   `ContextValidator.validate_context()` -> wraps `ContextValidator(context_data).validate_context_instance()`

2.  **Implement Deprecation Wrapper for Each Static Method:**
    *   For each of the identified static methods, modify or re-add it as a `staticmethod` that performs the following actions:
        a.  **Issue `DeprecationWarning`:** Use `warnings.warn()` to emit a `DeprecationWarning`. The message should clearly state that the static method is deprecated and advise on using the instance-based approach. Set `stacklevel=2` to ensure the warning points to the caller of the deprecated method.
            *   Example message structure: `f"Call to deprecated static method {ClassName}.{static_method_name}(). Instantiate `{ClassName}` and call `{instance_method_name}()` instead."`
        b.  **Instantiate the Class:** Based on the signature of the deprecated static method, extract the necessary arguments to instantiate the corresponding class. For example, for `BranchMatcher.find_profile_for_branch(branch_name)`, `branch_name` should be used to create `BranchMatcher(branch_name=branch_name)`.
        c.  **Call Instance Method:** Call the new instance method on the created object, passing any remaining arguments from the static method's original signature.
        d.  **Return Result:** Return the result of the instance method call.

3.  **Example Implementation Snippet (Illustrative for `BranchMatcher`):**
    ```python
    import warnings
    from typing import Optional # Assuming this is needed

    class BranchMatcher:
        def __init__(self, branch_name: str):
            self.branch_name = branch_name

        def find_profile_for_branch_instance(self) -> Optional[str]:
            # ... actual instance logic ...
            return "default_profile" # Placeholder

        @staticmethod
        def find_profile_for_branch(branch_name: str) -> Optional[str]:
            warnings.warn(
                f"Call to deprecated static method BranchMatcher.find_profile_for_branch(). "
                f"Instantiate `BranchMatcher` and call `find_profile_for_branch_instance()` instead.",
                DeprecationWarning, stacklevel=2
            )
            # Map static method arguments to constructor and instance method
            matcher_instance = BranchMatcher(branch_name=branch_name)
            return matcher_instance.find_profile_for_branch_instance()
    ```

4.  **Review Parameter Mapping:** Carefully analyze the argument signatures of the original static methods and their corresponding new instance methods and class constructors to ensure correct argument passing within the shims.

5.  **Documentation:** Add comments to the deprecated static methods indicating their deprecation and guiding towards the new usage pattern.

### Tags:
- `work_type:backward-compatibility`
- `work_type:refactoring`
- `component:context-control`
- `component:api-design`
- `scope:module-specific`
- `purpose:smooth-migration`
- `purpose:developer-experience`

**Test Strategy:**

A robust test strategy is essential to confirm the deprecation shims function as expected, both in terms of functionality and warning emission.

1.  **Unit Tests for Each Deprecated Static Method:**
    *   Create new test cases within `tests/backend/context_control/` (e.g., `test_context_control_deprecations.py`).
    *   For each of the four deprecated static methods, write a dedicated test.

2.  **Verify Functionality:**
    *   Inside each test, directly call the deprecated static method with appropriate arguments.
    *   Assert that the return value matches the expected output of the underlying instance method.

3.  **Verify DeprecationWarning Emission:**
    *   Utilize `pytest.warns(DeprecationWarning)` as a context manager to assert that the `DeprecationWarning` is raised when the static method is called.
    *   Optionally, assert that the warning message text contains the expected guidance for migration (e.g., mentioning the new instance method name).
    *   Example using `pytest`:
        ```python
        import pytest
        from src.backend.context_control.context_control import BranchMatcher

        def test_find_profile_for_branch_deprecation_shim():
            with pytest.warns(DeprecationWarning, match="Call to deprecated static method BranchMatcher.find_profile_for_branch().") as record:
                result = BranchMatcher.find_profile_for_branch(branch_name="feature/new-feat")
            assert len(record) == 1
            assert result == "default_profile" # Assuming "default_profile" is the expected result
        ```

4.  **Verify Stack Level of Warning:** Confirm that the warning reported by `pytest` (or manually by running the tests) correctly points to the test function making the deprecated call, not the shim itself, validating the `stacklevel=2` setting.

5.  **Integration with Existing Tests:** Briefly check if any existing tests currently call these static methods. While not the primary focus, ensure that these existing tests continue to pass, now potentially emitting warnings during their execution.

## Subtasks

### 33.1. Identify Target Context Control Methods and Map Arguments

**Status:** pending  
**Dependencies:** None  

Analyze the `context_control` module to precisely identify all static methods requiring deprecation shims and their corresponding new instance-based alternatives. Document the argument mapping from static method signatures to class constructors and instance method calls.

**Details:**

Focus on `BranchMatcher.find_profile_for_branch()`, `EnvironmentTypeDetector.determine_environment_type()`, `ContextFileResolver.resolve_accessible_files()`, and `ContextValidator.validate_context()`. For each identified static method, determine the exact parameters needed for class instantiation and subsequent instance method calls based on the static method's original arguments. This step involves carefully reviewing the signatures and constructor requirements.

### 33.2. Implement Deprecation Wrappers for Context Control Shims

**Status:** pending  
**Dependencies:** 33.1  

Create deprecated static wrappers for the identified `context_control` static methods. Each wrapper must instantiate the respective class, call its new instance-based alternative, and return the result. Crucially, each wrapper must issue a `DeprecationWarning` with a clear message and `stacklevel=2`.

**Details:**

For each target method in `src/backend/context_control/context_control.py` (or relevant file), modify or add the `@staticmethod` decorator. Inside the static method, implement the logic to: a) Issue a `DeprecationWarning` using `warnings.warn()` with `stacklevel=2` and a message advising instance-based usage. b) Instantiate the corresponding class using arguments derived from the static method's signature. c) Call the new instance method on the created object, passing any remaining necessary arguments. d) Return the result of the instance method call.

### 33.3. Develop Unit Tests for Context Control Deprecation Shims

**Status:** pending  
**Dependencies:** None  

Write comprehensive unit tests for each implemented deprecation shim. Tests must verify both the correct functional behavior of the shim (i.e., that it correctly calls the instance method and returns the expected result) and the proper emission of the `DeprecationWarning`, checking the warning message and `stacklevel`.

**Details:**

Create new test cases or add to existing ones within `tests/backend/context_control/`. For each shim, write a test function that: a) Asserts the correct `DeprecationWarning` is raised using `pytest.warns(DeprecationWarning, match='...')`. Ensure the warning message content is accurate and `stacklevel` is effectively 2. b) Mocks any external dependencies if necessary to isolate the shim's logic. c) Verifies that the shim correctly instantiates the target class and calls its instance method with the appropriate arguments. d) Confirms that the shim returns the expected result from the instance method call.

### 33.4. Update Documentation and Conduct Final Code Review

**Status:** pending  
**Dependencies:** None  

Add inline comments and docstrings to all newly implemented deprecated static methods, clearly indicating their deprecation status and guiding developers to use the new instance-based approach. Perform a final code review to ensure all shims are correctly implemented, warnings are precise, arguments are mapped accurately, and tests cover all cases.

**Details:**

For each deprecated static method, add a clear docstring explaining its deprecation and providing guidance on how to migrate to the instance-based alternative. Include inline comments where complex argument mapping or logic occurs. Conduct a comprehensive code review of all changes, paying close attention to: consistent `DeprecationWarning` messages, correct `stacklevel` usage, accurate argument passing between static method, constructor, and instance method, and thoroughness of unit tests. Ensure `src/backend/context_control/context_control.py` is updated as specified.
