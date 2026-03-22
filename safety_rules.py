"""
Clinical Safety Rules Engine
Implements rule-based clinical decision support and safety checks
"""

class SafetyRulesEngine:
    """Clinical safety rules and alerts"""
    
    def __init__(self):
        self.alerts = []
        self.warnings = []
        self.recommendations = []
    
    def evaluate_patient(self, patient_data):
        """Evaluate patient against all safety rules"""
        self.alerts = []
        self.warnings = []
        self.recommendations = []
        
        self._check_ovarian_reserve(patient_data)
        self._check_ohss_risk(patient_data)
        self._check_age_factors(patient_data)
        self._check_bmi(patient_data)
        self._check_previous_failures(patient_data)
        self._check_hormone_levels(patient_data)
        self._check_combined_risks(patient_data)
        
        return {
            'alerts': self.alerts,
            'warnings': self.warnings,
            'recommendations': self.recommendations,
            'risk_level': self._calculate_risk_level()
        }
    
    def _check_ovarian_reserve(self, data):
        """Check ovarian reserve status"""
        amh = data['amh']
        afc = data['afc']
        
        if amh < 0.5:
            self.alerts.append({
                'type': 'CRITICAL',
                'category': 'Ovarian Reserve',
                'message': f'Severely diminished ovarian reserve (AMH: {amh:.2f} ng/mL)',
                'action': 'Consider donor eggs or aggressive stimulation protocol'
            })
        elif amh < 1.0:
            self.warnings.append({
                'type': 'WARNING',
                'category': 'Ovarian Reserve',
                'message': f'Diminished ovarian reserve (AMH: {amh:.2f} ng/mL)',
                'action': 'High-dose stimulation protocol recommended'
            })
        
        if afc < 5:
            self.warnings.append({
                'type': 'WARNING',
                'category': 'Follicle Count',
                'message': f'Low antral follicle count (AFC: {afc})',
                'action': 'Expect lower egg yield'
            })
    
    def _check_ohss_risk(self, data):
        """Check OHSS risk factors"""
        amh = data['amh']
        pcos = data.get('pcos', 0)
        afc = data['afc']
        
        risk_factors = []
        
        if amh > 4:
            risk_factors.append(f'High AMH ({amh:.2f} ng/mL)')
        
        if pcos == 1:
            risk_factors.append('PCOS diagnosis')
        
        if afc > 15:
            risk_factors.append(f'High AFC ({afc})')
        
        if len(risk_factors) >= 2:
            self.alerts.append({
                'type': 'ALERT',
                'category': 'OHSS Risk',
                'message': f'High OHSS risk: {", ".join(risk_factors)}',
                'action': 'Consider antagonist protocol, GnRH trigger, coasting, or cycle cancellation if needed'
            })
            self.recommendations.append('Monitor estradiol levels closely during stimulation')
            self.recommendations.append('Consider elective freeze-all strategy')
        elif len(risk_factors) == 1:
            self.warnings.append({
                'type': 'WARNING',
                'category': 'OHSS Risk',
                'message': f'Moderate OHSS risk: {risk_factors[0]}',
                'action': 'Monitor closely during stimulation'
            })
    
    def _check_age_factors(self, data):
        """Check age-related factors"""
        age = data['age']
        
        if age >= 42:
            self.alerts.append({
                'type': 'ALERT',
                'category': 'Age',
                'message': f'Advanced maternal age ({age} years)',
                'action': 'Counsel on reduced success rates and increased aneuploidy risk'
            })
            self.recommendations.append('Consider PGT-A (preimplantation genetic testing)')
        elif age >= 38:
            self.warnings.append({
                'type': 'WARNING',
                'category': 'Age',
                'message': f'Age-related fertility decline ({age} years)',
                'action': 'Adjust expectations for success rates'
            })
        
        if age < 25:
            self.recommendations.append('Excellent age-related prognosis')
    
    def _check_bmi(self, data):
        """Check BMI factors"""
        bmi = data['bmi']
        
        if bmi < 18.5:
            self.warnings.append({
                'type': 'WARNING',
                'category': 'BMI',
                'message': f'Underweight (BMI: {bmi:.1f})',
                'action': 'May affect ovarian response and pregnancy outcomes'
            })
        elif bmi >= 35:
            self.alerts.append({
                'type': 'ALERT',
                'category': 'BMI',
                'message': f'Obesity Class II+ (BMI: {bmi:.1f})',
                'action': 'Recommend weight loss before IVF; increased pregnancy complications'
            })
        elif bmi >= 30:
            self.warnings.append({
                'type': 'WARNING',
                'category': 'BMI',
                'message': f'Obesity (BMI: {bmi:.1f})',
                'action': 'May require higher medication doses; monitor closely'
            })
    
    def _check_previous_failures(self, data):
        """Check previous IVF history"""
        previous = data.get('previous_ivf_attempts', 0)
        
        if previous >= 3:
            self.alerts.append({
                'type': 'ALERT',
                'category': 'IVF History',
                'message': f'Multiple previous failures ({previous} attempts)',
                'action': 'Consider changing protocol, additional testing, or alternative approaches'
            })
            self.recommendations.append('Review previous cycle details for optimization')
        elif previous >= 2:
            self.warnings.append({
                'type': 'WARNING',
                'category': 'IVF History',
                'message': f'Previous IVF failures ({previous} attempts)',
                'action': 'Analyze previous cycles for protocol adjustment'
            })
    
    def _check_hormone_levels(self, data):
        """Check hormone level abnormalities"""
        fsh = data['fsh']
        lh = data['lh']
        
        if fsh > 12:
            self.warnings.append({
                'type': 'WARNING',
                'category': 'FSH Level',
                'message': f'Elevated FSH ({fsh:.1f} mIU/mL)',
                'action': 'Indicates reduced ovarian reserve'
            })
        
        lh_fsh_ratio = lh / fsh
        if lh_fsh_ratio > 2:
            self.warnings.append({
                'type': 'WARNING',
                'category': 'LH/FSH Ratio',
                'message': f'Elevated LH/FSH ratio ({lh_fsh_ratio:.2f})',
                'action': 'Consistent with PCOS; monitor for OHSS'
            })
    
    def _check_combined_risks(self, data):
        """Check combined risk factors"""
        age = data['age']
        amh = data['amh']
        previous = data.get('previous_ivf_attempts', 0)
        
        # Poor prognosis combination
        if age >= 38 and amh < 1.5 and previous >= 1:
            self.alerts.append({
                'type': 'CRITICAL',
                'category': 'Combined Risk',
                'message': 'Multiple poor prognosis factors present',
                'action': 'Counsel on realistic expectations; consider alternative options'
            })
        
        # Excellent prognosis
        if age < 32 and amh > 2 and amh < 6 and previous == 0:
            self.recommendations.append('Excellent prognosis - favorable conditions for IVF success')
    
    def _calculate_risk_level(self):
        """Calculate overall risk level"""
        alert_count = len(self.alerts)
        warning_count = len(self.warnings)
        
        if alert_count >= 2:
            return 'HIGH'
        elif alert_count >= 1 or warning_count >= 3:
            return 'MODERATE'
        elif warning_count >= 1:
            return 'LOW'
        else:
            return 'MINIMAL'
    
    def get_protocol_recommendation(self, patient_data):
        """Recommend stimulation protocol based on rules"""
        amh = patient_data['amh']
        age = patient_data['age']
        pcos = patient_data.get('pcos', 0)
        
        if amh < 1:
            return {
                'protocol': 'Long Agonist',
                'rationale': 'Diminished ovarian reserve - maximize follicle recruitment',
                'dose_range': '300-450 IU'
            }
        elif amh > 5 or pcos == 1:
            return {
                'protocol': 'Antagonist',
                'rationale': 'High ovarian reserve / PCOS - reduce OHSS risk',
                'dose_range': '100-200 IU'
            }
        elif age < 35 and amh >= 2:
            return {
                'protocol': 'Mild Stimulation',
                'rationale': 'Good prognosis - minimize medication and cost',
                'dose_range': '150-225 IU'
            }
        else:
            return {
                'protocol': 'Antagonist',
                'rationale': 'Standard protocol for normal responders',
                'dose_range': '150-300 IU'
            }
