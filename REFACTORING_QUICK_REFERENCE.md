# Refactoring Quick Reference: Static → Instance Methods

## Conversion Mapping

### 1. BranchMatcher
```python
# OLD (static)
profiles = BranchMatcher.find_profile_for_branch(branch_name, profiles)

# NEW (instance)
matcher = BranchMatcher()
profiles = matcher.find_profile_for_branch(branch_name, profiles)

# NEW (with DI)
controller = ContextController(branch_matcher=BranchMatcher())
# Accessed via: controller.branch_matcher
```

### 2. EnvironmentTypeDetector
```python
# OLD (static)
env = EnvironmentTypeDetector.determine_environment_type("main")

# NEW (instance)
detector = EnvironmentTypeDetector()
env = detector.determine_environment_type("main")

# NEW (with DI)
creator = ContextCreator(environment_detector=EnvironmentTypeDetector())
# Accessed internally
```

### 3. ContextFileResolver
```python
# OLD (static)
allowed = ContextFileResolver.resolve_accessible_files(profile)
blocked = ContextFileResolver.resolve_restricted_files(profile)

# NEW (instance)
resolver = ContextFileResolver()
allowed = resolver.resolve_accessible_files(profile)
blocked = resolver.resolve_restricted_files(profile)

# NEW (with DI)
creator = ContextCreator(file_resolver=ContextFileResolver())
# Accessed internally
```

### 4. ContextValidator
```python
# OLD (single validator, static)
result = ContextValidator.validate_context(context)

# NEW (multiple validators, instance)
validator = ContextValidator(config=config)
result = validator.validate_context(context)

# NEW (composite approach)
composite = CompositeValidator()
profile_result = composite.validate_profile(profile)
context_result = composite.validate_context(context)
compat_result = composite.validate_profile_context_compatibility(profile, context)
```

### 5. ProfileStorage
```python
# OLD (file-based API)
storage = ProfileStorage()
profile = storage.load_profile_from_file(Path("/path/to/profile.json"))
storage.save_profile_to_file(profile, Path("/path/to/profile.json"))
profile = storage.find_profile_by_id("my_profile")

# NEW (ID-based API)
storage = ProfileStorage()
profile = storage.load_profile("my_profile")
storage.save_profile(profile)  # Saves to: profiles_dir/my_profile.json
profile = storage.load_profile("my_profile")
```

### 6. ContextController
```python
# OLD (some DI)
controller = ContextController()
context = controller.get_context_for_branch("main")

# NEW (full DI)
controller = ContextController(
    storage=ProfileStorage(),
    context_creator=ContextCreator(),
    context_validator=ContextValidator(),
    branch_matcher=BranchMatcher()
)
context = controller.get_context_for_branch("main")

# With defaults (backward compatible)
controller = ContextController()  # All dependencies auto-created
context = controller.get_context_for_branch("main")
```

---

## Key Differences

| Aspect | Old | New |
|--------|-----|-----|
| **Method Type** | Static (@staticmethod, @classmethod) | Instance methods |
| **Instantiation** | No instances needed | Must create instances |
| **Dependencies** | Hardcoded imports | Injected parameters |
| **Testability** | Hard (can't mock) | Easy (inject mocks) |
| **Flexibility** | Limited | High (implement interfaces) |
| **Performance** | Fast (no instantiation) | Slower (creates objects) |
| **Backward Compat** | N/A | Legacy classes provided |

---

## Testing Examples

### Before (Hard to test):
```python
def test_environment_detection():
    env = EnvironmentTypeDetector.determine_environment_type("feature/new-feature")
    assert env == "development"
    # Can't mock, can't inject custom logic
```

### After (Easy to test):
```python
class MockEnvironmentDetector(IEnvironmentDetector):
    def determine_environment_type(self, branch_name: str) -> str:
        return "test-env"

def test_context_creation():
    mock_detector = MockEnvironmentDetector()
    creator = ContextCreator(environment_detector=mock_detector)
    context = creator.create_context(profile, "test-branch", "test-agent")
    assert context.environment_type == "test-env"
```

---

## Integration Checklist

When integrating context_control module into codebase:

- [ ] Search for all old static method calls
- [ ] Replace with instance method calls
- [ ] Update any code creating instances of these classes
- [ ] Add mock implementations of interfaces for tests
- [ ] Test with real and mock implementations
- [ ] Check for circular imports
- [ ] Verify config initialization order
- [ ] Test multi-threaded scenarios

---

## Migration Timeline

### Phase 1: Now (Refactoring complete)
- ✅ New DI-based architecture in place
- ✅ Legacy classes created for compatibility
- ⏳ No usage in codebase yet

### Phase 2: Integration (When module is used)
- Create test suite for context_control
- Update all imports and calls
- Add deprecation warnings to legacy classes
- Update documentation

### Phase 3: Cleanup (Future)
- Remove legacy classes
- Remove static method aliases
- Enforce pure DI pattern
- Celebrate architectural improvement

---

## Common Pitfalls

### 1. Forgetting to instantiate
```python
# ❌ WRONG - Still static
env = EnvironmentTypeDetector.determine_environment_type("main")

# ✅ CORRECT - Instance method
env = EnvironmentTypeDetector().determine_environment_type("main")
```

### 2. Creating new instances every call
```python
# ❌ INEFFICIENT - Creates new instance each time
for branch in branches:
    env = EnvironmentTypeDetector().determine_environment_type(branch)

# ✅ BETTER - Reuse instance
detector = EnvironmentTypeDetector()
for branch in branches:
    env = detector.determine_environment_type(branch)
```

### 3. Forgetting to inject dependencies
```python
# ❌ WRONG - Will use default
controller = ContextController(
    # Missing other dependencies!
    storage=ProfileStorage()
)

# ✅ CORRECT - Provide all or let defaults handle it
controller = ContextController(
    storage=ProfileStorage(),
    context_creator=ContextCreator(),
    context_validator=ContextValidator(),
    branch_matcher=BranchMatcher()
)

# ✅ OR USE DEFAULTS - If defaults are fine
controller = ContextController()
```

### 4. Not implementing interfaces correctly
```python
# ❌ WRONG - Doesn't inherit from interface
class CustomDetector:
    def determine_environment_type(self, branch_name: str) -> str:
        return "custom"

# ✅ CORRECT - Implements interface
class CustomDetector(IEnvironmentDetector):
    def determine_environment_type(self, branch_name: str) -> str:
        return "custom"
```

---

## Performance Considerations

### Static Methods (Old)
- No memory overhead
- Faster lookup (no instance)
- Less flexible

### Instance Methods with DI (New)
- Memory overhead per instance
- Slight lookup overhead
- More flexible, testable
- Can use singleton pattern for shared instances

### Optimization Suggestion
```python
# If creating many controller instances, use singleton or factory
class ContextControllerFactory:
    _instance = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = ContextController()
        return cls._instance

# Usage
controller = ContextControllerFactory.get_instance()
```
