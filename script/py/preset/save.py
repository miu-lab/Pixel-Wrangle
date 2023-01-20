from _stubs import *
import TDJSON
import TDFunctions
from pathlib import Path, PurePosixPath
# Par Node
comp = parent.Comp


def buildPreset(fromComp):

    # Get Pages
    controlsPage = TDFunctions.getCustomPage(fromComp, "Controls")
    inputsPage = TDFunctions.getCustomPage(fromComp, "Inputs")
    outputsPage = TDFunctions.getCustomPage(fromComp, "Outputs")
    glslPage = TDFunctions.getCustomPage(fromComp, "GLSL")
    globalPage = TDFunctions.getCustomPage(fromComp, "Globals")

    # Build Parms Settings
    extraKeys = ["mode", "val", "expr", "bindExpr", "isDefault"]

    controlsParDict = TDJSON.pageToJSONDict(
        controlsPage, forceAttrLists=True, extraAttrs=extraKeys
    )
    inputsParDict = TDJSON.pageToJSONDict(
        inputsPage, forceAttrLists=True, extraAttrs=extraKeys)
    outputsParDict = TDJSON.pageToJSONDict(
        outputsPage, forceAttrLists=True, extraAttrs=extraKeys)
    glslParDict = TDJSON.pageToJSONDict(
        glslPage, forceAttrLists=True, extraAttrs=extraKeys)
    globalParDict = TDJSON.pageToJSONDict(
        glslPage, forceAttrLists=True, extraAttrs=extraKeys)

    # Get Code Pages
    functionsText = op("GET_FUNCTIONS").text
    uniformsText = op("GET_UNIFORMS").text
    outputsText = op("GET_OUTPUTS").text
    mainText = op("GET_MAIN").text

    # Init dict containers
    dicts = {"ctrls": controlsParDict, "in": inputsParDict,
             "out": outputsParDict, "gl": glslParDict, "global": globalParDict}
    currentPreset = {}

    # Keys to keep for static parameters
    inOutSavedkeys = [
        "val",
        "expr",
        "bindExpr",
        "mode",
        "name",
        "style",
        "page",
        "label",
        "size",
    ]

    for pageKey, pageDict in dicts.items():

        if pageKey == "ctrls":
            for parmKey, parmValue in pageDict.items():
                currentPreset[parmKey] = parmValue

        if pageKey in ["in", "out", "gl", "global"]:
            for parmKey, parmValue in pageDict.items():
                if parmValue["isDefault"] == True and parmKey != 'Glmode':
                    continue
                else:
                    # Keep only non-default parms
                    toRemoveKeys = [
                        x for x in list(parmValue.keys()) if x not in inOutSavedkeys
                    ]
                    [parmValue.pop(x, None) for x in toRemoveKeys]
                    currentPreset[parmKey] = parmValue

    # Merge Code blocks to preset
    currentPreset["UNIFORMS_CODE"] = uniformsText
    currentPreset["FUNCTIONS_CODE"] = functionsText
    currentPreset["OUTPUTS_CODE"] = outputsText
    currentPreset["MAIN_CODE"] = mainText

    return currentPreset


# def onSelect(info):
#     if info['button'] == 'Save':
#         name = info["enteredText"]
#         currentPreset = buildPreset(comp)
#         with open(f"{comp.par.Codeuserpresetpath}/{name}.json", "w") as f:
#             f.write(TDJSON.jsonToText(currentPreset))
#     else:
#         pass

def onSelect(info):
    if info['button'] == 'Save':
        currentPreset = buildPreset(comp)
        name = str(PurePosixPath(info["enteredText"]).name)
        path = parent.Comp.par.Codeuserpresetpath
        relpath = ''

        try:
            relpath = op('SAVE_TO_PATH')[1, 'relpath'].val
            path = f"{path}/{relpath}"
        except:
            pass
        if '/' in str(PurePosixPath(info["enteredText"])):
            folder = PurePosixPath(f"{path}/{PurePosixPath(info['enteredText'])}").parent
            Path(str(folder)).mkdir(parents=True, exist_ok=True)
            path = folder

        with open(f"{path}/{name}.json", "w") as f:
            f.write(TDJSON.jsonToText(currentPreset))
