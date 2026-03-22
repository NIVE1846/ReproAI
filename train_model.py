"""
Model Training Module
Trains ML models for pregnancy success, OHSS risk, and egg yield prediction
"""
import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, roc_auc_score, mean_absolute_error, r2_score
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.preprocessing import FertilityPreprocessor, load_dataset

def train_pregnancy_model(X, y):
    """Train pregnancy success prediction model"""
    print("\n" + "="*60)
    print("Training Pregnancy Success Model")
    print("="*60)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Random Forest
    rf_model = RandomForestClassifier(n_estimators=200, max_depth=10, min_samples_split=10,
                                     random_state=42, class_weight='balanced')
    rf_model.fit(X_train, y_train)
    
    # Gradient Boosting
    gb_model = GradientBoostingClassifier(n_estimators=150, max_depth=5, learning_rate=0.1,
                                         random_state=42)
    gb_model.fit(X_train, y_train)
    
    # Evaluate
    rf_score = roc_auc_score(y_test, rf_model.predict_proba(X_test)[:, 1])
    gb_score = roc_auc_score(y_test, gb_model.predict_proba(X_test)[:, 1])
    
    print(f"Random Forest AUC: {rf_score:.3f}")
    print(f"Gradient Boosting AUC: {gb_score:.3f}")
    
    # Use best model
    best_model = rf_model if rf_score > gb_score else gb_model
    print(f"\nBest Model: {'Random Forest' if rf_score > gb_score else 'Gradient Boosting'}")
    
    y_pred = best_model.predict(X_test)
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['No Success', 'Success']))
    
    return best_model

def train_ohss_model(X, y):
    """Train OHSS risk prediction model"""
    print("\n" + "="*60)
    print("Training OHSS Risk Model")
    print("="*60)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    model = RandomForestClassifier(n_estimators=150, max_depth=8, min_samples_split=15,
                                  random_state=42, class_weight='balanced')
    model.fit(X_train, y_train)
    
    score = roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])
    print(f"OHSS Model AUC: {score:.3f}")
    
    y_pred = model.predict(X_test)
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['No OHSS', 'OHSS Risk']))
    
    return model

def train_egg_yield_model(X, y):
    """Train egg yield prediction model"""
    print("\n" + "="*60)
    print("Training Egg Yield Model")
    print("="*60)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestRegressor(n_estimators=200, max_depth=12, min_samples_split=10,
                                 random_state=42)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"Mean Absolute Error: {mae:.2f} eggs")
    print(f"R² Score: {r2:.3f}")
    
    return model

def save_models(models, preprocessor):
    """Save trained models"""
    os.makedirs('models/saved', exist_ok=True)
    
    with open('models/saved/pregnancy_model.pkl', 'wb') as f:
        pickle.dump(models['pregnancy'], f)
    
    with open('models/saved/ohss_model.pkl', 'wb') as f:
        pickle.dump(models['ohss'], f)
    
    with open('models/saved/egg_yield_model.pkl', 'wb') as f:
        pickle.dump(models['egg_yield'], f)
    
    with open('models/saved/preprocessor.pkl', 'wb') as f:
        pickle.dump(preprocessor, f)
    
    print("\nModels saved to models/saved/")

def main():
    """Main training pipeline"""
    print("="*60)
    print("ReproAI Model Training Pipeline")
    print("="*60)
    
    # Load data
    print("\nLoading dataset...")
    df = load_dataset()
    print(f"Loaded {len(df)} patient records")
    
    # Preprocess
    print("\nPreprocessing features...")
    preprocessor = FertilityPreprocessor()
    
    # Prepare features for each target
    X_pregnancy, y_pregnancy = preprocessor.prepare_features(df, 'success')
    X_ohss, y_ohss = preprocessor.prepare_features(df, 'ohss_risk')
    X_eggs, y_eggs = preprocessor.prepare_features(df, 'eggs_retrieved')
    
    print(f"Feature set: {len(preprocessor.feature_names)} features")
    
    # Train models
    models = {}
    models['pregnancy'] = train_pregnancy_model(X_pregnancy, y_pregnancy)
    models['ohss'] = train_ohss_model(X_ohss, y_ohss)
    models['egg_yield'] = train_egg_yield_model(X_eggs, y_eggs)
    
    # Feature importance
    print("\n" + "="*60)
    print("Top 10 Features for Pregnancy Success")
    print("="*60)
    feature_importance = pd.DataFrame({
        'feature': preprocessor.feature_names,
        'importance': models['pregnancy'].feature_importances_
    }).sort_values('importance', ascending=False)
    
    print(feature_importance.head(10).to_string(index=False))
    
    # Save
    save_models(models, preprocessor)
    
    print("\n" + "="*60)
    print("Training Complete!")
    print("="*60)

if __name__ == "__main__":
    main()
