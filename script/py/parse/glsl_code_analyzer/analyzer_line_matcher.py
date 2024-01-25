import re
from analyzer_line_identifier import GLSLLineIdentifier
import analyzer_regex_patterns as regex_patterns
from gl_types import GLItemPage, LineMatch


class GLSLLineMatcher:
    @staticmethod
    def __match_GLSL_variable(stringLineGLSL: str, pattern: re.Pattern) -> re.Match:
        return re.match(pattern, stringLineGLSL)

    def __init__(
        self, code_line: str, line_identifier: GLSLLineIdentifier = GLSLLineIdentifier()
    ):
        self.code_line = code_line
        self.__line_identifier = line_identifier
        self.__match_functions = {
            self.__line_identifier.is_header: self.__build_ui_match_object,
            self.__line_identifier.is_constant: self.__build_constant_match_object,
            self.__line_identifier.is_atomic_counter: self.__build_atomic_counter_match_object,
            self.__line_identifier.is_matrix: self.__build_matrix_match_object,
            self.__line_identifier.is_array: self.__build_array_match_object,
        }

    def __build_standard_match_object(self) -> LineMatch:
        return {
            "gl_page": GLItemPage.VECTOR.name,
            "match": self.__match_GLSL_variable(
                self.code_line, regex_patterns.standard
            ),
        }

    def __build_array_match_object(self) -> LineMatch:
        return {
            "gl_page": GLItemPage.ARRAY.name,
            "match": self.__match_GLSL_variable(self.code_line, regex_patterns.array),
        }

    def __build_matrix_match_object(self) -> LineMatch:
        return {
            "gl_page": GLItemPage.MATRIX.name,
            "match": self.__match_GLSL_variable(
                self.code_line, regex_patterns.standard
            ),
        }

    def __build_atomic_counter_match_object(self) -> LineMatch:
        return {
            "gl_page": GLItemPage.ATOMIC.name,
            "match": self.__match_GLSL_variable(
                self.code_line, regex_patterns.standard
            ),
        }

    def __build_constant_match_object(self) -> LineMatch:
        return {
            "gl_page": GLItemPage.CONSTANT.name,
            "match": self.__match_GLSL_variable(
                self.code_line, regex_patterns.constant
            ),
        }

    def __build_ui_match_object(self) -> LineMatch:
        return {
            "gl_page": GLItemPage.UI.name,
            "match": self.__match_GLSL_variable(self.code_line, regex_patterns.ui),
        }

    def run(self):
        for check_func, match_func in self.__match_functions.items():
            if check_func(self.code_line):
                return match_func()
        return self.__build_standard_match_object()
