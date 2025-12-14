"""Evidence-based compliance models"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Literal
from datetime import datetime, timezone
from enum import Enum
import uuid


class AutomationLevel(str, Enum):
    """Level of automation for control verification"""
    AUTOMATED = "automated"
    SEMI_AUTOMATED = "semi-automated"
    MANUAL = "manual"


class EvidenceType(str, Enum):
    """Types of evidence"""
    FILE = "file"
    CODE = "code"
    CONFIG = "config"
    TEST = "test"
    LOG = "log"
    METRIC = "metric"
    DOCUMENTATION = "documentation"
    GIT = "git"
    CI_CD = "ci_cd"


class EvidenceStatus(str, Enum):
    """Status of evidence"""
    VALID = "valid"
    INVALID = "invalid"
    EXPIRED = "expired"
    MISSING = "missing"
    PENDING = "pending"


class FindingStatus(str, Enum):
    """Status of finding after verification"""
    COMPLIANT = "compliant"
    PARTIAL = "partial"
    NON_COMPLIANT = "non_compliant"
    NOT_APPLICABLE = "not_applicable"
    PENDING = "pending"


class SeverityLevel(str, Enum):
    """Severity of finding"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class ScanType(str, Enum):
    """Type of compliance scan"""
    QUESTIONNAIRE = "questionnaire"
    EVIDENCE = "evidence"
    HYBRID = "hybrid"


class ScanMethod(str, Enum):
    """Method used for scanning"""
    REPO = "repo"
    UPLOAD = "upload"
    API = "api"
    HYBRID = "hybrid"


# ============= CONTROL =============

class Control(BaseModel):
    """Control requirement from AI Act"""
    id: str = Field(..., description="Control ID, e.g., CTRL-009-001")
    article: str = Field(..., description="AI Act article, e.g., Article 9")
    article_number: int = Field(..., description="Article number for sorting")
    title: str
    description: str
    category: str = Field(..., description="Category: documentation, code, config, etc.")
    automation_level: AutomationLevel
    evidence_requirements: List[str] = Field(
        default_factory=list,
        description="List of required evidence patterns"
    )
    priority: SeverityLevel = Field(default=SeverityLevel.MEDIUM)
    references: List[str] = Field(default_factory=list, description="Links to regulations")
    tags: List[str] = Field(default_factory=list)


class ControlMapping(BaseModel):
    """Mapping between controls and AI Act articles"""
    article: str
    article_number: int
    controls: List[Control]
    total_controls: int
    automated_controls: int
    manual_controls: int


# ============= EVIDENCE =============

class EvidenceSource(BaseModel):
    """Source of evidence"""
    type: Literal["file", "directory", "git", "api", "manual"]
    path: Optional[str] = None
    url: Optional[str] = None
    commit: Optional[str] = None
    line_start: Optional[int] = None
    line_end: Optional[int] = None


class Evidence(BaseModel):
    """Evidence artifact"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    scan_id: str
    control_id: str
    type: EvidenceType
    source: EvidenceSource
    collected_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    content_hash: Optional[str] = None
    content_preview: Optional[str] = Field(None, max_length=500)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    status: EvidenceStatus = EvidenceStatus.VALID
    confidence_score: float = Field(default=0.0, ge=0.0, le=1.0)
    auto_collected: bool = True


# ============= FINDING =============

class Gap(BaseModel):
    """Compliance gap identified"""
    description: str
    severity: SeverityLevel
    recommendation: str
    required_evidence: List[str] = Field(default_factory=list)


class Finding(BaseModel):
    """Verification result for a control"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    scan_id: str
    control_id: str
    control_title: str
    article: str
    status: FindingStatus
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence in finding")
    auto_verified: bool
    evidence_ids: List[str] = Field(default_factory=list)
    evidence_count: int = 0
    gaps: List[Gap] = Field(default_factory=list)
    recommendation: str = ""
    severity: SeverityLevel = SeverityLevel.INFO
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)


# ============= EVIDENCE SCAN =============

class ScanTarget(BaseModel):
    """Target of the scan"""
    type: Literal["repository", "upload", "api"]
    path: Optional[str] = None
    url: Optional[str] = None
    commit: Optional[str] = None
    branch: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class CoverageStats(BaseModel):
    """Coverage statistics"""
    total_controls: int
    checked_controls: int
    compliant: int
    partial: int
    non_compliant: int
    not_applicable: int
    pending: int
    coverage_percentage: float = Field(..., ge=0.0, le=100.0)
    
    # By automation level
    automated_checked: int = 0
    automated_compliant: int = 0
    manual_required: int = 0
    manual_provided: int = 0
    
    # By article
    article_coverage: Dict[str, float] = Field(default_factory=dict)


class EvidenceScan(BaseModel):
    """Complete evidence-based scan result"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    type: ScanType
    scan_method: ScanMethod
    target: ScanTarget
    
    # Results
    findings: List[Finding] = Field(default_factory=list)
    evidence_count: int = 0
    coverage: CoverageStats
    
    # Metadata
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: Optional[datetime] = None
    duration_seconds: Optional[float] = None
    scanner_version: str = "1.0.0"
    
    # Links to other scans
    questionnaire_scan_id: Optional[str] = None
    related_scan_ids: List[str] = Field(default_factory=list)
    
    metadata: Dict[str, Any] = Field(default_factory=dict)


# ============= SCAN REQUEST/RESPONSE =============

class RepoScanRequest(BaseModel):
    """Request for repository scan"""
    name: str = Field(..., description="Name of the scan")
    repo_path: Optional[str] = Field(None, description="Local path to repository")
    repo_url: Optional[str] = Field(None, description="Git repository URL")
    branch: str = Field(default="main")
    commit: Optional[str] = None
    
    # Scan options
    include_git_history: bool = True
    max_file_size_mb: int = 10
    exclude_patterns: List[str] = Field(
        default_factory=lambda: [
            "node_modules/", "__pycache__/", ".git/", "*.pyc", "*.log"
        ]
    )
    
    # Control selection
    articles: Optional[List[int]] = Field(None, description="Specific articles to check")
    controls: Optional[List[str]] = Field(None, description="Specific control IDs")


class RepoScanResponse(BaseModel):
    """Response from repository scan"""
    scan_id: str
    status: str = "running"
    message: str
    estimated_duration_seconds: int = 60


class EvidenceScanResult(BaseModel):
    """Detailed scan result for UI"""
    scan: EvidenceScan
    findings_by_article: Dict[str, List[Finding]]
    critical_findings: List[Finding]
    recommendations: List[str]
    summary: str


# ============= ARTIFACT MAPPING =============

class ArtifactMapping(BaseModel):
    """User-uploaded artifact mapped to controls"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    artifact_id: str
    control_ids: List[str]
    mapped_by: str = "user"  # user | auto
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    notes: str = ""
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
