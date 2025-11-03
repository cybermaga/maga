#!/usr/bin/env python3
"""
Emergent AI Compliance CLI Tool

Command-line interface for the EU AI Act Compliance SDK.
"""

import typer
import json
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint
from sdk import RiskClassifier, ComplianceChecker, DocumentAnalyzer, ReportGenerator
from datetime import datetime, timezone

app = typer.Typer(help="EU AI Act Compliance Analysis CLI")
console = Console()

# Initialize SDK components
risk_classifier = RiskClassifier()
compliance_checker = ComplianceChecker()
document_analyzer = DocumentAnalyzer()
report_generator = ReportGenerator()


@app.command()
def scan(
    metadata_file: Path = typer.Option(..., "--metadata", "-m", help="Path to metadata JSON file"),
    output: Path = typer.Option(None, "--output", "-o", help="Output file path (optional)"),
    format: str = typer.Option("json", "--format", "-f", help="Output format: json, html, or pdf")
):
    """Run a compliance scan from a metadata file."""
    
    try:
        # Read metadata file
        with open(metadata_file, 'r') as f:
            metadata = json.load(f)
        
        console.print("\n[bold blue]Running EU AI Act Compliance Scan...[/bold blue]\n")
        
        # Parse metadata
        parsed_metadata = document_analyzer.parse_metadata(metadata)
        
        # Validate
        is_valid, missing = document_analyzer.validate_metadata(metadata)
        if not is_valid:
            console.print(f"[bold red]Error:[/bold red] Missing required fields: {', '.join(missing)}")
            raise typer.Exit(1)
        
        # Classify risk
        risk_result = risk_classifier.classify(parsed_metadata)
        
        # Check compliance
        compliance_result = compliance_checker.check_compliance(parsed_metadata)
        
        # Create scan result
        scan_result = {
            'id': f"cli-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
            'system_name': parsed_metadata['system_name'],
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'risk_classification': risk_result,
            'compliance_results': compliance_result,
            'metadata': parsed_metadata
        }
        
        # Display results
        display_results(scan_result)
        
        # Save output if requested
        if output:
            save_report(scan_result, output, format)
            console.print(f"\n[bold green]✓[/bold green] Report saved to {output}")
        
    except FileNotFoundError:
        console.print(f"[bold red]Error:[/bold red] File not found: {metadata_file}")
        raise typer.Exit(1)
    except json.JSONDecodeError:
        console.print(f"[bold red]Error:[/bold red] Invalid JSON in {metadata_file}")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        raise typer.Exit(1)


@app.command()
def quick_check(
    system_name: str = typer.Option(..., "--name", "-n", help="AI system name"),
    description: str = typer.Option(..., "--desc", "-d", help="System description"),
    use_case: str = typer.Option(..., "--use-case", "-u", help="Primary use case"),
    domain: str = typer.Option("", "--domain", help="Application domain")
):
    """Quick compliance check with minimal information."""
    
    metadata = {
        'system_name': system_name,
        'description': description,
        'use_case': use_case,
        'application_domain': domain
    }
    
    console.print("\n[bold blue]Running Quick Compliance Check...[/bold blue]\n")
    
    # Parse and classify
    parsed_metadata = document_analyzer.parse_metadata(metadata)
    risk_result = risk_classifier.classify(parsed_metadata)
    compliance_result = compliance_checker.check_compliance(parsed_metadata)
    
    # Display results
    console.print(Panel(f"[bold]{system_name}[/bold]", title="System Name"))
    
    risk_color = get_risk_color(risk_result['risk_level'])
    console.print(f"\n[bold]Risk Level:[/bold] [{risk_color}]{risk_result['risk_level'].upper()}[/{risk_color}]")
    console.print(f"[bold]Article Reference:[/bold] {risk_result['article_reference']}")
    console.print(f"[bold]Reasoning:[/bold] {risk_result['reasoning']}")
    
    score = compliance_result['overall_score']
    grade_color = get_grade_color(score['grade'])
    console.print(f"\n[bold]Overall Compliance:[/bold] [{grade_color}]Grade {score['grade']} - {score['percentage']}%[/{grade_color}]")
    console.print(f"[bold]Status:[/bold] {score['compliant_articles']} compliant, {score['partially_compliant_articles']} partial, {score['non_compliant_articles']} non-compliant\n")


