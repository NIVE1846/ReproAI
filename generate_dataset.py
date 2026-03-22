"""
Synthetic Fertility Dataset Generator
Generates realistic IVF patient data with clinical correlations
"""
import pandas as pd
import numpy as np

np.random.seed(42)

def generate_synthetic_dataset(n_samples=2000):
    """Generate synthetic fertility dataset with realistic clinical patterns"""
    
    data = []
    
    for _ in range(n_samples):
        # Demographics
        age = np.random.randint(25, 45)
        
        # PCOS and Endometriosis
        pcos = np.random.choice([0, 1], p=[0.7, 0.3])
        endometriosis = np.random.choice([0, 1], p=[0.85, 0.15])
        
        # BMI - higher in PCOS patients
        if pcos == 1:
            bmi = np.clip(np.random.normal(28, 4), 18, 40)
        else:
            bmi = np.clip(np.random.normal(24, 3), 18, 40)
        
        # AMH - higher in PCOS, decreases with age
        if pcos == 1:
            amh = np.clip(np.random.normal(8, 4), 0.1, 70)
        else:
            amh = np.clip(np.random.normal(3, 2) * (1 - (age - 25) * 0.02), 0.1, 30)
        
        # FSH - increases with age, lower reserve
        fsh = np.clip(np.random.normal(7, 2) + (age - 30) * 0.15, 2, 20)
        
        # LH - higher in PCOS
        if pcos == 1:
            lh = np.clip(np.random.normal(12, 3), 2, 25)
        else:
            lh = np.clip(np.random.normal(6, 2), 2, 15)
        
        # Estradiol
        estradiol = np.clip(np.random.normal(45, 15), 20, 100)
        
        # Antral Follicle Count - correlates with AMH
        afc = int(np.clip(amh * 2 + np.random.normal(0, 2), 2, 30))
        
        # Previous IVF attempts
        previous_ivf_attempts = np.random.choice([0, 1, 2, 3, 4], p=[0.5, 0.25, 0.15, 0.07, 0.03])
        
        # Male factor
        male_factor = np.random.choice([0, 1], p=[0.7, 0.3])
        
        # Protocol assignment based on ovarian reserve
        if amh < 1:
            protocol = "Long Agonist"
        elif amh > 5:
            protocol = "Antagonist"
        else:
            protocol = np.random.choice(["Mild", "Antagonist"], p=[0.3, 0.7])
        
        # Eggs retrieved - based on AMH, AFC, age
        base_eggs = amh * 1.5 + afc * 0.3
        age_penalty = (age - 30) * 0.2
        eggs_retrieved = int(np.clip(base_eggs - age_penalty + np.random.normal(0, 2), 1, 30))
        
        # OHSS risk - high AMH, PCOS, high eggs
        ohss_risk_prob = 0.05
        if amh > 5:
            ohss_risk_prob += 0.15
        if pcos == 1:
            ohss_risk_prob += 0.10
        if eggs_retrieved > 15:
            ohss_risk_prob += 0.10
        ohss_risk = np.random.choice([0, 1], p=[1 - ohss_risk_prob, ohss_risk_prob])
        
        # Success probability
        success_prob = 0.45
        if age > 38:
            success_prob -= 0.20
        elif age < 32:
            success_prob += 0.10
        if eggs_retrieved > 10:
            success_prob += 0.10
        if eggs_retrieved < 5:
            success_prob -= 0.15
        if previous_ivf_attempts > 1:
            success_prob -= 0.10
        if endometriosis == 1:
            success_prob -= 0.08
        if male_factor == 1:
            success_prob -= 0.05
        if ohss_risk == 1:
            success_prob -= 0.05
        
        success_prob = np.clip(success_prob, 0.05, 0.70)
        success = np.random.choice([0, 1], p=[1 - success_prob, success_prob])
        
        data.append({
            'age': age,
            'bmi': round(bmi, 1),
            'amh': round(amh, 2),
            'fsh': round(fsh, 1),
            'lh': round(lh, 1),
            'estradiol': round(estradiol, 1),
            'afc': afc,
            'pcos': pcos,
            'endometriosis': endometriosis,
            'previous_ivf_attempts': previous_ivf_attempts,
            'male_factor': male_factor,
            'success': success,
            'ohss_risk': ohss_risk,
            'eggs_retrieved': eggs_retrieved,
            'protocol': protocol
        })
    
    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    print("Generating synthetic fertility dataset...")
    df = generate_synthetic_dataset(2000)
    
    df.to_csv('data/synthetic_fertility_dataset.csv', index=False)
    
    print(f"Dataset created: {df.shape[0]} patients, {df.shape[1]} features")
    print(f"\nDataset Statistics:")
    print(f"  Age range: {df['age'].min()}-{df['age'].max()} years")
    print(f"  AMH range: {df['amh'].min():.2f}-{df['amh'].max():.2f} ng/mL")
    print(f"  PCOS prevalence: {df['pcos'].mean():.1%}")
    print(f"  Success rate: {df['success'].mean():.1%}")
    print(f"  OHSS rate: {df['ohss_risk'].mean():.1%}")
    print(f"  Avg eggs retrieved: {df['eggs_retrieved'].mean():.1f}")
    print(f"\nProtocol distribution:")
    print(df['protocol'].value_counts())
