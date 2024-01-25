from TDJSON import opToJSONOp, addParametersFromJSONOp
from LOAD_PRESET import loadPreset
def onTableChange(dat):
	from LOAD_PRESET import loadPreset
	preset = ''
	path = dat[0, 0].val
	isInstance = parent.Comp.op('UI/HEADER/GET_IS_INSTANCE')[0, 0].val
	isFollow = parent.Comp.op('UI/HEADER/btn_follow_selection').par.Value0.val == 1
	if isInstance == 'True' and isFollow :
		tarn = op(path)
		preset = tarn.storage['preset']
		curPar = opToJSONOp(tarn, extraAttrs=['val', 'expr', 'bindExpr'], forceAttrLists=True, includeCustomPages=True, includeBuiltInPages=False)
		loadPreset(preset['lastExportState'])
		addParametersFromJSONOp(parent.Comp, curPar, setValues=True, newAtEnd=False, fixParNames=True)
		
