from typing import TypeVar, List, Union

_T = TypeVar("_T")

class DataColumn(List[_T]):
    def _validate_length(self, other: List[_T]) -> None:
        if len(self) != len(other):
            raise ValueError(f"Column length mismatch: {len(self)} != {len(other)}")

    def column_sum(self, values: List[_T]):
        column_sum = 0
        for i in values: column_sum += i
        return column_sum

    def sort(self, reverse: bool = False) -> "DataColumn":
        if len(self) <= 1:
            return

        def _partition(low: int, high: int) -> int:
            pivot = self[high]
            i = low - 1

            if not reverse:
                for j in range(low, high):
                    if self[j] <= pivot:
                        i += 1
                        self[i], self[j] = self[j], self[i]
            else:
                for j in range(low, high):
                    if self[j] >= pivot:
                        i += 1
                        self[i], self[j] = self[j], self[i]

            i += 1
            self[i], self[high] = self[high], self[i]
            return i

        def _quick_sort(low: int, high: int) -> None:
            if low < high:
                p = _partition(low, high)
                _quick_sort(low, p - 1)
                _quick_sort(p + 1, high)

        _quick_sort(0, len(self) - 1)
        return self

    def sort_order(self, reverse: bool = False) -> List[int]:
        n = len(self)
        if n <= 1:
            return list(range(n))

        indices = list(range(n))

        def merge_sort(idxs: List[int]) -> List[int]:
            if len(idxs) <= 1:
                return idxs

            mid = len(idxs) // 2
            left = merge_sort(idxs[:mid])
            right = merge_sort(idxs[mid:])

            # merge step based on self[...] values
            i = j = 0
            merged: List[int] = []

            while i < len(left) and j < len(right):
                lv = self[left[i]]
                rv = self[right[j]]

                if not reverse:
                    if lv <= rv:
                        merged.append(left[i]); i += 1
                    else:
                        merged.append(right[j]); j += 1
                else:
                    if lv >= rv:
                        merged.append(left[i]); i += 1
                    else:
                        merged.append(right[j]); j += 1

            if i < len(left):
                merged.extend(left[i:])
            if j < len(right):
                merged.extend(right[j:])

            return merged

        return merge_sort(indices)

    def sum(self, decimal_places: int = None, to_int: bool = False) -> int | float:
        POSSIBLE_TYPES = [float, int, complex]
        if len(self) < 1:
            return 0
        if type(self[0]) not in POSSIBLE_TYPES:
            raise TypeError(f"Values in DataColumn not a numeric: {type(self[0])}")

        column_sum = self.column_sum(self)

        if to_int:
            column_sum = int(column_sum)
        elif decimal_places != None:
            column_sum = round(column_sum, decimal_places)
        
        return column_sum
    
    def mean(self, decimal_places: int = None, to_int: bool = False) -> int | float:
        POSSIBLE_TYPES = [float, int, complex]
        if len(self) < 1:
            return None
        if type(self[0]) not in POSSIBLE_TYPES:
            raise TypeError(f"Values in DataColumn not a numeric: {type(self[0])}")

        column_sum = self.sum()
        column_mean = column_sum/len(self)
        if to_int:
            column_mean = int(column_sum/len(self))
        elif decimal_places != None:
            column_mean = round(column_sum/len(self), decimal_places)
        
        return column_mean
    
    def median(self, decimal_places: int = None, to_int: bool = False) -> int | float:
        n = len(self)
        if n < 1:
            return None
        
        s = self.sort()
        median = (s[n//2-1]/2.0+s[n//2]/2.0, s[n//2])[n % 2]
        if to_int:
            median = int(median)
        elif decimal_places != None:
            median = round(median, decimal_places)

        return median
    
    def mode(self) -> _T:
        if not self:
            return None

        frequency = {}
        for item in self:
            if item in frequency:
                frequency[item] += 1
            else:
                frequency[item] = 1
        
        max_count = 0
        mode = None
        
        for key, value in frequency.items():
            if value > max_count:
                max_count = value
                mode = key
                
        return mode
    
    def min(self) -> _T:
        if not self:
            return None
        
        minimum = self[0]
        
        for item in self:
            if item < minimum:
                minimum = item
                
        return minimum
    
    def max(self) -> _T:
        if not self:
            return None
        
        maximum = self[0]
        
        for item in self:
            if item > maximum:
                maximum = item
                
        return maximum
    
    def std(self, decimal_places: int = None, to_int: bool = False) -> int | float:
        n = len(self)
        if n <= 1:
            return None
        mean = self.mean()
        summ = self.column_sum([(value - mean)**2 for value in self])
        std = (summ/n-1)**0.5

        if to_int:
            std = int(std)
        elif decimal_places != None:
            std = round(std, decimal_places)

        return std
    
    def add(self, other: Union[int, float, List[int | float]]) -> "DataColumn":
        if isinstance(other, list):
            self._validate_length(other)
            return DataColumn([x + y for x, y in zip(self, other)])
        return DataColumn([x + other for x in self])

    def sub(self, other: Union[int, float, List[int | float]]) -> "DataColumn":
        if isinstance(other, list):
            self._validate_length(other)
            return DataColumn([x - y for x, y in zip(self, other)])
        return DataColumn([x - other for x in self])

    def mul(self, other: Union[int, float, List[int | float]]) -> "DataColumn":
        if isinstance(other, list):
            self._validate_length(other)
            return DataColumn([x * y for x, y in zip(self, other)])
        return DataColumn([x * other for x in self])
    
    def div(self, other: Union[int, float, List[int | float]]) -> "DataColumn":
        if isinstance(other, list):
            self._validate_length(other)
            if any(y == 0 for y in other):
                 raise ValueError("Division by zero encountered in column operation.")
            return DataColumn([x / y for x, y in zip(self, other)])
        
        if other == 0:
            raise ValueError("Cannot divide column by zero.")
        return DataColumn([x / other for x in self])