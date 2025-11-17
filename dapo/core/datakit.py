from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Sequence

@dataclass
class DataKit:
    _data: List[List[Any]] = field(default_factory=list)
    _columns: List[str] = field(default_factory=list)
    _n_rows: int = 0

    # HELPERS
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
        
        length = {len(col) for col in columns.values()}
        if len(length) > 1:
            raise ValueError("All columns must have the same length")
        
        n_rows = length.pop()
        data = {name: list(values) for name, values in columns.items()}
        column_order = list(columns.keys())
        return cls(_data=data, _columns=column_order, _n_rows=n_rows)
    
    @classmethod
    def from_rows(cls, rows: Sequence[Sequence[Any]]) -> "DataKit":
        if not rows:
            return cls()
        
        header = [str(c) for c in rows[0]]
        n_cols = len(header)
        cols_data: List[List[Any]] = [[] for _ in range(n_cols)]
        n_rows = 0

        for r in rows[1:]:
            if len(r) != n_cols:
                raise ValueError(f"Row length {len(r)} != header length {n_cols}: {r}")
            for i, value in enumerate(r):
                cols_data[i].append(value)
            n_rows += 1

        return cls(_columns=header, _data=cols_data, _n_rows=n_rows)
    
    @property
    def columns(self) -> List[str]:
        return self._columns
    
    @property
    def n_cols(self) -> int:
        return len(self._columns)
    
    # ACCESS
    def get_column(self, name: str) -> List[Any]:
        idx = self._col_pos(name)
        return self._data[idx]
    
    def get_row(self, index: int) -> Dict[str, Any]:
        self._check_row_index(index)
        return {name: self._data[i][index] for i, name in enumerate(self._columns)}
    
    def iter_rows(self):
        for i in range(self._n_rows):
            yield self.get_row(i)

    def add_row(self, values: Dict[str, Any]) -> None:
        if not self._columns:
            self._columns = list(values.keys())
            self._data = [[] for _ in self._columns]

        for name in self._columns:
            if name not in values:
                raise ValueError(F"Missing value for column '{name}'")
            
        for i, name in enumerate(self._columns):
            self._data[i].append(values[name])

        self._n_rows += 1