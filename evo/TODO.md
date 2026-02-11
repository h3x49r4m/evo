# TODO - Improvements for evo Project

## Completed (Previous Sprint)

All previous items completed:
- Integration Tests ✅
- LLM Integration ✅
- Vector Database ✅
- Error Logging ✅
- Configuration Management ✅
- Test Coverage Gaps ✅
- Exception Handling ✅
- Dependency Injection ✅
- Input Validation ✅
- Tool Registration Duplication ✅
- Nested Class Documentation ✅
- Async Cleanup Tests ✅
- Type Hints ✅
- Performance Optimization ✅
- Pattern Detection Optimization ✅
- Priority Configuration ✅
- Environment Configuration ✅
- Documentation Expansion ✅

---

## Current Sprint - Coverage Gaps (High Priority)

### 1. Action Layer Coverage
- **Status**: In Progress
- **Description**: Add tests for uncovered lines in `src/evo/action/__init__.py`:
  - Lines 11-12 - OpenAI API key configuration with environment variable
  - Lines 91, 93 - LLM plan action error handling paths
  - Lines 174, 177 - Tool execution error paths
- **Current Coverage**: 92%

### 2. Capability Registry Coverage
- **Status**: Pending
- **Description**: Add tests for uncovered lines in `src/evo/capability/__init__.py`:
  - Line 27 - Tool search index rebuild edge case
  - Line 48 - Empty search query handling
  - Lines 101, 105, 129 - Error validation paths
- **Current Coverage**: 94%

### 3. Config Module Coverage
- **Status**: Pending
- **Description**: Add tests for uncovered line in `src/evo/config.py`:
  - Line 102 - Config.get_all() method
- **Current Coverage**: 97%

### 4. Goal Engine Coverage
- **Status**: Pending
- **Description**: Add tests for uncovered lines in `src/evo/goal/__init__.py`:
  - Line 21 - Internal goal removal edge case
  - Line 38 - Internal goal listing
- **Current Coverage**: 95%

### 5. Memory System Coverage
- **Status**: Pending
- **Description**: Add tests for uncovered lines in `src/evo/memory/__init__.py`:
  - Lines 10-11 - ChromaDB import handling
  - Line 134 - EpisodicMemory cleanup edge case
- **Current Coverage**: 95%

### 6. Safety Layer Coverage
- **Status**: Pending
- **Description**: Add tests for uncovered line in `src/evo/safety/__init__.py`:
  - Line 146 - Storage usage tracking reset
- **Current Coverage**: 99%

### 7. Validation Module Coverage
- **Status**: Pending
- **Description**: Add tests for uncovered line in `src/evo/validation.py`:
  - Line 74 - Goal name validation
- **Current Coverage**: 97%

---

## Medium Priority

### 8. Logging Configuration ✅
- **Status**: Completed
- **Description**: Improve logging: Config.LOG_LEVEL is defined but not used by logging module
  - Apply Config.LOG_LEVEL to logger configuration
  - Add Config.LOG_FORMAT to logger configuration

### 9. Handler Integration Tests ✅
- **Status**: Completed
- **Description**: Add integration test coverage for handler module
  - Added end-to-end tests for UserHandler workflow
  - Added end-to-end tests for SelfHandler workflow
  - Added cross-handler integration tests

### 10. OpenAI Streaming
- **Status**: Pending
- **Description**: Improve OpenAI integration with streaming response support
  - Add streaming option to `_llm_plan_action()`
  - Better error handling for API failures

### 11. OpenAI Retry with Backoff
- **Status**: Pending
- **Description**: Add retry with exponential backoff for OpenAI API calls
  - Currently has basic retry only in tool execution
  - Add to LLM plan action calls

---

## Low Priority

### 12. Type Hints for Internal Dictionary
- **Status**: Pending
- **Description**: Add type hints for internal `_internal_tools` dictionary in ActionLayer
  - Currently defined inline without type annotation

---

## Notes

- Current test coverage: 97% (268 tests passing, 19 lines missing)
- Required coverage threshold: 90%
- Architecture compliance: 100% (all 20 components implemented)
- Performance optimizations: Tool search O(n)→O(1), Pattern detection O(n*m)→O(n)
- Package manager: uv (not .venv)
- TDD workflow: tdd-enforce skill active