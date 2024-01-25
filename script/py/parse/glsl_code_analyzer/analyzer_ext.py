from analyzer_uniform_parser import GLSLUniformCodeParser
from json import dumps

class GLSLCodeAnalyzer:
    @staticmethod
    def __getCode(oppath: DAT) -> str or None:
        return op(oppath).text if isinstance(op(oppath), DAT) else None

    def __init__(
        self, 
        ownerComp: COMP, 
        parser: GLSLUniformCodeParser = GLSLUniformCodeParser
    ):
        self.__Parser = parser
        self.owner = ownerComp
        self.last_result = None

    @property
    def code(self):
        return self.__getCode(self.owner.par.Op)

    def Build_JSON(self) -> str:
        parser = self.__Parser
        line_obj_list = parser(self.code).get_items()
        self.last_result = dumps(line_obj_list, sort_keys=True, indent=4)
        return self.last_result

    def Send_to_textDAT(self, OP:textDAT) -> str or None:
        try:
            OP.clear()
            OP.text = self.Build_JSON()
            return self.last_result
        except Exception:
            print("This OP is not valid")
            return None
