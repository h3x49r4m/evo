# evo

An autonomous AI agent system with integrated cognitive architecture.

## Features

- **Autonomous Mode**: Run independently with self-directed goal execution
- **Cognitive Components**: Perception, Decision, Goal, Capability, Action, Memory, Metacognition, Exploration, Safety, Feedback
- **LLM Integration**: Support for multiple LLM providers (iFlow, OpenRouter)
- **Test-Driven Development**: Full test coverage with TDD workflow
- **Safety Layer**: Built-in safety checks and content filtering

## Examples

### Intelligent Research Agent
Automated research and academic paper generation.

```bash
uv run examples/intelligent_research_agent.py
```

### Financial Markets Sentinel
Global financial market tracking and trading signal generation.

```bash
uv run examples/financial_markets_sentinel.py
```

### Sci-Fi Story Writer
AI-powered science fiction story generation.

```bash
uv run examples/scifi_story_writer.py
```

## Installation

```bash
uv sync
```

## Configuration

Create `.env/llm_providers.json` for LLM configuration:

```json
{
  "provider": "iflow",
  "models": {
    "default": "deepseek-v3"
  },
  "api_keys": {
    "iflow": "your-api-key-here"
  }
}
```

See `.env/llm_providers.json.sample` for the full template.

## Running

### Autonomous Mode
```bash
uv run main.py --mode autonomous
```

### Demo
```bash
uv run demo.py
```

## Testing

```bash
uv run pytest
```

## Project Structure

```
evo/
├── evo/              # Core system modules
├── examples/         # Example applications
├── tests/            # Test suite
├── docs/             # Documentation
└── _out/             # Output files
```

## Architecture

The system is built on a cognitive architecture with these layers:

- **Perception Gateway**: Input processing and environmental awareness
- **Decision Engine**: Strategic planning and choice selection
- **Goal Engine**: Goal management and prioritization
- **Capability Registry**: Tool and skill management
- **Action Layer**: Execution and LLM integration
- **Memory System**: Knowledge storage and retrieval
- **Metacognition Layer**: Self-awareness and monitoring
- **Exploration Engine**: Discovery and learning
- **Safety Layer**: Risk assessment and filtering
- **Feedback Loop**: Learning and improvement
- **Integrative Core**: System coordination

## License

MIT