from LOAD_SETTINGS import *
import os
glCodeContainer = op(f"{parent.Comp.path}/BUILD_GLSL_CODE")
glPath = glCodeContainer.path

sourcesn = [op(f"{glPath}/UNIFORMS_AS_TEXT"),
            op(f"{glPath}/OUTPUTS"),
            op(f"{glPath}/CODE"),
            op(f"{glPath}/FUNCTIONS")]


def initTempFilePath(sourcesn):

    fileNames = ["inputs", "outputs", "main", "functions"]
    tempFolder = os.path.normpath(f"{var('TEMP')}\\touchtmp")

    targetFolder = os.path.join(
        tempFolder, project.name.split(".")[0], str(nComp.id))

    try:
        os.makedirs(targetFolder)
    except:
        pass

    for i, source in enumerate(sourcesn):
        ext = source.par.extension
        filePath = f'{targetFolder}/{fileNames[i]}.glsl'
        source.par.syncfile = 0
        with open(filePath, 'w') as f:
            f.write(source.text)
        source.par.file = filePath
        source.par.syncfile = 1


def resetKeys(opTable):
    rows = n.rows()
    rows.pop(0)
    for i, row in enumerate(rows):
        oppath = n[i+1, "path"].val
        curOP = op(oppath)
        curOP.par.clear.pulse(1, frames=4)
    return


def onCreate():
    op('Preset_Manager/POP_PRESET').par.Close.pulse(1, frames=4)
    op('Function_Manager/POP_FUNCTION').par.Close.pulse(1, frames=4)
    op(f"{glPath}/UNIFORMS_AS_TEXT").par.syncfile = 0
    op(f"{glPath}/OUTPUTS").par.syncfile = 0
    op(f"{glPath}/CODE").par.syncfile = 0
    op(f"{glPath}/FUNCTIONS").par.syncfile = 0
    initTempFilePath(sourcesn)
    resetKeys = op("RESET_KEYS")
    resetKeys.run(delayFrames=10)

    resetPanel = op('RESET_PANEL')
    op(f"{parent.Comp}/KEYBOARDS_SHORTCUTS/panel5").bypass = True
    resetPanel.run(delayFrames=10)

    try:
        with open(file) as settings:
            vscodePath = json.loads(settings.read())['vscodePath']
            nComp.par.Codeexternaleditorpath = vscodePath
    except:
        with open(file, "w") as settings:
            settings.write(initData)
            nComp.par.Codeexternaleditorpath = json.loads(initData)[
                'vscodePath']

    return


def onStart():
    op('Preset_Manager/POP_PRESET').par.Close.pulse(1, frames=4)
    op('Function_Manager/POP_FUNCTION').par.Close.pulse(1, frames=4)
    op(f"{glPath}/UNIFORMS_AS_TEXT").par.syncfile = 0
    op(f"{glPath}/OUTPUTS").par.syncfile = 0
    op(f"{glPath}/CODE").par.syncfile = 0
    op(f"{glPath}/FUNCTIONS").par.syncfile = 0
    initTempFilePath(sourcesn)

    resetKeys = op("RESET_KEYS")
    resetKeys.run(delayFrames=10)
    resetPanel = op('RESET_PANEL')
    op(f"{parent.Comp}/KEYBOARDS_SHORTCUTS/panel5").bypass = True
    resetPanel.run(delayFrames=10)
