# Emergent AI Compliance

**EU AI Act (Regulation (EU) 2024/1689) Compliance Analysis Tool**

A comprehensive SDK and web application for automatically evaluating AI systems against the EU AI Act requirements.

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![React](https://img.shields.io/badge/react-19.0-blue.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/fastapi-0.110-green.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)

![Dashboard Screenshot](https://via.placeholder.com/800x400?text=EU+AI+Compliance+Dashboard)

---

## 🚀 Quick Start with Docker

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/emergent-ai-compliance.git
cd emergent-ai-compliance

# Start with Docker Compose
docker-compose up -d

# Or use the quick start script
./docker-start.sh
```

**Access the application:**
- 🌐 **Frontend**: http://localhost:3000
- 🔧 **Backend API**: http://localhost:8001
- 📚 **API Docs**: http://localhost:8001/docs

**That's it!** No Python, Node.js, or MongoDB installation required. 🎉

---

## Features

### SDK (Python)
- **Risk Classification**: Automatically detects AI system risk level (prohibited, high, limited, minimal) according to Article 5, Article 6, and Annex III
- **Compliance Checking**: Analyzes compliance with Articles 9-15 (high-risk requirements):
  - Article 9: Risk Management System
  - Article 10: Data and Data Governance
  - Article 11: Technical Documentation
  - Article 12: Record-keeping
  - Article 13: Transparency and Information to Users
  - Article 14: Human Oversight
  - Article 15: Accuracy, Robustness and Cybersecurity
- **Document Analysis**: Parses metadata and documentation for compliance evaluation
- **Report Generation**: Exports reports in JSON, HTML, and PDF formats

### Web Application
- **Dashboard**: Overview of all compliance scans with statistics
- **New Scan Form**: Submit AI system metadata and documentation
- **Report Viewer**: Detailed compliance results with grade and recommendations
- **Export Options**: Download reports as PDF or HTML

### CLI Usage (Python SDK)
```python
from sdk import RiskClassifier, ComplianceChecker, DocumentAnalyzer, ReportGenerator

# Initialize components
risk_classifier = RiskClassifier()
compliance_checker = ComplianceChecker()
document_analyzer = DocumentAnalyzer()
report_generator = ReportGenerator()

# Parse metadata
metadata = {
    'system_name': 'Healthcare Diagnosis Assistant',
    'description': 'AI system for medical diagnosis support',
    'use_case': 'Assists doctors in diagnosing diseases',
    'application_domain': 'Healthcare',
    'risk_management': 'We implement comprehensive risk assessment...',
    # ... more fields
}

parsed_metadata = document_analyzer.parse_metadata(metadata)

# Classify risk
risk_result = risk_classifier.classify(parsed_metadata)
print(f"Risk Level: {risk_result['risk_level']}")

# Check compliance
compliance_result = compliance_checker.check_compliance(parsed_metadata)
print(f"Overall Score: {compliance_result['overall_score']['percentage']}%")

# Generate reports
html_report = report_generator.generate_html_report({
    'id': 'test-001',
    'system_name': metadata['system_name'],
    'timestamp': '2025-01-15T10:00:00',
    'risk_classification': risk_result,
    'compliance_results': compliance_result,
    'metadata': parsed_metadata
})

pdf_report = report_generator.generate_pdf_report({...})
```

## Architecture

```
/app/
├── backend/                # FastAPI backend
│   ├── sdk/               # Compliance SDK modules
│   │   ├── risk_classifier.py
│   │   ├── compliance_checker.py
│   │   ├── document_analyzer.py
│   │   └── report_generator.py
│   ├── server.py          # API endpoints
│   ├── requirements.txt   # Python dependencies
│   └── .env              # Environment variables
│
└── frontend/              # React frontend
    ├── src/
    │   ├── pages/         # Dashboard, NewScan, ReportView
    │   ├── components/ui/ # Shadcn UI components
    │   ├── App.js
    │   └── App.css
    ├── package.json
    └── .env
```

## Quick Start with Docker 🐳

**Recommended**: Use Docker for the easiest setup.

```bash
# Clone the repository
git clone <your-repo>
cd emergent-ai-compliance

# Start all services with Docker Compose
docker-compose up -d

# Or use Makefile
make setup
```

Access the application:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8001
- **API Documentation**: http://localhost:8001/docs

See [DOCKER.md](DOCKER.md) for detailed Docker instructions.

---

## Manual Setup (Without Docker)

### Prerequisites
- Python 3.11+
- Node.js 18+
- MongoDB (running on localhost:27017)

### Backend Setup

1. Install Python dependencies:
```bash
cd /app/backend
pip install -r requirements.txt
```

2. Configure environment variables (already set in `.env`):
```
MONGO_URL="mongodb://localhost:27017"
DB_NAME="test_database"
CORS_ORIGINS="*"
```

3. Start the backend server:
```bash
sudo supervisorctl restart backend
```

The API will be available at the configured backend URL (port 8001).

### Frontend Setup

1. Install Node.js dependencies:
```bash
cd /app/frontend
yarn install
```

2. Start the frontend development server:
```bash
sudo supervisorctl restart frontend
```

The web application will be available at port 3000.

### Verify Services

Check that both services are running:
```bash
sudo supervisorctl status
```

## API Endpoints

### POST `/api/compliance/scan`
Run a compliance scan on an AI system.

**Request Body:**
```json
{
  "system_name": "Healthcare Diagnosis Assistant",
  "description": "AI system for medical diagnosis support",
  "use_case": "Assists doctors in diagnosing diseases",
  "application_domain": "Healthcare",
  "model_type": "Neural Network",
  "provider": "Custom",
  "version": "1.0",
  "risk_management": "...",
  "data_governance": "...",
  "technical_docs": "...",
  "testing_procedures": "...",
  "human_oversight": "...",
  "accuracy_metrics": "..."
}
```

**Response:**
```json
{
  "id": "uuid",
  "system_name": "Healthcare Diagnosis Assistant",
  "timestamp": "2025-01-15T10:00:00",
  "risk_classification": {
    "risk_level": "high",
    "reasoning": "...",
    "article_reference": "Article 6 & Annex III"
  },
  "compliance_results": {
    "overall_score": {
      "percentage": 75.5,
      "grade": "C",
      "compliant_articles": 3,
      "partially_compliant_articles": 3,
      "non_compliant_articles": 1
    },
    "article_9": {...},
    "article_10": {...}
  }
}
```

### GET `/api/compliance/reports`
Get all compliance scan reports.

### GET `/api/compliance/reports/{report_id}`
Get a specific compliance report.

### GET `/api/compliance/reports/{report_id}/export?format=html|pdf|json`
Export a report in the specified format.

### DELETE `/api/compliance/reports/{report_id}`
Delete a compliance report.

## Compliance Rule Engine

### Risk Classification (Articles 5, 6, Annex III)

**Prohibited (Article 5):**
- Subliminal techniques
- Exploitation of vulnerabilities
- Social scoring by public authorities
- Real-time biometric identification in public spaces for law enforcement
- Biometric categorization based on sensitive attributes
- Emotion recognition in workplace/education

**High-Risk (Article 6 & Annex III):**
- Biometric identification and categorization
- Critical infrastructure management
- Education and vocational training
- Employment, worker management
- Essential private and public services (credit scoring, insurance)
- Law enforcement
- Migration, asylum, border control
- Administration of justice and democratic processes

**Limited-Risk (Article 52):**
- Chatbots
- Deepfakes
- Emotion recognition systems
- Biometric categorization systems (transparency required)

**Minimal-Risk:**
- All other AI systems not falling into above categories

### Compliance Requirements (Articles 9-15)

For high-risk AI systems, the SDK checks for documentation of:

1. **Article 9 - Risk Management**: risk identification, assessment, mitigation, testing, monitoring
2. **Article 10 - Data Governance**: training data quality, bias detection, data relevance and representativeness
3. **Article 11 - Technical Documentation**: general description, development process, design specs, performance metrics, validation
4. **Article 12 - Record-keeping**: automatic logging, event recording, traceability, audit trail
5. **Article 13 - Transparency**: user instructions, capabilities, limitations, performance level, oversight info
6. **Article 14 - Human Oversight**: oversight measures, human intervention, stop capability, monitoring
7. **Article 15 - Accuracy, Robustness, Cybersecurity**: accuracy metrics, robustness testing, security measures, resilience, error handling

### Scoring System

- **Compliant**: ≥ 80% of required elements found
- **Partially Compliant**: 40-79% of required elements found
- **Non-Compliant**: < 40% of required elements found

**Overall Grade:**
- A: ≥ 90%
- B: 80-89%
- C: 60-79%
- D: 40-59%
- F: < 40%

## Development Notes

### Modular Design
The SDK is designed with modularity in mind:
- Each component can be used independently
- Easy to extend with new compliance rules
- Designed for offline operation (no internet required)

### Future Enhancements
1. Real AI model file parsing (TensorFlow, PyTorch, ONNX)
2. Automated document extraction from PDF/DOCX files
3. Integration with model registries
4. Continuous compliance monitoring
5. Multi-language support
6. Expanded rule coverage for additional articles

## Testing

### Backend Testing
```bash
# Test API endpoints
curl -X POST http://localhost:8001/api/compliance/scan \
  -H "Content-Type: application/json" \
  -d '{
    "system_name": "Test System",
    "description": "Test AI system for biometric identification",
    "use_case": "Face recognition for security"
  }'
```

### Frontend Testing
Open the web application and:
1. Create a new compliance scan
2. Fill in system information
3. Submit and view the generated report
4. Export report as HTML or PDF

### Docker Testing
```bash
# Test all services
make health

# Or manually
curl -f http://localhost:8001/api/
curl -f http://localhost:3000
docker exec emergent-compliance-mongodb mongosh --eval "db.adminCommand('ping')"
```

## License

This project is built for educational and compliance analysis purposes.

## Support

For issues or questions, please refer to the Emergent platform documentation.

---

**Generated by Emergent AI Compliance SDK v1.0.0**
