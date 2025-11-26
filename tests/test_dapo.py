import unittest
from dapo import DataKit
from dapo.core.data_column import DataColumn

class TestDataKitCore(unittest.TestCase):
    def setUp(self):
        """Set up a basic DataKit instance before each test."""
        self.initial_data = {
            "id": [1, 2, 3, 4],
            "category": ["A", "B", "A", "C"],
            "value": [10.0, 20.0, 30.0, 40.0]
        }
        self.dk = DataKit.from_columns(self.initial_data)

    def test_initialization(self):
        """Test different ways to initialize DataKit."""
        # From columns
        self.assertEqual(len(self.dk), 4)
        self.assertEqual(self.dk.n_cols, 3)
        self.assertEqual(self.dk.columns, ["id", "category", "value"])

        # From rows
        rows = [
            ["col1", "col2"],
            [1, 2],
            [3, 4]
        ]
        dk_rows = DataKit.from_rows(rows)
        self.assertEqual(len(dk_rows), 2)
        self.assertEqual(dk_rows.get_column("col1"), [1, 3])

        # Empty
        dk_empty = DataKit()
        self.assertEqual(len(dk_empty), 0)

    def test_accessors(self):
        """Test accessing rows and columns."""
        # Get Column
        col = self.dk.get_column("category")
        self.assertIsInstance(col, DataColumn)
        self.assertEqual(col, ["A", "B", "A", "C"])

        # Get Row
        row = self.dk.get_row(1)
        self.assertEqual(row["id"], 2)
        self.assertEqual(row["value"], 20.0)

        # Iter rows
        rows = list(self.dk.iter_rows())
        self.assertEqual(len(rows), 4)

    def test_manipulation(self):
        """Test adding, updating, and deleting data."""
        # Add Row
        new_row = {"id": 5, "category": "B", "value": 50.0}
        self.dk.add_row(new_row)
        self.assertEqual(len(self.dk), 5)
        self.assertEqual(self.dk.get_column("id")[-1], 5)

        # Update Row
        self.dk.update_row(0, {"category": "Z", "value": 99.0})
        updated_row = self.dk.get_row(0)
        self.assertEqual(updated_row["category"], "Z")
        self.assertEqual(updated_row["value"], 99.0)
        # Ensure other fields remain untouched
        self.assertEqual(updated_row["id"], 1)

        # Delete Row
        self.dk.delete_row(0)
        self.assertEqual(len(self.dk), 4)
        self.assertEqual(self.dk.get_column("id")[0], 2) # Old row 1 is now row 0

        # Rename Column
        self.dk.rename_column("value", "amount")
        self.assertIn("amount", self.dk.columns)
        self.assertNotIn("value", self.dk.columns)

    def test_vector_operations(self):
        """Test DataColumn arithmetic."""
        vals = self.dk.get_column("value")
        
        # Scalar operations
        added = vals.add(5)
        self.assertEqual(added, [15.0, 25.0, 35.0, 45.0])
        
        multiplied = vals.mul(2)
        self.assertEqual(multiplied, [20.0, 40.0, 60.0, 80.0])

        # Column vector operations
        other = [1.0, 1.0, 1.0, 1.0]
        subtracted = vals.sub(other)
        self.assertEqual(subtracted, [9.0, 19.0, 29.0, 39.0])

    def test_statistics(self):
        """Test statistical methods."""
        vals = self.dk.get_column("value") # [10, 20, 30, 40]
        
        self.assertEqual(vals.sum(), 100.0)
        self.assertEqual(vals.mean(), 25.0)
        self.assertEqual(vals.max(), 40.0)
        self.assertEqual(vals.min(), 10.0)
        # Median of even set [10, 20, 30, 40] -> (20+30)/2 = 25
        self.assertEqual(vals.median(), 25.0)

    def test_filtering_and_querying(self):
        """Test filter, select, and unique."""
        # Filter
        filtered = self.dk.filter(lambda r: r["category"] == "A")
        self.assertEqual(len(filtered), 2)
        self.assertTrue(all(x == "A" for x in filtered.get_column("category")))

        # Select
        selected = self.dk.select(["id"])
        self.assertEqual(selected.columns, ["id"])
        self.assertEqual(selected.n_cols, 1)

        # Unique
        unique_cats = self.dk.unique("category")
        self.assertEqual(len(unique_cats), 3) # A, B, C

    def test_group_by(self):
        """Test aggregation functionality."""
        # Group by 'category' (A: 10+30=40, B: 20, C: 40)
        grouped = self.dk.group_by("category", {"value": "sum", "id": "count"})
        
        # Since dicts are unordered, we convert to list to check existence
        cats = grouped.get_column("category")
        sums = grouped.get_column("sum_value")
        counts = grouped.get_column("count_id")

        # Check for Category A
        idx_a = cats.index("A")
        self.assertEqual(sums[idx_a], 40.0)
        self.assertEqual(counts[idx_a], 2)

    def test_sorting(self):
        """Test sorting functionality."""
        # Sort desc by value
        self.dk.sort("value", reverse=True)
        self.assertEqual(self.dk.get_column("value"), [40.0, 30.0, 20.0, 10.0])
        self.assertEqual(self.dk.get_column("id"), [4, 3, 2, 1]) # IDs should follow

if __name__ == "__main__":
    unittest.main()