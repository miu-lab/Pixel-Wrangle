from abc import ABC, abstractmethod
from typing import Union
from analyzer_line_matcher import GLSLLineMatcher
from analyzer_code_splitter import GLSLCodeSplitter
from str_line_utils import (
    split_string_at_characters,
    JSONableMutable,
    try_parse_mutable,
    cast_value,
)
from gl_types import GLSL_TYPE_MAP, LineMatch, MatchPropTuple
from str_line_utils import build_TD_par_name


class GLSLCodeParser(ABC):
    @abstractmethod
    def __init__(self, code: str):
        self.code = code
        return

    @abstractmethod
    def get_items(self) -> dict:
        return


class GLSLUniformCodeParser(GLSLCodeParser):
    @staticmethod
    def __get_variable_prop(any_str: str) -> JSONableMutable:
        return cast_value(try_parse_mutable(any_str))

    def __init__(
        self,
        code: str,
        line_matcher: GLSLLineMatcher = GLSLLineMatcher,
        code_splitter: GLSLCodeSplitter = GLSLCodeSplitter,
    ):
        self.__line_matcher = line_matcher
        self.__code_splitter = code_splitter
        self.code = code
        return

    def __parse_prop_from_string(self, prop_str: str) -> Union[MatchPropTuple, None]:
        key, value_str = split_string_at_characters(prop_str.strip(), ["=", ":"], 1)
        try:
            value = self.__get_variable_prop(value_str)
            return key, value
        except ValueError as e:
            print(f"Error casting value for property '{key}': {e}")
            return None

    def __parse_dict_from_props(self, any_str: str) -> dict:
        props_list = split_string_at_characters(any_str, [";"])
        props = {}

        for any_str in props_list:
            prop = self.__parse_prop_from_string(any_str)
            if prop is not None:
                key, value = prop
                props[key] = value

        return props

    def __get_parameter_props(self, props_str: str) -> dict:
        return self.__parse_dict_from_props(props_str) if props_str else {}

    def __set_variable_item(self, line_match: LineMatch, code_line: str) -> dict:
        match = line_match["match"]
        item_object_from_match = self.__build_item_from_match(match)
        item_object_update = {"gl_page": line_match["gl_page"], "code": code_line}
        return {**item_object_from_match, **item_object_update}

    def __set_header_item(self, line_match: LineMatch, code_line: str) -> dict:
        match = line_match["match"]
        item_object_from_match = self.__build_item_from_match(match)
        gl_type = GLSL_TYPE_MAP["//---"]["style"]
        name = build_TD_par_name(item_object_from_match["props"]["label"], "H")
        item_object_update = {
            "gl_page": line_match["gl_page"],
            "code": code_line,
            "gl_type": gl_type,
            "name": name,
        }
        return {**item_object_from_match, **item_object_update}

    def __build_item_from_match(self, line_match: dict) -> dict:
        return {
            group: self.__get_parameter_props(line_match.group(group))
            if group == "props"
            else self.__get_variable_prop(line_match.group(group))
            for group in line_match.groupdict()
        }

    def get_items(self) -> dict:
        line_items = {}
        code_lines = self.__code_splitter(self.code).run()
        for code_line in code_lines:
            line_match = self.__line_matcher(code_line).run()
            if line_match["gl_page"] == "UI":
                line_object = self.__set_header_item(line_match, code_line)
            else:
                line_object = self.__set_variable_item(line_match, code_line)
            key = line_object["name"]
            line_items[key] = line_object
        return line_items
