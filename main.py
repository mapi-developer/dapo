from dapo.core.datakit import DataKit
import test_data as td

dk_1 = DataKit.from_columns(td.columns)
dk_2 = DataKit()

dk_3 = DataKit.from_csv("src/datasets/job_descriptions.csv")  # delimiter=None → auto-detect

print(dk_3.columns)

