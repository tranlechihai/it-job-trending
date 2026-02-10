import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from collections import Counter

def run_eda(input_path, output_dir):
    print(f"Loading cleaned data from {input_path}...")
    df = pd.read_csv(input_path)
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Set style
    sns.set_theme(style="whitegrid")
    
    # 1. Salary Distribution
    plt.figure(figsize=(10, 6))
    sns.histplot(data=df, x='Avg_Salary_Million', bins=20, kde=True, color='skyblue')
    plt.title('Distribution of IT Salaries in Vietnam (Million VND)')
    plt.xlabel('Salary (Million VND)')
    plt.ylabel('Count')
    plt.savefig(f"{output_dir}/1_salary_distribution.png")
    plt.close()
    print(f"Saved salary distribution plot to {output_dir}/1_salary_distribution.png")

    # 2. Salary by Experience Level
    plt.figure(figsize=(10, 6))
    # Define order
    order = ['Fresher', 'Junior', 'Senior', 'Lead', 'Manager']
    sns.boxplot(data=df, x='Experience', y='Avg_Salary_Million', order=order, palette='viridis')
    plt.title('Salary Ranges by Experience Level')
    plt.xlabel('Experience Level')
    plt.ylabel('Salary (Million VND)')
    plt.savefig(f"{output_dir}/2_salary_by_experience.png")
    plt.close()
    print(f"Saved salary by experience plot to {output_dir}/2_salary_by_experience.png")

    # 3. Top Skills Analysis
    all_skills = " ".join(df['Skills']).split(",")
    # Clean and split again properly because some inputs might be "Python, SQL"
    flat_skills = [s.strip() for sublist in df['Skills'].str.split(',') for s in sublist]
    
    skill_counts = Counter(flat_skills)
    top_15_skills = pd.DataFrame(skill_counts.most_common(15), columns=['Skill', 'Count'])
    
    plt.figure(figsize=(12, 8))
    sns.barplot(data=top_15_skills, x='Count', y='Skill', palette='magma')
    plt.title('Top 15 Most In-Demand IT Skills')
    plt.xlabel('Number of Job Postings')
    plt.savefig(f"{output_dir}/3_top_skills.png")
    plt.close()
    print(f"Saved top skills plot to {output_dir}/3_top_skills.png")
    
    # 4. Salary by Location
    plt.figure(figsize=(10, 6))
    sns.violinplot(data=df, x='Location', y='Avg_Salary_Million', palette='coolwarm')
    plt.title('Salary Distribution by Location')
    plt.xlabel('Location')
    plt.ylabel('Salary (Million VND)')
    plt.savefig(f"{output_dir}/4_salary_by_location.png")
    plt.close()
    print(f"Saved salary by location plot to {output_dir}/4_salary_by_location.png")

if __name__ == "__main__":
    input_csv = "data/vietnam_it_jobs_cleaned.csv"
    output_folder = "outputs/figures"
    run_eda(input_csv, output_folder)
