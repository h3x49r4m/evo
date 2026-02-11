# Implementation Steps

## Approach Summary

### 1. Activate Skills First
- **architecture-check**: Will verify implementation aligns with the architecture doc
- **tdd-enforce**: Will enforce test-first development with red-green-refactor cycle

### 2. Project Structure & Tech Stack
- **Language**: Python (using `uv` for package management)
- **Structure**: Following the architecture's component hierarchy
  - `src/` - Core implementation modules
  - `tests/` - Test files (TDD-first: tests before implementation)
  - `tests/integration/` - Integration tests for flows

### 3. Development Order (Bottom-Up)

**Layer 1: Core Infrastructure**
1. Memory System (working, episodic, semantic)
2. Capability Registry (tools, skills, knowledge tracking)
3. Safety & Constraints Layer (hard-coded boundaries)

**Layer 2: Decision & Processing**
4. Perception Gateway (input routing/prioritization)
5. Decision Engine (mode selector: responsive/autonomous)
6. Goal Engine (external + internal goals, drives)

**Layer 3: Action & Learning**
7. Action Layer (action planner, tool executor)
8. Feedback Loop (observation processor, memory manager)
9. Metacognition Layer (reflection, self-model update)
10. Exploration Engine (novelty detection, purpose synthesis)

**Layer 4: Integration**
11. User Handler & Self Handler
12. Integration tests for all flows

### 4. TDD Workflow Per Component
1. Write failing test → **Red**
2. Write minimal implementation → **Green**
3. Refactor → **Refactor**
4. Verify with `tdd-enforce` skill
5. Verify with `architecture-check` skill

### 5. Key Design Decisions
- **LLM Integration**: Use OpenAI API for decision/action planning
- **Vector DB**: Use chromadb for episodic memory (semantic search)
- **Async**: Use asyncio for concurrent processing
- **State Management**: Centralized state object passed through layers

### 6. Safety First
- Implement hard constraints in Safety Layer before any other component
- User override mechanism as the first implementation
- Resource limits (time, compute, storage) with strict enforcement

### 7. Continuous Verification
After each major component:
- Run `tdd-enforce` → ensure TDD compliance
- Run `architecture-check` → ensure architectural alignment