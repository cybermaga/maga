"""Pydantic models for artifacts, evidence, and enhanced reports"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from enum import Enum
import uuid


class ArtifactType(str, Enum):
    """Types of artifacts that can be uploaded"""
    CODE = "code"
    MODEL = "model"
    DATASET = "dataset"
    DOC = "doc"
    LOGS = "logs"


class EvidenceStatus(str, Enum):
    """Evidence check status"""
    PASS = "pass"
    WARN = "warn"
    FAIL = "fail"
    PENDING = "pending"
    ERROR = "error"


class Artifact(BaseModel):
    """Artifact metadata"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    scan_id: Optional[str] = None
    type: ArtifactType
    filename: str
    original_filename: str
    size: int
    mime_type: str
    sha256: str
    storage_path: str
    uploaded_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)


class Evidence(BaseModel):
    """Evidence from analyzer runs"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    scan_id: str
    artifact_id: str
    rule: str  # deps, bandit, onnx_meta, dataset_sanity
    status: EvidenceStatus
    articles: List[str] = Field(default_factory=list)  # e.g. ["Article 15", "Article 17"]
    summary: str = ""
    details: Dict[str, Any] = Field(default_factory=dict)
    raw_output_path: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ArtifactUploadResponse(BaseModel):
    """Response for artifact upload"""
    artifact_id: str
    filename: str
    size: int
    type: ArtifactType
    message: str


class EvidenceRunRequest(BaseModel):
    """Request to run evidence analyzers"""
    scan_id: str
    rules: List[str] = Field(default=["deps", "bandit", "onnx_meta", "dataset_sanity"])


class EvidenceRunResponse(BaseModel):
    """Response for evidence run request"""
    job_id: str
    scan_id: str
    rules: List[str]
    status: str
    message: str


class EvidenceSummary(BaseModel):
    """Summary of evidence for a scan"""
    scan_id: str
    total_evidence: int
    passed: int
    warned: int
    failed: int
    pending: int
    evidence_list: List[Evidence]
