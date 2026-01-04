# Task ID: 37

**Title:** Refactor EmailProfileManager API to ID-based Interface with Backward Compatibility

**Status:** pending

**Dependencies:** 23, 28

**Priority:** medium

**Description:** Refactor the `EmailProfileManager` API from file-path-based to ID-based, maintaining backward compatibility by deprecating old methods, adding export/import utilities, and documenting the new serialization format.

**Details:**

This task involves a significant refactoring of the `EmailProfileManager` in `src/backend/email_profile/email_profile_manager.py` to move from direct file path manipulation and profile naming conventions to a robust ID-based system utilizing the `id` field within `ProfileMetadata`. This refactoring must also ensure backward compatibility for existing usages and provide clear migration paths.

**

**Test Strategy:**

A comprehensive test strategy is crucial to ensure the correctness of the refactored API, proper deprecation warnings, and continued backward compatibility.

1.  **Unit Tests for New ID-based API:**
    *   Create a new test file, e.g., `src/tests/backend/email_profile/test_email_profile_manager_v2.py`.
    *   Test `get_profile(profile_id)`: Verify loading an existing profile, and correctly handling a non-existent profile (e.g., raising `ProfileNotFoundError`).
    *   Test `save_profile(profile: EmailProfileConfig)`: Verify creation of new profiles, updating existing profiles, and ensuring `profile.metadata.id` dictates the filename.
    *   Test `delete_profile(profile_id)`: Verify successful deletion and error handling for non-existent profiles.
    *   Test `list_available_profiles()`: Verify it correctly discovers profiles in the default directory and returns `ProfileMetadata` mapped by ID.
    *   Test profile lifecycle: Create, save, load, modify, save, delete, verify deletion.

2.  **Unit Tests for Deprecated Methods (Backward Compatibility):**
    *   Using `pytest.warns(DeprecationWarning)` context manager, ensure `DeprecationWarning` is issued when calling `load_profile(name)`, `save_profile(profile, name)`, `load_profile_from_path`, and `save_profile_to_path`.
    *   Verify that `load_profile(name)` and `save_profile(profile, name)` still correctly interact with profiles stored in the default `_profiles_dir` (assuming `name` is the `id`).
    *   Ensure `load_profile_from_path` and `save_profile_to_path` continue to function as expected for custom paths, despite being deprecated.

3.  **Unit Tests for Export/Import Utilities:**
    *   Test `export_profile(profile_id, target_path)`: Export a known profile to a temporary custom path, then verify the content of the exported file.
    *   Test `import_profile(source_path)`: Import a valid profile from a temporary custom path, ensure the returned `EmailProfileConfig` object is correct. Test importing from a non-existent path or an invalid JSON format.
    *   Verify that an imported profile can be subsequently saved using the new `save_profile(profile)` method.

4.  **Serialization Format Validation:**
    *   Create test profiles with various data complexities (multiple accounts, nested custom settings, missing optional fields) and ensure they can be saved and loaded without data loss or corruption, adhering to the documented JSON schema.
    *   Specifically test the handling of `profile.metadata.id` during serialization and deserialization.

5.  **Documentation Review:**
    *   Manually review `docs/profile_serialization_format.md` (and any related migration guide) for clarity, accuracy, completeness, and adherence to the specified JSON structure and Pydantic V2 details.
    *   Verify code examples in the migration guide are correct and functional.

6.  **Integration Testing (if applicable):**
    *   Run any existing integration tests that rely on `EmailProfileManager` to ensure the refactoring hasn't introduced regressions. Update these tests to use the new ID-based API where appropriate, demonstrating the migration path.

## Subtasks

### 37.1. Standardize Profile Storage Location by ID and Update `_get_profile_path`

**Status:** pending  
**Dependencies:** None  

Modify `EmailProfileManager._get_profile_path` to use the profile's unique `id` (from `ProfileMetadata`) for generating file paths. Ensure profiles are stored as `_profiles_dir / f'{profile_id}.json'` by default.

**Details:**

Locate the `_get_profile_path` method in `src/backend/email_profile/email_profile_manager.py`. Update its signature to accept `profile_id: str` and modify its internal logic to construct the file path using this ID. This change implicitly affects where new profiles will be saved by ID-based methods.

### 37.2. Implement Core ID-based Profile CRUD API (`get`, `save`, `delete`, `list`)

