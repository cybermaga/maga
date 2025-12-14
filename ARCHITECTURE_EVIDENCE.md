# Evidence-Based Compliance Architecture

## Overview

Переход от questionnaire-based к evidence-based compliance проверке для EU AI Act.

---

## Core Entities

```
AI Act Article 
    ↓
Control (требование)
    ↓
Evidence (доказательство)
    ↓
Finding (результат проверки)
```

### 1. Control
Конкретное требование из AI Act, которое можно проверить.

```python
{
    "id": "CTRL-009-001",
    "article": "Article 9",
    "title": "Risk Management System Documentation",
    "description": "System must have documented risk identification procedures",
    "category": "documentation",
    "automation_level": "semi-automated",  # automated | semi-automated | manual
    "evidence_requirements": [
        "risk_management_plan.pdf",
        "risk_register.csv",
        "risk_assessment_procedure.md"
    ]
}
```

### 2. Evidence
Артефакт или данные, подтверждающие выполнение контроля.

```python
{
    "id": "EVD-001",
    "control_id": "CTRL-009-001",
    "type": "file",  # file | code | config | test | log | metric
    "source": "docs/risk_management_plan.pdf",
    "collected_at": "2025-01-15T10:00:00Z",
    "content_hash": "sha256:...",
    "metadata": {
        "file_size": 1024,
        "last_modified": "2025-01-10",
        "scanner": "doc_scanner_v1"
    },
    "status": "valid"  # valid | invalid | expired | missing
}
```

### 3. Finding
Результат проверки контроля на основе evidence.

```python
{
    "id": "FND-001",
    "control_id": "CTRL-009-001",
    "evidence_ids": ["EVD-001", "EVD-002"],
    "status": "compliant",  # compliant | partial | non_compliant | not_applicable
    "confidence": 0.85,  # 0.0 - 1.0
    "auto_verified": true,
    "gaps": [
        "Missing risk assessment procedure document"
    ],
    "recommendation": "Upload risk assessment procedure to docs/",
    "severity": "medium"  # critical | high | medium | low | info
}
```

### 4. EvidenceScan
Результат полного сканирования.

```python
{
    "id": "SCAN-001",
    "type": "evidence",  # evidence | questionnaire | hybrid
    "scan_method": "repo",  # repo | upload | api | hybrid
    "target": {
        "type": "repository",
        "path": "/path/to/repo",
        "commit": "abc123"
    },
    "findings": [...],
    "coverage": {
        "total_controls": 45,
        "checked_controls": 38,
        "compliant": 25,
        "partial": 10,
        "non_compliant": 3,
        "coverage_percentage": 84.4
    },
    "created_at": "2025-01-15T10:00:00Z"
}
```

---

## AI Act Controls Mapping (Arts. 9-15 + Annex IV)

### Article 9: Risk Management System

| Control ID | Requirement | Evidence Type | Automation |
|------------|-------------|---------------|------------|
| CTRL-009-001 | Risk identification procedure | documentation | semi-automated |
| CTRL-009-002 | Risk assessment methodology | documentation | semi-automated |
| CTRL-009-003 | Risk mitigation measures | code, tests | automated |
| CTRL-009-004 | Continuous monitoring setup | config, logs | automated |
| CTRL-009-005 | Testing procedures | tests, CI logs | automated |

**Evidence sources:**
- `docs/risk_*.{pdf,md}` - Risk management documentation
- `tests/test_safety*.py` - Risk mitigation tests
- `.github/workflows/*.yml` - CI/CD monitoring
- `monitoring/` - Monitoring configs (Prometheus, Grafana)
- `CHANGELOG.md` - Risk updates tracking

---

### Article 10: Data and Data Governance

| Control ID | Requirement | Evidence Type | Automation |
|------------|-------------|---------------|------------|
| CTRL-010-001 | Training data documentation | documentation | semi-automated |
| CTRL-010-002 | Data quality checks | code, tests | automated |
| CTRL-010-003 | Bias detection implemented | code, metrics | automated |
| CTRL-010-004 | Data governance policy | documentation | manual |
| CTRL-010-005 | Data lineage tracking | config, logs | automated |

