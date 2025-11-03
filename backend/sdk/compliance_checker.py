"""Compliance checking for EU AI Act Articles 9-15 (high-risk requirements)"""
from typing import Dict, List
import re

class ComplianceChecker:
    """Checks compliance with EU AI Act requirements for high-risk systems"""
    
    # Define required elements for each article
    COMPLIANCE_REQUIREMENTS = {
        'article_9': {
            'title': 'Risk Management System',
            'required_elements': [
                'risk identification',
                'risk assessment',
                'risk mitigation',
                'testing',
                'monitoring'
            ]
        },
        'article_10': {
            'title': 'Data and Data Governance',
            'required_elements': [
                'training data',
                'data quality',
                'bias detection',
                'data relevance',
                'data representativeness'
            ]
        },
        'article_11': {
            'title': 'Technical Documentation',
            'required_elements': [
                'general description',
                'development process',
                'design specifications',
                'performance metrics',
                'validation procedures'
            ]
        },
        'article_12': {
            'title': 'Record-keeping',
            'required_elements': [
                'automatic logging',
                'event recording',
                'traceability',
                'audit trail'
            ]
        },
        'article_13': {
            'title': 'Transparency and Information to Users',
            'required_elements': [
                'user instructions',
                'capabilities description',
                'limitations',
                'performance level',
                'human oversight information'
            ]
        },
        'article_14': {
            'title': 'Human Oversight',
            'required_elements': [
                'oversight measures',
                'human intervention',
                'stop capability',
                'monitoring capability'
            ]
        },
        'article_15': {
            'title': 'Accuracy, Robustness and Cybersecurity',
            'required_elements': [
                'accuracy metrics',
                'robustness testing',
                'cybersecurity measures',
                'resilience',
                'error handling'
            ]
        }
    }
    
    def check_compliance(self, metadata: Dict, documents: List[str] = None) -> Dict:
        """Check compliance against EU AI Act requirements
        
        Args:
            metadata: System metadata
            documents: List of document contents to analyze
            
        Returns:
            Dictionary with compliance results per article
        """
        results = {}
        
        # Combine all text for analysis
        all_text = self._combine_text(metadata, documents)
        
        for article_id, requirements in self.COMPLIANCE_REQUIREMENTS.items():
            compliance_result = self._check_article_compliance(
                article_id,
                requirements,
                all_text
            )
            results[article_id] = compliance_result
        
        # Calculate overall compliance score
        results['overall_score'] = self._calculate_score(results)
        
        return results
    
    def _combine_text(self, metadata: Dict, documents: List[str] = None) -> str:
        """Combine all available text for analysis"""
        text_parts = []
        
        # Add metadata fields
        for key, value in metadata.items():
            if isinstance(value, str):
                text_parts.append(value.lower())
            elif isinstance(value, (list, dict)):
                text_parts.append(str(value).lower())
        
        # Add document contents
        if documents:
            for doc in documents:
                if isinstance(doc, str):
                    text_parts.append(doc.lower())
        
        return ' '.join(text_parts)
    
    def _check_article_compliance(self, article_id: str, requirements: Dict, text: str) -> Dict:
        """Check compliance for a specific article"""
        title = requirements['title']
        required_elements = requirements['required_elements']
        
        found_elements = []
        missing_elements = []
        evidence = {}
        
        for element in required_elements:
            # Check if element or related terms are present
            if self._search_element(element, text):
                found_elements.append(element)
                evidence[element] = self._extract_evidence(element, text)
            else:
                missing_elements.append(element)
        
        # Determine compliance status
        compliance_ratio = len(found_elements) / len(required_elements)
        
        if compliance_ratio >= 0.8:
            status = 'compliant'
        elif compliance_ratio >= 0.4:
            status = 'partially_compliant'
        else:
            status = 'non_compliant'
        
        return {
            'article_id': article_id,
            'title': title,
            'status': status,
            'compliance_ratio': compliance_ratio,
            'found_elements': found_elements,
            'missing_elements': missing_elements,
            'evidence': evidence,
            'recommendation': self._generate_recommendation(missing_elements, title)
        }
    
    def _search_element(self, element: str, text: str) -> bool:
        """Search for element or related terms in text"""
        # Create variations of the search term
        search_terms = [element]
        
        # Add related terms
        related_terms = {
            'risk identification': ['identify risks', 'risk analysis'],
            'risk assessment': ['assess risks', 'risk evaluation'],
            'training data': ['dataset', 'training set', 'data collection'],
            'bias detection': ['bias mitigation', 'fairness'],
            'human oversight': ['human in the loop', 'human supervision'],
            'accuracy metrics': ['accuracy', 'precision', 'recall', 'f1 score'],
        }
        
        if element in related_terms:
            search_terms.extend(related_terms[element])
        
        for term in search_terms:
            if term in text:
                return True
        
        return False
    
    def _extract_evidence(self, element: str, text: str, context_length: int = 100) -> str:
        """Extract evidence snippet from text"""
        element_lower = element.lower()
        idx = text.find(element_lower)
        
        if idx == -1:
            return "Element mentioned"
        
        start = max(0, idx - context_length // 2)
        end = min(len(text), idx + len(element_lower) + context_length // 2)
        
        snippet = text[start:end].strip()
        if start > 0:
            snippet = '...' + snippet
        if end < len(text):
            snippet = snippet + '...'
        
        return snippet
    
    def _generate_recommendation(self, missing_elements: List[str], article_title: str) -> str:
        """Generate recommendation for missing elements"""
        if not missing_elements:
            return f"System documentation adequately covers {article_title} requirements."
        
        return f"To achieve full compliance with {article_title}, provide documentation for: {', '.join(missing_elements)}."
    
    def _calculate_score(self, results: Dict) -> Dict:
        """Calculate overall compliance score"""
        scores = []
        compliant_count = 0
        partial_count = 0
        non_compliant_count = 0
        
        for article_id, result in results.items():
            if article_id == 'overall_score':
                continue
            
            scores.append(result['compliance_ratio'])
            
            if result['status'] == 'compliant':
                compliant_count += 1
            elif result['status'] == 'partially_compliant':
                partial_count += 1
            else:
                non_compliant_count += 1
        
        avg_score = sum(scores) / len(scores) if scores else 0
        
        return {
            'percentage': round(avg_score * 100, 2),
            'grade': self._get_grade(avg_score),
            'compliant_articles': compliant_count,
            'partially_compliant_articles': partial_count,
            'non_compliant_articles': non_compliant_count,
            'total_articles': len(scores)
        }
    
    def _get_grade(self, score: float) -> str:
        """Convert score to letter grade"""
        if score >= 0.9:
            return 'A'
        elif score >= 0.8:
            return 'B'
        elif score >= 0.6:
            return 'C'
        elif score >= 0.4:
            return 'D'
        else:
            return 'F'
