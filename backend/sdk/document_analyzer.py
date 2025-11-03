"""Document analysis utilities for metadata and documentation"""
from typing import Dict, List
import json

class DocumentAnalyzer:
    """Analyzes uploaded metadata and documentation"""
    
    def parse_metadata(self, metadata: Dict) -> Dict:
        """Parse and validate metadata structure
        
        Args:
            metadata: Raw metadata dictionary
            
        Returns:
            Parsed and validated metadata
        """
        parsed = {
            'system_name': metadata.get('system_name', 'Unnamed System'),
            'description': metadata.get('description', ''),
            'use_case': metadata.get('use_case', ''),
            'application_domain': metadata.get('application_domain', ''),
            'model_type': metadata.get('model_type', ''),
            'provider': metadata.get('provider', ''),
            'version': metadata.get('version', '1.0'),
        }
        
        # Extract optional documentation
        parsed['documentation'] = {
            'risk_management': metadata.get('risk_management', ''),
            'data_governance': metadata.get('data_governance', ''),
            'technical_docs': metadata.get('technical_docs', ''),
            'testing_procedures': metadata.get('testing_procedures', ''),
            'human_oversight': metadata.get('human_oversight', ''),
            'accuracy_metrics': metadata.get('accuracy_metrics', ''),
        }
        
        return parsed
    
    def extract_documents(self, file_content: str) -> List[str]:
        """Extract text from uploaded documents
        
        Args:
            file_content: Content of uploaded file
            
        Returns:
            List of extracted text sections
        """
        # For MVP, treat as plain text
        # In production, would parse PDF, DOCX, etc.
        if not file_content:
            return []
        
        # Split into sections if structured
        sections = []
        if '---' in file_content:
            sections = file_content.split('---')
        else:
            sections = [file_content]
        
        return [s.strip() for s in sections if s.strip()]
    
    def validate_metadata(self, metadata: Dict) -> tuple[bool, List[str]]:
        """Validate that required metadata fields are present
        
        Args:
            metadata: Metadata dictionary
            
        Returns:
            Tuple of (is_valid, list of missing fields)
        """
        required_fields = ['system_name', 'description', 'use_case']
        missing = []
        
        for field in required_fields:
            if field not in metadata or not metadata[field]:
                missing.append(field)
        
        return len(missing) == 0, missing
