# Dapo

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)

**dapo** is a Python package designed to modify and analyze 2D tables. It provides tools for handling tabular data structures, enabling users to perform modifications and analysis efficiently.

## Table of Contents

- [Getting Started](#getting-started)
- [Usage](#usage)

## Getting Started

**Create DataKit**

```python
from dapo import DataKit

data_kit = DataKit() # Empty DataKit
data_kit_csv = DataKit.from_csv(src) # DataKit from csv file
data_kit_json = DataKit.from_json(src) # DataKit from json file
data_kit_toon = DataKit.from_toon(src) # DataKit from toon
```

**Write DataKit into File**

```python
data_kit.to_csv(src) # DataKit to csv file
data_kit.to_json(src) # DataKit to json file
data_kit.to_toon(src) # DataKit to toon file
```

## Usage

**Get Data**

```python
data_kit.get_column() # Get DataColumn
data_kit.get_row() # Get Row by index
data_kit.iter_rows() # Iterate rows
```

**Change Data**

```python
data_kit.add_row() # Add Row: Dict[str, Any] into DataKit
data_kit.add_column() # Add Column into Datakit
data_kit.update_row() # Update Row by index
data_kit.delete_row() # Delete Row by index
```

## License

[MIT](./LICENSE) License © 2025-PRESENT [Matvei Pisarev](https://github.com/mapi-developer)
