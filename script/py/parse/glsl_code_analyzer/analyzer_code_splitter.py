from analyzer_line_identifier import GLSLLineIdentifier


class GLSLCodeSplitter:
    def __init__(
        self, code: str, line_identifier: GLSLLineIdentifier = GLSLLineIdentifier()
    ):
        self.identifier = line_identifier
        self.code = code

    def run(self) -> list[str]:
        '''Splits the code into lines and removes comments and empty lines.'''
        code_lines = list(filter(self.identifier.is_comment, self.code.splitlines()))
        return [x for x in code_lines if x != ""]
