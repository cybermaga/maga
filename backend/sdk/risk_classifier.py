"""Risk classification according to EU AI Act Articles 5, 6 and Annex III"""
from typing import Dict, List
import re

class RiskClassifier:
    """Classifies AI systems according to EU AI Act risk levels"""
    
    # Article 5 - Prohibited AI practices
    PROHIBITED_KEYWORDS = [
        'subliminal', 'manipulation', 'exploit vulnerabilities', 'social scoring',
        'real-time biometric identification', 'law enforcement', 'public spaces',
        'biometric categorization', 'sensitive attributes', 'emotion recognition',
        'workplace', 'educational institution'
    ]
    
    # Annex III - High-risk AI systems
    HIGH_RISK_CATEGORIES = {
        'biometric': ['biometric identification', 'biometric verification', 'face recognition', 'fingerprint'],
        'critical_infrastructure': ['traffic', 'water', 'gas', 'electricity', 'heating'],
        'education': ['education', 'vocational training', 'student assessment', 'exam scoring'],
        'employment': ['recruitment', 'hiring', 'worker management', 'employment', 'task allocation'],
        'essential_services': ['credit scoring', 'creditworthiness', 'insurance', 'risk assessment'],
        'law_enforcement': ['law enforcement', 'crime analytics', 'polygraph', 'evidence evaluation'],
        'migration': ['immigration', 'asylum', 'border control', 'visa'],
        'justice': ['judicial', 'legal', 'court', 'dispute resolution'],
    }
    
    def classify(self, metadata: Dict) -> Dict:
        """Classify AI system risk level
        
        Args:
            metadata: Dictionary containing system information
            
        Returns:
            Dictionary with risk_level and reasoning
        """
        system_description = str(metadata.get('description', '')).lower()
        use_case = str(metadata.get('use_case', '')).lower()
        application_domain = str(metadata.get('application_domain', '')).lower()
        
        combined_text = f"{system_description} {use_case} {application_domain}"
        
        # Check for prohibited practices
        prohibited_found = []
        for keyword in self.PROHIBITED_KEYWORDS:
            if keyword in combined_text:
                prohibited_found.append(keyword)
        
        if prohibited_found:
            return {
                'risk_level': 'prohibited',
                'reasoning': f'System matches prohibited AI practices (Article 5): {", ".join(prohibited_found)}',
                'article_reference': 'Article 5',
                'matched_terms': prohibited_found
            }
        
        # Check for high-risk categories
        high_risk_matches = []
        for category, keywords in self.HIGH_RISK_CATEGORIES.items():
            for keyword in keywords:
                if keyword in combined_text:
                    high_risk_matches.append((category, keyword))
        
        if high_risk_matches:
            categories = list(set([match[0] for match in high_risk_matches]))
            return {
                'risk_level': 'high',
                'reasoning': f'System falls under high-risk categories: {", ".join(categories)}',
                'article_reference': 'Article 6 & Annex III',
                'matched_categories': categories,
                'matched_terms': [match[1] for match in high_risk_matches]
            }
        
        # Check for limited risk (transparency obligations)
        limited_risk_keywords = ['chatbot', 'deepfake', 'emotion recognition', 'biometric categorization']
        limited_risk_found = [kw for kw in limited_risk_keywords if kw in combined_text]
        
        if limited_risk_found:
            return {
                'risk_level': 'limited',
                'reasoning': f'System requires transparency obligations: {", ".join(limited_risk_found)}',
                'article_reference': 'Article 52',
                'matched_terms': limited_risk_found
            }
        
        # Default to minimal risk
        return {
            'risk_level': 'minimal',
            'reasoning': 'System does not fall into prohibited, high-risk, or limited-risk categories',
            'article_reference': 'N/A',
            'matched_terms': []
        }
