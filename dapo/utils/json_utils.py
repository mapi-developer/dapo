def _skip_ws(s, i):
    while i < len(s) and s[i] in " \t\r\n":
        i += 1
    return i


def _parse_string(s, i):
    # s[i] == '"'
    i += 1
    result_chars = []
    while i < len(s):
        ch = s[i]
        if ch == '"':
            return "".join(result_chars), i + 1
        if ch == "\\":
            # Escape sequence
            i += 1
            if i >= len(s):
                raise ValueError("Invalid escape sequence at end of string")
            esc = s[i]
            if esc == '"':
                result_chars.append('"')
            elif esc == "\\":
                result_chars.append("\\")
            elif esc == "/":
                result_chars.append("/")
            elif esc == "b":
                result_chars.append("\b")
            elif esc == "f":
                result_chars.append("\f")
            elif esc == "n":
                result_chars.append("\n")
            elif esc == "r":
                result_chars.append("\r")
            elif esc == "t":
                result_chars.append("\t")
            else:
                # Very minimal: ignore unknown escapes as literal
                result_chars.append(esc)
            i += 1
        else:
            result_chars.append(ch)
            i += 1
    raise ValueError("Unterminated string")


def _parse_number(s, i):
    start = i
    if s[i] == "-":
        i += 1
    while i < len(s) and s[i].isdigit():
        i += 1
    if i < len(s) and s[i] == ".":
        i += 1
        while i < len(s) and s[i].isdigit():
            i += 1
    if i < len(s) and s[i] in "eE":
        i += 1
        if i < len(s) and s[i] in "+-":
            i += 1
        while i < len(s) and s[i].isdigit():
            i += 1
    num_str = s[start:i]
    # Decide int vs float
    if "." in num_str or "e" in num_str or "E" in num_str:
        return float(num_str), i
    return int(num_str), i


def _parse_literal(s, i, literal, value):
    end = i + len(literal)
    if s[i:end] == literal:
        return value, end
    raise ValueError("Unexpected literal at position {}".format(i))


def _parse_array(s, i):
    # s[i] == '['
    i += 1
    arr = []
    i = _skip_ws(s, i)
    if i < len(s) and s[i] == "]":
        return arr, i + 1
    while True:
        i = _skip_ws(s, i)
        v, i = _parse_value(s, i)
        arr.append(v)
        i = _skip_ws(s, i)
        if i < len(s) and s[i] == ",":
            i += 1
            continue
        if i < len(s) and s[i] == "]":
            return arr, i + 1
        raise ValueError("Expected ',' or ']' in array at position {}".format(i))


def _parse_object(s, i):
    # s[i] == '{'
    i += 1
    obj = {}
    i = _skip_ws(s, i)
    if i < len(s) and s[i] == "}":
        return obj, i + 1
    while True:
        i = _skip_ws(s, i)
        if i >= len(s) or s[i] != '"':
            raise ValueError("Expected string key at position {}".format(i))
        key, i = _parse_string(s, i)
        i = _skip_ws(s, i)
        if i >= len(s) or s[i] != ":":
            raise ValueError("Expected ':' after key at position {}".format(i))
        i += 1
        i = _skip_ws(s, i)
        value, i = _parse_value(s, i)
        obj[key] = value
        i = _skip_ws(s, i)
        if i < len(s) and s[i] == ",":
            i += 1
            continue
        if i < len(s) and s[i] == "}":
            return obj, i + 1
        raise ValueError("Expected ',' or '}' in object at position {}".format(i))


def _parse_value(s, i):
    i = _skip_ws(s, i)
    if i >= len(s):
        raise ValueError("Unexpected end of input while parsing value")

    ch = s[i]

    if ch == '"':
        return _parse_string(s, i)
    if ch == "{":
        return _parse_object(s, i)
    if ch == "[":
        return _parse_array(s, i)
    if ch == "t":
        return _parse_literal(s, i, "true", True)
    if ch == "f":
        return _parse_literal(s, i, "false", False)
    if ch == "n":
        return _parse_literal(s, i, "null", None)
    if ch == "-" or ch.isdigit():
        return _parse_number(s, i)

    raise ValueError("Unexpected character '{}' at position {}".format(ch, i))


def _load_json(text):
    value, i = _parse_value(text, 0)
    i = _skip_ws(text, i)
    if i != len(text):
        # Some trailing junk, but for simplicity we just ignore or raise
        # raise ValueError("Extra data after JSON at position {}".format(i))
        pass
    return value


# ---------- Public reader ----------

def read_json(path, encoding="utf-8"):
    with open(path, "r", encoding=encoding) as f:
        text = f.read()

    obj = _load_json(text)

    # Case 1: straight list of objects
    if isinstance(obj, list):
        records = []
        for r in obj:
            if isinstance(r, dict):
                records.append(r)
        return records

    # Case 2: { "data": [ ... ] }
    if isinstance(obj, dict) and "data" in obj and isinstance(obj["data"], list):
        records = []
        for r in obj["data"]:
            if isinstance(r, dict):
                records.append(r)
        return records

    raise ValueError(
        "JSON format not supported: expected [ {...}, ... ] or { 'data': [ {...}, ... ] }"
    )


# ---------- Writing / serialization ----------

def _encode_json_string(s):
    s = s.replace("\\", "\\\\")
    s = s.replace('"', '\\"')
    s = s.replace("\n", "\\n")
    s = s.replace("\r", "\\r")
    s = s.replace("\t", "\\t")
    return '"' + s + '"'


def _to_json_value(v):
    # None -> null
    if v is None:
        return "null"
    # bool -> true/false
    if isinstance(v, bool):
        return "true" if v else "false"
    # numbers
    if isinstance(v, (int, float)):
        return repr(v)
    # strings
    if isinstance(v, str):
        return _encode_json_string(v)
    # list / tuple
    if isinstance(v, (list, tuple)):
        inner = ", ".join(_to_json_value(x) for x in v)
        return "[" + inner + "]"
    # dict
    if isinstance(v, dict):
        parts = []
        for k, val in v.items():
            key_str = _encode_json_string(str(k))
            parts.append(key_str + ": " + _to_json_value(val))
        return "{" + ", ".join(parts) + "}"
    # fallback: convert to string
    return _encode_json_string(str(v))


def write_json(path, records, encoding="utf-8", indent=2):
    objs = [_to_json_value(rec) for rec in records]

    if indent and indent > 0:
        space = " " * indent
        inner = ",\n".join(space + o for o in objs)
        text = "[\n" + inner + "\n]"
    else:
        text = "[" + ", ".join(objs) + "]"

    with open(path, "w", encoding=encoding) as f:
        f.write(text)
