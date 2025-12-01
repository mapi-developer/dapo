# Dapo

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)

**Dapo** is a lightweight Python package designed for efficient modification, analysis, and transformation of 2D tabular data. It mimics the ease of use of tools like Pandas but keeps things simple with standard Python lists and minimal dependencies.

## Table of Contents

- [Getting Started](#getting-started)
- [Usage](#usage)
- [Documentation](#documentation)

## Getting Started

**Installation**

You can install `Dapo` package via pip

```bash
pip install dapo
```

**Create DataKit**

```python
from dapo import DataKit

data_kit = DataKit() # Empty DataKit
data_kit_csv = DataKit.from_csv(src) # DataKit from csv file
data_kit_json = DataKit.from_json(src) # DataKit from json file
```

**Write DataKit into File**

```python
data_kit.to_csv(src) # DataKit to csv file
data_kit.to_json(src) # DataKit to json file
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
data_kit.update_row() # Update Row by index
data_kit.delete_row() # Delete Row by index
```

## Documentation
You can find the comprehensive documentation describing all methods and features [here](https://github.com/mapi-developer/dapo/blob/main/docs/Documentation.md).

## License
[MIT](./LICENSE) License © 2025-PRESENT [Matvei Pisarev](https://github.com/mapi-developer)