**Evidence sources:**
- `data/README.md` - Dataset documentation
- `src/data_validation*.py` - Data quality checks
- `tests/test_bias*.py` - Bias detection tests
- `notebooks/*fairness*.ipynb` - Fairness analysis
- `dvc.yaml` or `data.yaml` - Data version control

---

### Article 11: Technical Documentation

| Control ID | Requirement | Evidence Type | Automation |
|------------|-------------|---------------|------------|
| CTRL-011-001 | System design documented | documentation | semi-automated |
| CTRL-011-002 | Architecture diagrams | documentation | semi-automated |
| CTRL-011-003 | API documentation | code, docs | automated |
| CTRL-011-004 | Model card present | documentation | automated |
| CTRL-011-005 | Development process | documentation, git | semi-automated |

**Evidence sources:**
- `README.md`, `docs/*.md` - System documentation
- `architecture/*.{png,svg}` - Architecture diagrams
- `openapi.yaml` or docstrings - API documentation
- `MODEL_CARD.md` - Model card (Hugging Face format)
- Git history - Development process

---

### Article 12: Record-keeping

| Control ID | Requirement | Evidence Type | Automation |
|------------|-------------|---------------|------------|
| CTRL-012-001 | Automatic logging enabled | code, config | automated |
| CTRL-012-002 | Audit trail implemented | code, logs | automated |
| CTRL-012-003 | Event recording system | code, config | automated |
| CTRL-012-004 | Log retention policy | config, docs | semi-automated |
| CTRL-012-005 | Traceability mechanism | code, logs | automated |

**Evidence sources:**
- `logging.conf`, `*.env` - Logging configuration
- `src/*logging*.py` - Logging implementation
- `logs/` - Log samples (anonymized)
- Database audit tables schema
- `docker-compose.yml` - Log management stack

---

### Article 13: Transparency

| Control ID | Requirement | Evidence Type | Automation |
|------------|-------------|---------------|------------|
| CTRL-013-001 | User instructions provided | documentation | automated |
| CTRL-013-002 | Limitations documented | documentation | semi-automated |
| CTRL-013-003 | Performance metrics disclosed | documentation, metrics | automated |
| CTRL-013-004 | Human oversight explained | documentation | semi-automated |
| CTRL-013-005 | Explainability features | code, docs | automated |

**Evidence sources:**
- `USER_GUIDE.md`, `FAQ.md` - User documentation
- `LIMITATIONS.md` - System limitations
- `benchmarks/*.json` - Performance metrics
- `explainability/` - SHAP, LIME implementations
- UI screenshots - Transparency disclosures

---

### Article 14: Human Oversight

| Control ID | Requirement | Evidence Type | Automation |
|------------|-------------|---------------|------------|
| CTRL-014-001 | Human review workflow | code, docs | semi-automated |
| CTRL-014-002 | Override mechanisms | code, tests | automated |
| CTRL-014-003 | Stop functionality | code, tests | automated |
| CTRL-014-004 | Monitoring interface | code, screenshots | semi-automated |
| CTRL-014-005 | Alert system for humans | code, config | automated |

**Evidence sources:**
- `src/*approval*.py` - Approval workflows
- `src/*override*.py` - Override mechanisms
- `tests/test_emergency_stop*.py` - Stop tests
- `dashboard/` - Monitoring UI code
- `alerts/` - Alert configurations

---

### Article 15: Accuracy, Robustness, Cybersecurity

| Control ID | Requirement | Evidence Type | Automation |
|------------|-------------|---------------|------------|
| CTRL-015-001 | Accuracy metrics tracked | metrics, tests | automated |
| CTRL-015-002 | Robustness tests implemented | tests, CI | automated |
| CTRL-015-003 | Security scanning enabled | CI, config | automated |
| CTRL-015-004 | Dependency vulnerability checks | CI, reports | automated |
| CTRL-015-005 | Error handling implemented | code, tests | automated |
| CTRL-015-006 | Input validation present | code, tests | automated |

