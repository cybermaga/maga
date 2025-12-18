"""Configuration settings"""
import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
ARTIFACTS_DIR = DATA_DIR / "artifacts"
EVIDENCE_DIR = DATA_DIR / "evidence"

# Create directories if they don't exist
ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)

# MongoDB
MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = os.environ.get('DB_NAME', 'emergent')

# Redis
REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')

# CORS
ALLOWED_ORIGINS = os.environ.get('ALLOWED_ORIGINS', 'http://localhost:3000').split(',')

# File upload limits
MAX_UPLOAD_SIZE = 100 * 1024 * 1024  # 100MB
ALLOWED_EXTENSIONS = {
    'code': ['.py', '.js', '.ts', '.java', '.go', '.zip', '.tar.gz', '.txt'],
    'model': ['.onnx', '.pt', '.pth', '.h5', '.pkl', '.joblib'],
    'dataset': ['.csv', '.json', '.jsonl', '.parquet', '.xlsx'],
    'doc': ['.pdf', '.docx', '.txt', '.md'],
    'logs': ['.log', '.txt'],
}

# Celery
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
