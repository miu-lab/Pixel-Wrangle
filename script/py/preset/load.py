from _stubs import *
from TDJSON import textToJSON, addParametersFromJSONDict
from TDFunctions import getCustomPage

def loadPreset(presetDict, comp=parent.Comp):
    feedbacksRep = op(f'{comp.path}/FEEDBACK_REPLICATOR')
    ntarUniforms = op(f'{comp.path}/BUILD_GLSL_CODE/UNIFORMS_AS_TEXT')
    ntarFunctions = op(f'{comp.path}/BUILD_GLSL_CODE/FUNCTIONS')
    ntarOutputs = op(f'{comp.path}/BUILD_GLSL_CODE/OUTPUTS')
    ntarCode = op(f'{comp.path}/BUILD_GLSL_CODE/CODE')

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
    else:
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
    
    ntarUniforms.par.syncfile = 0
    ntarUniforms.clear()
    ntarUniforms.write(uniformsCode)
    
    ntarFunctions.par.syncfile = 0
    ntarFunctions.clear()
    ntarFunctions.write(functionsCode)
    
    ntarOutputs.par.syncfile = 0
    ntarOutputs.clear()
    ntarOutputs.write(outputsCode)
    
    ntarCode.par.syncfile = 0
    ntarCode.clear()
    ntarCode.write(mainCode)
    
    addParametersFromJSONDict(comp, parameters, setValues=True, newAtEnd=False)

    feedbacksRep.par.recreateall.pulse()
    return