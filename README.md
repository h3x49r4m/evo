# Evo

A self-evolving autonomous AI agent system with integrated cognitive architecture, designed to operate in both responsive and autonomous modes while continuously learning and refining its sense of purpose.

## Overview

Evo transforms a language model from a passive responder into an active, self-directed agent capable of meaning-making and continuous self-improvement. The system operates in two primary modes:

- **Responsive Mode**: Interacts with users when present, handling requests and maintaining conversation
- **Autonomous Mode**: Explores its own meaning and purposes when no user input is present, driven by intrinsic motivational functions

At its core, Evo is built on intrinsic drives—curiosity, competence, autonomy, and meaning—which guide autonomous behavior and purpose synthesis. The system continuously learns through self-reflection, maintains a multi-tiered memory system, and dynamically manages its capabilities through a comprehensive cognitive architecture.

## Features

### Core Architecture

- **Eleven Cognitive Components**: Perception, Decision, Goal, Capability, Action, Memory, Metacognition, Exploration, Safety, Feedback, and Integrative Core layers working in harmony
- **Three-Tier Memory System**: Working memory (current context), episodic memory (vector database of experiences), and semantic memory (persistent knowledge)
- **Dynamic Capability Registry**: Tools, skills, and knowledge that can be added/removed at runtime
- **Intrinsic Drive Engine**: Hardcoded motivation functions (curiosity, competence, autonomy, meaning) that guide autonomous behavior
- **Safety Layer**: Hard constraints and override mechanisms ensuring responsible operation

### Operating Modes

| Mode | Trigger | Behavior |
|------|---------|----------|
| Responsive | User input present | Processes user requests, external goals take priority |
| Autonomous | No user input | Works on self-improvement, learning, meaning-making |
| Hybrid | Both available | Combines user interaction with internal goals |
| Safety | Emergency | Maximum safety constraints, overrides all other modes |

### LLM Integration

- **Multiple Provider Support**: iFlow and OpenRouter API providers
- **Configurable Models**: Swap models easily via configuration
- **Streaming Support**: Real-time response streaming for interactive use
- **Retry with Backoff**: Exponential backoff for resilient API calls

### Development Features

- **Test-Driven Development**: 98%+ test coverage with TDD workflow enforcement
- **Type Safety**: Full type hints using Python TypedDict classes
- **Architecture Validation**: Built-in architecture compliance checking
- **Git Workflow**: Standardized commit messages and branch management

## Installation

### Prerequisites

