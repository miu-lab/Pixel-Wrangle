import re
from dataclasses import dataclass
from enum import Enum, auto
from typing import TypedDict, Tuple
from str_line_utils import JSONableMutable


GLSL_TYPE_MAP = {
    "//---": {"style": "Header", "default_name": "Header"},
    "bool": {"style": "Toggle", "dimension": 1},
    "float": {"style": "Float", "dimension": 1},
    "double": {"style": "Float", "dimension": 1},
    "int": {"style": "Int", "dimension": 1},
    "uint": {"style": "Int", "dimension": 1},
    "atomic_uint": {"style": "Int", "dimension": 1},
    "vec2": {"style": "Float", "dimension": 2},
    "vec3": {"style": "Float", "dimension": 3},
    "vec4": {"style": "Float", "dimension": 4},
    "dvec2": {"style": "Float", "dimension": 2},
    "dvec3": {"style": "Float", "dimension": 3},
    "dvec4": {"style": "Float", "dimension": 4},
    "ivec2": {"style": "Int", "dimension": 2},
    "ivec3": {"style": "Int", "dimension": 3},
    "ivec4": {"style": "Int", "dimension": 4},
    "uvec2": {"style": "Int", "dimension": 2},
    "uvec3": {"style": "Int", "dimension": 3},
    "uvec4": {"style": "Int", "dimension": 4},
    "bvec2": {"style": "Int", "dimension": 2},
    "bvec3": {"style": "Int", "dimension": 3},
    "bvec4": {"style": "Int", "dimension": 4},
    "mat2": {"style": "Chop"},
    "mat3": {"style": "Chop"},
    "mat4": {"style": "Chop"},
}

@dataclass
class GLItemPage(Enum):
    UI = auto()
    VECTOR = auto()
    ARRAY = auto()
    MATRIX = auto()
    ATOMIC = auto()
    CONSTANT = auto()
    HEADER = auto()

LineMatch = TypedDict("LineMatch", {"gl_page": GLItemPage, "match": re.Match})
MatchPropTuple = Tuple[str, JSONableMutable]