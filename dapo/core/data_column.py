from __future__ import annotations

from typing import TypeVar, List

_T = TypeVar("_T")

class DataColumn(List[_T]):
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
