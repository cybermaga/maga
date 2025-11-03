"""Report generation for compliance scan results"""
from typing import Dict
import json
from datetime import datetime, timezone
from jinja2 import Template
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import io

class ReportGenerator:
    """Generates compliance reports in various formats"""
    
    def generate_json_report(self, scan_result: Dict) -> str:
        """Generate JSON format report"""
        return json.dumps(scan_result, indent=2, default=str)
    
    def generate_html_report(self, scan_result: Dict) -> str:
        """Generate HTML format report"""
        template = Template('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EU AI Act Compliance Report - {{ scan_result.system_name }}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.6;
            color: #1e293b;
            background: #f8fafc;
            padding: 2rem;
        }
        .container {
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.07);
            padding: 3rem;
        }
        h1 {
            color: #1e40af;
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            border-bottom: 3px solid #3b82f6;
            padding-bottom: 1rem;
        }
        h2 {
            color: #1e40af;
            font-size: 1.75rem;
            margin-top: 2.5rem;
            margin-bottom: 1rem;
            border-left: 4px solid #3b82f6;
            padding-left: 1rem;
        }
        h3 {
            color: #475569;
            font-size: 1.25rem;
            margin-top: 1.5rem;
            margin-bottom: 0.75rem;
        }
        .meta-info {
            background: #f1f5f9;
            padding: 1.5rem;
            border-radius: 8px;
            margin: 1.5rem 0;
        }
        .meta-info p {
            margin: 0.5rem 0;
        }
        .score-badge {
            display: inline-block;
            padding: 0.75rem 1.5rem;
            border-radius: 8px;
            font-weight: 600;
            font-size: 1.5rem;
            margin: 1rem 0;
        }
        .score-a { background: #10b981; color: white; }
        .score-b { background: #3b82f6; color: white; }
        .score-c { background: #f59e0b; color: white; }
        .score-d { background: #ef4444; color: white; }
        .score-f { background: #dc2626; color: white; }
        .risk-badge {
            display: inline-block;
            padding: 0.5rem 1rem;
            border-radius: 6px;
            font-weight: 600;
            font-size: 1.1rem;
        }
        .risk-prohibited { background: #dc2626; color: white; }
        .risk-high { background: #ef4444; color: white; }
        .risk-limited { background: #f59e0b; color: white; }
        .risk-minimal { background: #10b981; color: white; }
        .article-card {
            background: #ffffff;
            border: 2px solid #e2e8f0;
            border-radius: 8px;
            padding: 1.5rem;
            margin: 1rem 0;
        }
        .status-compliant { color: #10b981; font-weight: 600; }
        .status-partial { color: #f59e0b; font-weight: 600; }
        .status-non { color: #ef4444; font-weight: 600; }
        .progress-bar {
            width: 100%;
            height: 24px;
            background: #e2e8f0;
            border-radius: 12px;
            overflow: hidden;
            margin: 0.5rem 0;
        }
        .progress-fill {
            height: 100%;
            background: linear-gradient(to right, #3b82f6, #2563eb);
            transition: width 0.3s ease;
        }
        ul { margin-left: 2rem; margin-top: 0.5rem; }
        li { margin: 0.5rem 0; }
        .footer {
            margin-top: 3rem;
            padding-top: 2rem;
            border-top: 2px solid #e2e8f0;
            text-align: center;
            color: #64748b;
            font-size: 0.9rem;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>EU AI Act Compliance Report</h1>
        
        <div class="meta-info">
            <p><strong>System Name:</strong> {{ scan_result.system_name }}</p>
            <p><strong>Scan Date:</strong> {{ scan_result.timestamp }}</p>
            <p><strong>Report ID:</strong> {{ scan_result.id }}</p>
        </div>
        
        <h2>Overall Compliance Score</h2>
        <div class="score-badge score-{{ scan_result.compliance_results.overall_score.grade.lower() }}">
            Grade: {{ scan_result.compliance_results.overall_score.grade }} - 
            {{ scan_result.compliance_results.overall_score.percentage }}%
        </div>
        <div class="progress-bar">
            <div class="progress-fill" style="width: {{ scan_result.compliance_results.overall_score.percentage }}%"></div>
        </div>
        <p style="margin-top: 1rem;">
            <strong>{{ scan_result.compliance_results.overall_score.compliant_articles }}</strong> compliant, 
            <strong>{{ scan_result.compliance_results.overall_score.partially_compliant_articles }}</strong> partially compliant, 
            <strong>{{ scan_result.compliance_results.overall_score.non_compliant_articles }}</strong> non-compliant
            (out of {{ scan_result.compliance_results.overall_score.total_articles }} articles)
        </p>
        
        <h2>Risk Classification</h2>
        <p><strong>Risk Level:</strong> 
            <span class="risk-badge risk-{{ scan_result.risk_classification.risk_level }}">
                {{ scan_result.risk_classification.risk_level.upper() }}
            </span>
        </p>
        <p><strong>Article Reference:</strong> {{ scan_result.risk_classification.article_reference }}</p>
        <p><strong>Reasoning:</strong> {{ scan_result.risk_classification.reasoning }}</p>
        
        <h2>Detailed Compliance Results</h2>
        {% for article_id, article_data in scan_result.compliance_results.items() %}
            {% if article_id != 'overall_score' %}
            <div class="article-card">
                <h3>{{ article_data.article_id.replace('_', ' ').title() }}: {{ article_data.title }}</h3>
                <p><strong>Status:</strong> 
                    <span class="status-{{ article_data.status.split('_')[0] }}">
                        {{ article_data.status.replace('_', ' ').upper() }}
                    </span>
                </p>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {{ (article_data.compliance_ratio * 100)|round }}%"></div>
                </div>
                <p style="margin-top: 0.5rem;"><strong>Compliance Ratio:</strong> {{ (article_data.compliance_ratio * 100)|round }}%</p>
                
                {% if article_data.found_elements %}
                <p><strong>Found Elements:</strong></p>
                <ul>
                    {% for element in article_data.found_elements %}
                    <li style="color: #10b981;">✓ {{ element }}</li>
                    {% endfor %}
                </ul>
                {% endif %}
                
                {% if article_data.missing_elements %}
                <p><strong>Missing Elements:</strong></p>
                <ul>
                    {% for element in article_data.missing_elements %}
                    <li style="color: #ef4444;">✗ {{ element }}</li>
                    {% endfor %}
                </ul>
                {% endif %}
                
                <p style="margin-top: 1rem; background: #f8fafc; padding: 1rem; border-radius: 6px;">
                    <strong>Recommendation:</strong> {{ article_data.recommendation }}
                </p>
            </div>
            {% endif %}
        {% endfor %}
        
        <div class="footer">
            <p>Generated by Emergent AI Compliance SDK</p>
            <p>EU AI Act (Regulation (EU) 2024/1689) Compliance Analysis</p>
        </div>
    </div>
</body>
</html>
        ''')
        
        return template.render(scan_result=scan_result)
    
    def generate_pdf_report(self, scan_result: Dict) -> bytes:
        """Generate PDF format report"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
        
        # Container for the 'Flowable' objects
        elements = []
        
        # Define styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1e40af'),
            spaceAfter=12,
            alignment=TA_CENTER
        )
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#1e40af'),
            spaceAfter=10,
            spaceBefore=20
        )
        
        # Title
        elements.append(Paragraph("EU AI Act Compliance Report", title_style))
        elements.append(Spacer(1, 0.3*inch))
        
        # Metadata table
        meta_data = [
            ['System Name:', scan_result['system_name']],
            ['Scan Date:', str(scan_result['timestamp'])],
            ['Report ID:', scan_result['id']]
        ]
        meta_table = Table(meta_data, colWidths=[2*inch, 4.5*inch])
        meta_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f1f5f9')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0'))
        ]))
        elements.append(meta_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Overall Score
        elements.append(Paragraph("Overall Compliance Score", heading_style))
        score_data = scan_result['compliance_results']['overall_score']
        elements.append(Paragraph(
            f"<b>Grade: {score_data['grade']}</b> - {score_data['percentage']}%",
            styles['Normal']
        ))
        elements.append(Paragraph(
            f"{score_data['compliant_articles']} compliant, "
            f"{score_data['partially_compliant_articles']} partially compliant, "
            f"{score_data['non_compliant_articles']} non-compliant",
            styles['Normal']
        ))
        elements.append(Spacer(1, 0.2*inch))
        
        # Risk Classification
        elements.append(Paragraph("Risk Classification", heading_style))
        risk_data = scan_result['risk_classification']
        elements.append(Paragraph(
            f"<b>Risk Level:</b> {risk_data['risk_level'].upper()}",
            styles['Normal']
        ))
        elements.append(Paragraph(
            f"<b>Article Reference:</b> {risk_data['article_reference']}",
            styles['Normal']
        ))
        elements.append(Paragraph(
            f"<b>Reasoning:</b> {risk_data['reasoning']}",
            styles['Normal']
        ))
        
        # Compliance Details
        elements.append(PageBreak())
        elements.append(Paragraph("Detailed Compliance Results", heading_style))
        
        for article_id, article_data in scan_result['compliance_results'].items():
            if article_id == 'overall_score':
                continue
            
            elements.append(Spacer(1, 0.2*inch))
            elements.append(Paragraph(
                f"<b>{article_data['article_id'].replace('_', ' ').title()}</b>: {article_data['title']}",
                styles['Heading3']
            ))
            elements.append(Paragraph(
                f"Status: <b>{article_data['status'].replace('_', ' ').upper()}</b> "
                f"({int(article_data['compliance_ratio'] * 100)}%)",
                styles['Normal']
            ))
            
            if article_data['found_elements']:
                elements.append(Paragraph("<b>Found Elements:</b>", styles['Normal']))
                for element in article_data['found_elements']:
                    elements.append(Paragraph(f"  ✓ {element}", styles['Normal']))
            
            if article_data['missing_elements']:
                elements.append(Paragraph("<b>Missing Elements:</b>", styles['Normal']))
                for element in article_data['missing_elements']:
                    elements.append(Paragraph(f"  ✗ {element}", styles['Normal']))
            
            elements.append(Paragraph(
                f"<i>Recommendation: {article_data['recommendation']}</i>",
                styles['Normal']
            ))
        
        # Build PDF
        doc.build(elements)
        
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes
