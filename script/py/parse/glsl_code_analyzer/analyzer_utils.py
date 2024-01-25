
def get_parameters_target_op(comp) -> COMP:
    return op(comp.par.Host)


def get_glsl_target_op(comp) -> glslTOP or glslmultiTOP:
    return op(comp.par.Targetgl)



