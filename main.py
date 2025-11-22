from dapo.core.datakit import DataKit
import test_data as td

datasets_src = "src/datasets"

dk_1 = DataKit.from_toon(f"{datasets_src}/data.toon")
# dk_1 = DataKit.from_csv(f"{datasets_src}/job_descriptions_small.csv")
# dk_1 = DataKit.from_columns(td.columns)

dk_1.to_json(f"{datasets_src}/jobs.json")