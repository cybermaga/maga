"""Control definitions for EU AI Act Articles 9-15 + Annex IV"""
from typing import List, Optional
from evidence_models import Control, AutomationLevel, SeverityLevel, ControlMapping


# ============= ARTICLE 9: RISK MANAGEMENT SYSTEM =============

ARTICLE_9_CONTROLS = [
    Control(
        id="CTRL-009-001",
        article="Article 9",
        article_number=9,
        title="Risk Identification Procedure",
        description="Document and implement systematic risk identification procedures",
        category="documentation",
        automation_level=AutomationLevel.SEMI_AUTOMATED,
        evidence_requirements=[
            "docs/risk*.{pdf,md}",
            "RISK_MANAGEMENT*.md",
            "risk_identification*.{pdf,md}"
        ],
        priority=SeverityLevel.HIGH,
        references=["Article 9(2)(a)"],
        tags=["risk", "documentation", "procedure"]
    ),
    Control(
        id="CTRL-009-002",
        article="Article 9",
        article_number=9,
        title="Risk Assessment Methodology",
        description="Define and document risk assessment methodology and criteria",
        category="documentation",
        automation_level=AutomationLevel.SEMI_AUTOMATED,
        evidence_requirements=[
            "docs/risk_assessment*.{pdf,md}",
            "risk_matrix*.{pdf,png}"
        ],
        priority=SeverityLevel.HIGH,
        references=["Article 9(2)(b)"],
        tags=["risk", "assessment", "methodology"]
    ),
    Control(
        id="CTRL-009-003",
        article="Article 9",
        article_number=9,
        title="Risk Mitigation Implementation",
        description="Implement and test risk mitigation measures in code",
        category="code",
        automation_level=AutomationLevel.AUTOMATED,
        evidence_requirements=[
            "tests/test_*safety*.py",
            "tests/test_*risk*.py",
            "src/*safety*.py",
            "src/*mitigation*.py"
        ],
        priority=SeverityLevel.CRITICAL,
        references=["Article 9(2)(c)"],
        tags=["risk", "mitigation", "testing"]
    ),
    Control(
        id="CTRL-009-004",
        article="Article 9",
        article_number=9,
        title="Continuous Monitoring Setup",
        description="Configure monitoring and alerting for risk indicators",
        category="config",
        automation_level=AutomationLevel.AUTOMATED,
        evidence_requirements=[
            "monitoring/*.{yml,yaml,json}",
            "prometheus/*.yml",
            "grafana/*.json",
            ".github/workflows/*monitor*.yml"
        ],
        priority=SeverityLevel.HIGH,
        references=["Article 9(2)(d)"],
        tags=["monitoring", "alerts", "continuous"]
    ),
    Control(
        id="CTRL-009-005",
        article="Article 9",
        article_number=9,
        title="Testing Procedures",
        description="Implement comprehensive testing including risk scenarios",
        category="test",
        automation_level=AutomationLevel.AUTOMATED,
        evidence_requirements=[
            "tests/",
            "pytest.ini",
            ".github/workflows/*test*.yml",
            "test_*.py"
        ],
        priority=SeverityLevel.HIGH,
        references=["Article 9(4)"],
        tags=["testing", "validation"]
    ),
]


# ============= ARTICLE 10: DATA GOVERNANCE =============

