---
name: quality-assurance
description: Comprehensive project quality assurance following industrial standards for software delivery
version: 1.0.0
category: quality-assurance
---

# Quality Assurance Skill

Provides comprehensive project quality assurance following industrial standards for software delivery, ensuring the evo project meets production-ready criteria before deployment.

## Usage

```
/quality-assurance <command> [options]
```

## Available Commands

### Full Review
```
/quality-assurance review
```
Runs complete quality assurance suite including all checks below.

### Test Suite
```
/quality-assurance test [unit|integration|all]
```
Run test suites. Default: `all`.
- `unit` - Unit tests only
- `integration` - Integration tests only
- `all` - Full test suite

### Coverage Verification
```
/quality-assurance coverage [threshold=90]
```
Verify test coverage meets threshold. Default: 90%.

### Security Scan
```
/quality-assurance security [full|quick]
```
Run security vulnerability scans.
- `full` - Comprehensive security analysis
- `quick` - Fast security checks

### Static Analysis
```
/quality-assurance static-analysis [tools=all]
```
Run code quality static analysis tools.
- `all` - All available tools (pylint, mypy, bandit, ruff)
- Specific tools: `pylint`, `mypy`, `bandit`, `ruff`

### Compliance Check
```
/quality-assurance compliance [standard=iso25010]
```
Verify compliance with quality standards.
- `iso25010` - ISO/IEC 25010 Software Quality Model
- `ieee829` - IEEE 829 Test Documentation
- `all` - All standards

### Performance Test
```
/quality-assurance performance [load|stress|benchmark]
```
Run performance tests.
- `load` - Load testing
- `stress` - Stress testing
- `benchmark` - Performance benchmarks

### Documentation Check
```
/quality-assurance docs [check|generate]
```
- `check` - Verify documentation completeness
- `generate` - Generate missing documentation

### Dependency Audit
```
/quality-assurance dependencies
```
Audit dependencies for vulnerabilities and outdated packages.

### Code Review Checklist
```
/quality-assurance checklist
```
Interactive code review checklist.

### Report Generation
```
/quality-assurance report [format=markdown]
```
Generate comprehensive quality assurance report.
- `markdown` - Markdown format
- `json` - JSON format
- `html` - HTML format

## Standards Implemented

### ISO/IEC 25010 - Software Quality Model

| Quality Attribute | Description | Checks |
|-------------------|-------------|--------|
| Functional Suitability | Degree to which a product provides stated needs | Test coverage, feature completeness |
| Performance Efficiency | Relationship between performance and resources | Load testing, benchmarks, memory profiling |
| Compatibility | Degree to which products can exchange information | Python version compatibility, dependency resolution |
| Usability | Degree to which a product can be understood, learned, used | Documentation quality, error messages, UX |
| Reliability | Ability to perform required functions under stated conditions | Error handling, logging, recovery mechanisms |
| Security | Protection of information and data | OWASP checks, secrets scanning, input validation |
| Maintainability | Ease of modifying to improve, correct or adapt | Code quality metrics, documentation, modularity |
| Portability | Ability to transfer from one environment to another | Docker support, cross-platform testing |

### IEEE 829 - Test Documentation

Enforces proper test documentation structure:
- Test Plan
- Test Design Specification
- Test Case Specification
- Test Procedure Specification
- Test Item Transmittal Report
- Test Log
- Test Incident Report
- Test Summary Report

### OWASP Security Standards

- OWASP Top 10 vulnerability checks
- Dependency vulnerability scanning
- Secrets detection
- Input validation verification
- Authentication/authorization checks

### CI/CD Best Practices

- Automated testing in pipeline
- Code coverage gates
- Static analysis integration
- Security scanning automation
- Automated deployment checks

### Semantic Versioning

- Follows SemVer (MAJOR.MINOR.PATCH)
- Version bumping guidelines
- Changelog maintenance

## Review Checklist

### Functionality
- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] Test coverage ≥ 90%
- [ ] All examples run successfully
- [ ] Demo executes without errors
- [ ] Main entry point works correctly
- [ ] LLM integration verified
- [ ] API endpoints functional

### Performance
- [ ] Load tests completed
- [ ] Stress tests completed
- [ ] Performance benchmarks documented
- [ ] Memory usage within limits
- [ ] Response time acceptable
- [ ] No memory leaks detected
- [ ] Resource usage optimized

### Security
- [ ] OWASP Top 10 scan passed
- [ ] No secrets in code
- [ ] Dependency vulnerabilities fixed
- [ ] Input validation verified
- [ ] Authentication tested
- [ ] Authorization tested
- [ ] SQL injection prevented
- [ ] XSS prevention verified

### Code Quality
- [ ] Pylint score ≥ 8.0
- [ ] Mypy type checking passed
- [ ] Bandit security scan passed
- [ ] Ruff linting passed
- [ ] Code follows PEP 8
- [ ] Type hints complete
- [ ] Docstrings present
- [ ] No code duplication

### Maintainability
- [ ] Code review completed
- [ ] Documentation updated
- [ ] README accurate
- [ ] API documentation complete
- [ ] Architecture decision records updated
- [ ] Change log maintained
- [ ] Deprecation notices added
- [ ] Migration guides provided

### Reliability
- [ ] Error handling comprehensive
- [ ] Logging structured
- [ ] Recovery mechanisms tested
- [ ] Failover scenarios tested
- [ ] Data integrity verified
- [ ] Transaction management correct
- [ ] Timeout handling appropriate
- [ ] Circuit breakers implemented

