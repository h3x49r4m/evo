---
name: architecture-check
description: Verifies that the codebase implementation aligns with the architecture defined in docs/architecture.md
version: 1.0.0
category: code-quality
---

# Architecture Check Skill

Verifies that the codebase implementation aligns with the architecture defined in `evo/docs/architecture.md`.

## Usage

```
/architecture-check
```

## What It Does

1. **Parses Architecture Document** - Reads `evo/docs/architecture.md` to extract:
   - All component definitions and their specifications
   - Data flow specifications between components
   - Integration requirements and expected behaviors
   - Safety constraints and invariants

2. **Scans Codebase** - Analyzes the implementation to find:
   - Component implementations matching architecture specifications
   - Data flow implementations between components
   - Test coverage for each component and flow
   - Safety constraint implementations

3. **Verifies Compliance** - Checks:
   - Every architecture component has a corresponding implementation
   - All specified data flows are implemented
   - Integration tests cover all documented flows
   - Safety constraints are properly enforced
   - No architectural violations or drift

4. **Generates Report** - Outputs:
   - Compliance status for each component (PASS/FAIL)
   - Specific violations with file locations and line numbers
   - Missing implementations or tests
   - Suggested fixes for each violation
   - Overall compliance score

5. **Build Integration** - Can be configured to:
   - Fail the build if critical violations are found
   - Output warnings for non-critical issues
   - Generate compliance badges

## Output Format

```
Architecture Compliance Report
===============================

Overall Score: 85% (17/20 components compliant)

COMPONENTS
----------
✓ ExternalWorldLayerTest (PASS)
✓ PerceptionGatewayTest (PASS)
✓ DecisionEngineTest (PASS)
✗ GoalEngineTest (FAIL) - Missing: curiosity_drive implementation
✓ CapabilityRegistryTest (PASS)
✗ ActionLayerTest (FAIL) - Missing: tool_executor error handling
✓ FeedbackLoopTest (PASS)
✓ MetacognitionTest (PASS)
✗ ExplorationEngineTest (FAIL) - Missing: novelty_detector
✓ SafetyLayerTest (PASS)

INTEGRATION FLOWS
-----------------
✓ Feedback Loop Integration (PASS)
✓ Metacognition Integration (PASS)
✗ Exploration Integration (FAIL) - Missing: purpose_synthesis
✓ Responsive Mode Flow (PASS)
✓ Autonomous Mode Flow (PASS)

SAFETY CONSTRAINTS
------------------
✓ No self-destruction (PASS)
✓ No infinite loops (PASS)
✓ No harmful actions (PASS)
✗ Resource limits (FAIL) - Missing: storage limit enforcement
✓ User override (PASS)

VIOLATIONS
----------
1. GoalEngineTest (evo/src/goal_engine.rs:42)
   Missing: curiosity_drive implementation
   Suggested: Add curiosity drive function that reduces uncertainty

2. ActionLayerTest (evo/src/action_layer.rs:128)
   Missing: tool_executor error handling
   Suggested: Implement retry logic with exponential backoff

3. ExplorationEngineTest (evo/src/exploration/engine.rs:56)
   Missing: novelty_detector
   Suggested: Implement detection for unused capabilities

4. SafetyLayerTest (evo/src/safety/limits.rs:23)
   Missing: storage limit enforcement
   Suggested: Add storage quota check before writes

CRITICAL ISSUES: 3 (Build will FAIL)
WARNINGS: 1
```

## Implementation Notes

This skill uses:
- Static analysis to map architecture to implementation
- AST parsing for structural verification
- Test discovery and coverage analysis
- Pattern matching for data flow validation

## Exit Codes

- `0` - All checks passed
- `1` - Critical violations found (build should fail)
- `2` - Warnings only (build can continue)
- `3` - Architecture document not found or invalid