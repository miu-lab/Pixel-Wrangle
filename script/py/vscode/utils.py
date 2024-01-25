from pathlib import Path
from subprocess import Popen
from shutil import copyfile
from os import path, makedirs
from pprint import pprint

# from stackoverflow.com/questions/22974499/generate-id-from-string-in-python
def getID(string: str, last_idx: int = 6) -> str:
    import hashlib

    m = hashlib.md5()
    string = string.encode("utf-8")
    m.update(string)
    unique_name: str = str(int(m.hexdigest(), 16))[:last_idx]
    return unique_name

homePath = Path(parent.Comp.par.Codeuserpath.eval())
pwPath = Path(parent.Comp.par.Codelibrarypath.eval())
envPath = '.vscode'
userDataFolder = 'userdata'
extensionsFolder = 'extensions'
userDataPath = homePath.joinpath(envPath).joinpath(userDataFolder)
extensionsPath = homePath.joinpath(envPath).joinpath(extensionsFolder)

try:
    userDataPath.mkdir()
except Exception:
    pass

try:
    extensionsPath.mkdir()
except Exception:
    pass

nComp = parent.Comp

glCodeContainer = op(f"{parent.Comp.path}/BUILD_GLSL_CODE")
glPath = glCodeContainer.path

Inputsn = op(f"{glPath}/UNIFORMS_AS_TEXT")
Outputsn = op(f"{glPath}/OUTPUTS")
Mainn = op(f"{glPath}/CODE")
Functionsn = op(f"{glPath}/FUNCTIONS")

sourcesn 	= [Inputsn, Outputsn, Mainn, Functionsn]
fileNames  = ["inputs", "outputs", "main", "functions" ]
userdata = userDataPath
extensions = extensionsPath
vscodeenvcmd = "--user-data-dir"
vscodeextcmd = "--extensions-dir"
vscode = nComp.par.Codeexternaleditorpath.val
vscodeInstance = ''
vscode = nComp.par.Codeexternaleditorpath.val
vscodeInstance = ""


def openVSCode(targetFolder):
    global vscodeInstance
    vscodeInstance = Popen(
        [vscode, vscodeenvcmd, userdata, vscodeextcmd, extensions, targetFolder]
    )
    return vscodeInstance
