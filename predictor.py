"""
Predictor Module
Loads trained models and makes predictions
"""
import pickle
import pandas as pd
import numpy as np
import os

class FertilityPredictor:
    """Wrapper for trained fertility prediction models"""
    
    def __init__(self, model_dir='models/saved'):
        self.model_dir = model_dir
        self.models = {}
        self.preprocessor = None
        self.load_models()
    
    def load_models(self):
        """Load all trained models"""
        try:
            with open(f'{self.model_dir}/pregnancy_model.pkl', 'rb') as f:
                self.models['pregnancy'] = pickle.load(f)
            
            with open(f'{self.model_dir}/ohss_model.pkl', 'rb') as f:
                self.models['ohss'] = pickle.load(f)
            
            with open(f'{self.model_dir}/egg_yield_model.pkl', 'rb') as f:
                self.models['egg_yield'] = pickle.load(f)
            
            with open(f'{self.model_dir}/preprocessor.pkl', 'rb') as f:
                self.preprocessor = pickle.load(f)
            
            return True
        except FileNotFoundError:
            return False
    
    def predict_patient(self, patient_data):
        """Make predictions for a single patient"""
        # Convert to DataFrame
        df = pd.DataFrame([patient_data])
        
        # Preprocess
        X = self.preprocessor.prepare_features(df)
        
        # Predictions
        predictions = {}
        
        # Pregnancy success probability
        predictions['pregnancy_prob'] = self.models['pregnancy'].predict_proba(X)[0, 1]
        predictions['pregnancy_class'] = self.models['pregnancy'].predict(X)[0]
        
        # OHSS risk probability
        predictions['ohss_prob'] = self.models['ohss'].predict_proba(X)[0, 1]
        predictions['ohss_class'] = self.models['ohss'].predict(X)[0]
        
        # Expected egg yield
        predictions['egg_yield'] = max(1, int(round(self.models['egg_yield'].predict(X)[0])))
        
        return predictions
    
    def get_feature_importance(self, model_name='pregnancy'):
        """Get feature importance for a model"""
        if model_name not in self.models:
            return None
        
        importance = pd.DataFrame({
            'feature': self.preprocessor.feature_names,
            'importance': self.models[model_name].feature_importances_
        }).sort_values('importance', ascending=False)
        
        return importance
    
    def predict_with_confidence(self, patient_data):
        """Predict with confidence intervals"""
        predictions = self.predict_patient(patient_data)
        
        # Add confidence levels
        preg_prob = predictions['pregnancy_prob']
        if preg_prob > 0.6:
            predictions['confidence'] = 'High'
        elif preg_prob > 0.4:
            predictions['confidence'] = 'Moderate'
        else:
            predictions['confidence'] = 'Low'
        
        # Risk category
        ohss_prob = predictions['ohss_prob']
        if ohss_prob > 0.15:
            predictions['ohss_category'] = 'High Risk'
        elif ohss_prob > 0.08:
            predictions['ohss_category'] = 'Moderate Risk'
        else:
            predictions['ohss_category'] = 'Low Risk'
        
        return predictions
    
    def batch_predict(self, patients_df):
        """Predict for multiple patients"""
        X = self.preprocessor.prepare_features(patients_df)
        
        results = pd.DataFrame()
        results['pregnancy_prob'] = self.models['pregnancy'].predict_proba(X)[:, 1]
        results['ohss_prob'] = self.models['ohss'].predict_proba(X)[:, 1]
        results['egg_yield'] = self.models['egg_yield'].predict(X)
        
        return results