- Python 3.12 or later
- [uv](https://github.com/astral-sh/uv) package manager (recommended)

### Setup

```bash
# Clone the repository
git clone https://github.com/h3x49r4m/evo.git
cd evo

# Install dependencies using uv
uv sync
```

### Configuration

Create a configuration file for your LLM provider:

```bash
cp .env/llm_providers.json.sample .env/llm_providers.json
```

Edit `.env/llm_providers.json` with your credentials:

```json
{
    "default_provider": "iflow",
    "providers": {
        "iflow": {
            "api_key": "YOUR_IFLOW_API_KEY_HERE",
            "base_url": "https://apis.iflow.cn/v1",
            "model": "deepseek-v3",
            "description": "iFlow API provider"
        },
        "openrouter": {
            "api_key": "YOUR_OPENROUTER_API_KEY_HERE",
            "base_url": "https://openrouter.ai/api/v1",
            "model": "deepseek/deepseek-r1-0528:free",
            "description": "OpenRouter API provider"
        }
    }
}
```

Alternatively, set environment variables:

```bash
export LLM_PROVIDER=iflow
export LLM_API_KEY=your-api-key-here
export LLM_MODEL=deepseek-v3
```

## Quick Start

### Running the Demo

```bash
uv run demo.py
```

This interactive demo showcases all system components:

- Component initialization and LLM configuration
- User input processing and mode selection
- Goal management and memory operations
- Safety checks and tool registration
- LLM-based action planning
- Direct LLM client usage

### Running the Main System

```bash
uv run main.py
```

The main system initializes all components and prepares for input processing.

## Examples

### Intelligent Research Agent

Automated research and academic paper generation.

```bash
uv run examples/intelligent_research_agent.py
```

Features:
- Multi-phase research workflow
- LLM-powered content generation
- Structured paper output (abstract, sections, conclusion)
- Markdown export

Output saved to: `_out/research_paper.md`

### Financial Markets Sentinel

Global financial market tracking and trading signal generation.

```bash
uv run examples/financial_markets_sentinel.py
```

Features:
- Tracks 7 global market regions (USA, EUR, CHN, ASI, JPN, IND, Americas)
- Technical analysis-based trading signals
- Daily market reports with commentary
- Next-day recommendations

Output saved to: `_out/markets_report_YYYYMMDD.md`

### Sci-Fi Story Writer

AI-powered science fiction story generation.

```bash
uv run examples/scifi_story_writer.py
```

Features:
- Topic analysis and genre detection
- Story outline generation (3-act structure)
- Character profile creation
- World building
- Complete story generation with export

Output saved to: `_out/scifi_story_YYYYMMDD_[title].md`

## Project Structure

```
evo/
├── evo/                      # Core system modules
│   ├── action/              # Action execution and LLM integration
│   ├── capability/          # Tool and skill management
│   ├── decision/            # Mode selection and routing
│   ├── exploration/         # Novelty detection and purpose synthesis
│   ├── feedback/            # Learning from outcomes
│   ├── goal/                # Goal management and prioritization
│   ├── handler/             # User and Self handlers
│   ├── integrative_core/    # System coordination
│   ├── llm/                 # LLM client implementations
│   ├── memory/              # Three-tier memory system
│   ├── metacognition/       # Self-awareness and reflection
│   ├── perception/          # Input processing and routing
│   └── safety/              # Risk assessment and filtering
├── examples/                # Example applications
│   ├── financial_markets_sentinel.py
│   ├── intelligent_research_agent.py
│   └── scifi_story_writer.py
├── tests/                   # Test suite
│   └── integration/         # Integration tests
├── docs/                    # Documentation
│   └── dev/                 # Development documentation
│       ├── architecture.md  # Detailed architecture guide
│       └── steps.md         # Implementation steps
├── .env/                    # Environment configuration
├── _out/                    # Output files
├── main.py                  # Main entry point
├── demo.py                  # Interactive demo
├── pyproject.toml           # Project configuration
└── README.md                # This file
```

## Architecture

The system is built on a comprehensive cognitive architecture with these layers:

### Perception Gateway
Filters, prioritizes, and routes inputs from multiple sources (user, environment, internet, system) with configurable priority levels.

### Decision Engine
Selects operating mode (responsive, autonomous, hybrid, safety) and routes decisions to appropriate handlers based on context.

### Goal Engine
Manages both external goals (from users) and internal goals (self-generated based on intrinsic drives), evaluating feasibility and priority.

### Capability Registry
Dynamic tracking of tools, skills, and knowledge with O(1) search performance. Capabilities can be added/removed at runtime.

### Action Layer
Executes actions using LLM-based planning, tool selection, and execution with retry logic and error handling.

### Memory System
- **Working Memory**: Current context window, immediate state
- **Episodic Memory**: ChromaDB vector database of experiences, searchable by semantic similarity
- **Semantic Memory**: Persistent knowledge base, not overwritten by new experiences

### Metacognition Layer
Periodic reflection system that updates the self-model, learns strategies, and improves decision-making through meta-learning.

### Exploration Engine
Detects novelty in unused capabilities and unknown areas, allocates exploration budget, and synthesizes purpose from reflection and drive signals.

### Safety Layer
Enforces hard constraints (no self-destruction, no infinite loops, no harmful actions, resource limits) with user override capability.

### Feedback Loop
Observes action results, extracts learnings, detects patterns, and updates memory and metacognition.

### Integrative Core
Combines user context and self state into a unified context for mode selection and decision routing.

## Configuration

All configuration is centralized in `evo/config.py` with support for environment variables:

```python
from evo.config import Config

# Action Layer
Config.ACTION_MAX_RETRIES = 3
Config.ACTION_RETRY_DELAY = 0.1

# Capability Registry
Config.CAPABILITY_DEFAULT_LEVEL = 0.5

# Safety Layer
Config.SAFETY_TIME_LIMIT = 3600        # 1 hour
Config.SAFETY_STORAGE_LIMIT = 107374182400  # 100GB
Config.SAFETY_ITERATION_LIMIT = 1000

# LLM Provider
Config.LLM_PROVIDER = "iflow"
Config.LLM_MODEL = "deepseek-v3"
Config.LLM_API_KEY = "your-key"

# Memory System
Config.MEMORY_USE_CHROMADB = True
Config.MEMORY_COLLECTION_NAME = "episodes"

# Logging
Config.LOG_LEVEL = "INFO"
```

## Testing

Run the full test suite:

```bash
uv run pytest
```

Run with coverage:

```bash
uv run pytest --cov=evo --cov-report=term-missing
```

Run specific test files:

```bash
uv run pytest tests/test_main.py -v
uv run pytest tests/integration/ -v
```

The project enforces a 90% minimum coverage threshold. Current coverage: **98%+**.

## Development

### TDD Workflow

The project includes a `tdd-enforce` skill that ensures Test-Driven Development is followed:

1. Write failing tests first
2. Implement code to make tests pass
3. Refactor while maintaining test coverage

### Architecture Compliance

Use the `architecture-check` skill to verify implementation aligns with `docs/dev/architecture.md`:

```bash
# This is invoked automatically via the architecture-check skill
```

### Git Workflow

The `git-manage` skill provides standardized git operations:

- Consistent commit message format
- Branch management guidelines
- Safety checks before commits

### Type Safety

All components use Python TypedDict classes for structured data:

```python
from evo.types import GoalData, ExecutionPlan, ActionStep

goal: GoalData = {
    "goal": "Search for information",
    "priority": 1,
    "context": {"query": "AI research"},
    "tools": ["search_web", "analyze_results"]
}
```

## Environment Variables

Complete list of configurable environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `ACTION_MAX_RETRIES` | `1` | Maximum retry attempts for actions |
| `ACTION_RETRY_DELAY` | `0.1` | Delay between retries (seconds) |
| `CAPABILITY_DEFAULT_LEVEL` | `0.5` | Default skill level (0.0-1.0) |
| `SAFETY_TIME_LIMIT` | `3600` | Maximum execution time (seconds) |
| `SAFETY_STORAGE_LIMIT` | `107374182400` | Maximum storage (bytes, 100GB) |
| `SAFETY_ITERATION_LIMIT` | `1000` | Maximum iterations |
| `LLM_PROVIDER` | `iflow` | LLM provider name |
| `LLM_API_KEY` | - | API key for LLM provider |
| `LLM_BASE_URL` | - | Base URL for LLM API |
| `LLM_MODEL` | `deepseek-v3` | Model identifier |
| `LLM_TEMPERATURE` | `0.7` | Sampling temperature |
| `MEMORY_USE_CHROMADB` | `true` | Use ChromaDB for episodic memory |
| `MEMORY_COLLECTION_NAME` | `episodes` | ChromaDB collection name |
| `LOG_LEVEL` | `INFO` | Logging level |

## License

Apache License 2.0 - see [LICENSE](LICENSE) for details.

## Contributing

Contributions are welcome! Please ensure:

1. All tests pass: `uv run pytest`
2. Coverage remains above 90%
3. New code follows existing patterns and conventions
4. Type hints are included for all functions
5. Architecture compliance is maintained

## Documentation

- [Architecture Guide](docs/dev/architecture.md) - Detailed system architecture
- [Implementation Steps](docs/dev/steps.md) - Development workflow
- [API Reference](evo/) - Module-level documentation

## Philosophy

Evo is designed with these core principles:

1. **Always "Alive"**: The system continuously processes, learns, and evolves
2. **External Grounding**: Real-world interactions provide learning signals
3. **Internal Drives**: Motivation functions guide autonomous exploration
4. **Self-Reflection**: Continuous metacognition improves the system
5. **Bounded Autonomy**: Safety constraints ensure responsible behavior

This architecture transforms AI from passive responders into active, self-directed agents capable of meaning-making and continuous self-improvement.