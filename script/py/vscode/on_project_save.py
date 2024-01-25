
from utils import *


def onProjectPostSave():
    from utils import vscodeInstance

    tempFolder = path.normpath(f"{homePath}\\.cache")

    projectname = project.name.split(".")[0]
    projectVersion = project.name.split(".")[1]

    try:
        projectVersion = int(projectVersion)
    except Exception:
        projectVersion = 0

    targetFolder = path.join(
        tempFolder,
        f"{projectname}_{getID(project.folder)}",
        str(projectVersion),
        str(f"{nComp.name}_{nComp.id}"),
    )

    # Update VSCode process targetting the new folder if vscode window is already open, else pass
    try:
        if vscodeInstance.poll() == 0:
            vscodeInstance.kill()
        else:
            vscodeInstance.kill()
            vscodeInstance = openVSCode(targetFolder)
    except Exception:
        pass

    try:
        makedirs(targetFolder)
    except Exception:
        pass

    for i, source in enumerate(sourcesn):
        ext = source.par.extension
        filePath = f"{targetFolder}/{fileNames[i]}.{ext}"
        source.par.syncfile = 0
        with open(filePath, "w") as f:
            f.write(source.text)
        source.par.file = filePath
        source.par.syncfile = 1
    return


def onCreate():
    onProjectPostSave()


def onStart():
    onProjectPostSave()
