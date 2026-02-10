import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_it_jobs_data(n_samples=2000):
    # Seed for reproducibility
    np.random.seed(42)
    random.seed(42)

    # 1. Locations with weights (HCM & Hanoi are tech hubs)
    locations = ['Ho Chi Minh', 'Ha Noi', 'Da Nang', 'Remote', 'Can Tho']
    loc_weights = [0.45, 0.40, 0.10, 0.04, 0.01]

    # 2. Experience Levels
    experiences = ['Fresher', 'Junior', 'Senior', 'Lead', 'Manager']
    exp_weights = [0.15, 0.35, 0.35, 0.10, 0.05]
    
    # Base salary ranges (in Million VND) per level
    salary_map = {
        'Fresher': (8, 15),
        'Junior': (15, 25),
        'Senior': (25, 50),
        'Lead': (40, 70),
        'Manager': (60, 100)
    }

    # 3. Job Titles & Associated Skills
    titles_skills = {
        'Backend Developer': ['Python, Django', 'Java, Spring Boot', 'Go, Microservices', 'Node.js, Express'],
        'Frontend Developer': ['ReactJS, TypeScript', 'VueJS, Nuxt', 'Angular, RxJS', 'HTML, CSS, JS'],
        'Fullstack Developer': ['React, Node.js, Mongo', 'Java, Angular, SQL', 'Python, VueJS, Docker'],
        'Data Scientist': ['Python, Pandas, Scikit-learn', 'SQL, Tableau, Python', 'Python, PyTorch, AWS'],
        'AI/ML Engineer': ['Python, TensorFlow, CV', 'Python, NLP, HuggingFace', 'C++, CUDA, Computer Vision'],
        'DevOps Engineer': ['AWS, Docker, K8s', 'Azure, CI/CD, Terraform', 'Linux, Jenkins, Ansible'],
        'Mobile Developer': ['Flutter, Dart', 'React Native', 'Swift, iOS', 'Kotlin, Android'],
        'Tester/QA': ['Selenium, Python', 'Manual Testing, SQL', 'Java, Appium', 'Automation, Cypress']
    }
    
    job_titles = list(titles_skills.keys())

    data = []

    for _ in range(n_samples):
        # Pick Experience first to determine Salary
        exp = random.choices(experiences, weights=exp_weights, k=1)[0]
        
        # Pick Location
        loc = random.choices(locations, weights=loc_weights, k=1)[0]
        
        # Pick Job Title
        title = random.choice(job_titles)
        
        # Pick Skills (Random subset from the title's possibilities)
        possible_skills_groups = titles_skills[title]
        base_stack = random.choice(possible_skills_groups)
        
        # Determine Salary (Add some noise/variation)
        min_base, max_base = salary_map[exp]
        # Adjust salary based on location (HCM/Hanoi slightly higher)
        loc_mult = 1.1 if loc in ['Ho Chi Minh', 'Ha Noi'] else 0.9
        if loc == 'Remote': loc_mult = 1.05
        
        low_sal = int(min_base * loc_mult + random.uniform(-2, 2))
        high_sal = int(max_base * loc_mult + random.uniform(0, 5))
        
        # Ensure logical range
        if low_sal < 5: low_sal = 5
        if high_sal <= low_sal: high_sal = low_sal + 5
        
        salary_str = f"{low_sal}-{high_sal} millions"

        # Posted Date
        start_date = datetime(2024, 1, 1)
        end_date = datetime(2025, 12, 31)
        posted_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))

        data.append({
            'Job Title': title,
            'Company': f"Tech Company {random.randint(1, 500)}", # Anonymized
            'Location': loc,
            'Salary': salary_str,
            'Skills': base_stack,
            'Experience': exp,
            'Posted Date': posted_date.strftime("%Y-%m-%d")
        })

    df = pd.DataFrame(data)
    # Introduce some missing values to make cleaning step necessary
    for col in ['Salary', 'Location']:
        df.loc[df.sample(frac=0.05).index, col] = np.nan
        
    return df

if __name__ == "__main__":
    print("Generating synthetic IT Job Market data...")
    df = generate_it_jobs_data(2000)
    output_path = "data/vietnam_it_jobs.csv"
    
    # Ensure directory exists
    import os
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    df.to_csv(output_path, index=False)
    print(f"Dataset generated at {output_path}")
    print(df.head())
    print(df.info())
