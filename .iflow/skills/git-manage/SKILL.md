---
name: git-manage
description: Provides standardized git operations for the evo project with safety checks and best practices
version: 1.0.0
category: development-process
---

# Git Management Skill

Provides standardized git operations for the evo project with safety checks and best practices.

## Usage

```
/git-manage <command> [options]
```

## Available Commands

### Status Check
```
/git-manage status
```
Shows git status with test results, coverage, and pending checks.

### Add Files
```
/git-manage add <files...>
```
Stage files for commit. Supports glob patterns.

### Commit
```
/git-manage commit <type>[:scope] <description>
```
Create a commit with conventional commit format.

**Types:**
- `feat` - New feature
- `fix` - Bug fix
- `refactor` - Code refactoring
- `test` - Adding/updating tests
- `docs` - Documentation
- `chore` - Maintenance tasks

**Examples:**
```
/git-manage commit feat: implement memory system
/git-manage commit fix: correct safety constraint check
/git-manage commit test: add integration tests for decision engine
```

### Commit with Auto-Detection
```
/git-manage commit -a <description>
```
Auto-detects scope from changed files.

### Push
```
/git-manage push [remote] [branch]
```
Push commits with pre-push validation.

### Branch Operations
```
/git-manage branch create <name>        # Create new branch
/git-manage branch switch <name>        # Switch to branch
/git-manage branch delete <name>        # Delete branch
/git-manage branch list                 # List branches
```

## Pre-Commit Checks

Before any commit, the skill runs:

1. **Test Suite** - `uv run pytest tests/ -v --cov`
2. **Architecture Check** - Invokes `architecture-check` skill
3. **TDD Enforcement** - Invokes `tdd-enforce` skill
4. **Coverage Verification** - Ensures ≥90% coverage

**Blocking Rules:**
- Any test failure → Block commit
- Critical architecture violations → Block commit
- Critical TDD violations → Block commit
- Coverage below 90% → Block commit

## Commit Standards

### Conventional Commit Format
```
<type>[optional scope]: <description>

[optional body]

[optional footer]
```

### Auto-Generated Message Template
```
<type>[<scope>]: <description>

Changes:
- List of affected files

Verification:
- Tests: <count> passed
- Coverage: <percentage>%
- Architecture: ✓ compliant
- TDD: ✓ compliant
```

## Safety Mechanisms

### Secrets Detection
Scans for common secret patterns before committing:
- API keys (`api_key`, `apikey`, `secret`)
- Tokens (`token`, `access_token`)
- Passwords (`password`, `passwd`)
- Private keys (`private_key`, `.pem`)

### Branch Protection
- Prevents direct commits to `main` without review
- Requires feature branch workflow for major changes
- Validates branch naming conventions (`feat/`, `fix/`, `refactor/`)

### Backup Before Destructive Ops
Before `reset --hard` or `clean -fd`:
- Creates backup stash
- Shows confirmation prompt
- Allows rollback

## Integration with Existing Skills

### Architecture Check
- Automatically invoked before each commit
- Blocks commits if critical violations found
- Report included in commit message

### TDD Enforcement
- Automatically invoked before each commit
- Blocks commits if TDD cycle incomplete
- Report included in commit message

## Exit Codes

- `0` - Success
- `1` - Tests failed
- `2` - Architecture violations detected
- `3` - TDD violations detected
- `4` - No changes to commit
- `5` - Secrets detected
- `6` - Coverage below threshold
- `7` - Branch protection violation

## Examples

### Complete Workflow
```bash
# Check status with test results
/git-manage status

# Stage new implementation files
/git-manage add evo/src/evo/memory/
/git-manage add tests/test_memory_system.py

# Commit with auto-detection
/git-manage commit -a "implement three-tier memory system"

# Push to remote
/git-manage push origin feat/memory-system
```

### Feature Branch Workflow
```bash
# Create feature branch
/git-manage branch create feat/capability-registry

# Work and commit changes
/git-manage add evo/src/evo/capability/
/git-manage commit feat: add dynamic capability tracking

# Push and merge
/git-manage push origin feat/capability-registry
```

## Implementation Notes

This skill uses:
- `git` command for all git operations
- `pytest` for test execution
- `architecture-check` skill for compliance verification
- `tdd-enforce` skill for TDD compliance verification
- Pattern matching for secrets detection
- Conventional commits parser for message validation