ARTICLE_10_CONTROLS = [
    Control(
        id="CTRL-010-001",
        article="Article 10",
        article_number=10,
        title="Training Data Documentation",
        description="Document training data sources, collection, and characteristics",
        category="documentation",
        automation_level=AutomationLevel.SEMI_AUTOMATED,
        evidence_requirements=[
            "data/README.md",
            "DATA*.md",
            "dataset*.{pdf,md}",
            "data_card.md"
        ],
        priority=SeverityLevel.HIGH,
        references=["Article 10(2)"],
        tags=["data", "documentation", "training"]
    ),
    Control(
        id="CTRL-010-002",
        article="Article 10",
        article_number=10,
        title="Data Quality Checks",
        description="Implement automated data quality validation",
        category="code",
        automation_level=AutomationLevel.AUTOMATED,
        evidence_requirements=[
            "src/*data*valid*.py",
            "src/*data*quality*.py",
            "tests/test_data*.py"
        ],
        priority=SeverityLevel.HIGH,
        references=["Article 10(3)"],
        tags=["data", "quality", "validation"]
    ),
    Control(
        id="CTRL-010-003",
        article="Article 10",
        article_number=10,
        title="Bias Detection Implementation",
        description="Implement bias detection and mitigation measures",
        category="code",
        automation_level=AutomationLevel.AUTOMATED,
        evidence_requirements=[
            "src/*bias*.py",
            "src/*fairness*.py",
            "tests/test_*bias*.py",
            "notebooks/*fairness*.ipynb"
        ],
        priority=SeverityLevel.CRITICAL,
        references=["Article 10(2)(f)"],
        tags=["bias", "fairness", "ethics"]
    ),
    Control(
        id="CTRL-010-004",
        article="Article 10",
        article_number=10,
        title="Data Governance Policy",
        description="Establish and document data governance policies",
        category="documentation",
        automation_level=AutomationLevel.MANUAL,
        evidence_requirements=[
            "DATA_GOVERNANCE*.{pdf,md}",
            "policies/data*.{pdf,md}"
        ],
        priority=SeverityLevel.MEDIUM,
        references=["Article 10(5)"],
        tags=["data", "governance", "policy"]
    ),
    Control(
        id="CTRL-010-005",
        article="Article 10",
        article_number=10,
        title="Data Lineage Tracking",
        description="Implement data versioning and lineage tracking",
        category="config",
        automation_level=AutomationLevel.AUTOMATED,
        evidence_requirements=[
            "dvc.yaml",
            "dvc.lock",
            "data.yaml",
            ".dvc/",
            "mlflow*"
        ],
        priority=SeverityLevel.MEDIUM,
        references=["Article 10(4)"],
        tags=["data", "lineage", "versioning"]
    ),
]


# ============= ARTICLE 11: TECHNICAL DOCUMENTATION =============

ARTICLE_11_CONTROLS = [
    Control(
        id="CTRL-011-001",
        article="Article 11",
        article_number=11,
        title="System Design Documentation",
        description="Comprehensive system design and architecture documentation",
        category="documentation",
        automation_level=AutomationLevel.SEMI_AUTOMATED,
        evidence_requirements=[
            "README.md",
            "docs/*.md",
            "ARCHITECTURE.md",
            "DESIGN.md"
        ],
        priority=SeverityLevel.HIGH,
        references=["Article 11(1)", "Annex IV(1)"],
        tags=["documentation", "architecture"]
    ),
    Control(
        id="CTRL-011-002",
        article="Article 11",
        article_number=11,
        title="Architecture Diagrams",
        description="Visual architecture and component diagrams",
        category="documentation",
        automation_level=AutomationLevel.SEMI_AUTOMATED,
        evidence_requirements=[
            "docs/*.{png,svg,jpg}",
            "architecture/*.{png,svg}",
            "diagrams/*"
        ],
        priority=SeverityLevel.MEDIUM,
        references=["Annex IV(1)(b)"],
        tags=["documentation", "diagrams"]
    ),
    Control(
        id="CTRL-011-003",
        article="Article 11",
        article_number=11,
        title="API Documentation",
        description="Complete API documentation with endpoints and schemas",
        category="code",
        automation_level=AutomationLevel.AUTOMATED,
        evidence_requirements=[
            "openapi.{yaml,json}",
            "swagger.{yaml,json}",
            "src/**/*.py:def.*#.*@app",  # FastAPI routes with docstrings
            "docs/api.md"
        ],
        priority=SeverityLevel.HIGH,
        references=["Annex IV(1)(d)"],
        tags=["api", "documentation"]
    ),
    Control(
        id="CTRL-011-004",
        article="Article 11",
        article_number=11,
        title="Model Card",
        description="Model card with intended use, limitations, and performance",
        category="documentation",
        automation_level=AutomationLevel.AUTOMATED,
        evidence_requirements=[
            "MODEL_CARD.md",
            "model_card.json",
            "README.md:#Model"
        ],
        priority=SeverityLevel.HIGH,
        references=["Annex IV(2)"],
        tags=["model", "documentation"]
    ),
    Control(
        id="CTRL-011-005",
        article="Article 11",
        article_number=11,
        title="Development Process Documentation",
        description="Document development process, versions, and changes",
        category="git",
        automation_level=AutomationLevel.SEMI_AUTOMATED,
        evidence_requirements=[
            "CHANGELOG.md",
            "CONTRIBUTING.md",
            ".git/",
            "VERSION"
        ],
        priority=SeverityLevel.MEDIUM,
        references=["Annex IV(1)(f)"],
        tags=["development", "process"]
    ),
]


