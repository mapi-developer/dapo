from dapo import DataKit
import example_data as td

datasets_src = "src/datasets"

dk_1 = DataKit.from_toon(f"{datasets_src}/jobs.toon")
# dk_1 = DataKit()
# dk_1.add_column("latitude", [10, 5, 2, 46, 7, 8, 3, 6, 10, 10])
# dk_1.add_column("test", [10, 5, 2, 46, 7, 8, 3, 6, 10, 10])

dk_1 = dk_1.select(["Country", "Job Title"]).group_by("Country", {"Country": "count"}).sort("Country").filter(lambda x: x["Country"] < "G" and x["count_Country"] > 6)

dk_1.to_csv(f"{datasets_src}/test.csv")
