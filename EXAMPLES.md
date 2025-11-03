# Emergent AI Compliance - Usage Examples

## CLI Usage Examples

### 1. Quick Compliance Check

For a fast analysis with minimal information:

```bash
python3 cli.py quick-check \
  --name "Email Spam Filter" \
  --desc "AI system for filtering spam emails" \
  --use-case "Classify emails as spam or legitimate" \
  --domain "Email Services"
```

**Output:**
```
Risk Level: MINIMAL
Overall Compliance: Grade F - 5.71%
```

---

### 2. Full Compliance Scan from JSON File

Create a metadata file (`metadata.json`):

```json
{
  "system_name": "Healthcare Diagnosis Assistant",
  "description": "AI-powered system for supporting medical professionals in diagnosing diseases",
  "use_case": "Assists doctors in diagnosing diseases by analyzing patient data",
  "application_domain": "Healthcare",
  "model_type": "Deep Neural Network",
  "provider": "MedTech Solutions",
  "version": "2.1",
  "risk_management": "Comprehensive risk identification and assessment procedures",
  "data_governance": "Training data with quality checks and bias detection",
  "technical_docs": "Complete technical documentation with validation procedures",
  "testing_procedures": "Automated logging and audit trail maintenance",
  "human_oversight": "Physician review required for all AI suggestions",
  "accuracy_metrics": "94% diagnostic accuracy with robust testing"
}
```

Run the scan:

```bash
python3 cli.py scan --metadata metadata.json
```

Export to HTML:

```bash
python3 cli.py scan --metadata metadata.json --output report.html --format html
```

Export to PDF:

```bash
python3 cli.py scan --metadata metadata.json --output report.pdf --format pdf
```

---

## Python SDK Examples

### Example 1: Basic Risk Classification

```python
from sdk import RiskClassifier

classifier = RiskClassifier()

# Test prohibited system
metadata = {
    'description': 'Real-time biometric identification for law enforcement in public spaces',
    'use_case': 'Track suspects using facial recognition',
    'application_domain': 'Law Enforcement'
}

result = classifier.classify(metadata)
print(f"Risk Level: {result['risk_level']}")  # Output: prohibited
print(f"Reasoning: {result['reasoning']}")
```

### Example 2: Full Compliance Analysis

```python
from sdk import RiskClassifier, ComplianceChecker, DocumentAnalyzer

# Initialize components
classifier = RiskClassifier()
checker = ComplianceChecker()
analyzer = DocumentAnalyzer()

# Prepare metadata
metadata = {
    'system_name': 'Credit Scoring AI',
    'description': 'Automated credit scoring for loan applications',
    'use_case': 'Evaluate creditworthiness',
    'application_domain': 'Financial Services',
    'risk_management': 'Risk identification and mitigation in place',
    'data_governance': 'Bias detection and data quality checks implemented',
    'technical_docs': 'Full technical documentation available',
    'human_oversight': 'Human review for edge cases'
}

# Parse and validate
parsed = analyzer.parse_metadata(metadata)
is_valid, missing = analyzer.validate_metadata(metadata)

if is_valid:
    # Classify risk
    risk = classifier.classify(parsed)
    print(f"Risk: {risk['risk_level']} - {risk['reasoning']}")
    
    # Check compliance
    compliance = checker.check_compliance(parsed)
    score = compliance['overall_score']
    print(f"Score: {score['grade']} ({score['percentage']}%)")
    
    # View article details
    for article_id, details in compliance.items():
        if article_id != 'overall_score':
            print(f"{details['title']}: {details['status']}")
```

### Example 3: Generate Reports

```python
from sdk import ReportGenerator
from datetime import datetime, timezone

generator = ReportGenerator()

# Create scan result
scan_result = {
    'id': 'scan-001',
    'system_name': 'Credit Scoring AI',
    'timestamp': datetime.now(timezone.utc).isoformat(),
    'risk_classification': risk,  # from previous example
    'compliance_results': compliance,  # from previous example
    'metadata': parsed
}

# Generate HTML report
html_report = generator.generate_html_report(scan_result)
with open('report.html', 'w') as f:
    f.write(html_report)

# Generate PDF report
pdf_bytes = generator.generate_pdf_report(scan_result)
with open('report.pdf', 'wb') as f:
    f.write(pdf_bytes)

# Generate JSON report
json_report = generator.generate_json_report(scan_result)
with open('report.json', 'w') as f:
    f.write(json_report)
```

---

## Web Application Examples

### 1. Create a New Scan

1. Navigate to **Dashboard**
2. Click **"New Compliance Scan"** button
3. Fill in required fields:
   - System Name
   - Description
   - Use Case
4. Optionally fill in compliance documentation for better analysis
5. Click **"Run Compliance Scan"**

### 2. View Compliance Report

1. From Dashboard, click on any report card
2. View:
   - Overall compliance score and grade
   - Risk classification (Prohibited/High/Limited/Minimal)
   - Detailed results per EU AI Act article
   - Recommendations for improvement

### 3. Export Reports

From the report view page:
- Click **"Export HTML"** for web-viewable report
- Click **"Export PDF"** for printable report
- Share with stakeholders or archive for compliance records

