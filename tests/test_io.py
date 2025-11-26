import unittest
import tempfile
import os
from dapo import DataKit

class TestDataKitIO(unittest.TestCase):
    def setUp(self):
        self.data = DataKit.from_columns({"col1": [1, 2], "col2": ["x", "y"]})

    def test_csv_io(self):
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.csv') as tmp:
            path = tmp.name
        
        try:
            self.data.to_csv(path)
            loaded = DataKit.from_csv(path)
            self.assertEqual(len(loaded), 2)
            self.assertEqual(loaded.columns, ["col1", "col2"])
            self.assertEqual(loaded.get_column("col1"), [1, 2])
            self.assertEqual(loaded.get_column("col2"), ["x", "y"])
        finally:
            os.remove(path)

    def test_json_io(self):
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.json') as tmp:
            path = tmp.name
        
        try:
            self.data.to_json(path)
            loaded = DataKit.from_json(path)
            self.assertEqual(len(loaded), 2)
            self.assertEqual(loaded.columns, ["col1", "col2"])
            self.assertEqual(loaded.get_column("col1"), [1, 2])
            self.assertEqual(loaded.get_column("col2"), ["x", "y"])
        finally:
            os.remove(path)

    def test_toon_io(self):
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.toon') as tmp:
            path = tmp.name
        
        try:
            self.data.to_toon(path)
            loaded = DataKit.from_toon(path)
            self.assertEqual(len(loaded), 2)
            self.assertEqual(loaded.columns, ["col1", "col2"])
            self.assertEqual(loaded.get_column("col1"), [1, 2])
            self.assertEqual(loaded.get_column("col2"), ["x", "y"])
        finally:
            os.remove(path)

if __name__ == "__main__":
    unittest.main()