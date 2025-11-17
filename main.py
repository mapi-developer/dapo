from .dapo.core.datakit import DataKit
import test_data as td

dk = DataKit.from_rows(td.rows)
dk_2 = DataKit()

print(dk_2)

dk_2.add_row(td.single_row)

for row in dk_2.iter_rows():
    print(row)
