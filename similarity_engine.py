"""
Similarity Engine
Finds similar patients using k-Nearest Neighbors for cohort analysis
"""
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler

class SimilarityEngine:
    """Find similar patients for cohort comparison"""
    
    def __init__(self, dataset_path='data/synthetic_fertility_dataset.csv'):
        self.df = pd.read_csv(dataset_path)
        self.scaler = StandardScaler()
        self.knn = None
        self._prepare_similarity_model()
    
    def _prepare_similarity_model(self):
        """Prepare KNN model for similarity search"""
        # Features for similarity
        feature_cols = ['age', 'bmi', 'amh', 'fsh', 'lh', 'afc', 
                       'pcos', 'endometriosis', 'previous_ivf_attempts']
        
        self.feature_cols = feature_cols
        X = self.df[feature_cols].values
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Fit KNN
        self.knn = NearestNeighbors(n_neighbors=50, metric='euclidean')
        self.knn.fit(X_scaled)
    
    def find_similar_patients(self, patient_data, n_neighbors=50):
        """Find similar patients in the database"""
        # Extract features
        patient_features = [patient_data[col] for col in self.feature_cols]
        patient_array = np.array(patient_features).reshape(1, -1)
        
        # Scale
        patient_scaled = self.scaler.transform(patient_array)
        
        # Find neighbors
        distances, indices = self.knn.kneighbors(patient_scaled)
        
        # Get similar patients
        similar_patients = self.df.iloc[indices[0]].copy()
        similar_patients['similarity_distance'] = distances[0]
        
        return similar_patients
    
    def get_cohort_statistics(self, similar_patients):
        """Calculate statistics for similar patient cohort"""
        stats = {
            'cohort_size': len(similar_patients),
            'avg_age': similar_patients['age'].mean(),
            'avg_amh': similar_patients['amh'].mean(),
            'avg_bmi': similar_patients['bmi'].mean(),
            'avg_eggs_retrieved': similar_patients['eggs_retrieved'].mean(),
            'success_rate': similar_patients['success'].mean(),
            'ohss_rate': similar_patients['ohss_risk'].mean(),
            'pcos_prevalence': similar_patients['pcos'].mean(),
            'protocol_distribution': similar_patients['protocol'].value_counts().to_dict(),
            'age_range': (similar_patients['age'].min(), similar_patients['age'].max()),
            'amh_range': (similar_patients['amh'].min(), similar_patients['amh'].max()),
        }
        
        return stats
    
    def get_cohort_summary(self, patient_data):
        """Get complete cohort analysis"""
        similar_patients = self.find_similar_patients(patient_data)
        stats = self.get_cohort_statistics(similar_patients)
        
        # Add interpretations
        summary = {
            'statistics': stats,
            'interpretation': self._interpret_cohort(stats),
            'similar_patients': similar_patients
        }
        
        return summary
    
    def _interpret_cohort(self, stats):
        """Generate interpretation of cohort statistics"""
        interpretation = []
        
        success_rate = stats['success_rate']
        if success_rate > 0.5:
            interpretation.append(f"✓ Favorable cohort: {success_rate:.1%} success rate")
        elif success_rate > 0.35:
            interpretation.append(f"○ Moderate cohort: {success_rate:.1%} success rate")
        else:
            interpretation.append(f"⚠ Challenging cohort: {success_rate:.1%} success rate")
        
        ohss_rate = stats['ohss_rate']
        if ohss_rate > 0.15:
            interpretation.append(f"⚠ High OHSS risk in cohort: {ohss_rate:.1%}")
        elif ohss_rate > 0.08:
            interpretation.append(f"○ Moderate OHSS risk in cohort: {ohss_rate:.1%}")
        else:
            interpretation.append(f"✓ Low OHSS risk in cohort: {ohss_rate:.1%}")
        
        avg_eggs = stats['avg_eggs_retrieved']
        interpretation.append(f"Average egg retrieval: {avg_eggs:.1f} eggs")
        
        # Protocol insights
        protocols = stats['protocol_distribution']
        most_common = max(protocols, key=protocols.get)
        interpretation.append(f"Most common protocol: {most_common} ({protocols[most_common]} patients)")
        
        return interpretation
    
    def compare_protocols_in_cohort(self, similar_patients):
        """Compare outcomes by protocol in similar cohort"""
        protocol_comparison = []
        
        for protocol in similar_patients['protocol'].unique():
            subset = similar_patients[similar_patients['protocol'] == protocol]
            
            if len(subset) >= 5:  # Minimum sample size
                protocol_comparison.append({
                    'protocol': protocol,
                    'n_patients': len(subset),
                    'success_rate': subset['success'].mean(),
                    'ohss_rate': subset['ohss_risk'].mean(),
                    'avg_eggs': subset['eggs_retrieved'].mean()
                })
        
        return pd.DataFrame(protocol_comparison).sort_values('success_rate', ascending=False)
    
    def get_percentile_rank(self, patient_data):
        """Get patient's percentile rank in key metrics"""
        percentiles = {}
        
        percentiles['amh'] = (self.df['amh'] < patient_data['amh']).mean() * 100
        percentiles['age'] = (self.df['age'] > patient_data['age']).mean() * 100  # Lower age is better
        percentiles['afc'] = (self.df['afc'] < patient_data['afc']).mean() * 100
        
        return percentiles
