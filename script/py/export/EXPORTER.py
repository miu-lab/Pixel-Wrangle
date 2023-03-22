from _stubs import *
from TDJSON import pageToJSONDict, addParametersFromJSONDict, parameterToJSONPar, addParametersFromJSONList, destroyOtherPagesAndParameters
from TDFunctions import getCustomPage
from PRESET_UTILS import buildPreset

def getSelectedInstance(parent=parent.Comp):
    tarn = op(parent.op('UI/HEADER/GET_SELECTED_OP')[0, 0].val)
    if tarn != None and 'preset' in tarn.storage:
        return op(parent.op('UI/HEADER/GET_SELECTED_OP')[0, 0].val)
    else:
        return None

def setContainer(src=parent.Comp, name=f"{parent.Comp.name}_export"):
    container = getSelectedInstance()
    # If container does not exist, create it
    if container == None:
        container = src.parent().create(containerCOMP, name)
        # Set container position, parent shortcut, color from source
        container.par.parentshortcut = 'Comp'
        container.nodeY = src.nodeY - 200
        container.nodeX = src.nodeX
        container.color = tuple([x * .75 for x in list(src.color)])
    
    # else reset container
    else:
        childs = container.ops('*')
        destroyOtherPagesAndParameters(container, [], [])
        for op in childs:
            if op.valid:
                op.destroy()

    # Get source Pages
    controlsPage = getCustomPage(src, 'Controls')
    glslPage = getCustomPage(src, 'GLSL')
    globalsPage = getCustomPage(src, 'Globals')
    inputsPage = getCustomPage(src, 'Inputs')

    # Inputs Page parameters to keep
    inputsFilteredPage = []
    pFilterList = ["Inputstimeh",
                    "Inputsplay",
                    "Inputstimedep",
                    "Inputspanelh",
                    "Inputspanelsource",
                    "Inputspanel",
                    "Inputssmooth",
                    "Inputssmoothlag",
                    "Inputsglobalh",
                    "Inputsresetall"]

    for p in inputsPage:
        if p.name in pFilterList:
            inputsFilteredPage.append(parameterToJSONPar(
                p, extraAttrs="*", forceAttrLists=True))

    # Set nodename patterns to copy
    nodeNamesToCopy = ('renderselect', 'selectInputsactive', 'Inputsactive',
                        'feedbackInputsactive', 'cache', 'output', 'local',  'commenth', 'glsl1', 'BUILTINS_INIT', 'MOUSE', 'PANEL')

    nodesToCopy = []
    nodesToUpdate = []
    activeOutputs = []
    # Get corresponding nodes
    for node in src.children:
        if node.name.startswith(nodeNamesToCopy):
            if container.op(node.name) == None:
                nodesToCopy.append(node)
            elif node.OPType == 'glslmultiTOP' and container.op(node.name):
                container.op(node.name).destroy()
                nodesToCopy.append(node)
            else:
                nodesToUpdate.append(container.op(node.name))
            if node.name.startswith('output'):
                activeOutputs.append(node.digits)

    # print(nodesToCopy)
    # print(nodesToUpdate)
    # Batch Copy node in the new container
    nodes = container.copyOPs(nodesToCopy) + nodesToUpdate
    toDestroyOuts = []
    # Set init parameters for the new nodes
    for node in nodes:
        if node.name.startswith(nodeNamesToCopy):
            n = node
            if n.name.startswith('feedbackInputsactive'):
                n.par.reset.bindExpr = 'parent.Comp.par.Inputsresetall'
                n.par.resetpulse.bindExpr = 'parent.Comp.par.Inputsresetall'
            if n.name.startswith('selectInputsactive'):
                n.par.top.val = src.op(n.name).par.top.eval()
            if n.type in ['in', 'out']:
                n.par.label.mode = ParMode.CONSTANT
                label = src.op(node.name).par.label.eval()
                n.par.label.val = label
            if n.name in ['local', 'PANEL', 'MOUSE']:
                n.nodeY = 1800
            if n.name in ['BUILTINS_INIT']:
                n.nodeY = 2000
            if n.name.startswith(('renderselect','cache')) and n.digits not in activeOutputs:
                toDestroyOuts.append(n)

    # Merge Pages
    pages = [controlsPage, glslPage, globalsPage]

    # Destroy unnecessary Outputs
    for n in toDestroyOuts:
        n.destroy()

    # Get GLSL OP
    glsln = container.op('glsl1')
    glslCodeOPName = 'GLSL_PIXEL'
    # Copy GLSL Full Code
    glslPixelCodeText = src.op('BUILD_GLSL_CODE/OUT_GLSL_COMBINED').text
    
    try:
        glslPixelCoden = container.op(glslCodeOPName)
        glslPixelCoden.text = glslPixelCodeText
    except:
        glslPixelCoden = container.create(textDAT)
        glslPixelCoden.name = 'GLSL_PIXEL'
        glslPixelCoden.par.language = 'glsl'
        glslPixelCoden.text = glslPixelCodeText

    # Place GLSL CODE OP
    glslPixelCoden.nodeX = glsln.nodeX
    glslPixelCoden.nodeY = glsln.nodeY-200

    # Set GLSL CODE PATH and Buffer numbers according to source
    glsln.par.pixeldat = glslPixelCoden.name
    glsln.par.computedat = glslPixelCoden.name
    glsln.par.numcolorbufs.mode = ParMode.CONSTANT
    glsln.par.numcolorbufs = src.op('glsl1').par.numcolorbufs.eval()

    # Copy Macros and builtins
    if container.op('FACTORY_MACROS') != None:
        macroFactoryOP = container.op('FACTORY_MACROS')
    else:
        macroFactorySrc = src.op('BUILD_GLSL_CODE/FACTORY_MACROS')
        macroFactoryOP = container.copy(macroFactorySrc)
        macroFactoryOP.nodeX = glsln.nodeX - 200
        macroFactoryOP.nodeY = glsln.nodeY - 100
    
    if container.op('USER_MACROS') != None:
        macroUserSrc = src.op('BUILD_GLSL_CODE/USER_MACROS')
        macroUserOP = container.op('USER_MACROS')
        macroUserOP.par.file = macroUserSrc.par.file.eval()
        macroUserOP.par.syncfile = False
    else:
        macroUserSrc = src.op('BUILD_GLSL_CODE/USER_MACROS')
        macroUserOP = container.copy(macroUserSrc)
        macroUserOP.nodeX = glsln.nodeX - 200
        macroUserOP.nodeY = glsln.nodeY - 200
        macroUserOP.par.file = macroUserSrc.par.file.eval()
        macroUserOP.par.syncfile = False
    
    if container.op('BUILTIN_UNIFORMS') != None:
        builtinUniformsSrc = container.op('BUILTIN_UNIFORMS')
    else:
        builtinUniformsSrc = src.op('BUILD_GLSL_CODE/BUILTIN_UNIFORMS')
        builtinUniformOP = container.copy(builtinUniformsSrc)
        builtinUniformOP.nodeX = glsln.nodeX - 200
        builtinUniformOP.nodeY = glsln.nodeY - 300

    # Set Panel references
    panel = container.op('PANEL')
    panel.par.component.expr = "parent() if op('..').par.Inputspanelsource == 'internal' else parent().par.Inputspanel"
	
	# Set Mouse reference from parent panel
    container.op('MOUSE/VIEWER_MOUSE').par.panels.expr = 'parent.Comp'

    # Set First output as Background TOP
    container.par.top = container.op('output1')

    # Set container resolution according to GLSL TOP Resolution
    container.par.w.expr = "op('./GET_INFOS/RES')['resx']"
    container.par.h.expr = "op('./GET_INFOS/RES')['resy']"
    container.par.w.readOnly = True
    container.par.h.readOnly = True
    container.par.top = container.op('output1')
    container.par.opshortcut.expr = 'f"pwexport_{me.id}"'
    container.par.opshortcut.readOnly = True

    # Set Viewer on parent container
    container.viewer = True

    # Set Parameter pages on parent
    for page in pages:
        addParametersFromJSONDict(container, pageToJSONDict(
            page, extraAttrs="*", forceAttrLists=True))
    addParametersFromJSONList(container, inputsFilteredPage)

    # # Sort pages
    if len(controlsPage.pars) > 0:
        container.sortCustomPages('Controls', 'Inputs', 'GLSL', 'Globals')
    else:
        container.sortCustomPages('Inputs', 'GLSL', 'Globals')

    # Update Storage
    container.store('preset', {'lastExportState' : buildPreset(src)} )
    return

def onPulse(par):
    # Source OP
    src = parent.Comp
    parent.Comp.op('UI/HEADER/pop_set_name').Open()
    setContainer(src)
    return

def onSelect(info):
    src = parent.Comp
    if info ['button'] == "OK":
        name = info['enteredText'].replace(' ', '_')
        setContainer(src, name)

def onOpen(info):
    src = parent.Comp
    if getSelectedInstance() != None:
        parent.Comp.op('pop_set_name').Close()
        setContainer(src)
    else:
        pass

# def onClose(info):
#	"""Dialog has been closed"""
# 	pass
