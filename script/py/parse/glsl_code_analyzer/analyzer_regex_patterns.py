import re

OPTIONAL_UNIFORM_PATTERN = r"(uniform\s+)?"
CONSTANT_PATTERN         = r"const\s+"
TYPE_PATTERN             = r"(?P<gl_type>\w+)\s+"
NAME_PATTERN             = r"(?P<name>\w+)\s*"
ARRAY_LENGTH_PATTERN     = r"\[(?P<array_length>\d+)\]"
EQUAL_PATTERN            = r"=\s*"
INIT_VAL_PATTERN         = r"(?P<init_value>[\w.]+)"
SEMICOLON_PATTERN        = r";?"
OPTIONAL_PROPS_PATTERN   = r"(?:\s*//\s*(?P<props>.*))?"
UI_TYPE_PATTERN          = r"(?P<gl_type>//---)?"
UI_PROPS_PATTERN         = r"\s*(?P<props>.*)?"


# Example : const int MAX_LIGHTS = 8; // section=1; label=Max Lights; min=1; max=8;
constant = re.compile(
    rf"""
    {OPTIONAL_UNIFORM_PATTERN}
    {CONSTANT_PATTERN}
    {TYPE_PATTERN}
    {NAME_PATTERN}
    {EQUAL_PATTERN}
    {INIT_VAL_PATTERN}
    {SEMICOLON_PATTERN}
    {OPTIONAL_PROPS_PATTERN}
""",
    re.VERBOSE,
)
# Example : uniform vec3 LIGHTS[12]; // section=1; label=Lights
array = re.compile(
    rf"""
    {OPTIONAL_UNIFORM_PATTERN}
    {TYPE_PATTERN}
    {NAME_PATTERN}
    {ARRAY_LENGTH_PATTERN}
    {SEMICOLON_PATTERN}
    {OPTIONAL_PROPS_PATTERN}
""",
    re.VERBOSE,
)

# Example : vec4 Color; // section=1; label=Lights; style=Color
standard = re.compile(
    rf"""
    {OPTIONAL_UNIFORM_PATTERN}
    {TYPE_PATTERN}
    {NAME_PATTERN}
    {SEMICOLON_PATTERN}
    {OPTIONAL_PROPS_PATTERN}
""",
    re.VERBOSE,
)
# Example : //--- label=Light Controls; section=1
ui = re.compile(
    rf"""
    {UI_TYPE_PATTERN}
    {UI_PROPS_PATTERN}
""",
    re.VERBOSE,
)