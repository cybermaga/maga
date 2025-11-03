from fastapi import FastAPI, APIRouter, HTTPException, Response
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Dict, Optional
import uuid
from datetime import datetime, timezone

# Import SDK modules
from sdk import RiskClassifier, ComplianceChecker, DocumentAnalyzer, ReportGenerator

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI(title="Emergent AI Compliance API")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Initialize SDK components
risk_classifier = RiskClassifier()
compliance_checker = ComplianceChecker()
document_analyzer = DocumentAnalyzer()
report_generator = ReportGenerator()


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
    return {
        "message": "Emergent AI Compliance API",
        "version": "1.0.0",
        "documentation": "/docs"
    }


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
        await db.compliance_scans.insert_one(result_dict)
        
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


# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
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
