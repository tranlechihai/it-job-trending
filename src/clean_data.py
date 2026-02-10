import pandas as pd
import numpy as np
import re

def clean_data(input_path, output_path):
    print(f"Loading data from {input_path}...")
    df = pd.read_csv(input_path)
    
    # 1. Handle Missing Values
    print("Handling missing values...")
    # Drop rows without Salary or Location (Critical info)
    initial_len = len(df)
    df.dropna(subset=['Salary', 'Location'], inplace=True)
    print(f"Dropped {initial_len - len(df)} rows with missing Salary/Location.")
    
    # Fill missing Skills with 'Unspecified'
    df['Skills'] = df['Skills'].fillna('Unspecified')

    # 2. Parse Salary Column
    # Expected format: "15-25 millions" -> Extract numbers
    print("Parsing salary...")
    
    def extract_avg_salary(salary_str):
        if pd.isna(salary_str): return np.nan
        # Regex to find numbers
        matches = re.findall(r'\d+', str(salary_str))
        if len(matches) >= 2:
            low = float(matches[0])
            high = float(matches[1])
            return (low + high) / 2
        elif len(matches) == 1:
            return float(matches[0])
        return np.nan

    df['Avg_Salary_Million'] = df['Salary'].apply(extract_avg_salary)
    
    # Drop rows where salary parsing failed
    df.dropna(subset=['Avg_Salary_Million'], inplace=True)

    # 3. Standardize Text
    print("Standardizing text...")
    df['Skills'] = df['Skills'].str.lower().str.strip()
    df['Job Title'] = df['Job Title'].str.strip()

    # 4. Encoding Experience (Ordinal features)
    # Define order for logical sorting later
    exp_order = {'Fresher': 1, 'Junior': 2, 'Senior': 3, 'Lead': 4, 'Manager': 5}
    df['Exp_Level'] = df['Experience'].map(exp_order)

    # Save cleaned data
    print(f"Saving cleaned data to {output_path}...")
    df.to_csv(output_path, index=False)
    
    print("\nData Sample:")
    print(df[['Job Title', 'Location', 'Experience', 'Avg_Salary_Million']].head())
    print("\nData Info:")
    print(df.info())

if __name__ == "__main__":
    input_csv = "data/vietnam_it_jobs.csv"
    output_csv = "data/vietnam_it_jobs_cleaned.csv"
    clean_data(input_csv, output_csv)
