from _stubs import *
from TDJSON import addParametersFromJSONDict
from TDFunctions import getCustomPage

def loadPreset(presetDict, comp=parent.Comp):
    feedbacksRep  = comp.op('FEEDBACK_REPLICATOR')
    ntarUniforms  = comp.op('BUILD_GLSL_CODE/UNIFORMS_AS_TEXT')
    ntarFunctions = comp.op('BUILD_GLSL_CODE/FUNCTIONS')
    ntarOutputs   = comp.op('BUILD_GLSL_CODE/OUTPUTS')
    ntarCode      = comp.op('BUILD_GLSL_CODE/CODE')

    page = getCustomPage(comp, 'Controls')
    inputPage = getCustomPage(comp, 'Inputs')
    outputPage = getCustomPage(comp, 'Outputs')
    ioPages = [inputPage, outputPage]
    for iopage in ioPages:
        for iopar in iopage:
            iopar.val = iopar.default 

    if page:
        page.destroy()
    comp.appendCustomPage('Controls')
    comp.sortCustomPages('Controls', 'Code', 'Inputs', 'Outputs', 'GLSL', 'Globals' )

    currentPreset = presetDict

    # Make old presets compatible
    if 'codetabs' in currentPreset:
        uniformsCode =  currentPreset['codetabs']['inputs']
        functionsCode = currentPreset['codetabs']['function']
        outputsCode =   currentPreset['codetabs']['outputs']
        mainCode =      currentPreset['codetabs']['main']

    # Old preset scheme
    else:
        uniformsCode =  currentPreset['UNIFORMS_CODE']
        functionsCode = currentPreset['FUNCTIONS_CODE']
        outputsCode =   currentPreset['OUTPUTS_CODE']
        mainCode =      currentPreset['MAIN_CODE']

    if 'pars' in currentPreset:
        parameters = currentPreset['pars']

    # Old preset scheme
    else:
        parameters = currentPreset
        del parameters['UNIFORMS_CODE']
        del parameters['FUNCTIONS_CODE']
        del parameters['OUTPUTS_CODE']
        del parameters['MAIN_CODE']

    loadCode(ntarUniforms, uniformsCode)
    loadCode(ntarFunctions, functionsCode)
    loadCode(ntarOutputs, outputsCode)
    loadCode(ntarCode, mainCode)
    addParametersFromJSONDict(comp, parameters, setValues=True, newAtEnd=False)

    feedbacksRep.par.recreateall.pulse()
    return

def loadCode(targetOP, textContent):
    targetOP.par.syncfile = 0
    targetOP.clear()
    targetOP.write(textContent)