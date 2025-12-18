"""Celery worker configuration and tasks"""
from celery import Celery
import os
import json
import subprocess
import hashlib
from pathlib import Path
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

from config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND, ARTIFACTS_DIR, EVIDENCE_DIR, MONGO_URL, DB_NAME
from models import Evidence, EvidenceStatus
from mapping import get_articles_for_rule

# Initialize Celery
celery_app = Celery(
    'worker',
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)


def get_db():
    """Get MongoDB database"""
    client = AsyncIOMotorClient(MONGO_URL)
    return client[DB_NAME]


def save_evidence_sync(evidence: Evidence):
    """Save evidence to MongoDB synchronously"""
    async def _save():
        db = get_db()
        evidence_dict = evidence.model_dump()
        evidence_dict['created_at'] = evidence_dict['created_at'].isoformat()
        await db.evidence.insert_one(evidence_dict)
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(_save())
    loop.close()


@celery_app.task(name='run_pip_audit')
def run_pip_audit(artifact_id: str, scan_id: str):
    """Run pip-audit on Python dependencies"""
    try:
        artifact_dir = ARTIFACTS_DIR / artifact_id
        requirements_file = artifact_dir / "requirements.txt"
        
        if not requirements_file.exists():
            # Look for requirements.txt in uploaded zip
            for req_file in artifact_dir.rglob("requirements.txt"):
                requirements_file = req_file
                break
        
        if not requirements_file.exists():
            evidence = Evidence(
                scan_id=scan_id,
                artifact_id=artifact_id,
                rule="deps",
                status=EvidenceStatus.WARN,
                articles=get_articles_for_rule("deps"),
                summary="No requirements.txt found",
                details={"message": "No Python dependencies file found"}
            )
            save_evidence_sync(evidence)
            return {"status": "warn", "message": "No requirements.txt found"}
        
        # Run pip-audit
        result = subprocess.run(
            ["pip-audit", "--requirement", str(requirements_file), "--format", "json"],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        output_path = EVIDENCE_DIR / scan_id / "deps.json"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(result.stdout if result.stdout else result.stderr)
        
        # Parse results
        vulnerabilities = []
        if result.stdout:
            try:
                data = json.loads(result.stdout)
                vulnerabilities = data.get('dependencies', [])
            except json.JSONDecodeError:
                pass
        
        critical_count = sum(1 for v in vulnerabilities if v.get('vulns', []))
        status = EvidenceStatus.FAIL if critical_count > 0 else EvidenceStatus.PASS
        
        evidence = Evidence(
            scan_id=scan_id,
            artifact_id=artifact_id,
            rule="deps",
            status=status,
            articles=get_articles_for_rule("deps"),
            summary=f"Found {critical_count} packages with vulnerabilities" if critical_count > 0 else "No vulnerabilities found",
            details={
                "vulnerabilities_count": critical_count,
                "total_dependencies": len(vulnerabilities),
                "vulnerabilities": vulnerabilities[:10]  # Limit to first 10
            },
            raw_output_path=str(output_path)
        )
        
        save_evidence_sync(evidence)
        return {"status": status.value, "vulnerabilities": critical_count}
        
    except subprocess.TimeoutExpired:
        evidence = Evidence(
            scan_id=scan_id,
            artifact_id=artifact_id,
            rule="deps",
            status=EvidenceStatus.ERROR,
            articles=get_articles_for_rule("deps"),
            summary="pip-audit timed out",
            details={"error": "Analysis timed out after 60 seconds"}
        )
        save_evidence_sync(evidence)
        return {"status": "error", "message": "Timeout"}
    except Exception as e:
        evidence = Evidence(
            scan_id=scan_id,
            artifact_id=artifact_id,
            rule="deps",
            status=EvidenceStatus.ERROR,
            articles=get_articles_for_rule("deps"),
            summary=f"Error: {str(e)}",
            details={"error": str(e)}
        )
        save_evidence_sync(evidence)
        return {"status": "error", "message": str(e)}


@celery_app.task(name='run_bandit')
def run_bandit(artifact_id: str, scan_id: str):
    """Run bandit security scanner on Python code"""
    try:
        artifact_dir = ARTIFACTS_DIR / artifact_id
        
        # Run bandit
        result = subprocess.run(
            ["bandit", "-q", "-r", str(artifact_dir), "-f", "json"],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        output_path = EVIDENCE_DIR / scan_id / "bandit.json"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(result.stdout)
        
        # Parse results
        issues = []
        high_severity = 0
        medium_severity = 0
        
        if result.stdout:
            try:
                data = json.loads(result.stdout)
                issues = data.get('results', [])
                for issue in issues:
                    if issue.get('issue_severity') == 'HIGH':
                        high_severity += 1
                    elif issue.get('issue_severity') == 'MEDIUM':
                        medium_severity += 1
            except json.JSONDecodeError:
                pass
        
        if high_severity > 0:
            status = EvidenceStatus.FAIL
            summary = f"Found {high_severity} high severity security issues"
        elif medium_severity > 0:
            status = EvidenceStatus.WARN
            summary = f"Found {medium_severity} medium severity security issues"
        else:
            status = EvidenceStatus.PASS
            summary = "No security issues found"
        
        evidence = Evidence(
            scan_id=scan_id,
            artifact_id=artifact_id,
            rule="bandit",
            status=status,
            articles=get_articles_for_rule("bandit"),
            summary=summary,
            details={
                "high_severity": high_severity,
                "medium_severity": medium_severity,
                "total_issues": len(issues),
                "issues": issues[:5]  # First 5 issues
            },
            raw_output_path=str(output_path)
        )
        
        save_evidence_sync(evidence)
        return {"status": status.value, "high": high_severity, "medium": medium_severity}
        
    except Exception as e:
        evidence = Evidence(
            scan_id=scan_id,
            artifact_id=artifact_id,
            rule="bandit",
            status=EvidenceStatus.ERROR,
            articles=get_articles_for_rule("bandit"),
            summary=f"Error: {str(e)}",
            details={"error": str(e)}
        )
        save_evidence_sync(evidence)
        return {"status": "error", "message": str(e)}


@celery_app.task(name='run_onnx_meta')
def run_onnx_meta(artifact_id: str, scan_id: str):
    """Extract ONNX model metadata"""
    try:
        import onnx
        
        artifact_dir = ARTIFACTS_DIR / artifact_id
        onnx_file = None
        
        for file in artifact_dir.rglob("*.onnx"):
            onnx_file = file
            break
        
        if not onnx_file:
            evidence = Evidence(
                scan_id=scan_id,
                artifact_id=artifact_id,
                rule="onnx_meta",
                status=EvidenceStatus.WARN,
                articles=get_articles_for_rule("onnx_meta"),
                summary="No ONNX model found",
                details={"message": "No .onnx file found in artifact"}
            )
            save_evidence_sync(evidence)
            return {"status": "warn", "message": "No ONNX file found"}
        
        # Load model
        model = onnx.load(str(onnx_file))
        
        # Extract metadata
        metadata = {
            "opset_version": model.opset_import[0].version if model.opset_import else None,
            "producer_name": model.producer_name,
            "producer_version": model.producer_version,
            "domain": model.domain,
            "model_version": model.model_version,
            "doc_string": model.doc_string,
            "graph_name": model.graph.name if model.graph else None,
            "inputs": [inp.name for inp in model.graph.input] if model.graph else [],
            "outputs": [out.name for out in model.graph.output] if model.graph else [],
            "num_nodes": len(model.graph.node) if model.graph else 0,
        }
        
        output_path = EVIDENCE_DIR / scan_id / "onnx_meta.json"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(metadata, indent=2))
        
        evidence = Evidence(
            scan_id=scan_id,
            artifact_id=artifact_id,
            rule="onnx_meta",
            status=EvidenceStatus.PASS,
            articles=get_articles_for_rule("onnx_meta"),
            summary=f"Model: {metadata['producer_name']} v{metadata['producer_version']}",
            details=metadata,
            raw_output_path=str(output_path)
        )
        
        save_evidence_sync(evidence)
        return {"status": "pass", "metadata": metadata}
        
    except Exception as e:
        evidence = Evidence(
            scan_id=scan_id,
            artifact_id=artifact_id,
            rule="onnx_meta",
            status=EvidenceStatus.ERROR,
            articles=get_articles_for_rule("onnx_meta"),
            summary=f"Error: {str(e)}",
            details={"error": str(e)}
        )
        save_evidence_sync(evidence)
        return {"status": "error", "message": str(e)}


@celery_app.task(name='run_dataset_sanity')
def run_dataset_sanity(artifact_id: str, scan_id: str):
    """Run dataset sanity checks"""
    try:
        import pandas as pd
        import re
        
        artifact_dir = ARTIFACTS_DIR / artifact_id
        dataset_file = None
        
        # Find CSV or JSONL file
        for ext in ['.csv', '.jsonl', '.json']:
            for file in artifact_dir.rglob(f"*{ext}"):
                dataset_file = file
                break
            if dataset_file:
                break
        
        if not dataset_file:
            evidence = Evidence(
                scan_id=scan_id,
                artifact_id=artifact_id,
                rule="dataset_sanity",
                status=EvidenceStatus.WARN,
                articles=get_articles_for_rule("dataset_sanity"),
                summary="No dataset file found",
                details={"message": "No CSV/JSON dataset found"}
            )
            save_evidence_sync(evidence)
            return {"status": "warn", "message": "No dataset found"}
        
        # Load dataset
        if dataset_file.suffix == '.csv':
            df = pd.read_csv(dataset_file)
        else:
            df = pd.read_json(dataset_file, lines=True)
        
        # Run checks
        total_rows = len(df)
        total_cols = len(df.columns)
        missing_values = df.isnull().sum().sum()
        duplicates = df.duplicated().sum()
        
        # PII detection (simple heuristics)
        pii_patterns = {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
        }
        
        pii_found = {}
        for col in df.columns:
            if df[col].dtype == 'object':
                for pii_type, pattern in pii_patterns.items():
                    matches = df[col].astype(str).str.contains(pattern, regex=True, na=False).sum()
                    if matches > 0:
                        pii_found[f"{col}_{pii_type}"] = int(matches)
        
        issues = []
        if missing_values > total_rows * total_cols * 0.1:  # More than 10% missing
            issues.append(f"High missing values: {missing_values}")
        if duplicates > total_rows * 0.05:  # More than 5% duplicates
            issues.append(f"High duplicate rows: {duplicates}")
        if pii_found:
            issues.append(f"PII detected: {list(pii_found.keys())}")
        
        status = EvidenceStatus.FAIL if len(issues) > 0 else EvidenceStatus.PASS
        summary = "; ".join(issues) if issues else "Dataset quality checks passed"
        
        details = {
            "total_rows": int(total_rows),
            "total_columns": int(total_cols),
            "missing_values": int(missing_values),
            "duplicate_rows": int(duplicates),
            "pii_detected": pii_found,
            "issues": issues
        }
        
        output_path = EVIDENCE_DIR / scan_id / "dataset_sanity.json"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(details, indent=2))
        
        evidence = Evidence(
            scan_id=scan_id,
            artifact_id=artifact_id,
            rule="dataset_sanity",
            status=status,
            articles=get_articles_for_rule("dataset_sanity"),
            summary=summary,
            details=details,
            raw_output_path=str(output_path)
        )
        
        save_evidence_sync(evidence)
        return {"status": status.value, "issues": issues}
        
    except Exception as e:
        evidence = Evidence(
            scan_id=scan_id,
            artifact_id=artifact_id,
            rule="dataset_sanity",
            status=EvidenceStatus.ERROR,
            articles=get_articles_for_rule("dataset_sanity"),
            summary=f"Error: {str(e)}",
            details={"error": str(e)}
        )
        save_evidence_sync(evidence)
        return {"status": "error", "message": str(e)}
