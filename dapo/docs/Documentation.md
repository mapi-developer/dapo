Classes:
    1. DataKit
    2. DataColumn

DataKit:

DataKit is a dataclass to store 2D table. Column data storage can give much more space to make faster calculation and analytic under data, easier access to special columns.

_data: DataColumn[Any] (table stored as columns of the same datatype)
_columns: List[str] (represent columns titles)
_n_rows: int (amount of rows of the table)

Properties:
.n_cols
.columns
.n_rows

Methods:
.__len__()
.__repr__()
.from_columns(columns: Dict[str, Sequence[Any]])
.from_rows(rows: Sequence[Sequence[Any]])
.from_csv(path: str, delimiter: Optional[str], encoding: str)
.from_json(path: str, encoding: str)
.from_toon(path: str, encoding: str)
.to_csv(path: str, delimiter: str, encoding: str, newline: str)
.to_json(path: str, encoding: str, indent: int)
.to_toon(path: str, encoding: str, indent: int)
.get_column(name: str)
.get_row(index: int)
.iter_rows()
.add_row(values: Dict[str, Any])
.add_column(header: str, values: List[Any])
.update_row(index: int, values: Dict[str, Any])
.delete_row(index: int)
.sort(column: str, reverse: bool = False)

DataColumn:

DataColumn is a part of Datakit data. Represent table column of values.

Methods:
.sort(reverse: bool)
.sort_order(reverse: bool)
.sum(decimal_places: int, to_int: bool)
.mean(decimal_places: int, to_int: bool)
.median(decimal_places: int, to_int: bool)
.min()
.max()
.std(decimal_places: int, to_int: bool)