"""Repository scanner for evidence collection - MVP version"""
import os
import re
import zipfile
import tempfile
import shutil
from pathlib import Path
from typing import List, Dict, Any, Tuple
import json

from evidence_models import (
    Evidence, EvidenceType, EvidenceStatus, EvidenceSource,
    Finding, FindingStatus, Gap, SeverityLevel,
    EvidenceScan, ScanType, ScanMethod, ScanTarget, CoverageStats
)
from controls_definitions import get_control_by_id


# ============= FIRST WAVE CONTROLS (8-10 simple automated checks) =============

FIRST_WAVE_CONTROLS = [
    "CTRL-011-001",  # README presence
    "CTRL-011-002",  # Architecture diagrams
    "CTRL-011-005",  # CHANGELOG
    "CTRL-012-001",  # Logging config
    "CTRL-012-002",  # Audit trail code
    "CTRL-015-003",  # CI/CD security
    "CTRL-015-004",  # Dependencies
    "CTRL-ANX4-001",  # System description
    "CTRL-ANX4-003",  # Requirements
    "CTRL-ANX4-005",  # Version info
]


class RepoScanner:
    """Scans repository for compliance evidence"""
    
    def __init__(self, scan_id: str, repo_path: Path):
        self.scan_id = scan_id
        self.repo_path = Path(repo_path)
        self.evidence_list: List[Evidence] = []
        self.findings_list: List[Finding] = []
    
    def scan(self) -> Tuple[List[Evidence], List[Finding]]:
        """Run all scanners and return evidence + findings"""
        
        # Run collectors for first wave controls
        for control_id in FIRST_WAVE_CONTROLS:
            control = get_control_by_id(control_id)
            if not control:
                continue
            
            evidence_items = []
            
            # Route to appropriate scanner based on control
            if control_id == "CTRL-011-001":  # README
                evidence_items = self._scan_readme()
            elif control_id == "CTRL-011-002":  # Diagrams
                evidence_items = self._scan_diagrams()
            elif control_id == "CTRL-011-005":  # CHANGELOG
                evidence_items = self._scan_changelog()
            elif control_id == "CTRL-012-001":  # Logging config
                evidence_items = self._scan_logging_config()
            elif control_id == "CTRL-012-002":  # Audit trail
                evidence_items = self._scan_audit_trail()
            elif control_id == "CTRL-015-003":  # CI/CD
                evidence_items = self._scan_ci_config()
            elif control_id == "CTRL-015-004":  # Dependencies
                evidence_items = self._scan_dependencies()
            elif control_id == "CTRL-ANX4-001":  # System description
                evidence_items = self._scan_system_docs()
            elif control_id == "CTRL-ANX4-003":  # Requirements
                evidence_items = self._scan_requirements()
            elif control_id == "CTRL-ANX4-005":  # Version
                evidence_items = self._scan_version()
            
            # Create finding based on evidence
            finding = self._create_finding(control_id, evidence_items)
            self.findings_list.append(finding)
            self.evidence_list.extend(evidence_items)
        
        return self.evidence_list, self.findings_list
    
    # ============= SCANNERS =============
    
    def _scan_readme(self) -> List[Evidence]:
        """Check for README file"""
        evidence = []
        
        for pattern in ["README.md", "README.rst", "README.txt", "README"]:
            files = list(self.repo_path.glob(pattern))
            if files:
                for file in files[:1]:  # Take first match
                    content_preview = self._read_file_preview(file)
                    evidence.append(Evidence(
                        scan_id=self.scan_id,
                        control_id="CTRL-011-001",
                        type=EvidenceType.DOCUMENTATION,
                        source=EvidenceSource(
                            type="file",
                            path=str(file.relative_to(self.repo_path))
                        ),
                        content_preview=content_preview,
                        status=EvidenceStatus.VALID,
                        confidence_score=1.0,
                        metadata={"file_size": file.stat().st_size}
                    ))
        
        return evidence
    
    def _scan_diagrams(self) -> List[Evidence]:
        """Check for architecture diagrams"""
        evidence = []
        
        diagram_patterns = ["*.png", "*.svg", "*.jpg", "*.jpeg"]
        diagram_dirs = ["docs", "architecture", "diagrams", "."]
        
        for dir_pattern in diagram_dirs:
            dir_path = self.repo_path / dir_pattern if dir_pattern != "." else self.repo_path
            if dir_path.exists():
                for pattern in diagram_patterns:
                    for file in dir_path.glob(pattern):
                        # Check if filename suggests it's a diagram
                        if any(keyword in file.name.lower() for keyword in 
                               ["architecture", "diagram", "flow", "system", "design"]):
                            evidence.append(Evidence(
                                scan_id=self.scan_id,
                                control_id="CTRL-011-002",
                                type=EvidenceType.DOCUMENTATION,
                                source=EvidenceSource(
                                    type="file",
                                    path=str(file.relative_to(self.repo_path))
                                ),
                                status=EvidenceStatus.VALID,
                                confidence_score=0.8,
                                metadata={"file_size": file.stat().st_size}
                            ))
        
        return evidence[:5]  # Limit to first 5
    
    def _scan_changelog(self) -> List[Evidence]:
        """Check for CHANGELOG"""
        evidence = []
        
        for pattern in ["CHANGELOG.md", "CHANGELOG.rst", "CHANGELOG.txt", "CHANGELOG"]:
            files = list(self.repo_path.glob(pattern))
            if files:
                for file in files[:1]:
                    content_preview = self._read_file_preview(file)
                    evidence.append(Evidence(
                        scan_id=self.scan_id,
                        control_id="CTRL-011-005",
                        type=EvidenceType.DOCUMENTATION,
                        source=EvidenceSource(
                            type="file",
                            path=str(file.relative_to(self.repo_path))
                        ),
                        content_preview=content_preview,
                        status=EvidenceStatus.VALID,
                        confidence_score=1.0
                    ))
        
        return evidence
    
    def _scan_logging_config(self) -> List[Evidence]:
        """Check for logging configuration"""
        evidence = []
        
        # Config files
        config_patterns = ["logging.conf", "logging.ini", "logging.yaml", "logging.json"]
        for pattern in config_patterns:
            for file in self.repo_path.rglob(pattern):
                evidence.append(Evidence(
                    scan_id=self.scan_id,
                    control_id="CTRL-012-001",
                    type=EvidenceType.CONFIG,
                    source=EvidenceSource(
                        type="file",
                        path=str(file.relative_to(self.repo_path))
                    ),
                    status=EvidenceStatus.VALID,
                    confidence_score=1.0
                ))
        
        # Code with logging setup
        for file in self.repo_path.rglob("*.py"):
            if self._file_contains_pattern(file, ["import logging", "logging.basicConfig"]):
                evidence.append(Evidence(
                    scan_id=self.scan_id,
                    control_id="CTRL-012-001",
                    type=EvidenceType.CODE,
                    source=EvidenceSource(
                        type="file",
                        path=str(file.relative_to(self.repo_path))
                    ),
                    status=EvidenceStatus.VALID,
                    confidence_score=0.7
                ))
                break  # Just one example
        
        return evidence[:3]
    
    def _scan_audit_trail(self) -> List[Evidence]:
        """Check for audit trail implementation"""
        evidence = []
        
        # Look for audit-related code
        keywords = ["audit", "log", "track", "record"]
        
        for file in self.repo_path.rglob("*.py"):
            if any(keyword in file.name.lower() for keyword in keywords):
                if self._file_contains_pattern(file, keywords):
                    evidence.append(Evidence(
                        scan_id=self.scan_id,
                        control_id="CTRL-012-002",
                        type=EvidenceType.CODE,
                        source=EvidenceSource(
                            type="file",
                            path=str(file.relative_to(self.repo_path))
                        ),
                        status=EvidenceStatus.VALID,
                        confidence_score=0.6
                    ))
                    if len(evidence) >= 3:
                        break
        
        return evidence
    
    def _scan_ci_config(self) -> List[Evidence]:
        """Check for CI/CD configuration"""
        evidence = []
        
        # GitHub Actions
        gh_workflows = self.repo_path / ".github" / "workflows"
        if gh_workflows.exists():
            for file in gh_workflows.glob("*.yml"):
                evidence.append(Evidence(
                    scan_id=self.scan_id,
                    control_id="CTRL-015-003",
                    type=EvidenceType.CI_CD,
                    source=EvidenceSource(
                        type="file",
                        path=str(file.relative_to(self.repo_path))
                    ),
                    status=EvidenceStatus.VALID,
                    confidence_score=1.0
                ))
        
        # GitLab CI
        gitlab_ci = self.repo_path / ".gitlab-ci.yml"
        if gitlab_ci.exists():
            evidence.append(Evidence(
                scan_id=self.scan_id,
                control_id="CTRL-015-003",
                type=EvidenceType.CI_CD,
                source=EvidenceSource(
                    type="file",
                    path=str(gitlab_ci.relative_to(self.repo_path))
                ),
                status=EvidenceStatus.VALID,
                confidence_score=1.0
            ))
        
        # CircleCI
        circle_ci = self.repo_path / ".circleci" / "config.yml"
        if circle_ci.exists():
            evidence.append(Evidence(
                scan_id=self.scan_id,
                control_id="CTRL-015-003",
                type=EvidenceType.CI_CD,
                source=EvidenceSource(
                    type="file",
                    path=str(circle_ci.relative_to(self.repo_path))
                ),
                status=EvidenceStatus.VALID,
                confidence_score=1.0
            ))
        
        return evidence[:5]
    
    def _scan_dependencies(self) -> List[Evidence]:
        """Check for dependency files"""
        evidence = []
        
        dep_files = [
            "requirements.txt",
            "package.json",
            "Pipfile",
            "poetry.lock",
            "yarn.lock",
            "go.mod",
            "Gemfile"
        ]
        
        for dep_file in dep_files:
            file_path = self.repo_path / dep_file
            if file_path.exists():
                evidence.append(Evidence(
                    scan_id=self.scan_id,
                    control_id="CTRL-015-004",
                    type=EvidenceType.FILE,
                    source=EvidenceSource(
                        type="file",
                        path=dep_file
                    ),
                    status=EvidenceStatus.VALID,
                    confidence_score=1.0,
                    metadata={"dependency_manager": dep_file}
                ))
        
        return evidence
    
    def _scan_system_docs(self) -> List[Evidence]:
        """Check for system documentation"""
        evidence = []
        
        # Check docs folder
        docs_dir = self.repo_path / "docs"
        if docs_dir.exists():
            for file in docs_dir.glob("*.md"):
                if any(keyword in file.name.lower() for keyword in ["system", "overview", "architecture"]):
                    evidence.append(Evidence(
                        scan_id=self.scan_id,
                        control_id="CTRL-ANX4-001",
                        type=EvidenceType.DOCUMENTATION,
                        source=EvidenceSource(
                            type="file",
                            path=str(file.relative_to(self.repo_path))
                        ),
                        status=EvidenceStatus.VALID,
                        confidence_score=0.8
                    ))
        
        # Check README for system description
        readme = self.repo_path / "README.md"
        if readme.exists():
            content = self._read_file_preview(readme, max_chars=1000)
            if any(keyword in content.lower() for keyword in ["system", "architecture", "overview"]):
                evidence.append(Evidence(
                    scan_id=self.scan_id,
                    control_id="CTRL-ANX4-001",
                    type=EvidenceType.DOCUMENTATION,
                    source=EvidenceSource(
                        type="file",
                        path="README.md"
                    ),
                    content_preview=content[:200],
                    status=EvidenceStatus.VALID,
                    confidence_score=0.6
                ))
        
        return evidence[:3]
    
    def _scan_requirements(self) -> List[Evidence]:
        """Check for requirements documentation"""
        evidence = []
        
        for file in ["requirements.txt", "Dockerfile", "docker-compose.yml"]:
            file_path = self.repo_path / file
            if file_path.exists():
                evidence.append(Evidence(
                    scan_id=self.scan_id,
                    control_id="CTRL-ANX4-003",
                    type=EvidenceType.CONFIG,
                    source=EvidenceSource(
                        type="file",
                        path=file
                    ),
                    status=EvidenceStatus.VALID,
                    confidence_score=1.0
                ))
        
        return evidence
    
    def _scan_version(self) -> List[Evidence]:
        """Check for version information"""
        evidence = []
        
        version_files = ["VERSION", "version.txt", "CHANGELOG.md"]
        for file in version_files:
            file_path = self.repo_path / file
            if file_path.exists():
                evidence.append(Evidence(
                    scan_id=self.scan_id,
                    control_id="CTRL-ANX4-005",
                    type=EvidenceType.FILE,
                    source=EvidenceSource(
                        type="file",
                        path=file
                    ),
                    status=EvidenceStatus.VALID,
                    confidence_score=1.0
                ))
        
        # Check package.json or pyproject.toml for version
        for file in ["package.json", "pyproject.toml"]:
            file_path = self.repo_path / file
            if file_path.exists():
                if self._file_contains_pattern(file_path, ["version"]):
                    evidence.append(Evidence(
                        scan_id=self.scan_id,
                        control_id="CTRL-ANX4-005",
                        type=EvidenceType.CONFIG,
                        source=EvidenceSource(
                            type="file",
                            path=file
                        ),
                        status=EvidenceStatus.VALID,
                        confidence_score=0.9
                    ))
        
        return evidence[:3]
    
    # ============= HELPERS =============
    
    def _file_contains_pattern(self, file_path: Path, patterns: List[str]) -> bool:
        """Check if file contains any of the patterns"""
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            return any(pattern.lower() in content.lower() for pattern in patterns)
        except:
            return False
    
    def _read_file_preview(self, file_path: Path, max_chars: int = 500) -> str:
        """Read preview of file content"""
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            return content[:max_chars]
        except:
            return ""
    
    def _create_finding(self, control_id: str, evidence_items: List[Evidence]) -> Finding:
        """Create finding based on evidence"""
        control = get_control_by_id(control_id)
        
        if not evidence_items:
            # No evidence found
            status = FindingStatus.NON_COMPLIANT
            confidence = 0.0
            gaps = [Gap(
                description=f"No evidence found for {control.title}",
                severity=control.priority,
                recommendation=f"Add {', '.join(control.evidence_requirements[:3])}",
                required_evidence=control.evidence_requirements
            )]
        elif len(evidence_items) >= len(control.evidence_requirements) * 0.5:
            # Good evidence coverage
            status = FindingStatus.COMPLIANT
            confidence = min(1.0, len(evidence_items) / len(control.evidence_requirements))
            gaps = []
        else:
            # Partial evidence
            status = FindingStatus.PARTIAL
            confidence = len(evidence_items) / max(1, len(control.evidence_requirements))
            gaps = [Gap(
                description=f"Incomplete evidence for {control.title}",
                severity=SeverityLevel.MEDIUM,
                recommendation=f"Add more documentation: {', '.join(control.evidence_requirements)}",
                required_evidence=control.evidence_requirements
            )]
        
        return Finding(
            scan_id=self.scan_id,
            control_id=control_id,
            control_title=control.title,
            article=control.article,
            status=status,
            confidence=confidence,
            auto_verified=True,
            evidence_ids=[ev.id for ev in evidence_items],
            evidence_count=len(evidence_items),
            gaps=gaps,
            recommendation=gaps[0].recommendation if gaps else "Control satisfied",
            severity=control.priority
        )


