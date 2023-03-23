from LOAD_SETTINGS import *
from pathlib import Path
from PRESET_UTILS import buildPreset	

import os

sourcesn = [iop.uniform,
            iop.outputs,
            iop.code,
            iop.function]

glCodeContainer = op(f"{parent.Comp.path}/BUILD_GLSL_CODE")
glPath = glCodeContainer.path
opid = parent.Comp.id

def initStorage():
    try:
        op.pwstorage.valid
    except Exception:
        parent = op('/').create(baseCOMP, 'storage')
        tarn = parent.create(baseCOMP, 'Pixel_Wrangle')
        tarn.par.opshortcut = 'pwstorage'

def initStorageOP(comp=parent.Comp):
    lastState = buildPreset(comp)
    op.pwstorage.store(comp.path, {'opid':comp.id, 'lastState':lastState, 'connections' : {'inputs' : [], 'outputs': []}})

def savePresetInStorage(comp=parent.Comp):
    opid = comp.id
    oppath = comp.path
    inputs = [{'index': x.index, 'op':x.connections[0].owner.path if len(x.connections) >= 1 else None} for x in comp.inputConnectors]
    outputs = [{'index': x.index, 'op':x.connections[0].owner.path if len(x.connections) >= 1 else None} for x in comp.outputConnectors]

    lastState = buildPreset(comp)
    op.pwstorage.store(oppath, {'opid':opid, 'lastState':lastState, 'connections' : {'inputs' : inputs, 'outputs': outputs}})

def resetKeys(opTable):
    rows = n.rows()
    rows.pop(0)
    for i, row in enumerate(rows):
        oppath = n[i+1, "path"].val
        curOP = op(oppath)
        curOP.par.clear.pulse(1, frames=1)
    return

def retrieveConnections(inputs, outputs):
    if len(inputs)>0:
        for i in inputs:
            index = i['index']
            tarn = i['op']
            parent.Comp.inputCOMPConnectors[index].connect(op(tarn))
    if len(outputs)>0:
        for o in outputs:
            index = o['index']
            tarn = o['op']
            parent.Comp.outputCOMPConnectors[index].connect(op(tarn))


def createUserDirectories():
    Path(parent.Comp.par.Codeuserpresetpath.eval()).mkdir(parents=True, exist_ok=True)
    Path(parent.Comp.par.Codeuserfunctionpath.eval()).mkdir(parents=True, exist_ok=True)
    if (
        Path(f'{parent.Comp.par.Codeuserpath.eval()}/Macros.glsl').exists
        != True
    ):
        with open(str(Path(f'{parent.Comp.par.Codeuserpath.eval()}/Macros.glsl')), 'w') as f:
            f.write('/* USER MACROS */\n')

def onCreate():
    initStorage()
    initStorageOP()
    createUserDirectories()
    resetKeys = op("RESET_KEYS")
    resetKeys.run(delayFrames=10)

    resetPanel = op('RESET_PANEL')
    op(f"{parent.Comp}/KEYBOARDS_SHORTCUTS/panel5").bypass = True
    resetPanel.run(delayFrames=10)

    try:
        with open(file) as settings:
            vscodePath = json.loads(settings.read())['vscodePath']
            nComp.par.Codeexternaleditorpath = vscodePath
    except Exception:
        with open(file, "w") as settings:
            settings.write(initData)
            nComp.par.Codeexternaleditorpath = json.loads(initData)[
                'vscodePath']

    return


def onStart():
    from LOAD_PRESET import loadPreset
    initStorage()
    preset = op.pwstorage.fetch(parent.Comp.path)
    try:
        loadPreset(preset['lastState'])
    except Exception:
        pass
    createUserDirectories()
    resetKeys = op("RESET_KEYS")
    resetKeys.run(delayFrames=10)
    resetPanel = op('RESET_PANEL')
    op(f"{parent.Comp}/KEYBOARDS_SHORTCUTS/panel5").bypass = True
    resetPanel.run(delayFrames=15)
    run('parent.Comp.op("ON_CODE_CHANGE").par.active = 1', delayMilliSeconds=150)
    op('UPDATE_GLSL_PARMS').run(delayFrames=60)
    
def onProjectPreSave():
    from LOAD_PRESET import loadPreset
    initStorage()
    savePresetInStorage(parent.Comp)
    
def onExit():
    initStorage()
    savePresetInStorage(parent.Comp)

