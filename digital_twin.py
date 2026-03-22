"""
Digital Twin Simulator
Simulates ovarian response under different stimulation protocols
"""
import numpy as np
import pandas as pd

class DigitalTwinSimulator:
    """Simulate patient response to different IVF protocols"""
    
    def __init__(self):
        self.protocols = {
            'Mild Stimulation': {
                'dose_range': (150, 225),
                'cost_index': 1,
                'description': 'Lower medication dose, natural cycle approach'
            },
            'Antagonist': {
                'dose_range': (150, 300),
                'cost_index': 2,
                'description': 'Standard protocol with GnRH antagonist'
            },
            'Long Agonist': {
                'dose_range': (300, 450),
                'cost_index': 3,
                'description': 'High-dose protocol with pituitary suppression'
            }
        }
    
    def simulate_protocol(self, patient_data, protocol_name):
        """Simulate patient response to a specific protocol"""
        protocol = self.protocols[protocol_name]
        
        # Base parameters
        age = patient_data['age']
        amh = patient_data['amh']
        afc = patient_data['afc']
        bmi = patient_data['bmi']
        pcos = patient_data.get('pcos', 0)
        
        # Simulate egg yield
        egg_yield = self._simulate_egg_yield(amh, afc, age, protocol_name)
        
        # Simulate OHSS risk
        ohss_risk = self._simulate_ohss_risk(amh, pcos, egg_yield, protocol_name)
        
        # Simulate success probability
        success_prob = self._simulate_success(age, egg_yield, patient_data, protocol_name)
        
        # Calculate dose
        dose = self._calculate_dose(amh, age, protocol)
        
        # Calculate cost
        cost_estimate = self._estimate_cost(protocol, dose)
        
        return {
            'protocol': protocol_name,
            'description': protocol['description'],
            'estimated_eggs': egg_yield,
            'egg_range': (max(1, egg_yield - 2), egg_yield + 2),
            'success_probability': success_prob,
            'success_range': (max(0.05, success_prob - 0.08), min(0.95, success_prob + 0.08)),
            'ohss_risk': ohss_risk,
            'ohss_category': self._categorize_ohss(ohss_risk),
            'medication_dose': dose,
            'cost_index': protocol['cost_index'],
            'cost_estimate': cost_estimate,
            'suitability_score': self._calculate_suitability(patient_data, protocol_name)
        }
    
    def _simulate_egg_yield(self, amh, afc, age, protocol):
        """Simulate expected egg yield"""
        # Base yield from AMH and AFC
        base_yield = amh * 1.5 + afc * 0.4
        
        # Age penalty
        age_factor = 1 - (age - 30) * 0.015
        
        # Protocol modifier
        if protocol == 'Mild Stimulation':
            protocol_factor = 0.7
        elif protocol == 'Long Agonist':
            protocol_factor = 1.2
        else:
            protocol_factor = 1.0
        
        # Calculate
        eggs = base_yield * age_factor * protocol_factor
        
        # Add variability
        eggs = eggs + np.random.normal(0, 1.5)
        
        return int(np.clip(eggs, 1, 30))
    
    def _simulate_ohss_risk(self, amh, pcos, egg_yield, protocol):
        """Simulate OHSS risk probability"""
        risk = 0.03
        
        # AMH factor
        if amh > 5:
            risk += 0.15
        elif amh > 3:
            risk += 0.05
        
        # PCOS
        if pcos == 1:
            risk += 0.12
        
        # Egg yield
        if egg_yield > 15:
            risk += 0.15
        elif egg_yield > 12:
            risk += 0.08
        
        # Protocol factor
        if protocol == 'Antagonist':
            risk *= 0.7  # Lower risk with antagonist
        elif protocol == 'Long Agonist':
            risk *= 1.2  # Higher risk with agonist
        
        return np.clip(risk, 0.01, 0.50)
    
    def _simulate_success(self, age, egg_yield, patient_data, protocol):
        """Simulate pregnancy success probability"""
        base_prob = 0.45
        
        # Age factor
        if age < 30:
            base_prob += 0.12
        elif age < 35:
            base_prob += 0.05
        elif age > 38:
            base_prob -= 0.15
        elif age > 40:
            base_prob -= 0.25
        
        # Egg yield factor
        if egg_yield > 12:
            base_prob += 0.10
        elif egg_yield > 8:
            base_prob += 0.05
        elif egg_yield < 5:
            base_prob -= 0.15
        
        # Previous failures
        previous = patient_data.get('previous_ivf_attempts', 0)
        base_prob -= previous * 0.08
        
        # Endometriosis
        if patient_data.get('endometriosis', 0) == 1:
            base_prob -= 0.08
        
        # Male factor
        if patient_data.get('male_factor', 0) == 1:
            base_prob -= 0.05
        
        # Protocol adjustment
        if protocol == 'Mild Stimulation' and egg_yield < 8:
            base_prob -= 0.05
        
        return np.clip(base_prob, 0.05, 0.75)
    
    def _calculate_dose(self, amh, age, protocol):
        """Calculate medication dose"""
        dose_range = protocol['dose_range']
        
        # Base on AMH
        if amh < 1:
            dose = dose_range[1]  # High dose
        elif amh > 5:
            dose = dose_range[0]  # Low dose
        else:
            # Interpolate
            dose = dose_range[0] + (dose_range[1] - dose_range[0]) * (1 - (amh - 1) / 4)
        
        return int(dose)
    
    def _estimate_cost(self, protocol, dose):
        """Estimate treatment cost"""
        # Base cost by protocol
        base_cost = protocol['cost_index'] * 3000
        
        # Medication cost (roughly $50 per 75 IU)
        med_cost = (dose / 75) * 50 * 10  # 10 days average
        
        total = base_cost + med_cost
        
        return int(total)
    
    def _categorize_ohss(self, risk):
        """Categorize OHSS risk"""
        if risk > 0.15:
            return 'High Risk'
        elif risk > 0.08:
            return 'Moderate Risk'
        else:
            return 'Low Risk'
    
    def _calculate_suitability(self, patient_data, protocol):
        """Calculate protocol suitability score (0-100)"""
        score = 50
        
        amh = patient_data['amh']
        age = patient_data['age']
        pcos = patient_data.get('pcos', 0)
        
        if protocol == 'Mild Stimulation':
            if age < 35 and amh > 2 and amh < 6:
                score += 30
            if pcos == 1:
                score -= 20
        
        elif protocol == 'Antagonist':
            if amh > 3:
                score += 20
            if pcos == 1:
                score += 25
            score += 10  # Generally versatile
        
        elif protocol == 'Long Agonist':
            if amh < 1.5:
                score += 30
            if age > 38:
                score += 15
            if pcos == 1:
                score -= 25
        
        return int(np.clip(score, 0, 100))
    
    def simulate_all_protocols(self, patient_data):
        """Simulate all protocols and return comparison"""
        results = []
        
        for protocol_name in self.protocols.keys():
            result = self.simulate_protocol(patient_data, protocol_name)
            results.append(result)
        
        return results
    
    def rank_protocols(self, simulations):
        """Rank protocols using multi-objective optimization"""
        scored = []
        
        for sim in simulations:
            # Multi-objective score
            score = (
                0.50 * sim['success_probability'] +
                -0.20 * sim['ohss_risk'] +
                -0.15 * (sim['medication_dose'] / 450) +  # Normalized
                -0.15 * (sim['cost_index'] / 3)  # Normalized
            )
            
            sim['optimization_score'] = score
            scored.append(sim)
        
        # Sort by score
        ranked = sorted(scored, key=lambda x: x['optimization_score'], reverse=True)
        
        return ranked
