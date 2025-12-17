import os
from models import EvidenceRunRequest, EvidenceRunResponse, ArtifactUploadResponse
from pydantic import BaseModel
from typing import Any, Dict, Optional

class GenericResponse(BaseModel):
    status: str = "ok"
    message: Optional[str] = None
    data: Optional[Dict[str, Any]] = None

EvidenceRunResponse = GenericResponse
EvidenceSummary = GenericResponse
List = GenericResponse
# END AUTO-GENERATED RESPONSE MODELS

from pydantic import BaseModel
from typing import Optional, Any, Dict

class ArtifactUploadResponse(BaseModel):
    artifact_id: str
    status: str = "uploaded"
    filename: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
from fastapi import FastAPI, APIRouter, HTTPException, Response, UploadFile, File, Form
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Dict, Optional
import uuid
from datetime import datetime, timezone
import tempfile
import shutil

# Import SDK modules
from sdk import RiskClassifier, ComplianceChecker, DocumentAnalyzer, ReportGenerator

# Import evidence-based scanning modules
from evidence_models import EvidenceScan, Finding, Evidence, CoverageStats
from repo_scanner import RepositoryScanner
from controls_definitions import controls_to_dict

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
import os

MONGO_URL = os.getenv("MONGO_URL", "mongodb://mongodb:27017")
DB_NAME = os.getenv("DB_NAME", "emergent")
client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]

# Create the main app without a prefix
app = FastAPI(title="Emergent AI Compliance API")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Initialize SDK components
risk_classifier = RiskClassifier()
compliance_checker = ComplianceChecker()
document_analyzer = DocumentAnalyzer()
report_generator = ReportGenerator()

# Initialize evidence-based scanner
repo_scanner = RepositoryScanner()


# Define Models
class ComplianceScanRequest(BaseModel):
    """Request model for compliance scan"""
    system_name: str
    description: str
    use_case: str
    application_domain: str = ""
    model_type: str = ""
    provider: str = ""
    version: str = "1.0"
    
    # Optional documentation fields
    risk_management: str = ""
    data_governance: str = ""
    technical_docs: str = ""
    testing_procedures: str = ""
    human_oversight: str = ""
    accuracy_metrics: str = ""
    
    # NEW: Artifact IDs
    artifact_ids: List[str] = Field(default_factory=list)


class ComplianceScanResult(BaseModel):
    """Compliance scan result model"""
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    system_name: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    risk_classification: Dict
    compliance_results: Dict
    metadata: Dict


# API Routes
@api_router.get("/")
async def root():
    return {"message": "Emergent AI Compliance API", "version": "1.0.0"}


@api_router.get("/health")
async def health():
    """Health check endpoint"""
    return {"ok": True, "version": "0.1.0", "service": "emergent-ai-compliance"}


# ============= ARTIFACT ENDPOINTS =============