def extract_zip_to_temp(zip_file_path: str) -> Path:
    """Extract zip file to temporary directory"""
    temp_dir = Path(tempfile.mkdtemp(prefix="repo_scan_"))
    
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)
    
    # Find the actual repo root (might be nested)
    subdirs = list(temp_dir.iterdir())
    if len(subdirs) == 1 and subdirs[0].is_dir():
        return subdirs[0]
    
    return temp_dir


def calculate_coverage(findings: List[Finding]) -> CoverageStats:
    """Calculate coverage statistics"""
    total = len(findings)
    compliant = sum(1 for f in findings if f.status == FindingStatus.COMPLIANT)
    partial = sum(1 for f in findings if f.status == FindingStatus.PARTIAL)
    non_compliant = sum(1 for f in findings if f.status == FindingStatus.NON_COMPLIANT)
    
    coverage_pct = (compliant + 0.5 * partial) / max(1, total) * 100
    
    # By article
    article_coverage = {}
    by_article = {}
    for finding in findings:
        article = finding.article
        if article not in by_article:
            by_article[article] = {"total": 0, "compliant": 0, "partial": 0}
        by_article[article]["total"] += 1
        if finding.status == FindingStatus.COMPLIANT:
            by_article[article]["compliant"] += 1
        elif finding.status == FindingStatus.PARTIAL:
            by_article[article]["partial"] += 1
    
    for article, stats in by_article.items():
        article_coverage[article] = round(
            (stats["compliant"] + 0.5 * stats["partial"]) / stats["total"] * 100,
            1
        )
    
    return CoverageStats(
        total_controls=total,
        checked_controls=total,
        compliant=compliant,
        partial=partial,
        non_compliant=non_compliant,
        not_applicable=0,
        pending=0,
        coverage_percentage=round(coverage_pct, 1),
        automated_checked=total,
        automated_compliant=compliant,
        article_coverage=article_coverage
    )