# ============= ARTICLE 12: RECORD-KEEPING =============

ARTICLE_12_CONTROLS = [
    Control(
        id="CTRL-012-001",
        article="Article 12",
        article_number=12,
        title="Automatic Logging Configuration",
        description="Configure comprehensive logging for all operations",
        category="config",
        automation_level=AutomationLevel.AUTOMATED,
        evidence_requirements=[
            "logging.conf",
            "*.env:LOG_LEVEL",
            "config/*logging*.{py,yaml,json}"
        ],
        priority=SeverityLevel.HIGH,
        references=["Article 12(1)"],
        tags=["logging", "configuration"]
    ),
    Control(
        id="CTRL-012-002",
        article="Article 12",
        article_number=12,
        title="Audit Trail Implementation",
        description="Implement audit trail for all critical operations",
        category="code",
        automation_level=AutomationLevel.AUTOMATED,
        evidence_requirements=[
            "src/*audit*.py",
            "src/*log*.py",
            "models/*audit*.py"
        ],
        priority=SeverityLevel.CRITICAL,
        references=["Article 12(1)"],
        tags=["audit", "trail", "logging"]
    ),
    Control(
        id="CTRL-012-003",
        article="Article 12",
        article_number=12,
        title="Event Recording System",
        description="Structured event logging and recording",
        category="code",
        automation_level=AutomationLevel.AUTOMATED,
        evidence_requirements=[
            "src/*event*.py",
            "src/*tracking*.py",
            "tests/test_*logging*.py"
        ],
        priority=SeverityLevel.HIGH,
        references=["Article 12(1)"],
        tags=["events", "recording"]
    ),
    Control(
        id="CTRL-012-004",
        article="Article 12",
        article_number=12,
        title="Log Retention Policy",
        description="Define and implement log retention policies",
        category="config",
        automation_level=AutomationLevel.SEMI_AUTOMATED,
        evidence_requirements=[
            "docker-compose.yml:logging",
            "LOG_RETENTION*.md",
            "policies/logging*.{pdf,md}"
        ],
        priority=SeverityLevel.MEDIUM,
        references=["Article 12(2)"],
        tags=["retention", "policy"]
    ),
    Control(
        id="CTRL-012-005",
        article="Article 12",
        article_number=12,
        title="Traceability Mechanism",
        description="Implement end-to-end traceability of decisions",
        category="code",
        automation_level=AutomationLevel.AUTOMATED,
        evidence_requirements=[
            "src/*trace*.py",
            "src/*decision*.py",
            "tests/test_*trace*.py"
        ],
        priority=SeverityLevel.HIGH,
        references=["Article 12(1)"],
        tags=["traceability", "decisions"]
    ),
]


# ============= ARTICLE 13: TRANSPARENCY =============

ARTICLE_13_CONTROLS = [
    Control(
        id="CTRL-013-001",
        article="Article 13",
        article_number=13,
        title="User Instructions",
        description="Provide clear instructions for users",
        category="documentation",
        automation_level=AutomationLevel.AUTOMATED,
        evidence_requirements=[
            "USER_GUIDE.md",
            "INSTRUCTIONS.md",
            "docs/user*.md",
            "README.md:#Usage"
        ],
        priority=SeverityLevel.HIGH,
        references=["Article 13(3)(b)(1)"],
        tags=["transparency", "users", "instructions"]
    ),
    Control(
        id="CTRL-013-002",
        article="Article 13",
        article_number=13,
        title="Limitations Documentation",
        description="Clearly document system limitations and constraints",
        category="documentation",
        automation_level=AutomationLevel.SEMI_AUTOMATED,
        evidence_requirements=[
            "LIMITATIONS.md",
            "README.md:#Limitations",
            "docs/*limit*.md"
        ],
        priority=SeverityLevel.CRITICAL,
        references=["Article 13(3)(b)(2)"],
        tags=["transparency", "limitations"]
    ),
    Control(
        id="CTRL-013-003",
        article="Article 13",
        article_number=13,
        title="Performance Metrics Disclosure",
        description="Disclose performance metrics and benchmarks",
        category="documentation",
        automation_level=AutomationLevel.AUTOMATED,
        evidence_requirements=[
            "benchmarks/*.json",
            "PERFORMANCE.md",
            "metrics/*.{json,csv}",
            "README.md:#Performance"
        ],
        priority=SeverityLevel.HIGH,
        references=["Article 13(3)(b)(3)"],
        tags=["transparency", "performance", "metrics"]
    ),
    Control(
        id="CTRL-013-004",
        article="Article 13",
        article_number=13,
        title="Human Oversight Information",
        description="Explain human oversight mechanisms to users",
        category="documentation",
        automation_level=AutomationLevel.SEMI_AUTOMATED,
        evidence_requirements=[
            "docs/*oversight*.md",
            "README.md:#Oversight",
            "HUMAN_OVERSIGHT.md"
        ],
        priority=SeverityLevel.HIGH,
        references=["Article 13(3)(b)(4)"],
        tags=["transparency", "oversight"]
    ),
    Control(
        id="CTRL-013-005",
        article="Article 13",
        article_number=13,
        title="Explainability Features",
        description="Implement explainability and interpretability features",
        category="code",
        automation_level=AutomationLevel.AUTOMATED,
        evidence_requirements=[
            "src/*explain*.py",
            "src/*interpret*.py",
            "src/*shap*.py",
            "src/*lime*.py"
        ],
        priority=SeverityLevel.HIGH,
        references=["Article 13(1)"],
        tags=["explainability", "interpretability"]
    ),
]


