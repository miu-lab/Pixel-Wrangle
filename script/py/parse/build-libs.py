from _stubs import *
import itertools
import TDFunctions
from pathlib import PurePosixPath, Path
from re import sub
tarN = op(me.par.dat)


def getUniquePathList(dat, relPathColumn = "relpath"):
	rows = dat.rows()
	rows.pop(0)
	pathList = []
	for id, row in enumerate(rows):
		relPath = tarN[id+1, relPathColumn].val
		if relPath is not None or '':
			splittedPath = relPath.split('/')
			if len(splittedPath) > 1 and relPath.endswith('.glsl'):
				del splittedPath[len(splittedPath)-1]
				pathList.append(splittedPath)
		else:
			pass	
	pathList.sort()
	return ["/".join(x) for x in list(l for l,_ in itertools.groupby(pathList))]


def createFolderStructure(pathList, parent = "/libs"):
	if op(parent) == None:
		parent = op("/").create(baseCOMP, "libs")	
	for path in pathList:
		pathSegments = path.split("/")
		maxDepth = len(pathSegments)
		completePath = []
		for i in range(maxDepth):
			completePath.append(pathSegments[i])
			currentPath = "/".join(completePath)
			if op(f"{parent}/{currentPath}") == None:
				ancestor = PurePosixPath(f"{parent}/{currentPath}").parent
				node = op(str(ancestor)).create(baseCOMP, pathSegments[i])
				TDFunctions.arrangeNode(node, position='left', spacing=20)
			else:
				continue
	return parent


def correctGLSL(filePath):
	with open(filePath) as f:
		originalLines = f.readlines()
		output = []
		for line in originalLines:
			if line.startswith("#include "):
				lineList = line.split(" ")
				posixPath = PurePosixPath(lineList[1].replace('"', "").replace("\n", ""))
				curLineFolder = str(posixPath.parent)
				curLineName = str(posixPath.name)
				curLineName = curLineName.replace(".", "_")
				curLine = f"{curLineFolder}/{curLineName}"
				if curLine.startswith("./"):
					curLine = curLine[2:]
				curLine = f"{lineList[0]} <{curLine}>\n"
				output.append(curLine)
			elif(line.find("texture") != -1):
				line = sub("(texture).*[(]", "texture(", line)
				output.append(line)
			else:
				output.append(line)
		return "".join(output)



def createFiles(root, dat):
	rows = dat.rows()
	rows.pop(0)
	basePath = f"{root}/"
	paths = []
	for i, row in enumerate(rows):
		relPath = PurePosixPath(basePath + dat[i+1, "relpath"].val)
		opPath = str(relPath.parent)
		opName = str(relPath.stem)
		opExt = str(relPath.suffix)
		lang = opExt.replace(".", "")
		targetOP = op(f"{opPath}/{opName}{opExt.replace('.', '_')}")
		if targetOP == None:
			opTarget = dat[i+1, "path"].val
			current = op(opPath).create(textDAT, f"{opName}{opExt.replace('.', '_')}")
			TDFunctions.arrangeNode(current, position='left', spacing=20)
			text = correctGLSL(opTarget)
			formatedFilePath = parent.Comp.par.Codelibrarypath + "/Functions/dist/" + str(dat[i+1, "relpath"].val)
			formatedFile = Path(formatedFilePath)
			formatedFile.parent.mkdir(exist_ok=True, parents=True)
			formatedFile.write_text(text)
			# current.write(text)
			try:
				current.par.file = str(Path(formatedFilePath))
				current.par.file.readOnly = True
				current.par.syncfile = 1
				current.par.syncfile.readOnly = True
				current.par.language = lang.lower()
			except:
				pass
			paths.append(current.path)
		else:
			paths.append(targetOP.path)

	return paths


def updateTable(table, pathlist):
	for id, path in enumerate(pathlist):
		if path != "":
			table[id, 0].val = path
		else:
			continue
	

def onTableChange(dat):
	if len(dat.rows()) > 1:
		table = op("oppaths")
		uniquePathList = getUniquePathList(dat)
		rootFolder = createFolderStructure(uniquePathList)
		pathList = createFiles(rootFolder, dat)
		table.par.rows = len(pathList)
		updateTable(table, pathList)
	return

def onRowChange(dat, rows):
	return

def onColChange(dat, cols):
	return

def onCellChange(dat, cells, prev):
	return

def onSizeChange(dat):
	return
	