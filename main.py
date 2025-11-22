from dapo.core.datakit import DataKit
import test_data as td

datasets_src = "src/datasets"

dk_1 = DataKit.from_toon(f"{datasets_src}/jobs.toon")
# dk_1 = DataKit()
# dk_1.add_column("latitude", [10, 5, 2, 46, 7, 8, 3, 6, 10, 10])
# dk_1.add_column("test", [10, 5, 2, 46, 7, 8, 3, 6, 10, 10])

# dk_1 = dk_1.select(["Work Type", "Job Title", "Salary Range"]).filter(lambda x: x["Work Type"] == "Full-Time").sort("Job Title").unique("Job Title")

# dk_1.to_csv(f"{datasets_src}/test.csv")
