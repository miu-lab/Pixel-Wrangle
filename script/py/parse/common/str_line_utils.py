import re, ast
from typing import Union

JSONableValue = Union[int, float, str]
JSONableMutable = Union[dict, list, JSONableValue]


def try_parse_int(value: JSONableValue) -> int or None:
    try:
        return int(value)
    except ValueError:
        return None


def try_parse_float(value: JSONableValue) -> float or None:
    try:
        return float(value)
    except ValueError:
        return None


def cast_string(value: str) -> JSONableValue:
    int_value = try_parse_int(value)
    if int_value is not None:
        return int_value
    float_value = try_parse_float(value)
    return float_value if float_value is not None else value


def cast_dict(value: dict) -> dict[JSONableMutable]:
    return {k: cast_value(v) for k, v in value.items()}


def cast_list(value: list) -> list[JSONableMutable]:
    return [cast_value(x) for x in value]


def cast_value(value: JSONableMutable) -> JSONableMutable:
    if isinstance(value, dict):
        return cast_dict(value)
    elif isinstance(value, list):
        return cast_list(value)
    elif isinstance(value, str):
        return cast_string(value)
    else:
        return value


def try_parse_mutable(any_str: any) -> JSONableMutable:
    try:
        return eval_type(any_str)
    except (SyntaxError, ValueError):
        return any_str


def eval_type(any_str: str) -> any:
    return ast.literal_eval(any_str)


def split_string_at_characters(
    string: str, characters: list[str], maxsplit: int = 0
) -> list[str]:
    split_pattern = "|".join(map(re.escape, characters))
    split_result = re.split(split_pattern, string, maxsplit)
    return [x.strip() for x in split_result if x.strip()]

def build_TD_par_name(anystr: str, prefix:str = "") -> str:
    cleaned_string = prefix + re.sub(r"[^a-zA-Z]+", "", anystr)
    return cleaned_string.capitalize()