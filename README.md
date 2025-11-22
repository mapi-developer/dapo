# Dapo

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)

**dapo** is a Python package designed to modify and analyze 2D tables. It provides tools for handling tabular data structures, enabling users to perform modifications and analysis efficiently.

## Table of Contents

- [Getting Started](#gettingstarted)

## Getting Started

**Create DataKit**

'''python
from dapo import DataKit

data_kit = DataKit() # Empty DataKit
data_kit_csv = DataKit.from_csv(src) # DataKit from csv file
data_kit_json = DataKit.from_json(src) # DataKit from json file
'''

**Write DataKit into File**

'''python
from dapo import DataKit

data_kit = DataKit()
data_kit.to_csv(src) # DataKit to csv file
data_kit.to_json(src) # DataKit to json file
'''

## License

[MIT](./LICENSE) License © 2025-PRESENT [Matvei Pisarev](https://github.com/mapi-developer)
