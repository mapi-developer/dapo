import re
from typing import Any, Dict, List
from .csv_utils import parse_csv_line, csv_escape

def read_toon(path: str, encoding: str = "utf-8") -> List[Dict[str, Any]]:
    with open(path, "r", encoding=encoding) as f:
        lines = f.readlines()

    if not lines:
        return []

    content_lines = [line.strip() for line in lines if line.strip() and not line.strip().startswith("#")]
    
    if not content_lines:
        return []

    header_line = content_lines[0]
    
    match = re.match(r"^\[(\d+),?\]\{(.+)\}:", header_line)
    
    records: List[Dict[str, Any]] = []
    
    if match:
        n_rows = int(match.group(1))
        columns_str = match.group(2)
        columns = [c.strip() for c in columns_str.split(",")]
        
        data_lines = content_lines[1:]

        for line in data_lines:
            values = parse_csv_line(line, delimiter=",")
            
            record = {}
            for i, col in enumerate(columns):
                val = values[i] if i < len(values) else None
                
                if val == "true": val = True
                elif val == "false": val = False
                elif val == "null": val = None
                else:
                    # Try number
                    try:
                        if "." in val: val = float(val)
                        else: val = int(val)
                    except (ValueError, TypeError):
                        pass # Keep as string
                        
                record[col] = val
            records.append(record)
            
        return records
    
    else:
        print("Warning: Only tabular TOON arrays ( [N]{cols}: ) are currently supported.")
        return []

def write_toon(
    path: str, 
    records: List[Dict[str, Any]], 
    encoding: str = "utf-8",
    indent: int = 2
) -> None:
    if not records:
        with open(path, "w", encoding=encoding) as f:
            f.write("[0]{}:")
        return

    columns = list(records[0].keys())
    n_rows = len(records)
    
    header_cols = ",".join(columns)
    header = f"[{n_rows}]{{{header_cols}}}:"
    
    lines = [header]
    
    indent_str = " " * indent

    for record in records:
        row_values = []
        for col in columns:
            val = record.get(col)
            
            if val is None: s_val = "null"
            elif val is True: s_val = "true"
            elif val is False: s_val = "false"
            else: s_val = str(val)
            
            s_val = csv_escape(s_val, delimiter=",")
            row_values.append(s_val)
        
        lines.append(indent_str + ",".join(row_values))

    with open(path, "w", encoding=encoding) as f:
        f.write("\n".join(lines))