import pandas as pd
import numpy as np

def generate_synthetic_data(n_samples=1000):
    np.random.seed(42)
    age = np.random.randint(20, 42, n_samples)
    lactation_months = np.random.randint(0, 12, n_samples)
    bed_rest_days = np.random.randint(1, 30, n_samples)
    calcium_intake_mg = np.random.randint(400, 1500, n_samples)
    vit_d_ngml = np.random.uniform(10, 50, n_samples)
    
    risk_score = (
        (42 - age) * 0.1 + 
        lactation_months * 1.5 + 
        bed_rest_days * 0.8 - 
        calcium_intake_mg * 0.005 - 
        vit_d_ngml * 0.3
    )
    high_risk = (risk_score > np.median(risk_score)).astype(int)
    
    df = pd.DataFrame({
        'age': age,
        'lactation_months': lactation_months,
        'bed_rest_days': bed_rest_days,
        'calcium_intake_mg': calcium_intake_mg,
        'vit_d_ngml': vit_d_ngml,
        'high_risk': high_risk
    })
    return df

if __name__ == "__main__":
    df = generate_synthetic_data()
    df.to_csv("bone_health_data.csv", index=False)
    print("Dataset generated successfully!")