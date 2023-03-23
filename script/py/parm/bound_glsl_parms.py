from _stubs import *
from bound_glsl_utils import *

def updateParms():

    # MASTER
    bindMaster = parent.Comp
    selectedPage = 'Controls'

    # GLSL NODE
    target = bindMaster.op("glsl1")
    bindMasterRelativePath = target.relativePath(bindMaster)

    # PARM LIST FROM MASTER OP
    source = op("PARMS_TO_BIND")

    # PARM LIST FROM CODE DECLARATIONS
    fromCodeParms = op("CODE_DECLARATIONS")

    # GET SOURCE LIST
    plist = source.rows() # Structure [name, label, style, pargroup]
    namesRow = plist[0]
    plist.pop(0)
    updatedPlist = [
        p
        for p in plist
        if bindMaster.par[p[0].val].page == selectedPage
        and p[2].val
        in ['Int', 'Float', 'RGB', 'RGBA', 'Menu', 'CHOP', 'Toggle', 'Pulse']
    ]
    plist = updatedPlist

    # GROUP BY PARGROUPS
    parGroups = getParGroups(plist, namesRow)

    # Custom Parameters Offsets to leave space to built-ins
    GLUniParOffset   = 14
    GLarrayParOffset = 0
    GLmatParOffset   = 0
    GLacParOffset    = 0
    GLconstParOffset = 0

    GLuniCurrentParmsOP   = op("CURRENT_UNIFORMS")
    GLarrayCurrentParmsOP = op("CURRENT_ARRAY")
    GLmatCurrentParmsOP   = op("CURRENT_MATRIX")
    GLacCurrentParmsOP    = op("CURRENT_ATOMIC")
    GLconstCurrentParmsOP = op("CURRENT_CONST")

    GLuniParGroups        = []
    GLarrayParGroups      = []
    GLmatParGroups        = []
    GLacParGroups         = []
    GLconstParGroups      = []

    toResetParms = [{"op": GLuniCurrentParmsOP, "offset": GLUniParOffset},
                    {"op": GLarrayCurrentParmsOP, "offset": GLarrayParOffset},
                    {"op": GLmatCurrentParmsOP, "offset": GLmatParOffset},
                    {"op": GLacCurrentParmsOP, "offset": GLacParOffset},
                    {"op": GLconstCurrentParmsOP, "offset": GLconstParOffset},]

    # Reset parms with corresponding offsets
    resetParameters(target, toResetParms)
    # Reordering each GL Parm
    setParameterSection(fromCodeParms, parGroups, GLuniParGroups, GLarrayParGroups, GLmatParGroups, GLacParGroups, GLconstParGroups)
    ## SET STANDARD UNIFORMS ##
    setUniforms(target, source, bindMasterRelativePath, GLUniParOffset, GLuniParGroups)
    ## SET ARRAY UNIFORMS ##
    setArrays(target, fromCodeParms, bindMasterRelativePath, GLarrayParOffset, GLarrayParGroups)
    ## SET MATRIX UNIFORMS ##
    setMatrices(target, bindMasterRelativePath, GLmatParOffset, GLmatParGroups)
    ## SET ATOMIC COUNTERS ##
    setAtomicCounters(target, fromCodeParms, bindMasterRelativePath, GLacParOffset, GLacParGroups)
    ## SET CONST ##
    setVulkanConstants(target, bindMasterRelativePath, GLconstParOffset, GLconstParGroups)
    return

## BUILTIN FUNCTIONS ##
def onOffToOn(channel, sampleIndex, val, prev):
    updateParms()
    return
