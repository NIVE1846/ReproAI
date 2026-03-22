"""
Multi-Objective Optimization Engine
Ranks treatment protocols using weighted scoring
"""
import numpy as np
import pandas as pd

class OptimizationEngine:
    """Multi-objective optimization for protocol selection"""
    
    def __init__(self):
        # Default weights
        self.weights = {
            'success': 0.50,
            'ohss_risk': -0.20,
            'medication_dose': -0.15,
            'cost': -0.15
        }
    
    def set_weights(self, success=0.50, ohss_risk=-0.20, medication_dose=-0.15, cost=-0.15):
        """Set custom optimization weights"""
        total = abs(success) + abs(ohss_risk) + abs(medication_dose) + abs(cost)
        
        self.weights = {
            'success': success / total,
            'ohss_risk': ohss_risk / total,
            'medication_dose': medication_dose / total,
            'cost': cost / total
        }
    
    def calculate_score(self, protocol_result):
        """Calculate optimization score for a protocol"""
        # Normalize values
        success_norm = protocol_result['success_probability']
        ohss_norm = protocol_result['ohss_risk']
        dose_norm = protocol_result['medication_dose'] / 450  # Max dose
        cost_norm = protocol_result['cost_index'] / 3  # Max cost index
        
        # Calculate weighted score
        score = (
            self.weights['success'] * success_norm +
            self.weights['ohss_risk'] * ohss_norm +
            self.weights['medication_dose'] * dose_norm +
            self.weights['cost'] * cost_norm
        )
        
        return score
    
    def rank_protocols(self, protocol_results):
        """Rank protocols by optimization score"""
        scored_protocols = []
        
        for result in protocol_results:
            score = self.calculate_score(result)
            result['optimization_score'] = score
            result['rank'] = 0  # Will be set after sorting
            scored_protocols.append(result)
        
        # Sort by score (descending)
        ranked = sorted(scored_protocols, key=lambda x: x['optimization_score'], reverse=True)
        
        # Assign ranks
        for i, protocol in enumerate(ranked):
            protocol['rank'] = i + 1
        
        return ranked
    
    def get_recommendation(self, ranked_protocols):
        """Get top recommendation with explanation"""
        if not ranked_protocols:
            return None
        
        top_protocol = ranked_protocols[0]
        
        recommendation = {
            'protocol': top_protocol['protocol'],
            'score': top_protocol['optimization_score'],
            'rationale': self._generate_rationale(top_protocol, ranked_protocols),
            'key_metrics': {
                'Success Probability': f"{top_protocol['success_probability']:.1%}",
                'OHSS Risk': f"{top_protocol['ohss_risk']:.1%}",
                'Expected Eggs': f"{top_protocol['estimated_eggs']} eggs",
                'Medication Dose': f"{top_protocol['medication_dose']} IU",
                'Cost Estimate': f"${top_protocol['cost_estimate']:,}"
            },
            'alternatives': ranked_protocols[1:] if len(ranked_protocols) > 1 else []
        }
        
        return recommendation
    
    def _generate_rationale(self, top_protocol, all_protocols):
        """Generate explanation for recommendation"""
        rationale = []
        
        # Why this protocol is best
        rationale.append(f"Recommended: {top_protocol['protocol']}")
        
        # Success rate
        success = top_protocol['success_probability']
        if success > 0.5:
            rationale.append(f"✓ High success probability ({success:.1%})")
        elif success > 0.35:
            rationale.append(f"○ Moderate success probability ({success:.1%})")
        else:
            rationale.append(f"⚠ Lower success probability ({success:.1%})")
        
        # OHSS risk
        ohss = top_protocol['ohss_risk']
        if ohss < 0.08:
            rationale.append(f"✓ Low OHSS risk ({ohss:.1%})")
        elif ohss < 0.15:
            rationale.append(f"○ Moderate OHSS risk ({ohss:.1%})")
        else:
            rationale.append(f"⚠ Higher OHSS risk ({ohss:.1%}) - requires monitoring")
        
        # Cost efficiency
        if top_protocol['cost_index'] == 1:
            rationale.append("✓ Most cost-effective option")
        elif top_protocol['cost_index'] == 2:
            rationale.append("○ Moderate cost")
        else:
            rationale.append("Higher cost but may be necessary for optimal response")
        
        # Comparison to alternatives
        if len(all_protocols) > 1:
            second_best = all_protocols[1]
            score_diff = top_protocol['optimization_score'] - second_best['optimization_score']
            
            if score_diff > 0.1:
                rationale.append(f"Significantly better than {second_best['protocol']}")
            else:
                rationale.append(f"Marginally better than {second_best['protocol']} - both viable")
        
        return rationale
    
    def compare_protocols(self, protocol_results):
        """Generate detailed comparison table"""
        comparison = []
        
        for result in protocol_results:
            comparison.append({
                'Protocol': result['protocol'],
                'Success Rate': f"{result['success_probability']:.1%}",
                'OHSS Risk': f"{result['ohss_risk']:.1%}",
                'Expected Eggs': result['estimated_eggs'],
                'Dose (IU)': result['medication_dose'],
                'Cost': f"${result['cost_estimate']:,}",
                'Score': f"{result.get('optimization_score', 0):.3f}",
                'Rank': result.get('rank', '-')
            })
        
        return pd.DataFrame(comparison)
    
    def sensitivity_analysis(self, protocol_results):
        """Perform sensitivity analysis on weights"""
        scenarios = {
            'Success-Focused': {'success': 0.70, 'ohss_risk': -0.15, 'medication_dose': -0.075, 'cost': -0.075},
            'Safety-Focused': {'success': 0.30, 'ohss_risk': -0.50, 'medication_dose': -0.10, 'cost': -0.10},
            'Cost-Focused': {'success': 0.40, 'ohss_risk': -0.15, 'medication_dose': -0.15, 'cost': -0.30},
            'Balanced': {'success': 0.50, 'ohss_risk': -0.20, 'medication_dose': -0.15, 'cost': -0.15}
        }
        
        results = {}
        
        for scenario_name, weights in scenarios.items():
            # Temporarily set weights
            original_weights = self.weights.copy()
            self.set_weights(**weights)
            
            # Rank with these weights
            ranked = self.rank_protocols(protocol_results.copy())
            results[scenario_name] = ranked[0]['protocol']
            
            # Restore original weights
            self.weights = original_weights
        
        return results
    
    def get_optimization_breakdown(self, protocol_result):
        """Show how each factor contributes to the score"""
        breakdown = {
            'Success Contribution': self.weights['success'] * protocol_result['success_probability'],
            'OHSS Contribution': self.weights['ohss_risk'] * protocol_result['ohss_risk'],
            'Dose Contribution': self.weights['medication_dose'] * (protocol_result['medication_dose'] / 450),
            'Cost Contribution': self.weights['cost'] * (protocol_result['cost_index'] / 3),
            'Total Score': protocol_result.get('optimization_score', 0)
        }
        
        return breakdown
