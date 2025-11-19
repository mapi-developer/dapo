from dapo.core.datakit import DataKit
import test_data as td

dk_1 = DataKit.from_csv("src/datasets/output.csv")
dk_1.add_row(td.single_row)
dk_1.to_csv("src/datasets/output.csv")

# dk_2 = DataKit()
# dk_2.add_row(td.single_row)
# print(dk_2)