# ============= ARTICLE 14: HUMAN OVERSIGHT =============

ARTICLE_14_CONTROLS = [
    Control(
        id="CTRL-014-001",
        article="Article 14",
        article_number=14,
        title="Human Review Workflow",
        description="Implement human-in-the-loop review workflows",
        category="code",
        automation_level=AutomationLevel.SEMI_AUTOMATED,
        evidence_requirements=[
            "src/*review*.py",
            "src/*approval*.py",
            "src/*workflow*.py",
            "docs/WORKFLOW.md"
        ],
        priority=SeverityLevel.CRITICAL,
        references=["Article 14(4)(a)"],
        tags=["oversight", "review", "workflow"]
    ),
    Control(
        id="CTRL-014-002",
        article="Article 14",
        article_number=14,
        title="Override Mechanisms",
        description="Implement mechanisms for humans to override decisions",
        category="code",
        automation_level=AutomationLevel.AUTOMATED,
        evidence_requirements=[
            "src/*override*.py",
            "src/*manual*.py",
            "tests/test_*override*.py"
        ],
        priority=SeverityLevel.CRITICAL,
        references=["Article 14(4)(b)"],
        tags=["oversight", "override"]
    ),
    Control(
        id="CTRL-014-003",
        article="Article 14",
        article_number=14,
        title="Stop Functionality",
        description="Implement emergency stop and intervention capability",
        category="code",
        automation_level=AutomationLevel.AUTOMATED,
        evidence_requirements=[
            "src/*stop*.py",
            "src/*emergency*.py",
            "tests/test_*stop*.py"
        ],
        priority=SeverityLevel.CRITICAL,
        references=["Article 14(4)(c)"],
        tags=["oversight", "stop", "emergency"]
    ),
    Control(
        id="CTRL-014-004",
        article="Article 14",
        article_number=14,
        title="Monitoring Interface",
        description="Provide monitoring dashboard for human oversight",
        category="code",
        automation_level=AutomationLevel.SEMI_AUTOMATED,
        evidence_requirements=[
            "dashboard/",
            "src/dashboard*.py",
            "frontend/*dashboard*",
            "monitoring/"
        ],
        priority=SeverityLevel.HIGH,
        references=["Article 14(4)(d)"],
        tags=["oversight", "monitoring", "dashboard"]
    ),
    Control(
        id="CTRL-014-005",
        article="Article 14",
        article_number=14,
        title="Alert System",
        description="Configure alerts for human attention",
        category="config",
        automation_level=AutomationLevel.AUTOMATED,
        evidence_requirements=[
            "alerts/*.{yaml,json}",
            "src/*alert*.py",
            "prometheus/*alert*.yml"
        ],
        priority=SeverityLevel.HIGH,
        references=["Article 14(4)(d)"],
        tags=["oversight", "alerts"]
    ),
]


# ============= ARTICLE 15: ACCURACY, ROBUSTNESS, CYBERSECURITY =============