### Compatibility
- [ ] Python 3.12+ compatibility verified
- [ ] Dependencies compatible
- [ ] Platform compatibility tested
- [ ] Browser compatibility (if applicable)
- [ ] API versioning correct
- [ ] Backward compatibility maintained

### Documentation
- [ ] README comprehensive
- [ ] API documentation complete
- [ ] Installation instructions clear
- [ ] Usage examples provided
- [ ] Contributing guidelines present
- [ ] License documented
- [ ] Changelog updated
- [ ] Architecture documentation current

## Tools Used

### Testing
- `pytest` - Test framework
- `pytest-cov` - Coverage reporting
- `pytest-asyncio` - Async test support

### Static Analysis
- `pylint` - Code quality linting
- `mypy` - Static type checking
- `bandit` - Security linter
- `ruff` - Fast Python linter

### Security
- `safety` - Dependency vulnerability scanner
- `bandit` - Security vulnerability scanner
- `git-secrets` - Secrets detection

### Performance
- `pytest-benchmark` - Performance benchmarking
- `memory-profiler` - Memory profiling
- `locust` - Load testing

### Documentation
- `sphinx` - Documentation generator
- `mkdocs` - Static site generator
- `pydocstyle` - Docstring style checker

## Exit Codes

- `0` - All checks passed
- `1` - Tests failed
- `2` - Coverage below threshold
- `3` - Security vulnerabilities found
- `4` - Static analysis failed
- `5` - Performance issues detected
- `6` - Documentation incomplete
- `7` - Dependency issues found
- `8` - Compliance violations
- `9` - Configuration errors
- `10` - Tool execution failed

## Integration with Existing Skills

### Architecture Check
- Invokes `architecture-check` skill during compliance review
- Includes architecture compliance in overall report

### TDD Enforcement
- Invokes `tdd-enforce` skill during test review
- Verifies TDD workflow compliance

### Git Management
- Uses `git-manage` skill for commit verification
- Checks git history quality

## Report Format

### Markdown Report Template

```markdown
# Quality Assurance Report

**Project**: Evo  
**Date**: YYYY-MM-DD  
**Reviewer**: [System]  
**Version**: X.Y.Z

## Executive Summary

- Overall Status: ✅ PASS / ⚠️ WARN / ❌ FAIL
- Test Coverage: XX%
- Security Score: XX/10
- Code Quality Score: XX/10
- Total Issues: XX

## Detailed Results

### Test Suite
- Unit Tests: ✅ PASS (X passed, Y failed)
- Integration Tests: ✅ PASS (X passed, Y failed)
- Coverage: XX.X% (threshold: 90%)

### Security
- OWASP Scan: ✅ PASS
- Dependency Scan: ✅ PASS
- Secrets Detection: ✅ PASS

### Code Quality
- Pylint Score: X.X/10
- Mypy: ✅ PASS
- Bandit: ✅ PASS
- Ruff: ✅ PASS

### Performance
- Load Test: ✅ PASS
- Stress Test: ✅ PASS
- Benchmark: Baseline established

### Documentation
- README: ✅ COMPLETE
- API Docs: ✅ COMPLETE
- Examples: ✅ FUNCTIONAL

## Issues Found

### Critical (X)
- [Issue description]

### High (X)
- [Issue description]

### Medium (X)
- [Issue description]

### Low (X)
- [Issue description]

## Recommendations

1. [Recommendation 1]
2. [Recommendation 2]
3. [Recommendation 3]

## Compliance

- ISO/IEC 25010: ✅ COMPLIANT
- IEEE 829: ✅ COMPLIANT
- OWASP: ✅ COMPLIANT

## Conclusion

[Summary statement]

---
**Report Generated**: YYYY-MM-DD HH:MM:SS
```

## Examples

### Full Review
```bash
# Run complete quality assurance
/quality-assurance review

# Generate report
/quality-assurance report markdown > _out/qa_report.md
```

### Quick Security Check
```bash
# Quick security scan
/quality-assurance security quick
```

### Coverage Verification
```bash
# Verify coverage with custom threshold
/quality-assurance coverage threshold=95
```

### Static Analysis
```bash
# Run specific static analysis tools
/quality-assurance static-analysis tools=pylint,mypy
```

### Performance Testing
```bash
# Run performance benchmarks
/quality-assurance performance benchmark
```

### Compliance Check
```bash
# Verify ISO/IEC 25010 compliance
/quality-assurance compliance standard=iso25010
```

## Pre-Deployment Checklist

Before any deployment, run:

```bash
/quality-assurance review
```

This ensures:
- All tests pass
- Coverage thresholds met
- No security vulnerabilities
- Code quality standards met
- Performance acceptable
- Documentation complete
- Compliance verified

## Best Practices

1. **Run Early, Run Often** - Execute quality checks frequently during development
2. **Automate in CI/CD** - Integrate quality gates in deployment pipeline
3. **Fix Issues Promptly** - Address findings before they accumulate
4. **Document Exceptions** - Record reasons for any waived checks
5. **Continuous Improvement** - Update checklist based on lessons learned

## Implementation Notes

This skill uses:
- `pytest` for test execution
- `pytest-cov` for coverage reporting
- `pylint`, `mypy`, `bandit`, `ruff` for static analysis
- `safety` for dependency scanning
- Custom validators for compliance checks
- Template engine for report generation

## Maintenance

Update this skill when:
- New quality standards are adopted
- Tools are added or removed
- Check criteria change
- Standards are updated
- New compliance requirements emerge