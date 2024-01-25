class GLSLLineIdentifier:
    @staticmethod
    def is_header(stringLineGLSL: str) -> bool:
        return stringLineGLSL.startswith("//---")

    @staticmethod
    def is_constant(stringLineGLSL: str) -> bool:
        return stringLineGLSL.startswith("const ")

    @staticmethod
    def is_matrix(stringLineGLSL: str) -> bool:
        return stringLineGLSL.startswith("mat")

    @staticmethod
    def is_atomic_counter(stringLineGLSL: str) -> bool:
        return stringLineGLSL.startswith("atomic_uint")

    @staticmethod
    def is_array(stringLineGLSL: str) -> bool:
        lineBegin = stringLineGLSL.split("//")[0]
        return "[" in lineBegin and "]" in lineBegin

    @staticmethod
    def is_comment(stringLineGLSL: str) -> bool:
        is_comment = stringLineGLSL.startswith(("//", "/*"))
        return not is_comment or GLSLLineIdentifier.is_header(stringLineGLSL)

