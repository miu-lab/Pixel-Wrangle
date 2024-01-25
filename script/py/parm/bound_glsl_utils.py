from pprint import pprint

from re import findall

## CUSTOM FUNCTIONS ##
def getUntouched(refTable, offset):
    result = []
    for row in refTable.rows():
        val = row[0].val
        digit = int(findall(r"\d+", val)[0])
        if digit < offset:
            result.append(val)
    return result


def resetParms(refTable, targetGLSL, offset):
    untouched = getUntouched(refTable, offset)
    for row in refTable.rows():
        if row[0].val not in untouched:
            p = targetGLSL.par[row[0].val]
            p.bindExpr = ""
            p.expr = ""
            p.mode = ParMode.CONSTANT
            if p.style in [
                "SOP",
                "PanelCOMP",
                "Python",
                "TOP",
                "MAT",
                "COMP",
                "CHOP",
                "File",
                "Folder",
                "Str",
                "StrMenu",
            ]:
                p.val = ""
            else:
                p.val = 0


def getCellValue(dat, row, search, refRow=0):
    return row[dat.findCell(search, rows=[refRow]).col].val


def getParGroups(parmList, namesRow, selectedColName="pargroup"):
    if type(selectedColName) == int:
        rmDouble = {k[selectedColName].val: v for v, k in enumerate(reversed(parmList))}
    elif type(selectedColName) == str:
        index = [name.val for name in namesRow].index(selectedColName)
        selectedColName = index
        rmDouble = {k[selectedColName].val: v for v, k in enumerate(reversed(parmList))}
    sortedKeys = sorted(rmDouble, key=rmDouble.get, reverse=True)
    result = []
    for pGroupName in sortedKeys:
        parGroup = [p for p in parmList if p[selectedColName].val == pGroupName]
        result.append(parGroup)
    return result

def buildTargetName(index, ptype):
    #build type dict
    #get current ptype
    #
    pass

def setAtomicCounters(
    target, fromCodeParms, bindMasterRelativePath, GLacParOffset, GLacParGroups
):
    for i, parGroup in enumerate(GLacParGroups):
        index = i + GLacParOffset
        pGroupName = parGroup[0][3].val
        pAtomicType = fromCodeParms[pGroupName, "acinitval"].val
        target.par[f"ac{str(index)}name"].val = pGroupName # 2022 -> f"acname{str(index)}"
        target.par[f"ac{str(index)}initvalue"].val = pAtomicType # 2022 -> f"acinitval{str(index)}"
        if pAtomicType == "chop":
            target.par[
                f"ac{str(index)}chopvalue" # 2022 -> f"acchopval{str(index)}"
            ].expr = f"op('{bindMasterRelativePath}').par['{pGroupName}']"
        else:
            target.par[
                f"ac{str(index)}singlevalue" # 2022 -> f"acsingleval{str(index)}"
            ].expr = f"op('{bindMasterRelativePath}').par['{pGroupName}']"


def setExpression(pGroupName, tarpName, tarpVal, bindMasterRelativePath):
    tarpName.val = pGroupName
    tarpVal.mode = ParMode.EXPRESSION
    tarpVal.expr = f"op('{bindMasterRelativePath}').par['{pGroupName}']"


def setVulkanConstants(
    target, bindMasterRelativePath, GLconstParOffset, GLconstParGroups
):
    for i, parGroup in enumerate(GLconstParGroups):
        index = i + GLconstParOffset
        pGroupName = parGroup[0][3].val
        tarpName = target.par[f"const{str(index)}name" ] # 2022 -> f"constname{str(index)}"
        tarpVal = target.par[f"const{str(index)}value"] # 2022 -> f"constvalue{str(index)}"
        setExpression(pGroupName, tarpName, tarpVal, bindMasterRelativePath)


def setMatrices(target, bindMasterRelativePath, GLmatParOffset, GLmatParGroups):
    for i, parGroup in enumerate(GLmatParGroups):
        index = i + GLmatParOffset
        tarpName = target.par[f"matrix{str(index)}name"] # 2022 -> f"matuniname{str(index)}"
        tarpVal = target.par[f"matrix{str(index)}value"] # 2022 -> f"matvalue{str(index)}"
        pGroupName = parGroup[0][3].val
        setExpression(pGroupName, tarpName, tarpVal, bindMasterRelativePath)


def setArrays(
    target, fromCodeParms, bindMasterRelativePath, GLarrayParOffset, GLarrayParGroups
):
    for i, parGroup in enumerate(GLarrayParGroups):
        index = i + GLarrayParOffset
        pGroupName = parGroup[0][3].val
        pArrayType = fromCodeParms[pGroupName, "arraytype"].val
        pArrayValueType = fromCodeParms[pGroupName, "vtype"].val
        pArrayChop = fromCodeParms[pGroupName, "chop"].val
        target.par[f"array{str(index)}name"].val = pGroupName # 2022 -> f"chopuniname{str(index)}"
        target.par[f"array{str(index)}arraytype"].val = pArrayType # 2022 -> f"choparraytype{str(index)}"
        target.par[f"array{str(index)}type"].val = pArrayValueType # 2022 -> f"chopunitype{str(index)}"
        if pArrayChop:
            target.par[f"array{str(index)}chop"].mode = ParMode.EXPRESSION # 2022 -> f"chop{str(index)}"
            target.par[
                f"array{str(index)}chop" # 2022 -> f"chop{str(index)}"
            ].expr = f"op('{bindMasterRelativePath}').par['{pGroupName}']"


def setUniforms(target, source, bindMasterRelativePath, GLUniParOffset, GLuniParGroups):
    for i, parGroup in enumerate(GLuniParGroups):
        uniComponent = ["x", "y", "z", "w"]
        index = i + GLUniParOffset
        pGroupName = parGroup[0][3].val
        target.par[f"vec{str(index)}name"].val = pGroupName  # 2022 -> f"uniname{str(index)}"

        ## BIND EACH PARM COMPONENTS ##
        for j, p in enumerate(parGroup):
            pName = getCellValue(source, p, "name")
            targetp = target.par[f"vec{str(index)}value{uniComponent[j]}" ] # 2022 -> f"value{str(index)}{uniComponent[j]}"
            targetp.mode = ParMode.EXPRESSION
            targetp.expr = f"op('{bindMasterRelativePath}').par['{pName}']"


def setParameterSection(
    fromCodeParms,
    parGroups,
    GLuniParGroups,
    GLarrayParGroups,
    GLmatParGroups,
    GLacParGroups,
    GLconstParGroups,
):
    for parGroup in parGroups:
        pGroupName = parGroup[0][3].val
        pGLType = fromCodeParms[pGroupName, "gl_type"].val
        pIsArray = fromCodeParms[pGroupName, "array"].val
        # Array uniform type
        if pIsArray == "1":
            GLarrayParGroups.append(parGroup)
        elif pGLType == "mat":
            GLmatParGroups.append(parGroup)
        elif pGLType == "ac":
            GLacParGroups.append(parGroup)
        elif pGLType == "const":
            GLconstParGroups.append(parGroup)
        else:
            GLuniParGroups.append(parGroup)


def resetParameters(target, toResetParms):
    for toReset in toResetParms:
        curParmOP = toReset["op"]
        offset = toReset["offset"]
        resetParms(curParmOP, target, offset)
