"""Repository scanner for evidence-based compliance analysis"""
import os
import zipfile
import tempfile
import shutil
from pathlib import Path
from typing import List, Dict, Tuple
import logging

from evidence_models import Finding, Evidence, CoverageStats, EvidenceScan
from controls_definitions import get_all_controls, Control

logger = logging.getLogger(__name__)


class RepositoryScanner:
    """Scans code repositories for EU AI Act compliance evidence"""
    
    def __init__(self):
        self.controls = get_all_controls()
    
    def scan_zip(self, zip_path: str, system_name: str) -> EvidenceScan:
        """Scan a ZIP file containing a repository"""
        logger.info(f"Starting scan of {zip_path} for system: {system_name}")
        
        # Extract ZIP to temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)
                
                # Scan the extracted repository
                findings, evidence = self._scan_directory(temp_dir)
                
                # Calculate coverage statistics
                coverage_stats = self._calculate_coverage(findings)
                
                # Create scan result
                scan_result = EvidenceScan(
                    system_name=system_name,
                    repository_path=zip_path,
                    findings=findings,
                    evidence_items=evidence,
                    coverage_stats=coverage_stats,
                    metadata={"scan_type": "repository", "source": "zip_upload"}
                )
                
                logger.info(f"Scan completed: {len(findings)} findings, {len(evidence)} evidence items")
                return scan_result
                
            except zipfile.BadZipFile:
                logger.error(f"Invalid ZIP file: {zip_path}")
                raise ValueError("Invalid ZIP file")
            except Exception as e:
                logger.error(f"Error scanning repository: {e}")
                raise
    
    def _scan_directory(self, directory: str) -> Tuple[List[Finding], List[Evidence]]:
        """Scan a directory for compliance evidence"""
        findings = []
        evidence = []
        
        dir_path = Path(directory)
        
        # Get all files in repository
        all_files = []
        for root, dirs, files in os.walk(directory):
            # Skip common non-code directories
            dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', 'node_modules', '.venv', 'venv']]
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, directory)
                all_files.append(rel_path)
        
        # Check each control
        for control in self.controls:
            if control.check_type == "file_presence":
                result = self._check_file_presence(control, all_files, directory)
                if result['finding']:
                    findings.append(result['finding'])
                if result['evidence']:
                    evidence.append(result['evidence'])
            
            elif control.check_type == "code_analysis":
                result = self._check_code_patterns(control, all_files, directory)
                if result['finding']:
                    findings.append(result['finding'])
                if result['evidence']:
                    evidence.append(result['evidence'])
            
            elif control.check_type == "security_scan":
                result = self._check_security(control, all_files, directory)
                if result['finding']:
                    findings.append(result['finding'])
        
        return findings, evidence
    
    def _check_file_presence(self, control: Control, files: List[str], base_dir: str) -> Dict:
        """Check for presence of specific files"""
        # Define file patterns for each control
        file_patterns = {
            "C-ART9-001": ["risk", "risk_management", "risk_assessment"],
            "C-ART9-002": ["risk_assessment", "risk_analysis"],
            "C-ART10-001": ["data", "dataset", "training_data"],
            "C-ART11-001": ["readme.md", "readme.txt", "readme"],
            "C-ART11-002": ["architecture", "model", "design"],
            "C-ART11-003": ["metrics", "performance", "evaluation"],
            "C-ART13-001": ["user_guide", "manual", "documentation"],
            "C-ART14-001": ["oversight", "review", "approval"],
            "C-ART15-001": ["test", "tests", "testing"],
        }
        
        patterns = file_patterns.get(control.control_id, [])
        found_files = []
        
        for file in files:
            file_lower = file.lower()
            for pattern in patterns:
                if pattern in file_lower:
                    found_files.append(file)
                    break
        
        if found_files:
            # Control passed
            return {
                'finding': Finding(
                    control_id=control.control_id,
                    description=control.description,
                    severity=control.severity,
                    status="pass",
                    article_reference=control.article,
                    file_path=found_files[0],
                    recommendation=None
                ),
                'evidence': Evidence(
                    control_id=control.control_id,
                    description=f"Found: {found_files[0]}",
                    file_path=found_files[0],
                    status="present",
                    article_reference=control.article,
                    evidence_type="file"
                )
            }
        else:
            # Control failed
            return {
                'finding': Finding(
                    control_id=control.control_id,
                    description=control.description,
                    severity=control.severity,
                    status="fail",
                    article_reference=control.article,
                    recommendation=f"Add documentation for {control.title}"
                ),
                'evidence': None
            }
    
    def _check_code_patterns(self, control: Control, files: List[str], base_dir: str) -> Dict:
        """Check for specific code patterns"""
        # Define code patterns for each control
        code_patterns = {
            "C-ART10-002": ["validate", "quality", "check"],
            "C-ART10-003": ["bias", "fairness", "discrimination"],
            "C-ART12-001": ["logging", "logger", "log"],
            "C-ART12-002": ["audit", "trail", "history"],
            "C-ART13-002": ["explain", "interpret", "shap", "lime"],
            "C-ART14-002": ["override", "manual", "human_review"],
            "C-ART15-002": ["test", "assert", "unittest"],
            "C-ART15-004": ["validate", "sanitize", "verify"],
            "C-ART15-005": ["try", "except", "error", "exception"],
        }
        
        patterns = code_patterns.get(control.control_id, [])
        found = False
        found_file = None
        
        # Search in Python files
        python_files = [f for f in files if f.endswith('.py')]
        
        for file in python_files[:10]:  # Check first 10 Python files
            try:
                file_path = os.path.join(base_dir, file)
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read().lower()
                    for pattern in patterns:
                        if pattern in content:
                            found = True
                            found_file = file
                            break
                if found:
                    break
            except Exception:
                continue
        
        if found:
            return {
                'finding': Finding(
                    control_id=control.control_id,
                    description=control.description,
                    severity=control.severity,
                    status="pass",
                    article_reference=control.article,
                    file_path=found_file,
                    recommendation=None
                ),
                'evidence': Evidence(
                    control_id=control.control_id,
                    description=f"Code pattern found in {found_file}",
                    file_path=found_file,
                    status="present",
                    article_reference=control.article,
                    evidence_type="code"
                )
            }
        else:
            return {
                'finding': Finding(
                    control_id=control.control_id,
                    description=control.description,
                    severity=control.severity,
                    status="fail",
                    article_reference=control.article,
                    recommendation=f"Implement {control.title}"
                ),
                'evidence': None
            }
    
    def _check_security(self, control: Control, files: List[str], base_dir: str) -> Dict:
        """Check for security issues"""
        # Simple security check - look for common issues
        python_files = [f for f in files if f.endswith('.py')]
        
        security_issues = []
        
        for file in python_files[:20]:  # Check first 20 files
            try:
                file_path = os.path.join(base_dir, file)
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    # Check for hardcoded credentials
                    if any(pattern in content.lower() for pattern in ['password =', 'api_key =', 'secret =']):
                        security_issues.append((file, "Potential hardcoded credentials"))
            except Exception:
                continue
        
        if security_issues:
            return {
                'finding': Finding(
                    control_id=control.control_id,
                    description=f"{control.description} - Found {len(security_issues)} potential issue(s)",
                    severity="high",
                    status="fail",
                    article_reference=control.article,
                    file_path=security_issues[0][0],
                    recommendation="Review and fix security vulnerabilities"
                ),
                'evidence': None
            }
        else:
            return {
                'finding': Finding(
                    control_id=control.control_id,
                    description=control.description,
                    severity=control.severity,
                    status="pass",
                    article_reference=control.article,
                    recommendation=None
                ),
                'evidence': None
            }
    
    def _calculate_coverage(self, findings: List[Finding]) -> CoverageStats:
        """Calculate compliance coverage statistics"""
        total = len(self.controls)
        passed = len([f for f in findings if f.status == "pass"])
        failed = len([f for f in findings if f.status == "fail"])
        
        coverage_percentage = (passed / total * 100) if total > 0 else 0
        
        return CoverageStats(
            total_controls=total,
            controls_passed=passed,
            controls_failed=failed,
            coverage_percentage=round(coverage_percentage, 2)
        )
