import json
from platform import system
nComp = parent.Comp

file = f'{parent.Comp.par.Codelibrarypath.eval()}/settings.json'
vscodePath = ''
defaultvscodePath = f"{'/'.join(var('MYDOCUMENTS').split('/')[:-1])}/AppData/Local/Programs/Microsoft VS Code/Code.exe"

if system == 'darwin':
	defaultvscodePath = "/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code"

initData = json.dumps({ "vscodePath" : defaultvscodePath }, indent=4)