ARTICLE_15_CONTROLS = [
    Control(
        id="CTRL-015-001",
        article="Article 15",
        article_number=15,
        title="Accuracy Metrics Tracking",
        description="Track and report model accuracy metrics",
        category="test",
        automation_level=AutomationLevel.AUTOMATED,
        evidence_requirements=[
            "tests/test_*accuracy*.py",
            "tests/test_*metric*.py",
            "metrics/*.json",
            "benchmarks/"
        ],
        priority=SeverityLevel.HIGH,
        references=["Article 15(1)"],
        tags=["accuracy", "metrics", "testing"]
    ),
    Control(
        id="CTRL-015-002",
        article="Article 15",
        article_number=15,
        title="Robustness Tests",
        description="Implement robustness and adversarial testing",
        category="test",
        automation_level=AutomationLevel.AUTOMATED,
        evidence_requirements=[
            "tests/test_*robust*.py",
            "tests/test_*adversarial*.py",
            "tests/test_*edge*.py"
        ],
        priority=SeverityLevel.HIGH,
        references=["Article 15(2)"],
        tags=["robustness", "testing", "adversarial"]
    ),
    Control(
        id="CTRL-015-003",
        article="Article 15",
        article_number=15,
        title="Security Scanning",
        description="Enable automated security scanning in CI/CD",
        category="ci_cd",
        automation_level=AutomationLevel.AUTOMATED,
        evidence_requirements=[
            ".github/workflows/*security*.yml",
            ".github/workflows/*scan*.yml",
            "Snyk*",
            "bandit.yml"
        ],
        priority=SeverityLevel.CRITICAL,
        references=["Article 15(3)"],
        tags=["security", "scanning", "ci"]
    ),
    Control(
        id="CTRL-015-004",
        article="Article 15",
        article_number=15,
        title="Dependency Vulnerability Checks",
        description="Check dependencies for known vulnerabilities",
        category="ci_cd",
        automation_level=AutomationLevel.AUTOMATED,
        evidence_requirements=[
            "requirements.txt",
            ".github/workflows/*audit*.yml",
            "renovate.json",
            "dependabot.yml"
        ],
        priority=SeverityLevel.CRITICAL,
        references=["Article 15(3)"],
        tags=["dependencies", "vulnerabilities", "security"]
    ),
    Control(
        id="CTRL-015-005",
        article="Article 15",
        article_number=15,
        title="Error Handling",
        description="Implement comprehensive error handling",
        category="code",
        automation_level=AutomationLevel.AUTOMATED,
        evidence_requirements=[
            "src/*error*.py",
            "src/*exception*.py",
            "tests/test_*error*.py"
        ],
        priority=SeverityLevel.HIGH,
        references=["Article 15(4)"],
        tags=["error-handling", "resilience"]
    ),
    Control(
        id="CTRL-015-006",
        article="Article 15",
        article_number=15,
        title="Input Validation",
        description="Validate and sanitize all inputs",
        category="code",
        automation_level=AutomationLevel.AUTOMATED,
        evidence_requirements=[
            "src/*valid*.py",
            "src/*sanitize*.py",
            "tests/test_*valid*.py"
        ],
        priority=SeverityLevel.CRITICAL,
        references=["Article 15(3)"],
        tags=["validation", "security", "input"]
    ),
]


# ============= ANNEX IV: TECHNICAL DOCUMENTATION =============

