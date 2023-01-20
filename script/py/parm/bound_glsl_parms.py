from _stubs import *
from bound_glsl_utils import *

# UTILS

# GLSL NODE
target = op(f"{parent.Comp.path}/glsl1")
# PARM LIST FROM MASTER OP
source = op("PARMS_TO_BIND")
curParms = op('get_current')

# PARM LIST FROM CODE DECLARATIONS
fromCodeParms = op("CODE_DECLARATIONS")

# MASTER UI NODE
bindMaster = parent.Comp
bindMasterRelativePath = target.relativePath(bindMaster)
selectedPage = 'Controls'

# OFFSET PARMS IN TARGET PAGE
offset = 0


def updateParms():

    # GET SOURCE LIST
    plist = source.rows()
    namesRow = plist[0]
    plist.pop(0)

    # FILTER SOURCE PARMS BY PAGE
    updatedPlist = []

    for i, p in enumerate(plist):
        if bindMaster.par[p[0].val].page == selectedPage:
            if p[2].val in ['Int', 'Float', 'RGB', 'RGBA', 'Menu', 'CHOP', 'Toggle', 'Pulse']:
                updatedPlist.append(p)

    plist = updatedPlist  # Structure [name, label, style, pargroup]

    # GROUP BY PARGROUPS
    parGroups = getParGroups(plist, namesRow)

    # Custom Parameters Offsets to leave space to built-ins
    GLUniParOffset = 10
    GLarrayParOffset = 0
    GLmatParOffset = 0
    GLacParOffset = 0
    GLconstParOffset = 0

    GLuniCurrentParmsOP = op("CURRENT_UNIFORMS")
    GLarrayCurrentParmsOP = op("CURRENT_ARRAY")
    GLmatCurrentParmsOP = op("CURRENT_MATRIX")
    GLacCurrentParmsOP = op("CURRENT_ATOMIC")
    GLconstCurrentParmsOP = op("CURRENT_CONST")

    GLuniParGroups = []
    GLarrayParGroups = []
    GLmatParGroups = []
    GLacParGroups = []
    GLconstParGroups = []

    toResetParms = [{"op": GLuniCurrentParmsOP, "offset": GLUniParOffset},
                    {"op": GLarrayCurrentParmsOP, "offset": GLarrayParOffset},
                    {"op": GLmatCurrentParmsOP, "offset": GLmatParOffset},
                    {"op": GLacCurrentParmsOP, "offset": GLacParOffset},
                    {"op": GLconstCurrentParmsOP, "offset": GLconstParOffset},]

    # Reset parms with corresponding offsets
    for toReset in toResetParms:
        curParmOP = toReset["op"]
        offset = toReset["offset"]
        resetParms(curParmOP, target, offset)

    # Reordering each GL Parm
    for i, parGroup in enumerate(parGroups):
        index = i
        pGroupName = parGroup[0][3].val
        pGLType = fromCodeParms[pGroupName, "gltype"].val
        pIsArray = fromCodeParms[pGroupName, "array"].val
        # Array uniform type
        if pIsArray == "1":
            GLarrayParGroups.append(parGroup)
            pass
        # Matrix uniform type
        elif pGLType == "mat":
            GLmatParGroups.append(parGroup)
            pass
        # Atomic uniform type
        elif pGLType == "ac":
            GLacParGroups.append(parGroup)
            pass
        # Constant type
        elif pGLType == "const":
            GLconstParGroups.append(parGroup)
            pass
        else:
            GLuniParGroups.append(parGroup)

    ## SET STANDARD UNIFORMS ##
    for i, parGroup in enumerate(GLuniParGroups):
        uniComponent = ['x', 'y', 'z', 'w']
        index = i+GLUniParOffset
        pGroupName = parGroup[0][3].val
        pGLType = fromCodeParms[pGroupName, "gltype"].val
        pIsArray = fromCodeParms[pGroupName, "array"].val
        target.par[f"uniname{str(index)}"].val = pGroupName

        ## BIND EACH PARM COMPONENTS ##
        for j, p in enumerate(parGroup):
            pName = getCellValue(source, p, 'name')
            targetp = target.par[f"value{str(index)}{uniComponent[j]}"]
            targetp.mode = ParMode.EXPRESSION
            targetp.expr = f"op('{bindMasterRelativePath}').par['{pName}']"

    ## SET ARRAY UNIFORMS ##
    for i, parGroup in enumerate(GLarrayParGroups):
        index = i+GLarrayParOffset
        pGroupName = parGroup[0][3].val
        pArrayType = fromCodeParms[pGroupName, "arraytype"].val
        pArrayValueType = fromCodeParms[pGroupName, "vtype"].val
        pArrayChop = fromCodeParms[pGroupName, "chop"].val
        target.par[f"chopuniname{str(index)}"].val = pGroupName
        target.par[f"choparraytype{str(index)}"].val = pArrayType
        target.par[f"chopunitype{str(index)}"].val = pArrayValueType
        if pArrayChop:
            target.par[f"chop{str(index)}"].mode = ParMode.EXPRESSION
            target.par[f"chop{str(index)}"].expr = f"op('{bindMasterRelativePath}').par['{pGroupName}']"

    ## SET MATRIX UNIFORMS ##
    for i, parGroup in enumerate(GLmatParGroups):
        index = i+GLmatParOffset
        pGroupName = parGroup[0][3].val
        tarpName = target.par[f"matuniname{str(index)}"]
        tarpVal = target.par[f"matvalue{str(index)}"]
        tarpName.val = pGroupName
        tarpVal.mode = ParMode.EXPRESSION
        tarpVal.expr = f"op('{bindMasterRelativePath}').par['{pGroupName}']"

    ## SET ATOMIC COUNTERS ##
    for i, parGroup in enumerate(GLacParGroups):
        index = i+GLacParOffset
        pGroupName = parGroup[0][3].val
        pAtomicType = fromCodeParms[pGroupName, "acinitval"].val
        target.par[f"acname{str(index)}"].val = pGroupName
        target.par[f"acinitval{str(index)}"].val = pAtomicType
        if pAtomicType == "chop":
            target.par[f"chop{str(index)}"].mode = ParMode.EXPRESSION
            target.par[f"acchopval{str(index)}"].expr = f"op('{bindMasterRelativePath}').par['{pGroupName}']"
        else:
            target.par[f"acsingleval{str(index)}"].expr = f"op('{bindMasterRelativePath}').par['{pGroupName}']"

    ## SET CONST ##
    for i, parGroup in enumerate(GLconstParGroups):
        index = i+GLconstParOffset
        pGroupName = parGroup[0][3].val
        tarpName = target.par[f"constname{str(index)}"]
        tarpVal = target.par[f"constvalue{str(index)}"]
        tarpName.val = pGroupName
        tarpVal.mode = ParMode.EXPRESSION
        tarpVal.expr = f"op('{bindMasterRelativePath}').par['{pGroupName}']"

    return

## BUILTIN FUNCTIONS ##


def onOffToOn(channel, sampleIndex, val, prev):
    updateParms()
    return