@api_router.post("/artifacts/upload", response_model=ArtifactUploadResponse)
async def upload_artifact(
    file: UploadFile = File(...),
    type: str = Form(...),
    scan_id: Optional[str] = Form(None)
):
    """Upload an artifact (code, model, dataset, doc, logs)"""
    try:
        # Validate type
        if type not in [t.value for t in ArtifactType]:
            raise HTTPException(status_code=400, detail=f"Invalid type. Must be one of: {[t.value for t in ArtifactType]}")
        
        # Check file size
        file.file.seek(0, 2)  # Seek to end
        file_size = file.file.tell()
        file.file.seek(0)  # Reset to start
        
        if file_size > MAX_UPLOAD_SIZE:
            raise HTTPException(status_code=413, detail=f"File too large. Max size: {MAX_UPLOAD_SIZE / 1024 / 1024}MB")
        
        # Generate artifact ID and paths
        artifact_id = str(uuid.uuid4())
        artifact_dir = ARTIFACTS_DIR / artifact_id
        artifact_dir.mkdir(parents=True, exist_ok=True)
        
        # Save file
        file_path = artifact_dir / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Calculate SHA256
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        sha256 = sha256_hash.hexdigest()
        
        # Extract if zip
        if file.filename.endswith('.zip'):
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(artifact_dir)
        
        # Create artifact record
        artifact = Artifact(
            id=artifact_id,
            scan_id=scan_id,
            type=ArtifactType(type),
            filename=file.filename,
            original_filename=file.filename,
            size=file_size,
            mime_type=file.content_type or "application/octet-stream",
            sha256=sha256,
            storage_path=str(artifact_dir),
            metadata={"original_name": file.filename}
        )
        
        # Save to database
        artifact_dict = artifact.model_dump()
        artifact_dict['uploaded_at'] = artifact_dict['uploaded_at'].isoformat()
        await db.artifacts.insert_one(artifact_dict)
        
        return ArtifactUploadResponse(
            artifact_id=artifact_id,
            filename=file.filename,
            size=file_size,
            type=ArtifactType(type),
            message="Artifact uploaded successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error uploading artifact: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@api_router.get("/artifacts/{artifact_id}")
async def get_artifact(artifact_id: str):
    """Get artifact metadata"""
    artifact = await db.artifacts.find_one({"id": artifact_id}, {"_id": 0})
    if not artifact:
        raise HTTPException(status_code=404, detail="Artifact not found")
    return artifact


# ============= EVIDENCE ENDPOINTS =============

@api_router.post("/evidence/run", response_model=EvidenceRunResponse)
async def run_evidence_analyzers(request: EvidenceRunRequest):
    """Run evidence analyzers for a scan"""
    try:
        # Validate scan exists
        scan = await db.compliance_scans.find_one({"id": request.scan_id}, {"_id": 0})
        if not scan:
            raise HTTPException(status_code=404, detail="Scan not found")
        
        # Get artifacts for this scan
        artifacts = await db.artifacts.find({"scan_id": request.scan_id}, {"_id": 0}).to_list(100)
        
        if not artifacts:
            raise HTTPException(status_code=400, detail="No artifacts found for this scan")
        
        # Generate job ID
        job_id = str(uuid.uuid4())
        
        # Dispatch Celery tasks
        task_results = []
        for artifact in artifacts:
            artifact_id = artifact['id']
            artifact_type = artifact['type']
            
            # Run relevant analyzers based on artifact type and requested rules
            if 'deps' in request.rules and artifact_type in ['code']:
                task = celery_app.send_task('run_pip_audit', args=[artifact_id, request.scan_id])
                task_results.append(task.id)
            
            if 'bandit' in request.rules and artifact_type in ['code']:
                task = celery_app.send_task('run_bandit', args=[artifact_id, request.scan_id])
                task_results.append(task.id)
            
            if 'onnx_meta' in request.rules and artifact_type in ['model']:
                task = celery_app.send_task('run_onnx_meta', args=[artifact_id, request.scan_id])
                task_results.append(task.id)
            
            if 'dataset_sanity' in request.rules and artifact_type in ['dataset']:
                task = celery_app.send_task('run_dataset_sanity', args=[artifact_id, request.scan_id])
                task_results.append(task.id)
        
        return EvidenceRunResponse(
            job_id=job_id,
            scan_id=request.scan_id,
            rules=request.rules,
            status="running",
            message=f"Dispatched {len(task_results)} analysis tasks"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error running evidence analyzers: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to run analyzers: {str(e)}")


@api_router.get("/evidence/{scan_id}", response_model=EvidenceSummary)
async def get_evidence(scan_id: str):
    """Get all evidence for a scan"""
    try:
        # Get all evidence for this scan
        evidence_list = await db.evidence.find({"scan_id": scan_id}, {"_id": 0}).to_list(1000)
        
        # Convert datetime strings back to datetime objects
        for ev in evidence_list:
            if isinstance(ev.get('created_at'), str):
                ev['created_at'] = datetime.fromisoformat(ev['created_at'])
        
        # Count by status
        passed = sum(1 for ev in evidence_list if ev.get('status') == 'pass')
        warned = sum(1 for ev in evidence_list if ev.get('status') == 'warn')
        failed = sum(1 for ev in evidence_list if ev.get('status') == 'fail')
        pending = sum(1 for ev in evidence_list if ev.get('status') == 'pending')
        
        return EvidenceSummary(
            scan_id=scan_id,
            total_evidence=len(evidence_list),
            passed=passed,
            warned=warned,
            failed=failed,
            pending=pending,
            evidence_list=evidence_list
        )
        
    except Exception as e:
        logging.error(f"Error fetching evidence: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch evidence: {str(e)}")


@api_router.get("/evidence/{scan_id}/{evidence_id}/raw")
async def get_raw_evidence(scan_id: str, evidence_id: str):
    """Get raw JSON evidence output"""
    try:
        evidence = await db.evidence.find_one({"id": evidence_id, "scan_id": scan_id}, {"_id": 0})
        
        if not evidence:
            raise HTTPException(status_code=404, detail="Evidence not found")
        
        raw_path = evidence.get('raw_output_path')
        if not raw_path or not Path(raw_path).exists():
            return {"details": evidence.get('details', {})}
        
        with open(raw_path, 'r') as f:
            raw_data = f.read()
        
        return Response(content=raw_data, media_type="application/json")
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error fetching raw evidence: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch raw evidence: {str(e)}")


# ============= UPDATED COMPLIANCE SCAN ENDPOINTS =============


@api_router.post("/compliance/scan", response_model=ComplianceScanResult)
async def create_compliance_scan(request: ComplianceScanRequest):
    """Run a compliance scan on an AI system"""
    try:
        # Parse metadata
        metadata = document_analyzer.parse_metadata(request.model_dump())
        
        # Validate metadata
        is_valid, missing_fields = document_analyzer.validate_metadata(metadata)
        if not is_valid:
            raise HTTPException(
                status_code=400,
                detail=f"Missing required fields: {', '.join(missing_fields)}"
            )
        
        # Classify risk level
        risk_classification = risk_classifier.classify(metadata)
        
        # Check compliance (only relevant for high-risk systems)
        documents = []
        for key, value in metadata['documentation'].items():
            if value:
                documents.append(value)
        
        compliance_results = compliance_checker.check_compliance(metadata, documents)
        
        # Create result object
        scan_result = ComplianceScanResult(
            system_name=metadata['system_name'],
            risk_classification=risk_classification,
            compliance_results=compliance_results,
            metadata=metadata
        )
        
        # Store in database
        result_dict = scan_result.model_dump()
        result_dict['timestamp'] = result_dict['timestamp'].isoformat()
        
        # Add artifact_ids to the scan record
        result_dict['artifact_ids'] = request.artifact_ids
        
        await db.compliance_scans.insert_one(result_dict)
        
        # Update artifacts with scan_id
        if request.artifact_ids:
            for artifact_id in request.artifact_ids:
                await db.artifacts.update_one(
                    {"id": artifact_id},
                    {"$set": {"scan_id": scan_result.id}}
                )
        
        return scan_result
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error in compliance scan: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@api_router.get("/compliance/reports", response_model=List[ComplianceScanResult])
async def get_compliance_reports():
    """Get all compliance scan reports"""
    try:
        reports = await db.compliance_scans.find({}, {"_id": 0}).sort("timestamp", -1).to_list(100)
        
        # Convert ISO string timestamps back to datetime objects
        for report in reports:
            if isinstance(report['timestamp'], str):
                report['timestamp'] = datetime.fromisoformat(report['timestamp'])
        
        return reports
    except Exception as e:
        logging.error(f"Error fetching reports: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching reports: {str(e)}")


@api_router.get("/compliance/reports/{report_id}", response_model=ComplianceScanResult)
async def get_compliance_report(report_id: str):
    """Get a specific compliance report by ID"""
    try:
        report = await db.compliance_scans.find_one({"id": report_id}, {"_id": 0})
        
        if not report:
            raise HTTPException(status_code=404, detail="Report not found")
        
        # Convert ISO string timestamp back to datetime
        if isinstance(report['timestamp'], str):
            report['timestamp'] = datetime.fromisoformat(report['timestamp'])
        
        return report
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error fetching report: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching report: {str(e)}")


@api_router.get("/compliance/reports/{report_id}/export")
async def export_report(report_id: str, format: str = "html"):
    """Export report in specified format (html or pdf)"""
    try:
        # Fetch report
        report = await db.compliance_scans.find_one({"id": report_id}, {"_id": 0})
        
        if not report:
            raise HTTPException(status_code=404, detail="Report not found")
        
        # Convert ISO string timestamp back to datetime
        if isinstance(report['timestamp'], str):
            report['timestamp'] = datetime.fromisoformat(report['timestamp'])
        
        # Generate report in requested format
        if format.lower() == "pdf":
            pdf_bytes = report_generator.generate_pdf_report(report)
            return Response(
                content=pdf_bytes,
                media_type="application/pdf",
                headers={
                    "Content-Disposition": f"attachment; filename=compliance_report_{report_id}.pdf"
                }
            )
        elif format.lower() == "html":
            html_content = report_generator.generate_html_report(report)
            return Response(
                content=html_content,
                media_type="text/html",
                headers={
                    "Content-Disposition": f"attachment; filename=compliance_report_{report_id}.html"
                }
            )
        elif format.lower() == "json":
            json_content = report_generator.generate_json_report(report)
            return Response(
                content=json_content,
                media_type="application/json",
                headers={
                    "Content-Disposition": f"attachment; filename=compliance_report_{report_id}.json"
                }
            )
        else:
            raise HTTPException(status_code=400, detail="Invalid format. Use 'html', 'pdf', or 'json'")
            
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error exporting report: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error exporting report: {str(e)}")


@api_router.delete("/compliance/reports/{report_id}")
async def delete_report(report_id: str):
    """Delete a compliance report"""
    try:
        result = await db.compliance_scans.delete_one({"id": report_id})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Report not found")
        
        return {"message": "Report deleted successfully", "id": report_id}
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error deleting report: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error deleting report: {str(e)}")


# ============================================
# Evidence-Based Repository Scanning Endpoints
# ============================================

@api_router.post("/compliance/scan/repo")
async def scan_repository(
    zip_file: UploadFile = File(...),
    system_name: str = Form(...)
):
    """
    Upload and scan a repository ZIP file for EU AI Act compliance.
    Returns evidence-based analysis with findings and coverage statistics.
    """
    try:
        # Validate file type
        if not zip_file.filename.endswith('.zip'):
            raise HTTPException(status_code=400, detail="File must be a ZIP archive")
        
        # Save uploaded file to temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as temp_file:
            shutil.copyfileobj(zip_file.file, temp_file)
            temp_path = temp_file.name
        
        try:
            # Scan the repository
            scan_result = repo_scanner.scan_zip(temp_path, system_name)
            
            # Convert to dict for MongoDB storage
            scan_dict = scan_result.model_dump()
            scan_dict['timestamp'] = scan_dict['timestamp'].isoformat()
            
            # Store in database
            await db.evidence_scans.insert_one(scan_dict)
            
            logging.info(f"Repository scan completed for {system_name}: {scan_result.id}")
            
            return scan_result
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.unlink(temp_path)
                
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error scanning repository: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error scanning repository: {str(e)}")


@api_router.get("/compliance/scan/repo/{scan_id}")
async def get_repository_scan(scan_id: str):
    """Get a specific repository scan result by ID"""
    try:
        scan = await db.evidence_scans.find_one({"id": scan_id}, {"_id": 0})
        
        if not scan:
            raise HTTPException(status_code=404, detail="Scan not found")
        
        # Convert ISO string timestamp back to datetime
        if isinstance(scan.get('timestamp'), str):
            scan['timestamp'] = datetime.fromisoformat(scan['timestamp'])
        
        return scan
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error fetching scan: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching scan: {str(e)}")


@api_router.get("/compliance/scan/repo")
async def get_all_repository_scans():
    """Get all repository scan results"""
    try:
        scans = await db.evidence_scans.find({}, {"_id": 0}).sort("timestamp", -1).to_list(100)
        
        # Convert ISO string timestamps back to datetime objects
        for scan in scans:
            if isinstance(scan.get('timestamp'), str):
                scan['timestamp'] = datetime.fromisoformat(scan['timestamp'])
        
        return scans
    except Exception as e:
        logging.error(f"Error fetching scans: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching scans: {str(e)}")


@api_router.delete("/compliance/scan/repo/{scan_id}")
async def delete_repository_scan(scan_id: str):
    """Delete a repository scan"""
    try:
        result = await db.evidence_scans.delete_one({"id": scan_id})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Scan not found")
        
        return {"message": "Scan deleted successfully", "id": scan_id}
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error deleting scan: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error deleting scan: {str(e)}")


@api_router.get("/controls")
async def get_controls():
    """Get all defined compliance controls"""
    try:
        controls = controls_to_dict()
        return {
            "total": len(controls),
            "controls": controls
        }
    except Exception as e:
        logging.error(f"Error fetching controls: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching controls: {str(e)}")


@api_router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": "1.0.0"
    }


# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