ANNEX_IV_CONTROLS = [
    Control(
        id="CTRL-ANX4-001",
        article="Annex IV",
        article_number=99,  # For sorting at end
        title="System Description",
        description="General description of the AI system",
        category="documentation",
        automation_level=AutomationLevel.SEMI_AUTOMATED,
        evidence_requirements=[
            "README.md",
            "SYSTEM.md",
            "docs/OVERVIEW.md"
        ],
        priority=SeverityLevel.HIGH,
        references=["Annex IV(1)(a)"],
        tags=["documentation", "overview"]
    ),
    Control(
        id="CTRL-ANX4-002",
        article="Annex IV",
        article_number=99,
        title="Intended Purpose",
        description="Clear definition of intended purpose and use cases",
        category="documentation",
        automation_level=AutomationLevel.SEMI_AUTOMATED,
        evidence_requirements=[
            "README.md:#Purpose",
            "INTENDED_USE.md"
        ],
        priority=SeverityLevel.HIGH,
        references=["Annex IV(1)(b)"],
        tags=["documentation", "purpose"]
    ),
    Control(
        id="CTRL-ANX4-003",
        article="Annex IV",
        article_number=99,
        title="Hardware Requirements",
        description="Specify hardware and software requirements",
        category="documentation",
        automation_level=AutomationLevel.AUTOMATED,
        evidence_requirements=[
            "requirements.txt",
            "Dockerfile",
            "docker-compose.yml",
            "README.md:#Requirements"
        ],
        priority=SeverityLevel.MEDIUM,
        references=["Annex IV(1)(c)"],
        tags=["requirements", "infrastructure"]
    ),
    Control(
        id="CTRL-ANX4-004",
        article="Annex IV",
        article_number=99,
        title="Input/Output Specifications",
        description="Define input and output specifications",
        category="code",
        automation_level=AutomationLevel.AUTOMATED,
        evidence_requirements=[
            "schema.json",
            "openapi.{yaml,json}",
            "src/models/*.py",
            "src/schemas/*.py"
        ],
        priority=SeverityLevel.HIGH,
        references=["Annex IV(1)(d)"],
        tags=["api", "specifications"]
    ),
    Control(
        id="CTRL-ANX4-005",
        article="Annex IV",
        article_number=99,
        title="Version Information",
        description="Maintain version information and changelogs",
        category="git",
        automation_level=AutomationLevel.AUTOMATED,
        evidence_requirements=[
            "VERSION",
            "CHANGELOG.md",
            ".git/refs/tags/",
            "pyproject.toml:version"
        ],
        priority=SeverityLevel.MEDIUM,
        references=["Annex IV(1)(f)"],
        tags=["versioning", "changelog"]
    ),
]


# ============= CONTROL REGISTRY =============

ALL_CONTROLS = (
    ARTICLE_9_CONTROLS +
    ARTICLE_10_CONTROLS +
    ARTICLE_11_CONTROLS +
    ARTICLE_12_CONTROLS +
    ARTICLE_13_CONTROLS +
    ARTICLE_14_CONTROLS +
    ARTICLE_15_CONTROLS +
    ANNEX_IV_CONTROLS
)


def get_all_controls() -> List[Control]:
    """Get all control definitions"""
    return ALL_CONTROLS


def get_controls_by_article(article_number: int) -> List[Control]:
    """Get controls for a specific article"""
    return [c for c in ALL_CONTROLS if c.article_number == article_number]


def get_control_by_id(control_id: str) -> Optional[Control]:
    """Get a specific control by ID"""
    for control in ALL_CONTROLS:
        if control.id == control_id:
            return control
    return None


def get_control_mappings() -> List[ControlMapping]:
    """Get control mappings grouped by article"""
    mappings = {}
    
    for control in ALL_CONTROLS:
        article_key = f"{control.article} (Art. {control.article_number})"
        if article_key not in mappings:
            mappings[article_key] = {
                "article": control.article,
                "article_number": control.article_number,
                "controls": [],
                "total_controls": 0,
                "automated_controls": 0,
                "manual_controls": 0
            }
        
        mappings[article_key]["controls"].append(control)
        mappings[article_key]["total_controls"] += 1
        
        if control.automation_level == AutomationLevel.AUTOMATED:
            mappings[article_key]["automated_controls"] += 1
        elif control.automation_level == AutomationLevel.MANUAL:
            mappings[article_key]["manual_controls"] += 1
    
    return [
        ControlMapping(**mapping)
        for mapping in sorted(
            mappings.values(),
            key=lambda x: x["article_number"]
        )
    ]


# ============= SUMMARY STATISTICS =============

def get_control_statistics():
    """Get summary statistics about controls"""
    total = len(ALL_CONTROLS)
    by_automation = {
        AutomationLevel.AUTOMATED: 0,
        AutomationLevel.SEMI_AUTOMATED: 0,
        AutomationLevel.MANUAL: 0
    }
    by_priority = {
        SeverityLevel.CRITICAL: 0,
        SeverityLevel.HIGH: 0,
        SeverityLevel.MEDIUM: 0,
        SeverityLevel.LOW: 0
    }
    
    for control in ALL_CONTROLS:
        by_automation[control.automation_level] += 1
        by_priority[control.priority] += 1
    
    return {
        "total_controls": total,
        "by_automation": {k.value: v for k, v in by_automation.items()},
        "by_priority": {k.value: v for k, v in by_priority.items()},
        "articles_covered": len(set(c.article_number for c in ALL_CONTROLS)),
        "automation_percentage": round(
            (by_automation[AutomationLevel.AUTOMATED] / total * 100), 1
        )
    }
