from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Sequence, Iterator, Callable

from dapo.core.data_column import DataColumn

from dapo.core.csv_utils import read_csv, write_csv
from dapo.core.json_utils import read_json, write_json
from dapo.core.toon_utils import read_toon, write_toon

@dataclass
class DataKit:
    _data: List[DataColumn[Any]] = field(default_factory=list)
    _columns: List[str] = field(default_factory=list)
    _n_rows: int = 0

    # HELPERS
    def _validate_length(self, other: DataColumn[Any]) -> None:
        if self._n_rows > 0 and self._n_rows != len(other):
            raise ValueError(f"Column length mismatch: {len(self)} != {len(other)}")

    def _check_row_index(self, index: int) -> None:
        if index < 0 or index >= self._n_rows:
            raise IndexError("Row index out of range")

    def _col_pos(self, name: str) -> int:
        try:
            return self._columns.index(name)
        except ValueError:
            raise KeyError(f"Unknown column '{name}'") from None

    # CONSTRUCTORS
    @classmethod
    def from_columns(cls, columns: Dict[str, Sequence[Any]]) -> "DataKit":
        if not columns:
            return cls()
        
        lengths = {len(col) for col in columns.values()}
        if len(lengths) > 1:
            raise ValueError("All columns must have the same length")
        
        n_rows = lengths.pop()
        column_order = list(columns.keys())
        cols_data = [list(columns[name]) for name in column_order]

        return cls(_data=cols_data, _columns=column_order, _n_rows=n_rows)

    @classmethod
    def from_rows(cls, rows: Sequence[Sequence[Any]]) -> "DataKit":
        if not rows:
            return cls()
        
        header = [str(c) for c in rows[0]]
        n_cols = len(header)
        cols_data: List[DataColumn[Any]] = [[] for _ in range(n_cols)]
        n_rows = 0

        for r in rows[1:]:
            if len(r) != n_cols:
                raise ValueError(f"Row length {len(r)} != header length {n_cols}: {r}")
            for i, value in enumerate(r):
                cols_data[i].append(value)
            n_rows += 1

        return cls(_columns=header, _data=cols_data, _n_rows=n_rows)
    
    @classmethod
    def from_csv(
        cls,
        path: str,
        delimiter: Optional[str] = None,
        encoding: str = "utf-8",
    ) -> "DataKit":
        data: List[DataColumn[Any]] = []
        columns: List[str] = []
        first = True

        for row_dict in read_csv(path, delimiter=delimiter, has_header=True, encoding=encoding):
            if first:
                columns = list(row_dict.keys())
                first = False
                data.append(columns)
            data.append([row_dict[c] for c in columns])

        return cls.from_rows(data)
    
    @classmethod
    def from_json(
        cls,
        path: str,
        encoding: str = "utf-8",
    ) -> "DataKit":
        records = read_json(path, encoding=encoding)

        if not records:
            return cls(_data=[], _columns=[])

        columns: List[str] = list(records[0].keys())

        data: List[DataColumn[Any]] = [[] for _ in columns]
        n_rows = 0

        for rec in records:
            for col_idx, col_name in enumerate(columns):
                data[col_idx].append(rec.get(col_name))
            n_rows += 1

        return cls(_data=data, _columns=columns, _n_rows=n_rows)

    @classmethod
    def from_toon(
        cls,
        path: str,
        encoding: str = "utf-8",
    ) -> "DataKit":
        records = read_toon(path, encoding=encoding)

        if not records:
            return cls(_data=[], _columns=[])

        columns: List[str] = list(records[0].keys())

        data: List[DataColumn[Any]] = [[] for _ in columns]
        n_rows = 0

        for rec in records:
            for col_idx, col_name in enumerate(columns):
                data[col_idx].append(rec.get(col_name))
            n_rows += 1

        return cls(_data=data, _columns=columns, _n_rows=n_rows)

    @property
    def columns(self) -> List[str]:
        return self._columns
    
    @property
    def n_cols(self) -> int:
        return len(self._columns)
    
    @property
    def n_rows(self) -> int:
        return self._n_rows
    
    def __len__(self) -> int:
        return self._n_rows

    def __repr__(self) -> str:
        return f"DataKit(n_rows={self._n_rows}, n_cols={self.n_cols}, columns={self._columns})"
    
    # ACCESS
    def get_column(self, name: str) -> DataColumn[Any]:
        idx = self._col_pos(name)
        return DataColumn(self._data[idx])
    
    def get_row(self, index: int) -> Dict[str, Any]:
        self._check_row_index(index)
        return {name: self._data[i][index] for i, name in enumerate(self._columns)}
    
    def iter_rows(self, max_amount: int | None = None) -> "Iterator[Dict[str, Any]]":
        rows_range = max_amount if max_amount != None and max_amount < self._n_rows else self._n_rows
        for i in range(rows_range):
            yield self.get_row(i)

    def add_row(self, values: Dict[str, Any]) -> Dict[str, Any]:
        if not self._columns:
            self._columns = list(values.keys())
            self._data = [[] for _ in self._columns]

        for name in self._columns:
            if name not in values:
                raise ValueError(F"Missing value for column '{name}'")
            
        for i, name in enumerate(self._columns):
            self._data[i].append(values[name])

        self._n_rows += 1
        return values

    def add_column(self, header: str, values: List[Any]) -> DataColumn[Any]:
        self._validate_length(values)
        data_column = DataColumn(values)
        self._columns.append(header)
        self._data.append(data_column)

        if self._n_rows == 0:
            self._n_rows = len(values)

        return data_column

    def update_row(self, index: int, values: Dict[str, Any]) -> Dict[str, Any]:
        self._check_row_index(index)

        for name in values:
            if name not in self._columns:
                raise KeyError(f"Unknown column '{name}' in update")
            
        old_row = self.get_row(index)

        for i, name in enumerate(self._columns):
            if name in values:
                self._data[i][index] = values[name]

        return old_row

    def delete_row(self, index: int) -> Dict[str, Any]:
        self._check_row_index(index)

        removed = {name: self._data[i][index] for i, name in enumerate(self._columns)}

        for col in self._data:
            col.pop(index)

        self._n_rows -= 1
        return removed

    def to_csv(
        self,
        path: str,
        delimiter: str = ",",
        encoding: str = "utf-8",
        newline: str = "\n",
    ) -> None:
        n_cols = len(self._columns)

        if n_cols == 0:
            write_csv(path, [], [], delimiter=delimiter, encoding=encoding, newline=newline)
            return

        n_rows = len(self._data[0])

        for idx, col in enumerate(self._data):
            if len(col) != n_rows:
                raise ValueError(
                    f"Column {idx} ('{self._columns[idx]}') length {len(col)} "
                    f"!= {n_rows} (length of first column)"
                )

        rows: List[List[object]] = []
        for row_idx in range(n_rows):
            row = [self._data[col_idx][row_idx] for col_idx in range(n_cols)]
            rows.append(row)

        write_csv(
            path=path,
            columns=self._columns,
            rows=rows,
            delimiter=delimiter,
            encoding=encoding,
            newline=newline,
        )

    def to_json(
        self,
        path: str,
        encoding: str = "utf-8",
        indent: int = 2,
    ) -> None:
        columns = self._columns
        data = self._data

        if not columns:
            write_json(path, [], encoding=encoding, indent=indent)
            return

        n_cols = len(columns)
        n_rows = len(data[0]) if n_cols > 0 else 0

        for idx, col_vals in enumerate(data):
            if len(col_vals) != n_rows:
                raise ValueError(
                    f"Column {idx} ('{columns[idx]}') length {len(col_vals)} "
                    f"!= {n_rows} (length of first column)"
                )

        records: List[dict[str, Any]] = []
        for row_idx in range(n_rows):
            record = {
                columns[col_idx]: data[col_idx][row_idx]
                for col_idx in range(n_cols)
            }
            records.append(record)

        write_json(
            path=path,
            records=records,
            encoding=encoding,
            indent=indent,
        )

    def to_toon(
        self,
        path: str,
        encoding: str = "utf-8",
        indent: int = 2,
    ) -> None:
        columns = self._columns
        data = self._data

        if not columns:
            write_toon(path, [], encoding=encoding, indent=indent)
            return

        n_cols = len(columns)
        n_rows = len(data[0]) if n_cols > 0 else 0

        records: List[dict[str, Any]] = []
        for row_idx in range(n_rows):
            record = {
                columns[col_idx]: data[col_idx][row_idx]
                for col_idx in range(n_cols)
            }
            records.append(record)

        write_toon(
            path=path,
            records=records,
            encoding=encoding,
            indent=indent,
        )

    def sort(
        self, 
        columns: str | List[str], 
        reverse: bool | List[bool] = False
    ) -> "DataKit":
        if self._n_rows <= 1:
            return

        if isinstance(columns, str):
            columns = [columns]
        
        if isinstance(reverse, bool):
            reverse = [reverse] * len(columns)
            
        if len(columns) != len(reverse):
            raise ValueError("Length of 'columns' and 'reverse' must match")

        indices = list(range(self._n_rows))

        for col_name, is_reverse in zip(reversed(columns), reversed(reverse)):
            col_idx = self._col_pos(col_name)
            col_data = self._data[col_idx]
            
            indices.sort(key=lambda i: col_data[i], reverse=is_reverse)

        for i, col in enumerate(self._data):
            self._data[i] = [col[j] for j in indices]
        
        return self

    def rename_column(self, old_name: str, new_name: str) -> "DataKit":
        if new_name in self._columns:
            raise ValueError(f"Column '{new_name}' already exists")
            
        idx = self._col_pos(old_name)
        self._columns[idx] = new_name
        return self

    def filter(self, condition: Callable[[Dict[str, Any]], bool]) -> "DataKit":
        header = self._columns
        matched_data = [header]

        for row_dict in self.iter_rows():
            if condition(row_dict):
                row_values = [row_dict[col] for col in header]
                matched_data.append(row_values)

        return self.from_rows(matched_data)
    
    def select(self, columns: List[str]) -> "DataKit":
        selected_data = []
        
        for name in columns:
            col_data = self.get_column(name)
            selected_data.append(col_data)

        return DataKit(
            _data=selected_data,
            _columns=columns,
            _n_rows=self._n_rows
        )
    
    def unique(self, column: str) -> "DataKit":
        target_col_idx = self._col_pos(column)
        
        seen = set()
        indices_to_keep = []

        target_data = self._data[target_col_idx]
        
        for i in range(self._n_rows):
            val = target_data[i]
            if val not in seen:
                seen.add(val)
                indices_to_keep.append(i)

        new_data = []
        for col in self._data:
            new_col_data = [col[i] for i in indices_to_keep]
            new_data.append(new_col_data)

        return DataKit(
            _data=new_data, 
            _columns=list(self._columns), 
            _n_rows=len(indices_to_keep)
        )
    
    def apply(self, func: Callable[[Any], Any], column: str) -> "DataKit":
        idx = self._col_pos(column)
        col_data = self._data[idx]
        
        for i in range(len(col_data)):
            col_data[i] = func(col_data[i])

    def group_by(self, column: str, agg: Dict[str, str]) -> "DataKit":
        group_col_idx = self._col_pos(column)
        
        groups: Dict[Any, List[int]] = {}
        for i in range(self._n_rows):
            key = self._data[group_col_idx][i]
            if key not in groups:
                groups[key] = []
            groups[key].append(i)

        new_agg_names = []
        for target_col, op in agg.items():
            new_agg_names.append(f"{op}_{target_col}")

        result_columns = [column] + new_agg_names
        
        result_data = [[] for _ in result_columns]
        
        for key, indices in groups.items():
            result_data[0].append(key)
            
            for idx, (target_col, operation) in enumerate(agg.items()):
                result_col_idx = idx + 1
                
                src_col_idx = self._col_pos(target_col)
                values = [self._data[src_col_idx][i] for i in indices]
                
                if operation == "count":
                    val = len(values)
                elif operation == "sum":
                    val = sum(values)
                elif operation == "mean":
                    val = sum(values) / len(values) if values else 0
                elif operation == "max":
                    val = max(values) if values else None
                elif operation == "min":
                    val = min(values) if values else None
                else:
                    raise ValueError(f"Unknown aggregation: {operation}")
                
                result_data[result_col_idx].append(val)

        return DataKit(
            _data=result_data, 
            _columns=result_columns, 
            _n_rows=len(groups)
        )

    def head(self, n: int = 5) -> "DataKit":
        n = min(n, self._n_rows)
        new_data = [col[:n] for col in self._data]
        return DataKit(_data=new_data, _columns=list(self._columns), _n_rows=n)

    def tail(self, n: int = 5) -> "DataKit":
        if n <= 0:
            return DataKit(_columns=list(self._columns))
        
        start = max(0, self._n_rows - n)
        new_data = [col[start:] for col in self._data]
        return DataKit(_data=new_data, _columns=list(self._columns), _n_rows=len(new_data[0]))