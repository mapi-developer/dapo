import matplotlib.pyplot as plt
from dapo import DataKit

def main():
    print("Loading data...")
    csv_path = "examples/datasets/job_descriptions_small.csv"
    dk = DataKit.from_csv(csv_path)

    def parse_salary(salary_str):
        if not isinstance(salary_str, str): return 0.0
        clean = salary_str.replace('$', '').replace('K', '').strip()
        try:
            if '-' in clean:
                low, high = map(float, clean.split('-'))
                return (low + high) / 2 * 1000
            return float(clean) * 1000
        except ValueError:
            return 0.0

    salary_col = dk.get_column("Salary Range")
    avg_salaries = [parse_salary(s) for s in salary_col]
    dk.add_column("AvgSalary", avg_salaries)

    dk = dk.filter(lambda row: row["AvgSalary"] > 0)

    output_file = "examples/example_out/output.csv"
    out_dk = dk.select(["Job Id", "Salary Range", "AvgSalary", "Country", "Job Title"]).filter(lambda row: row["AvgSalary"] > 80000)
    out_dk.to_csv(output_file)

    def get_10k_bin(salary):
        lower = int(salary / 10000) * 10
        upper = lower + 10
        return f"${lower}k-${upper}k"

    salary_bins = [get_10k_bin(s) for s in dk.get_column("AvgSalary")]
    dk.add_column("SalaryBin", salary_bins)

    dk_grouped = dk.group_by("SalaryBin", {"SalaryBin": "count"})
    dk_grouped_qualifications = dk.group_by("Qualifications", {"Qualifications": "count"})
    
    dk_grouped.sort("SalaryBin")
    dk_grouped_qualifications.sort("count_Qualifications", reverse=True)

    labels = dk_grouped.get_column("SalaryBin")
    counts = dk_grouped.get_column("count_SalaryBin")

    qualifications = dk_grouped_qualifications.get_column("Qualifications")
    counts_qual = dk_grouped_qualifications.get_column("count_Qualifications")

    plt.figure(figsize=(10, 8))
    plt.pie(counts, 
            labels=labels, 
            autopct='%1.1f%%', 
            startangle=140,
            wedgeprops={'edgecolor': 'white'}) # Add white lines between slices for clarity

    plt.title("Job Distribution by Salary (10k Intervals)")

    print("Displaying pie chart...")
    plt.show()

    plt.figure(figsize=(10, 6))
    plt.bar(qualifications, counts_qual, color='lightgreen', edgecolor='black')
    plt.title("Job Count by Qualification", fontsize=16)
    plt.xlabel("Qualification", fontsize=12)
    plt.ylabel("Number of Jobs", fontsize=12)

    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    print("Displaying bar chart...")
    plt.show()

if __name__ == "__main__":
    main()