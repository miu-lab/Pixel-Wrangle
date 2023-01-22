from _stubs import *
from utils import *

def onProjectPostSave():
	from utils import vscodeInstance
	tempFolder = path.normpath(f"{homePath}\\.cache")
	targetFolder = path.join(tempFolder, project.name.split(".")[0], project.name.split(".")[1], str(f"{nComp.name}_{nComp.id}"))
	
	# Update VSCode process targetting the new folder if vscode window is already open, else pass
	try:
		if vscodeInstance.poll() == 0:
			pass
		else:
			vscodeInstance.kill()
			vscodeInstance = openVSCode(targetFolder)
	except:
		pass

	try:
		makedirs(targetFolder)
	except:
		pass
		
	for i, source in enumerate(sourcesn):
		ext = source.par.extension
		filePath = f'{targetFolder}/{fileNames[i]}.{ext}'
		source.par.syncfile = 0
		with open(filePath, 'w') as f:
			f.write(source.text)
		source.par.file = filePath
		source.par.syncfile = 1
	return

	