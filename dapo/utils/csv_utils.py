from typing import List, Iterable, Iterator, Dict, Optional, Any

CANDIDATE_DELIMITERS = [",", ";", "\t", "|", ":"]

def parse_csv_line(line: str, delimiter: str = ",", quotechar: str = '"') -> List[str]:
    fields: List[str] = []
    current: List[str] = []
    in_quotes = False
    i = 0
    length = len(line)

    while i < length:
        ch = line[i]

        if ch == quotechar:
            if in_quotes and i + 1 < length and line[i + 1] == quotechar:
                current.append(quotechar)
                i += 2
                continue
            in_quotes = not in_quotes
            i += 1
            continue

        if not in_quotes and ch == delimiter:
            fields.append("".join(current))
            current = []
            i += 1
            continue

        current.append(ch)
        i += 1

    fields.append("".join(current))
    return [f.strip() for f in fields]

def sniff_delimiter_from_lines(
    lines: Iterable[str],
    max_lines: int = 20,
    candidates: Optional[List[str]] = None,
) -> str:
    if candidates is None:
        candidates = CANDIDATE_DELIMITERS

    stats = {d: [] for d in candidates}
    used_lines = 0

    for raw_line in lines:
        line = raw_line.strip("\n\r")
        if not line:
            continue
        used_lines += 1

        for d in candidates:
            fields = parse_csv_line(line, delimiter=d)
            stats[d].append(len(fields))

        if used_lines >= max_lines:
            break

    best_delim = ","
    best_cols = 1

    for d, counts in stats.items():
        if not counts or len(counts) != used_lines:
            continue
        if len(set(counts)) == 1:
            cols = counts[0]
            if cols > best_cols:
                best_cols = cols
                best_delim = d

    return best_delim

def sniff_delimiter(path: str, max_lines: int = 20) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return sniff_delimiter_from_lines(f, max_lines=max_lines)

def _infer_type(value: str) -> Any:
    if value == "":
        return value
        
    # Check for booleans
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
        
    # Check for numbers
    try:
        if "." in value:
            return float(value)
        return int(value)
    except (ValueError, TypeError):
        pass
        
    return value

def read_csv(
    path: str,
    delimiter: Optional[str] = None,
    has_header: bool = True,
    encoding: str = "utf-8",
) -> Iterator[Dict[str, Any]]:
    if delimiter is None:
        delimiter = sniff_delimiter(path)

    with open(path, "r", encoding=encoding, newline="") as f:
        header = None

        for raw_line in f:
            line = raw_line.rstrip("\n\r")
            if not line:
                continue

            fields = parse_csv_line(line, delimiter=delimiter)

            if has_header and header is None:
                header = fields
                continue

            fields = [_infer_type(f) for f in fields]

            if has_header:
                if len(fields) < len(header):
                    fields += [""] * (len(header) - len(fields))
                elif len(fields) > len(header):
                    fields = fields[:len(header)]
                yield dict(zip(header, fields))
            else:
                yield {str(i): v for i, v in enumerate(fields)}


def csv_escape(value: str, delimiter: str = ",", quotechar: str = '"') -> str:
    needs_quotes = (
        delimiter in value
        or quotechar in value
        or "\n" in value
        or "\r" in value
    )

    value = value.replace(quotechar, quotechar + quotechar)

    if needs_quotes:
        return f'{quotechar}{value}{quotechar}'
    return value

def write_csv(
    path: str,
    columns: List[str],
    rows: List[List[object]],
    delimiter: str = ",",
    encoding: str = "utf-8",
    newline: str = "\n",
) -> None:
    with open(path, "w", encoding=encoding, newline="") as f:
        header_line = delimiter.join(
            csv_escape(col, delimiter) for col in columns
        )
        f.write(header_line + newline)

        for row in rows:
            line = delimiter.join(
                csv_escape(str(v), delimiter) for v in row
            )
            f.write(line + newline)
        
        f.close()