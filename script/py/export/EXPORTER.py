from _stubs import *
from TDJSON import pageToJSONDict, addParametersFromJSONDict, parameterToJSONPar, addParametersFromJSONList
from TDFunctions import getCustomPage

# Source OP
nComp = parent.Comp


def onPulse(par):
    # Create container
    container = nComp.parent().create(containerCOMP, f"{nComp.name}_export")
    
    # Set container position, parent shortcut, color from source
    container.par.parentshortcut = 'Comp'
    container.nodeY = nComp.nodeY - 200
    container.nodeX = nComp.nodeX
    container.color = tuple([x * .75 for x in list(nComp.color)])

    # Get source Pages
    controlsPage = getCustomPage(nComp, 'Controls')
    glslPage = getCustomPage(nComp, 'GLSL')
    globalsPage = getCustomPage(nComp, 'Globals')
    inputsPage = getCustomPage(nComp, 'Inputs')

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

    # Get corresponding nodes
    for node in nComp.children:
        if node.name.startswith(nodeNamesToCopy):
            nodesToCopy.append(node)

    # Batch Copy node in the new container
    nodes = container.copyOPs(nodesToCopy)

    # Set init parameters for the new nodes
    for node in nodes:
        if node.name.startswith(nodeNamesToCopy):
            n = node
            if n.name.startswith('feedbackInputsactive'):
                n.par.reset.bindExpr = 'parent.Comp.par.Inputsresetall'
                n.par.resetpulse.bindExpr = 'parent.Comp.par.Inputsresetall'
            if n.name.startswith('selectInputsactive'):
                texname = n.par.top.val.split('/')[-1:]
                n.par.top.val = f"BUILTINS_INIT/{texname[0]}"
            if n.type in ['in', 'out']:
                n.par.label.mode = ParMode.CONSTANT
                label = nComp.op(node.name).par.label.eval()
                n.par.label.val = label

    # Merge Pages
    pages = [controlsPage, glslPage, globalsPage]

    # Get GLSL OP
    glsln = container.op('glsl1')

    # Copy GLSL Full Code
    glslPixelCodeText = nComp.op('BUILD_GLSL_CODE/OUT_GLSL_COMBINED').text
    glslPixelCoden = container.create(textDAT)
    glslPixelCoden.name = 'GLSL_PIXEL'
    glslPixelCoden.par.language = 'glsl'
    glslPixelCoden.write(glslPixelCodeText)

    # Place GLSL CODE OP
    glslPixelCoden.nodeX = glsln.nodeX
    glslPixelCoden.nodeY = glsln.nodeY-200

    # Set GLSL CODE PATH and Buffer numbers according to source
    glsln.par.pixeldat = glslPixelCoden.name
    glsln.par.computedat = glslPixelCoden.name
    glsln.par.numcolorbufs.mode = ParMode.CONSTANT
    glsln.par.numcolorbufs = nComp.op('glsl1').par.numcolorbufs.eval()

    # Set Panel references
    panel = container.op('PANEL')
    panel.par.component.expr = "parent() if op('..').par.Inputspanelsource == 'internal' else parent().par.Inputspanel"

    # Set First output as Background TOP
    container.par.top = container.op('output1')

    # Set container resolution according to GLSL TOP Resolution
    container.par.w.expr = "op('./GET_INFOS/RES')['resx']"
    container.par.h.expr = "op('./GET_INFOS/RES')['resy']"
    container.par.w.readOnly = True
    container.par.h.readOnly = True
    container.par.top = container.op('output1')

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
    ## END
    return