def display_results(scan_result):
    """Display scan results in a formatted way."""
    
    # System info
    console.print(Panel(f"[bold]{scan_result['system_name']}[/bold]", title="System Name"))
    
    # Risk classification
    risk = scan_result['risk_classification']
    risk_color = get_risk_color(risk['risk_level'])
    
    console.print(f"\n[bold]Risk Classification[/bold]")
    console.print(f"  Level: [{risk_color}]{risk['risk_level'].upper()}[/{risk_color}]")
    console.print(f"  Article: {risk['article_reference']}")
    console.print(f"  Reasoning: {risk['reasoning']}")
    
    # Overall compliance
    score = scan_result['compliance_results']['overall_score']
    grade_color = get_grade_color(score['grade'])
    
    console.print(f"\n[bold]Overall Compliance Score[/bold]")
    console.print(f"  Grade: [{grade_color}]{score['grade']}[/{grade_color}]")
    console.print(f"  Percentage: {score['percentage']}%")
    console.print(f"  Compliant: {score['compliant_articles']}")
    console.print(f"  Partially Compliant: {score['partially_compliant_articles']}")
    console.print(f"  Non-Compliant: {score['non_compliant_articles']}")
    
    # Article breakdown
    console.print(f"\n[bold]Detailed Results by Article[/bold]")
    
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Article", style="cyan", width=40)
    table.add_column("Status", width=20)
    table.add_column("Score", justify="right", width=10)
    
    for article_id, article_data in scan_result['compliance_results'].items():
        if article_id == 'overall_score':
            continue
        
        title = f"{article_data['article_id'].replace('_', ' ').title()}"
        status = article_data['status'].replace('_', ' ').upper()
        score_pct = f"{int(article_data['compliance_ratio'] * 100)}%"
        
        status_color = "green" if status == "COMPLIANT" else "yellow" if "PARTIAL" in status else "red"
        
        table.add_row(
            title,
            f"[{status_color}]{status}[/{status_color}]",
            score_pct
        )
    
    console.print(table)


def save_report(scan_result, output_path: Path, format: str):
    """Save report to file in specified format."""
    
    if format == "json":
        with open(output_path, 'w') as f:
            json.dump(scan_result, f, indent=2, default=str)
    
    elif format == "html":
        html_content = report_generator.generate_html_report(scan_result)
        with open(output_path, 'w') as f:
            f.write(html_content)
    
    elif format == "pdf":
        pdf_bytes = report_generator.generate_pdf_report(scan_result)
        with open(output_path, 'wb') as f:
            f.write(pdf_bytes)
    
    else:
        raise ValueError(f"Unsupported format: {format}")


def get_risk_color(risk_level: str) -> str:
    """Get color for risk level."""
    colors = {
        'prohibited': 'red',
        'high': 'red',
        'limited': 'yellow',
        'minimal': 'green'
    }
    return colors.get(risk_level, 'white')


def get_grade_color(grade: str) -> str:
    """Get color for grade."""
    colors = {
        'A': 'green',
        'B': 'blue',
        'C': 'yellow',
        'D': 'red',
        'F': 'red'
    }
    return colors.get(grade, 'white')


@app.command()
def version():
    """Display SDK version information."""
    console.print("\n[bold blue]Emergent AI Compliance SDK[/bold blue]")
    console.print("Version: 1.0.0")
    console.print("EU AI Act (Regulation (EU) 2024/1689)")
    console.print("\nFor more information, visit: https://emergent.sh\n")


if __name__ == "__main__":
    app()
