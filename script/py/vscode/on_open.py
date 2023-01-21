from _stubs import *
from utils import *

tempFolder = path.normpath(f"{homePath}\\.cache")
targetFolder = path.join(tempFolder, project.name.split(".")[0], project.name.split(".")[1], str(f"{nComp.name}_{nComp.id}"))

try:
	makedirs(targetFolder)
except:
	pass
	
for i, source in enumerate(sourcesn):
	ext = source.par.extension
	filePath = f'{targetFolder}/{fileNames[i]}.{ext}'
	with open(filePath, 'w') as f:
		f.write(source.text)
	source.par.file = filePath
	source.par.syncfile = 1

# Open new Visual Studio Code Instance with a brand new environments located in your Pixel-Wrangle USER folder
openVSCode(targetFolder)

# Get configs paths
extjson = Path(str(extensionsPath) + '/extensions.json')
settingsjson = Path(str(userDataPath) + '/User/settings.json')
keybindingsjson = Path(str(userDataPath) + '/User/keybindings.json')


# If environment does not exist, initialize with Pixel-Wrangle default settings, keybindings, extensions
if(extjson.exists() == True):
	isEmpty = False
	
	with open(str(extjson), 'r') as f:
		text = f.read()
		if text == '[]':
			isEmpty = True
	# Init extensions
	if isEmpty == True:
		original = str(Path(str(pwPath) + '/vscode/extensions.json'))
		target = str(Path(str(extensionsPath) + '/extensions.json'))
		copyfile(original, target)

else:
	extensionsPath.mkdir(parents=True, exist_ok=True)
	original = str(Path(str(pwPath) + '/vscode/extensions.json'))
	target = str(Path(str(extensionsPath) + '/extensions.json'))
	copyfile(original, target)

if(settingsjson.exists() == True):
	pass
else:
	# Init settings
	Path(str(userDataPath) + '/User').mkdir(parents=True, exist_ok=True)
	original = str(Path(str(pwPath) + '/vscode/settings.json'))
	target = str(Path(str(settingsjson)))
	copyfile(original, target)

if(keybindingsjson.exists() == True):
	pass
else:
	# Init keybindings
	Path(str(userDataPath) + '/User').mkdir(parents=True, exist_ok=True)
	original = str(Path(str(pwPath) + '/vscode/keybindings.json'))
	target = str(Path(str(keybindingsjson)))
	copyfile(original, target)