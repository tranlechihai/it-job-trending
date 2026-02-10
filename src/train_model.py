import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder, StandardScaler, OrdinalEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, r2_score
import os

def train_model():
    input_path = "data/vietnam_it_jobs_cleaned.csv"
    model_path = "models/salary_model.pkl"
    
    # Check if data exists
    if not os.path.exists(input_path):
        print("Data file not found!")
        return

    print("Loading data...")
    df = pd.read_csv(input_path)
    
    # Feature Engineering
    # We will use Experience (Ordinal), Job Title (Nominal), Location (Nominal)
    # Target: Avg_Salary_Million
    
    features = ['Experience', 'Job Title', 'Location']
    target = 'Avg_Salary_Million'
    
    X = df[features]
    y = df[target]
    
    # Define preprocessing
    # Experience Level needs specific ordering
    exp_order = [['Fresher', 'Junior', 'Senior', 'Lead', 'Manager']]
    
    categorical_features = ['Job Title', 'Location']
    ordinal_features = ['Experience']
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('ord', OrdinalEncoder(categories=exp_order), ordinal_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ])
    
    # Create Pipeline
    model_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
    ])
    
    # Split Data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training Random Forest model...")
    model_pipeline.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model_pipeline.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"Model Performance:\nMAE: {mae:.2f} Million VND\nR2 Score: {r2:.2f}")
    
    # Save Model
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(model_pipeline, model_path)
    print(f"Model saved to {model_path}")

if __name__ == "__main__":
    train_model()
