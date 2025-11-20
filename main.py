from dapo.core.datakit import DataKit
import test_data as td

datasets_src = "src/datasets"

dk_1 = DataKit.from_json(f"{datasets_src}/jobs.json")
# dk_1 = DataKit()

col = dk_1.get_column("location").sort(reverse=True)

# dk_1.to_csv(f"{datasets_src}/test.csv")

# dk_2 = DataKit()
# dk_2.add_row(td.single_row)
# print(dk_2)