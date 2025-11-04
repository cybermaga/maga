"""Mapping of analyzer rules to EU AI Act articles"""
from typing import Dict, List


RULE_TO_ARTICLES: Dict[str, List[str]] = {
    "deps": [
        "Article 15",  # Accuracy, robustness and cybersecurity
        "Article 17",  # Quality management system
    ],
    "bandit": [
        "Article 15",  # Accuracy, robustness and cybersecurity
    ],
    "onnx_meta": [
        "Article 6",   # Classification rules for high-risk AI systems
        "Annex III",   # High-risk AI systems
        "Article 11",  # Technical documentation
    ],
    "dataset_sanity": [
        "Article 10",  # Data and data governance
        "Article 15",  # Accuracy, robustness and cybersecurity
    ],
}


RULE_DESCRIPTIONS: Dict[str, str] = {
    "deps": "Dependency vulnerability scan - checks for known CVEs in Python dependencies",
    "bandit": "Security vulnerability scan - identifies common security issues in Python code",
    "onnx_meta": "Model metadata extraction - analyzes ONNX model structure and properties",
    "dataset_sanity": "Dataset quality check - validates data completeness, PII, and balance",
}


def get_articles_for_rule(rule: str) -> List[str]:
    """Get AI Act articles mapped to a rule"""
    return RULE_TO_ARTICLES.get(rule, [])


def get_rule_description(rule: str) -> str:
    """Get description for a rule"""
    return RULE_DESCRIPTIONS.get(rule, "Unknown rule")


def get_all_rules() -> List[str]:
    """Get all available rules"""
    return list(RULE_TO_ARTICLES.keys())
