# Dapo Documentation

**Dapo** is a lightweight Python package designed for efficient modification, analysis, and transformation of 2D tabular data. It mimics the ease of use of tools like Pandas but keeps things simple with standard Python lists and minimal dependencies.

## Table of Contents

- [Core Classes](#core-classes)
- [Getting Started](#getting-started)
- [Input / Output](#input--output)
  - [CSV](#csv)
  - [JSON](#json)
  - [TOON](#toon)
- [Data Inspection](#data-inspection)
- [Data Access](#data-access)
- [Data Manipulation](#data-manipulation)
- [Vector & Math Operations](#vector--math-operations)
- [Querying & Filtering](#querying--filtering)
- [Analysis & Aggregation](#analysis--aggregation)
- [Sorting](#sorting)

---

## Core Classes

### 1. DataKit

The main entry point for the library. `DataKit` stores data in a column-oriented format (list of lists) but provides row-oriented access methods for convenience.

* **Structure**: Stores data as a list of `DataColumn` objects.
* **Consistency**: Ensures all columns have the same length (row count).

### 2. DataColumn

A subclass of the standard Python `List`. It represents a single column of data and includes helper methods for vector math (add, sub, mul) and statistics.

---

## Getting Started

**Installation**

You can install `Dapo` package via pip

```bash
pip install dapo
```

```python
from dapo import DataKit

# Initialize an empty DataKit
dk = DataKit()

# Or initialize from a dictionary of columns
data = {
    "id": [1, 2, 3],
    "name": ["Alice", "Bob", "Charlie"],
    "sales": [150.0, 200.5, 120.0]
}
dk = DataKit.from_columns(data)
```

## Input / Output

Dapo supports reading and writing to CSV, JSON, and TOON formats.

### CSV

```python
# specific delimiter is optional (default is auto-sniffed or ',')
dk = DataKit.from_csv("data.csv", delimiter=",", encoding="utf-8")

# Write to CSV
dk.to_csv("output.csv", delimiter=",")
```

### JSON

Supports list-of-objects JSON structure.

```python
dk = DataKit.from_json("data.json")

# Write to JSON (indent controls pretty-printing)
dk.to_json("output.json", indent=2)
```

### TOON

Supports the Token-Oriented Object Notation (Tabular Array format) for LLM efficiency.

```python
dk = DataKit.from_toon("data.toon")

dk.to_toon("output.toon")
```

## Data Inspection

Quickly preview your data.

Head / Tail

```python
# Get the first 5 rows
preview = dk.head(5)

# Get the last 3 rows
recent = dk.tail(3)
```

## Data Access

### Get Column
Returns a DataColumn (list-like object).

```python
prices = dk.get_column("price")
```

### Get Row
Returns a dictionary representing the row at a specific index.

```python
row_data = dk.get_row(0)
# Output: {'id': 1, 'name': 'Alice', ...}
```

### Iterate Rows
Loop through the dataset efficiently.

```python
for row in dk.iter_rows():
    print(row["name"])
```

## Data Manipulation
Dapo allows in-place modification of the dataset structure.

### Add, Update, Delete

```python
# Add a new row
dk.add_row({"id": 4, "name": "Diana", "sales": 300.0})

# Update specific fields of a row at index 1
dk.update_row(1, {"name": "Robert"})

# Delete row at index 2
deleted_data = dk.delete_row(2)
```

### Rename Column

```python
# Rename 'sales' to 'revenue'
dk.rename_column("sales", "revenue")
```

## Vector & Math Operations
Perform element-wise math on DataColumn objects without loops.

### Arithmetic

```python
price = dk.get_column("price")
qty = dk.get_column("quantity")

# Column-to-Column
revenue = price.mul(qty)

# Column-to-Scalar
discounted = price.sub(5.0)  # Subtract 5 from all prices
taxed = price.mul(1.2)       # Add 20% tax

# Add new calculated column back to DataKit
dk.add_column("total", revenue)
```

## Statistics
Available methods on numeric columns:

* .sum()
* .mean()
* .median()
* .mode()
* .min() / .max()
* .std()

```python
avg_price = dk.get_column("price").mean()
total_sales = dk.get_column("sales").sum()
```

## Querying & Filtering
Extract specific subsets of your data.

### Filter
Returns a new DataKit with rows that match a condition.

```python
# Get high-value transactions
high_value = dk.filter(lambda r: r["price"] > 100)
```

### Select
Returns a new DataKit with only the specified columns.

```python
# Create a report with specific columns
report = dk.select(["product_name", "revenue"])
```

### Unique
Returns a new DataKit containing unique rows based on a specific column (removes duplicates).

```python
# Get unique list of countries
unique_countries = dk.unique("country")
```

### Apply
Applies a function to every value in a column (in-place).

```python
# Convert date string to datetime object
from datetime import datetime
dk.apply(lambda d: datetime.strptime(d, "%Y-%m-%d"), "date")
```

## Analysis & Aggregation

### Group By
Groups data by a category and calculates statistics for other columns. Supported aggregations: "sum", "mean", "count", "min", "max".

```python
# Calculate average price and total sales count per category
# Automatically creates columns like 'mean_price' and 'count_id'
report = dk.group_by(
    column="category", 
    agg={
        "price": "mean",
        "id": "count"
    }
)
```

## Sorting
Sort the entire dataset in-place by one or more columns.

```python
# Simple Sort
dk.sort("price")

# Reverse Sort
dk.sort("date", reverse=True)

# Multi-Column Sort
# Sort by Country (A-Z), then by Sales (Highest first)
dk.sort(columns=["country", "sales"], reverse=[False, True])
```