---

## API Examples

### POST /api/compliance/scan

Create a new compliance scan:

```bash
curl -X POST http://localhost:8001/api/compliance/scan \
  -H "Content-Type: application/json" \
  -d '{
    "system_name": "AI Recruitment Tool",
    "description": "AI system for screening job applications",
    "use_case": "Automated candidate evaluation for hiring",
    "application_domain": "Employment",
    "risk_management": "Risk assessment procedures implemented",
    "human_oversight": "HR professionals review all recommendations"
  }'
```

### GET /api/compliance/reports

Get all compliance reports:

```bash
curl -X GET http://localhost:8001/api/compliance/reports
```

### GET /api/compliance/reports/{id}

Get specific report:

```bash
curl -X GET http://localhost:8001/api/compliance/reports/abc-123
```

### GET /api/compliance/reports/{id}/export

Export report:

```bash
# HTML
curl -X GET "http://localhost:8001/api/compliance/reports/abc-123/export?format=html" \
  -o report.html

# PDF
curl -X GET "http://localhost:8001/api/compliance/reports/abc-123/export?format=pdf" \
  -o report.pdf

# JSON
curl -X GET "http://localhost:8001/api/compliance/reports/abc-123/export?format=json" \
  -o report.json
```

---

## Test Scenarios

### Scenario 1: Prohibited AI System

```json
{
  "system_name": "Social Scoring Platform",
  "description": "AI system for scoring citizens based on social behavior",
  "use_case": "Evaluate and rank citizens for government services",
  "application_domain": "Public Administration"
}
```

**Expected Result:** Risk Level = PROHIBITED (Article 5)

### Scenario 2: High-Risk AI System

```json
{
  "system_name": "Loan Approval AI",
  "description": "Automated credit scoring and loan approval",
  "use_case": "Evaluate loan applications and approve/reject automatically",
  "application_domain": "Banking and Finance"
}
```

**Expected Result:** Risk Level = HIGH (Article 6 & Annex III - Essential Services)

### Scenario 3: Limited-Risk AI System

```json
{
  "system_name": "Customer Service Chatbot",
  "description": "AI chatbot for answering customer questions",
  "use_case": "Provide automated customer support",
  "application_domain": "Customer Service"
}
```

**Expected Result:** Risk Level = LIMITED (Article 52 - Transparency obligations)

### Scenario 4: Minimal-Risk AI System

```json
{
  "system_name": "Video Game AI",
  "description": "AI for controlling non-player characters in games",
  "use_case": "Create realistic game opponents",
  "application_domain": "Entertainment"
}
```

**Expected Result:** Risk Level = MINIMAL

---

## Best Practices

1. **Provide Complete Documentation**: The more documentation you provide (risk management, data governance, etc.), the more accurate the compliance analysis.

2. **Regular Scans**: Run compliance scans at different stages of AI system development:
   - Initial design phase
   - After major updates
   - Before deployment
   - Periodic reviews

3. **Use Detailed Descriptions**: Include specific details about your AI system's capabilities, limitations, and safeguards.

4. **Archive Reports**: Keep compliance reports as evidence of due diligence for regulatory audits.

5. **Act on Recommendations**: Use the detailed recommendations to improve your AI system's compliance posture.

---

## Integration Examples

### Integrate into CI/CD Pipeline

```yaml
# .github/workflows/compliance-check.yml
name: EU AI Act Compliance Check

on:
  push:
    branches: [main]

jobs:
  compliance:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Run Compliance Scan
        run: |
          python3 cli.py scan --metadata ai_metadata.json --output compliance_report.html --format html
      
      - name: Upload Report
        uses: actions/upload-artifact@v2
        with:
          name: compliance-report
          path: compliance_report.html
```

### Integrate into Python Application

```python
from sdk import RiskClassifier, ComplianceChecker, DocumentAnalyzer

def check_ai_system_compliance(system_metadata):
    """Check if AI system meets EU AI Act requirements"""
    
    analyzer = DocumentAnalyzer()
    classifier = RiskClassifier()
    checker = ComplianceChecker()
    
    # Validate metadata
    is_valid, missing = analyzer.validate_metadata(system_metadata)
    if not is_valid:
        raise ValueError(f"Missing fields: {missing}")
    
    # Parse and analyze
    parsed = analyzer.parse_metadata(system_metadata)
    risk = classifier.classify(parsed)
    
    # Block prohibited systems
    if risk['risk_level'] == 'prohibited':
        raise ValueError(f"Prohibited AI system: {risk['reasoning']}")
    
    # Check compliance for high-risk systems
    if risk['risk_level'] == 'high':
        compliance = checker.check_compliance(parsed)
        if compliance['overall_score']['percentage'] < 60:
            raise ValueError(f"Insufficient compliance: {compliance['overall_score']['percentage']}%")
    
    return {
        'approved': True,
        'risk_level': risk['risk_level'],
        'compliance_score': compliance.get('overall_score', {}).get('percentage', 100)
    }
```

---

For more information, see the [README.md](README.md) file.