**Status:** pending  
**Dependencies:** 37.1  

Develop new ID-based methods: `get_profile(profile_id)`, `save_profile(profile: EmailProfileConfig)`, `delete_profile(profile_id)`, and update `list_available_profiles()` to use the new ID-based storage and identification. Ensure `ProfileNotFoundError` is raised where appropriate.

**Details:**

In `EmailProfileManager`, implement `get_profile` to load a profile by ID, `save_profile` (which takes an `EmailProfileConfig` object and uses its `metadata.id` for saving), and `delete_profile` to remove a profile file by ID. Update `list_available_profiles` to scan `_profiles_dir` for `.json` files, load only their `ProfileMetadata` (or `id` and `name`), and return a dictionary mapping profile IDs to `ProfileMetadata` objects.

### 37.3. Deprecate Legacy Path-based API Methods with Warnings

**Status:** pending  
**Dependencies:** None  

Modify existing path-based `load_profile(profile_name)`, `save_profile(profile, profile_name)`, `load_profile_from_path`, and `save_profile_to_path` methods by adding `DeprecationWarning`s. Internally, delegate to the new ID-based API or retain existing functionality with clear warnings.

**Details:**

For `load_profile(profile_name)` and `save_profile(profile: EmailProfileConfig, profile_name: str)`, add `DeprecationWarning`s and internally delegate to the new `get_profile` (assuming `profile_name` is treated as `profile_id`) and `save_profile(profile)`. For `load_profile_from_path(file_path: Path)` and `save_profile_to_path(profile: EmailProfileConfig, file_path: Path)`, add `DeprecationWarning`s and maintain their existing functionality while signaling their replacement by new import/export utilities.

### 37.4. Implement Profile Export and Import Utilities for Custom Locations

**Status:** pending  
**Dependencies:** None  

Create `export_profile(profile_id: str, target_path: Path)` to save a profile to a user-specified path and `import_profile(source_path: Path) -> EmailProfileConfig` to load a profile from a custom path, validating the data without automatically saving it to the manager.

**Details:**

Implement `export_profile` in `EmailProfileManager` which uses `get_profile(profile_id)` to retrieve a profile and then saves its `model_dump_json()` representation to the `target_path`, ensuring parent directories exist. Implement `import_profile` which reads a JSON file from `source_path`, validates its content against `EmailProfileConfig` using `model_validate_json()` (from Pydantic V2), and returns the instance without affecting the manager's default storage.

### 37.5. Document New `EmailProfileConfig` Serialization Format

**Status:** pending  
**Dependencies:** None  

Create a new Markdown file at `docs/profile_serialization_format.md` detailing the expected JSON structure for `EmailProfileConfig`, `ProfileMetadata`, `EmailAccountConfig`, and `AgentConfig`. Emphasize `metadata.id` as the primary unique identifier.

**Details:**

Create `docs/profile_serialization_format.md`. Include clear descriptions and JSON examples for `EmailProfileConfig` and its nested Pydantic models. Explicitly state the role of `metadata.id` for profile identification and mention that Pydantic V2's `model_dump(mode='json')` is the recommended method for compliant JSON serialization.

### 37.6. Develop Migration Guide for Custom Profile Storage Usage

**Status:** pending  
**Dependencies:** 37.3, 37.4  

Create a dedicated migration guide (e.g., in `docs/migration_guides/profile_storage_migration.md` or a section within `docs/profile_serialization_format.md`) explaining how to transition from legacy `load_profile_from_path`/`save_profile_to_path` calls to using the new `import_profile`, `export_profile`, and ID-based manager methods.

**Details:**

Author a comprehensive guide that provides clear instructions and practical code examples for users to migrate their existing custom profile storage logic. Detail how to use `import_profile` to load profiles from arbitrary locations, `export_profile` to save them, and how to integrate these with the new ID-based `save_profile`/`get_profile` methods for default manager interactions.

### 37.7. Perform Final Code Review, Refinement, and Cleanup

**Status:** pending  
**Dependencies:** 37.1, 37.3, 37.4  

Conduct a comprehensive review of all implemented changes, ensure all necessary imports are in place, update `__init__.py` files if new modules or sub-packages were created, and remove any dead code, unused imports, or unnecessary complexity introduced during the refactoring process.

**Details:**

Thoroughly review `src/backend/email_profile/email_profile_manager.py` and any other affected files. Verify that `
