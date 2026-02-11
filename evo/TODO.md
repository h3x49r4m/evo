# TODO - Improvements for evo Project

## Critical Priority

### 1. Integration Tests
- **Status**: `tests/integration/` directory is empty
- **Description**: Add end-to-end integration tests for all documented flows:
  - Responsive Mode Flow
  - Autonomous Mode Flow
  - Hybrid Mode Flow
  - Safety Mode Flow
- **Reference**: `docs/steps.md`

### 2. LLM Integration
- **Status**: Not implemented
- **Description**: Implement OpenAI API integration in ActionLayer's `plan_action()` method
- **Current**: Uses simple planner instead of LLM-based action planner as specified in architecture
- **Reference**: `src/evo/action/__init__.py`

### 3. Vector Database
- **Status**: Mock implementation
- **Description**: Replace in-memory `_experiences` dict with actual `chromadb.Client()` for semantic search
- **Current**: MemorySystem uses dictionary instead of true vector database
- **Reference**: `src/evo/memory/__init__.py`

## High Priority

### 4. Error Logging
- **Status**: Not implemented
- **Description**: Add structured logging using Python's `logging` module for:
  - Mode transitions
  - Safety violations
  - Critical errors
  - Action execution results

### 5. Configuration Management
- **Status**: Magic numbers throughout code
- **Description**: Extract magic numbers to configuration file or constants module:
  - `0.1` - retry delay (action/__init__.py:52)
  - `0.5` - default skill level (capability/__init__.py)
  - `3600` - time limit (safety/__init__.py)
  - `107374182400` - storage limit (safety/__init__.py)
  - `1000` - iteration limit (safety/__init__.py)

### 6. Test Coverage Gaps
- **Status**: 5 lines uncovered in safety layer
- **Description**: Add tests for uncovered lines in `src/evo/safety/__init__.py`:
  - Line 66 - user override edge cases
  - Line 77 - resource limit boundary conditions
  - Line 88 - error handling paths
  - Line 109 - time tracking edge cases
  - Line 130 - storage usage validation

### 7. Exception Handling
- **Status**: Bare exception handling
- **Description**: Replace `except Exception:` with `except Exception as e:` and log error details
- **Location**: `src/evo/action/__init__.py:48`

## Medium Priority

### 8. Dependency Injection
- **Status**: Separate instances
- **Description**: Implement dependency injection pattern for shared memory system across components
- **Current**: Components create their own MemorySystem instances

### 9. Input Validation
- **Status**: No validation
- **Description**: Add validation for:
  - Capability/skill levels (0.0 to 1.0 bounds)
  - Goal names (null/empty string checks)
  - Tool names (valid identifier checks)

### 10. Tool Registration Duplication
- **Status**: Duplicate implementations
- **Description**: Consolidate tool registration to single registry
- **Current**: Both ActionLayer and CapabilityRegistry register tools

### 11. Nested Class Documentation
- **Status**: Missing docstrings
- **Description**: Add class-level docstrings for nested classes in MemorySystem:
  - WorkingMemory
  - EpisodicMemory
  - SemanticMemory

### 12. Async Cleanup Tests
- **Status**: Not tested
- **Description**: Add tests that verify `cleanup()` properly releases resources

## Low Priority

### 13. Type Hints
- **Status**: Generic `Any` types
- **Description**: Replace `Any` with more specific types where possible:
  - `Dict[str, Union[str, int, float]]`
  - Custom TypedDict classes

### 14. Performance Optimization
- **Status**: O(n) linear search
- **Description**: Optimize `CapabilityRegistry.search_tools()` for better performance with many tools

### 15. Pattern Detection Optimization
- **Status**: O(n*m) complexity
- **Description**: Optimize FeedbackLoop pattern detection algorithm

### 16. Priority Configuration
- **Status**: Hardcoded values
- **Description**: Make PerceptionGateway.PRIORITY_MAP configurable

### 17. Environment Configuration
- **Status**: Single environment
- **Description**: Add environment variable support via `python-dotenv`:
  - Development
  - Staging
  - Production

### 18. Documentation Expansion
- **Status**: Minimal docstrings
- **Description**: Expand module-level docstrings with:
  - Usage examples
  - Component interaction patterns
  - Common use cases

---

## Notes

- Current test coverage: 98.02% (353 statements, 7 missed)
- Total tests: 133
- Architecture compliance: 100% (all 20 components implemented)