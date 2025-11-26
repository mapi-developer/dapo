import pandas as pd
import matplotlib.pyplot as plt
import io

# Load your data
# (Replace 'your_file.csv' with your actual file path if running locally)
# df = pd.read_csv('your_file.csv')

# For this example, I am using the snippet you provided:

df = pd.read_csv("src/datasets/job_descriptions.csv")


# Load your data (replace with pd.read_csv('your_file.csv'))
# df = pd.read_csv('your_file.csv')

# ... (Data Loading logic same as before) ...

# --- Preprocessing ---

# 1. Salary Cleaning (Same as before)
def process_salary(salary_str):
    if not isinstance(salary_str, str): return None
    clean_str = salary_str.replace('$', '').replace('K', '')
    try:
        min_sal, max_sal = clean_str.split('-')
        return ((float(min_sal) + float(max_sal)) / 2) * 1000
    except ValueError:
        return None

df['Avg_Salary'] = df['Salary Range'].apply(process_salary)

# 2. Experience Cleaning
# Converts "5 to 15 Years" into the average: 10.0
def process_experience(exp_str):
    if not isinstance(exp_str, str): return None
    try:
        # Assumes format "Min to Max Years"
        parts = exp_str.split(' ')
        min_exp = float(parts[0])
        max_exp = float(parts[2])
        return (min_exp + max_exp) / 2
    except (ValueError, IndexError):
        return None

df['Avg_Experience'] = df['Experience'].apply(process_experience)

# --- Visualization 1: Average Salary by Qualification ---
plt.figure(figsize=(8, 5))
# Group by Qualification and calculate mean salary
qual_salary = df.groupby('Qualifications')['Avg_Salary'].mean().sort_values()
qual_salary.plot(kind='bar', color='lightgreen', edgecolor='black')
plt.title('Average Salary by Qualification')
plt.ylabel('Average Salary ($)')
plt.xlabel('Qualification')
plt.xticks(rotation=0)
plt.show()

# --- Visualization 2: Job Count by Country ---
plt.figure(figsize=(8, 5))
country_counts = df['Country'].value_counts()
country_counts.plot(kind='bar', color='coral', edgecolor='black')
plt.title('Job Posting Count by Country')
plt.ylabel('Number of Jobs')
plt.xlabel('Country')
plt.xticks(rotation=0)
plt.show()

# --- Visualization 3: Salary vs Experience ---
plt.figure(figsize=(8, 5))
plt.scatter(df['Avg_Experience'], df['Avg_Salary'], color='purple', s=100)
plt.title('Average Salary vs Average Experience Required')
plt.xlabel('Average Experience (Years)')
plt.ylabel('Average Salary ($)')
plt.grid(True, linestyle='--', alpha=0.5)

# Label the points with Job Titles
for i, txt in enumerate(df['Job Title']):
    # Safety check to ensure we don't index out of bounds if data has NaNs
    if pd.notna(df['Avg_Experience'].iloc[i]) and pd.notna(df['Avg_Salary'].iloc[i]):
         plt.annotate(txt, (df['Avg_Experience'].iloc[i], df['Avg_Salary'].iloc[i]),
                 xytext=(5, 5), textcoords='offset points')
plt.show()