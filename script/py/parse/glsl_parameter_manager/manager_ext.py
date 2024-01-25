
class GLSLParameterManager:
    def __init__(
        self,
        ownerComp: COMP,
    ):
        self.owner = ownerComp
        self.host = None
        self.glslTOP = None
        self.input = ownerComp.par.Source.eval().jsonObject
        self.actions = {}
        self.factory = None

    def Set_target_operators(self, hostCOMP: COMP, glslTOP: glslTOP):
        pass
    def Update_parameters(self):
        pass
