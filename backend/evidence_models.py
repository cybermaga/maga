"""Data models for evidence-based compliance scanning"""
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime, timezone
import uuid


class Finding(BaseModel):
    """Represents a compliance finding from code analysis"""
    control_id: str
    description: str
    severity: str  # critical, high, medium, low, info
    status: str  # pass, fail, warning
    article_reference: str
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    recommendation: Optional[str] = None


class Evidence(BaseModel):
    """Represents evidence of compliance found in repository"""
    control_id: str
    description: str
    file_path: str
    status: str  # present, absent, partial
    article_reference: str
    evidence_type: str  # file, code, documentation, test, etc.


class CoverageStats(BaseModel):
    """Statistics about compliance coverage"""
    total_controls: int
    controls_passed: int
    controls_failed: int
    coverage_percentage: float


class EvidenceScan(BaseModel):
    """Complete evidence-based scan result"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    system_name: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    repository_path: Optional[str] = None
    findings: List[Finding] = []
    evidence_items: List[Evidence] = []
    coverage_stats: CoverageStats
    metadata: Dict = {}