**Evidence sources:**
- `tests/test_accuracy*.py` - Accuracy tests
- `tests/test_robustness*.py` - Robustness tests
- `.github/workflows/security.yml` - Security scanning
- `requirements.txt` + pip-audit reports
- `src/validators/*.py` - Input validation
- `tests/test_error_handling*.py` - Error handling tests

---

### Annex IV: Technical Documentation Requirements

| Control ID | Requirement | Evidence Type | Automation |
|------------|-------------|---------------|------------|
| CTRL-ANX4-001 | System description | documentation | semi-automated |
| CTRL-ANX4-002 | Intended purpose defined | documentation | semi-automated |
| CTRL-ANX4-003 | Hardware requirements | documentation | automated |
| CTRL-ANX4-004 | Input/output specifications | documentation, code | automated |
| CTRL-ANX4-005 | Version information | git, config | automated |
| CTRL-ANX4-006 | Training data description | documentation | semi-automated |
| CTRL-ANX4-007 | Validation/testing procedures | tests, docs | automated |
| CTRL-ANX4-008 | Performance metrics | metrics, docs | automated |

**Evidence sources:**
- `README.md`, `SYSTEM.md` - System description
- `requirements.txt`, `Dockerfile` - Hardware/software requirements
- `schema.json`, OpenAPI spec - I/O specifications
- `VERSION`, Git tags - Version tracking
- `data/README.md` - Training data documentation
- `tests/`, `pytest.ini` - Test procedures
- `benchmarks/`, `metrics.json` - Performance data

---

## Evidence Collection Strategy

### Automated Evidence
Can be collected automatically by scanners:
- Code structure and patterns
- Test coverage and results
- Configuration files
- Dependency lists
- Git history and commits
- CI/CD pipeline logs
- API documentation (from code)

### Semi-Automated Evidence
Requires file presence verification + content analysis:
- Documentation files (README, guides)
- Architecture diagrams
- Model cards
- Risk management plans
- Data governance policies

### Manual Evidence
Cannot be fully automated, requires human review:
- Quality of documentation content
- Completeness of risk assessments
- Real operational logs (privacy concerns)
- Third-party audit reports
- Contracts and agreements
- Physical security measures

---

## Gap Analysis Framework

For each control, identify:

1. **Found Evidence** - What was automatically collected
2. **Missing Evidence** - What is required but not found
3. **Insufficient Evidence** - What was found but incomplete
4. **Recommendations** - Specific actions to close gaps

Example:
```json
{
  "control": "CTRL-009-001",
  "status": "partial",
  "found": [
    "docs/risk_overview.md"
  ],
  "missing": [
    "docs/risk_assessment_procedure.md",
    "docs/risk_register.csv"
  ],
  "recommendations": [
    "Create detailed risk assessment procedure document",
    "Implement risk register in docs/risk_register.csv",
    "Add risk identification workflow diagram"
  ]
}
```

---

## Coverage Calculation

```python
# Per Article
article_coverage = (compliant_controls + 0.5 * partial_controls) / total_controls * 100

# Overall
overall_coverage = sum(all_compliant + 0.5 * all_partial) / total_controls * 100

# By Evidence Type
automated_coverage = automated_compliant / automated_total * 100
manual_coverage = manual_provided / manual_required * 100
```

---

## Storage Schema

### MongoDB Collections

**controls** - Static control definitions
**evidence** - Collected evidence items
**findings** - Verification results
**evidence_scans** - Complete scan results
**artifact_uploads** - User-uploaded documents mapped to controls

---

## Next Steps

1. Implement models in `backend/evidence_models.py`
2. Create control definitions in `backend/controls_definitions.py`
3. Build repo scanner in `backend/repo_scanner.py`
4. Add POST /api/compliance/scan/repo endpoint
5. Update UI to show evidence-based results
6. Create CLI tool
7. Build GitHub Action

See IMPLEMENTATION_EVIDENCE.md for detailed implementation plan.
