"""EU AI Act compliance controls definitions"""
from typing import Dict, List


class Control:
    """Represents a compliance control mapped to AI Act articles"""
    
    def __init__(self, control_id: str, article: str, title: str, description: str, 
                 check_type: str, severity: str = "medium"):
        self.control_id = control_id
        self.article = article
        self.title = title
        self.description = description
        self.check_type = check_type
        self.severity = severity


# Define all compliance controls
CONTROLS = [
    # Article 9 - Risk Management System
    Control(
        "C-ART9-001",
        "Article 9",
        "Risk Management Documentation",
        "System must have documented risk management procedures",
        "file_presence",
        "high"
    ),
    Control(
        "C-ART9-002",
        "Article 9",
        "Risk Assessment Process",
        "Evidence of risk assessment methodology",
        "file_presence",
        "high"
    ),
    
    # Article 10 - Data and Data Governance
    Control(
        "C-ART10-001",
        "Article 10",
        "Training Data Documentation",
        "Documentation of training data sources and quality",
        "file_presence",
        "high"
    ),
    Control(
        "C-ART10-002",
        "Article 10",
        "Data Quality Checks",
        "Automated data quality validation",
        "code_analysis",
        "medium"
    ),
    Control(
        "C-ART10-003",
        "Article 10",
        "Bias Detection",
        "Bias detection and mitigation procedures",
        "code_analysis",
        "high"
    ),
    
    # Article 11 - Technical Documentation
    Control(
        "C-ART11-001",
        "Article 11",
        "README Documentation",
        "Project must have comprehensive README",
        "file_presence",
        "medium"
    ),
    Control(
        "C-ART11-002",
        "Article 11",
        "Model Architecture Documentation",
        "Documentation of model architecture and design",
        "file_presence",
        "high"
    ),
    Control(
        "C-ART11-003",
        "Article 11",
        "Performance Metrics",
        "Documentation of model performance metrics",
        "file_presence",
        "medium"
    ),
    
    # Article 12 - Record-keeping
    Control(
        "C-ART12-001",
        "Article 12",
        "Logging Implementation",
        "Code must implement comprehensive logging",
        "code_analysis",
        "high"
    ),
    Control(
        "C-ART12-002",
        "Article 12",
        "Audit Trail",
        "System maintains audit trail of decisions",
        "code_analysis",
        "high"
    ),
    
    # Article 13 - Transparency
    Control(
        "C-ART13-001",
        "Article 13",
        "User Documentation",
        "User-facing documentation exists",
        "file_presence",
        "medium"
    ),
    Control(
        "C-ART13-002",
        "Article 13",
        "Model Explainability",
        "Implementation of model explainability features",
        "code_analysis",
        "medium"
    ),
    
    # Article 14 - Human Oversight
    Control(
        "C-ART14-001",
        "Article 14",
        "Human Review Process",
        "Documentation of human review procedures",
        "file_presence",
        "high"
    ),
    Control(
        "C-ART14-002",
        "Article 14",
        "Override Mechanism",
        "Code implements human override capabilities",
        "code_analysis",
        "high"
    ),
    
    # Article 15 - Accuracy, Robustness and Cybersecurity
    Control(
        "C-ART15-001",
        "Article 15",
        "Testing Framework",
        "Automated testing framework present",
        "file_presence",
        "high"
    ),
    Control(
        "C-ART15-002",
        "Article 15",
        "Test Coverage",
        "Adequate test coverage of critical functions",
        "code_analysis",
        "medium"
    ),
    Control(
        "C-ART15-003",
        "Article 15",
        "Security Scanning",
        "No critical security vulnerabilities",
        "security_scan",
        "critical"
    ),
    Control(
        "C-ART15-004",
        "Article 15",
        "Input Validation",
        "Proper input validation implemented",
        "code_analysis",
        "high"
    ),
    Control(
        "C-ART15-005",
        "Article 15",
        "Error Handling",
        "Comprehensive error handling",
        "code_analysis",
        "medium"
    ),
]


def get_all_controls() -> List[Control]:
    """Return all defined controls"""
    return CONTROLS


def get_control_by_id(control_id: str) -> Control:
    """Get a specific control by ID"""
    for control in CONTROLS:
        if control.control_id == control_id:
            return control
    return None


def get_controls_by_article(article: str) -> List[Control]:
    """Get all controls for a specific article"""
    return [c for c in CONTROLS if c.article == article]


def controls_to_dict() -> List[Dict]:
    """Convert controls to dictionary format"""
    return [
        {
            "control_id": c.control_id,
            "article": c.article,
            "title": c.title,
            "description": c.description,
            "check_type": c.check_type,
            "severity": c.severity
        }
        for c in CONTROLS
    ]
