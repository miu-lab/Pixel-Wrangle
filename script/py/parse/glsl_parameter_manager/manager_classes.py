from abc import ABC, abstractmethod
from gl_types import GLItemPage

class GLItem(ABC):
    def __init__(self, **item_attrs : dict):
        self.code: str                        = item_attrs.get('code','')
        self.gl_page: GLItemPage              = item_attrs.get('gl_page','VECTOR')
        self.gl_type: str                     = item_attrs.get('gl_type', 'float')
        self.name: str                        = item_attrs.get('name','Parameter')
        self.props: dict                      = item_attrs.get('props', {})
        self.par: Par                         = item_attrs.get('par')
        self.host_comp: COMP                  = item_attrs.get('host_comp')
        self.bind_op: glslmultiTOP or glslTOP = item_attrs.get('bind_op')

    @abstractmethod
    def createPar(self) -> Par or None:
        print("A parameter was created")

    @abstractmethod
    def destroyPar(self, par: Par) -> bool:
        print("A parameter was destroyed")

    @abstractmethod
    def updatePar(self, par: Par) -> Par:
        print("A parameter was updated")


class GLVectorPageItem(GLItem):
    def __init__(self, **item_attrs : dict):
        super().__init__(**item_attrs)


class GLArrayPageItem(GLItem):
    def __init__(self, **item_attrs : dict):
        self.array_length = item_attrs.pop('array_length', 1)
        super().__init__(**item_attrs)


class GLMatrixPageItem(GLItem):
    def __init__(self, **item_attrs : dict):
        super().__init__(**item_attrs)


class GLAtomicPageItem(GLItem):
    def __init__(self, **item_attrs):
        super().__init__(**item_attrs)


class GLConstantPageItem(GLItem):
    def __init__(self, **item_attrs : dict):
        self.init_value = item_attrs.pop('init_value', 0)
        super().__init__(**item_attrs)


class GLUIItem(GLItem):
    def __init__(self, **item_attrs : dict):
        super().__init__(**item_attrs)
