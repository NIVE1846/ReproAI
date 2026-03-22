"""
Explainability Module
Generates interpretable explanations for AI recommendations
"""
import pandas as pd
import numpy as np

class ExplainabilityEngine:
    """Generate human-readable explanations for predictions"""
    
    def __init__(self, predictor=None):
        self.predictor = predictor
    
    def explain_prediction(self, patient_data, predictions, cohort_stats=None):
        """Generate comprehensive explanation for prediction"""
        explanation = {
            'summary': self._generate_summary(patient_data, predictions),
            'key_factors': self._identify_key_factors(patient_data, predictions),
            'feature_contributions': self._explain_features(patient_data),
            'cohort_context': self._explain_cohort_context(cohort_stats) if cohort_stats else None,
            'natural_language': self._generate_natural_language(patient_data, predictions, cohort_stats)
        }
        
        return explanation
    
    def _generate_summary(self, patient_data, predictions):
        """Generate high-level summary"""
        preg_prob = predictions['pregnancy_prob']
        
        if preg_prob > 0.55:
            outlook = "favorable"
        elif preg_prob > 0.40:
            outlook = "moderate"
        else:
            outlook = "challenging"
        
        summary = f"This patient has a {outlook} prognosis with an estimated {preg_prob:.1%} pregnancy success probability."
        
        return summary
    
    def _identify_key_factors(self, patient_data, predictions):
        """Identify key factors influencing the prediction"""
        factors = []
        
        # Age factor
        age = patient_data['age']
        if age < 30:
            factors.append({
                'factor': 'Age',
                'value': f"{age} years",
                'impact': 'Positive',
                'explanation': 'Young age associated with better outcomes'
            })
        elif age > 38:
            factors.append({
                'factor': 'Age',
                'value': f"{age} years",
                'impact': 'Negative',
                'explanation': 'Advanced age reduces success probability'
            })
        else:
            factors.append({
                'factor': 'Age',
                'value': f"{age} years",
                'impact': 'Neutral',
                'explanation': 'Age within optimal range'
            })
        
        # AMH factor
        amh = patient_data['amh']
        if amh < 1:
            factors.append({
                'factor': 'Ovarian Reserve (AMH)',
                'value': f"{amh:.2f} ng/mL",
                'impact': 'Negative',
                'explanation': 'Diminished ovarian reserve limits egg production'
            })
        elif amh > 5:
            factors.append({
                'factor': 'Ovarian Reserve (AMH)',
                'value': f"{amh:.2f} ng/mL",
                'impact': 'Positive',
                'explanation': 'Excellent ovarian reserve, but monitor OHSS risk'
            })
        else:
            factors.append({
                'factor': 'Ovarian Reserve (AMH)',
                'value': f"{amh:.2f} ng/mL",
                'impact': 'Positive',
                'explanation': 'Normal ovarian reserve'
            })
        
        # Expected eggs
        eggs = predictions.get('egg_yield', 0)
        if eggs > 12:
            factors.append({
                'factor': 'Expected Egg Yield',
                'value': f"{eggs} eggs",
                'impact': 'Positive',
                'explanation': 'High egg yield increases chances of success'
            })
        elif eggs < 5:
            factors.append({
                'factor': 'Expected Egg Yield',
                'value': f"{eggs} eggs",
                'impact': 'Negative',
                'explanation': 'Low egg yield may limit embryo selection'
            })
        
        # PCOS
        if patient_data.get('pcos', 0) == 1:
            factors.append({
                'factor': 'PCOS',
                'value': 'Present',
                'impact': 'Mixed',
                'explanation': 'Good egg numbers but increased OHSS risk'
            })
        
        # Previous failures
        previous = patient_data.get('previous_ivf_attempts', 0)
        if previous >= 2:
            factors.append({
                'factor': 'Previous IVF Attempts',
                'value': f"{previous} cycles",
                'impact': 'Negative',
                'explanation': 'Multiple previous failures reduce success probability'
            })
        
        # OHSS risk
        ohss_prob = predictions.get('ohss_prob', 0)
        if ohss_prob > 0.15:
            factors.append({
                'factor': 'OHSS Risk',
                'value': f"{ohss_prob:.1%}",
                'impact': 'Caution',
                'explanation': 'Elevated OHSS risk requires careful monitoring'
            })
        
        return factors
    
    def _explain_features(self, patient_data):
        """Explain individual feature contributions"""
        contributions = []
        
        # Age contribution
        age = patient_data['age']
        age_score = max(0, 1 - (age - 25) / 20)  # Simplified scoring
        contributions.append({
            'feature': 'Age',
            'value': age,
            'contribution_score': age_score,
            'interpretation': 'Higher' if age_score > 0.7 else 'Moderate' if age_score > 0.4 else 'Lower'
        })
        
        # AMH contribution
        amh = patient_data['amh']
        amh_score = min(1, amh / 5)
        contributions.append({
            'feature': 'AMH',
            'value': f"{amh:.2f}",
            'contribution_score': amh_score,
            'interpretation': 'Strong' if amh_score > 0.7 else 'Moderate' if amh_score > 0.4 else 'Weak'
        })
        
        # AFC contribution
        afc = patient_data['afc']
        afc_score = min(1, afc / 15)
        contributions.append({
            'feature': 'Antral Follicle Count',
            'value': afc,
            'contribution_score': afc_score,
            'interpretation': 'High' if afc_score > 0.7 else 'Normal' if afc_score > 0.4 else 'Low'
        })
        
        return sorted(contributions, key=lambda x: x['contribution_score'], reverse=True)
    
    def _explain_cohort_context(self, cohort_stats):
        """Explain how patient compares to similar cohort"""
        if not cohort_stats:
            return None
        
        context = {
            'cohort_size': cohort_stats['statistics']['cohort_size'],
            'cohort_success_rate': cohort_stats['statistics']['success_rate'],
            'comparison': []
        }
        
        success_rate = cohort_stats['statistics']['success_rate']
        if success_rate > 0.5:
            context['comparison'].append("Similar patients have shown favorable outcomes")
        elif success_rate > 0.35:
            context['comparison'].append("Similar patients have moderate success rates")
        else:
            context['comparison'].append("Similar patients face challenges, but success is possible")
        
        return context
    
    def _generate_natural_language(self, patient_data, predictions, cohort_stats):
        """Generate natural language explanation"""
        age = patient_data['age']
        amh = patient_data['amh']
        preg_prob = predictions['pregnancy_prob']
        eggs = predictions.get('egg_yield', 0)
        
        # Build explanation
        explanation = []
        
        # Opening
        explanation.append(f"Based on comprehensive analysis of this {age}-year-old patient:")
        
        # Ovarian reserve
        if amh < 1:
            explanation.append(f"The AMH level of {amh:.2f} ng/mL indicates diminished ovarian reserve, which may limit egg production.")
        elif amh > 5:
            explanation.append(f"The AMH level of {amh:.2f} ng/mL indicates excellent ovarian reserve with good egg production potential.")
        else:
            explanation.append(f"The AMH level of {amh:.2f} ng/mL indicates normal ovarian reserve.")
        
        # Expected outcome
        explanation.append(f"We expect approximately {eggs} eggs to be retrieved, leading to an estimated {preg_prob:.1%} pregnancy success probability.")
        
        # Age consideration
        if age > 38:
            explanation.append(f"Age is a significant factor, as success rates decline after 38 years.")
        elif age < 32:
            explanation.append(f"Age is favorable, as younger patients typically have better outcomes.")
        
        # OHSS risk
        ohss_prob = predictions.get('ohss_prob', 0)
        if ohss_prob > 0.15:
            explanation.append(f"There is an elevated OHSS risk ({ohss_prob:.1%}), requiring careful monitoring during stimulation.")
        
        # Cohort context
        if cohort_stats:
            cohort_success = cohort_stats['statistics']['success_rate']
            cohort_size = cohort_stats['statistics']['cohort_size']
            explanation.append(f"Among {cohort_size} similar patients in our database, the average success rate is {cohort_success:.1%}.")
        
        # Recommendation driver
        if amh > 3 and age < 35:
            explanation.append("Recommendation driven by good ovarian reserve and favorable age.")
        elif amh < 1.5 or age > 38:
            explanation.append("Recommendation considers reduced ovarian reserve and/or age factors.")
        else:
            explanation.append("Recommendation based on balanced clinical profile.")
        
        return " ".join(explanation)
    
    def get_feature_importance_chart(self):
        """Get feature importance from model"""
        if not self.predictor:
            return None
        
        importance = self.predictor.get_feature_importance('pregnancy')
        return importance.head(10)
    
    def generate_report(self, patient_data, predictions, recommendation, cohort_stats=None):
        """Generate comprehensive explanation report"""
        explanation = self.explain_prediction(patient_data, predictions, cohort_stats)
        
        report = {
            'patient_summary': explanation['summary'],
            'key_factors': explanation['key_factors'],
            'natural_language_explanation': explanation['natural_language'],
            'recommended_protocol': recommendation['protocol'],
            'recommendation_rationale': recommendation['rationale'],
            'cohort_context': explanation['cohort_context'],
            'confidence_level': predictions.get('confidence', 'Moderate')
        }
        
        return report
