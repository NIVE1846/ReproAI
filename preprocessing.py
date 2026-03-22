"""
Data Preprocessing Utilities
Handles feature engineering and data transformation
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

class FertilityPreprocessor:
    """Preprocessor for fertility data"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.feature_names = None
        
    def create_features(self, df):
        """Create engineered features"""
        df = df.copy()
        
        # Ovarian reserve category
        df['ovarian_reserve'] = pd.cut(df['amh'], 
                                       bins=[0, 1, 4, 100],
                                       labels=['Low', 'Normal', 'High'])
        
        # Age category
        df['age_category'] = pd.cut(df['age'],
                                    bins=[0, 30, 35, 40, 100],
                                    labels=['<30', '30-35', '35-40', '>40'])
        
        # BMI category
        df['bmi_category'] = pd.cut(df['bmi'],
                                    bins=[0, 18.5, 25, 30, 100],
                                    labels=['Underweight', 'Normal', 'Overweight', 'Obese'])
        
        # LH/FSH ratio (PCOS indicator)
        df['lh_fsh_ratio'] = df['lh'] / df['fsh']
        
        # Total follicle score
        df['follicle_score'] = df['afc'] * df['amh']
        
        # Age-adjusted AMH
        df['age_adjusted_amh'] = df['amh'] * (1 - (df['age'] - 25) * 0.01)
        
        # Risk score
        df['risk_score'] = (df['age'] > 38).astype(int) + \
                          (df['amh'] < 1).astype(int) + \
                          (df['previous_ivf_attempts'] > 1).astype(int)
        
        return df
    
    def prepare_features(self, df, target_col=None):
        """Prepare features for modeling"""
        df = self.create_features(df)
        
        # Select numeric features
        numeric_features = ['age', 'bmi', 'amh', 'fsh', 'lh', 'estradiol', 'afc',
                           'previous_ivf_attempts', 'lh_fsh_ratio', 'follicle_score',
                           'age_adjusted_amh', 'risk_score']
        
        # Binary features
        binary_features = ['pcos', 'endometriosis', 'male_factor']
        
        feature_cols = numeric_features + binary_features
        X = df[feature_cols].copy()
        
        self.feature_names = feature_cols
        
        if target_col:
            y = df[target_col]
            return X, y
        
        return X
    
    def scale_features(self, X, fit=True):
        """Scale features"""
        if fit:
            return self.scaler.fit_transform(X)
        return self.scaler.transform(X)
    
    def get_patient_summary(self, patient_data):
        """Generate clinical summary for a patient"""
        summary = {}
        
        # Ovarian reserve
        amh = patient_data['amh']
        if amh < 1:
            summary['ovarian_reserve'] = 'Low (Diminished Reserve)'
        elif amh <= 4:
            summary['ovarian_reserve'] = 'Normal'
        else:
            summary['ovarian_reserve'] = 'High (Good Reserve)'
        
        # Age prognosis
        age = patient_data['age']
        if age < 30:
            summary['age_prognosis'] = 'Excellent'
        elif age < 35:
            summary['age_prognosis'] = 'Good'
        elif age < 38:
            summary['age_prognosis'] = 'Fair'
        elif age < 40:
            summary['age_prognosis'] = 'Reduced'
        else:
            summary['age_prognosis'] = 'Significantly Reduced'
        
        # PCOS status
        summary['pcos_status'] = 'Yes' if patient_data.get('pcos', 0) == 1 else 'No'
        
        # Endometriosis
        summary['endometriosis'] = 'Yes' if patient_data.get('endometriosis', 0) == 1 else 'No'
        
        # LH/FSH ratio
        lh_fsh = patient_data['lh'] / patient_data['fsh']
        summary['lh_fsh_ratio'] = f"{lh_fsh:.2f}"
        if lh_fsh > 2:
            summary['lh_fsh_interpretation'] = 'Elevated (PCOS pattern)'
        else:
            summary['lh_fsh_interpretation'] = 'Normal'
        
        return summary

def load_dataset(filepath='data/synthetic_fertility_dataset.csv'):
    """Load the fertility dataset"""
    return pd.read_csv(filepath)
