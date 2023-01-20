# This file and all related intellectual property rights are
# owned by Derivative Inc. ("Derivative").  The use and modification
# of this file is governed by, and only permitted under, the terms
# of the Derivative [End-User License Agreement]
# [https://www.derivative.ca/Agreements/UsageAgreementTouchDesigner.asp]
# (the "License Agreement").  Among other terms, this file can only
# be used, and/or modified for use, with Derivative's TouchDesigner
# software, and only by employees of the organization that has licensed
# Derivative's TouchDesigner software by [accepting] the License Agreement.
# Any redistribution or sharing of this file, with or without modification,
# to or with any other person is strictly prohibited [(except as expressly
# permitted by the License Agreement)].
#
# Version: 099.2017.30440.28Sep
#
# _END_HEADER_

import json
import collections
import types

NUMATTRS = ('min', 'max', 'normMin', 'normMax', 'clampMin', 'clampMax')
LISTATTRS = NUMATTRS + ('default', 'val', 'eval', 'expr', 'mode',
								 'bindExpr', 'bindMaster', 'exportOP',
								 'exportSource', 'prevMode')

def jsonToText(jsonObject, indent='\t'):
	"""
	Return a JSON object as text

	indent: The indent argument to json.dumps. Defaults to '\t' for readability.
		Set to None for default json.dumps behavior.
	"""
	return json.dumps(jsonObject, indent=indent)

def jsonToDat(jsonObject, dat):
	"""
	Write a JSON object into a dat.
	"""
	dat.text = jsonToText(jsonObject)

def textToJSON(text, orderedDict=False, showErrors=False):
	"""
	Turn a JSON object stored as text into a Python object.
	Will be forced to a Python collections.OrderedDict if orderedDict argument
	is True.
	"""
	try:
		if orderedDict:
			return json.loads(text, object_pairs_hook=collections.OrderedDict)
		else:
			return json.loads(text)
	except:
		if showErrors:
			raise
		else:
			return None

def datToJSON(dat, orderedDict=False, showErrors=False):
	"""
	Returns a JSONable dict from a dat
	"""
	return textToJSON(dat.text, orderedDict, showErrors)

def serializeTDData(data, verbose=True):
	"""
	Return a serializable value for a piece of TD data. Standardizes serialized
	format for TD types OP, Cell, Channel, Page, Par, ParMode.
	:param data: anything
	:param verbose: if True, provide extra details for Cell, Channel, Page, Par
	:return: standardized serializable format or repr(data) if not of type
				listed or int, float, str, long, bool, list, dict None
	"""
	TDObject = True
	if isinstance(data, OP):
		verboseData = ['OP']
		tdData = data.path
	elif isinstance(data, ParMode):
		verboseData = ['ParMode']
		tdData = data.name
	elif isinstance(data, Par):
		verboseData = ['Par', data.owner.path]
		tdData = data.name
	elif isinstance(data, Page):
		verboseData = ['Page', data.owner.path]
		tdData = data.name
	elif isinstance(data, Channel):
		verboseData = ['Channel', data.owner.path]
		tdData = data.name
	elif isinstance(data, Cell):
		verboseData = ['Cell', data.owner.path]
		tdData = [data.row, data.col]
	else:
		TDObject = False
	if TDObject:
		if verbose:
			verboseData.append(tdData)
			return verboseData
		else:
			return tdData
	elif isinstance(data, (int, float, str, bool, type(None), list, dict)):
		return data
	else:
		return repr(data)

def deserializeTDData(data, verboseData=None):
	"""
	return a TD object if data is in format returned by serializeTDData
		method with verbose=True. If verbose was not set to True, additionalInfo
		must be provided if a TD object is to be returned. If a TD object is not
		returned, data will be retuned unchanged.
	:param data: anything
	:param verboseData: The following lists must be provided to get a TD
		object back for non-verbose data created by serializeTDData:
		Parameter: ['Par', par owner path]
		Page: ['Page', par owner path]
		Channel: ['Channel', channel owner path]
		Cell: ['Cell', cell owner path]
	:return: TD object if appropriate info is provided. Otherwise returns data
		argument unchanged.
	"""
	if verboseData:
		testData = verboseData + [data]
	else:
		testData = data
	if isinstance(testData, list):
		try:
			if testData[0] == 'OP' and len(testData) == 2:
				return op(testData[-1])
			elif testData[0] == 'ParMode' and len(testData) == 2:
				return getattr(ParMode, testData[-1])
			elif testData[0] == 'Par' and len(testData) == 3:
				return getattr(op(testData[1]).par, testData[-1])
			elif testData[0] == 'Page' and len(testData) == 3:
				o = op(testData[1])
				for p in o.customPages:
					if p.name == testData[-1]:
						return p
			elif testData[0] == 'Channel' and len(testData) == 3:
				return op(testData[1])[testData[-1]]
			elif testData[0] == 'Cell' and len(testData) == 3:
				return op(testData[1])[testData[-1][0], testData[-1][1]]
		except:
			return data
	return data

def parameterToJSONPar(p, extraAttrs=None, forceAttrLists=False):
	"""
	Convert a parameter or tuplet to a jsonable python dictionary.
	extraAttrs: a list or tuple of attribute names that are not normally
		stored. For example, 'val' and 'order'. Can also be a string: '*'
		indicating all properties of the parameter.
	forceAttrLists: If True, all attributes will be stored in a list with the
		length of the tuplet
	NOTE: a parameter that is a member of a multi-value tuplet will create a
		JSON for the entire tuplet.
	"""
	# just grab the first parameter if it's a tuplet...
	if isinstance(p, tuple):
		p = p[0]

	parAttrs = ('name', 'label', 'page', 'style', 'size', 'default', 'enable',
				'startSection', 'cloneImmune', 'readOnly', 'enableExpr',
				'help')
	if extraAttrs == '*':
		extraAttrs = []
		for m in dir(p):
			try:
				if not m.startswith('_') and not isinstance(getattr(p, m),
						(types.FrameType, types.BuiltinFunctionType,
						types.MethodType, types.BuiltinMethodType)):
					extraAttrs.append(m)
			except:
				pass		
	numAttrs = NUMATTRS

	# set up special par types
	if p.isMenu:
		if p.menuSource:
			parAttrs += ('menuSource',)
		else:
			parAttrs += ('menuNames', 'menuLabels')
	if p.isNumber:
		parAttrs += numAttrs
	if extraAttrs is not None:
		for a in extraAttrs:
			if a not in parAttrs:
				parAttrs += (a,)

	# create dictionary
	jDict = dict()
	# grab attrs
	for attr in parAttrs:
		if attr == 'size' and (p.style in ('Int', 'Float') or not p.isCustom):
			jDict['size'] = len(p.tuplet)
			continue
		elif attr == 'eval':
			if 'val' not in parAttrs:
				jDict['val'] = serializeTDData(p.eval(), True)
			continue
		try:
			if not hasattr(p, attr):
				continue
		except:
			continue
		attrVal = getattr(p, attr)
		if isinstance(attrVal, (Page, OP, ParMode)):
			jDict[attr] = serializeTDData(attrVal, False)
		elif attr == 'name':
			jDict['name'] = p.tupletName
		elif attr == 'menuSource':
			jDict['menuSource'] = p.menuSource or ''
		elif attr == 'tuplet':
			jDict['tuplet'] = [p.name for p in attrVal]
		# elif isinstance(attrVal, (Cell, Channel, Par)):
		# 	jDict[attr] = serializeTDData(attrVal, True)
		else:
			try:
				jDict[attr] = serializeTDData(attrVal, True)
				# jDict[attr] = getattr(p, attr)
			except:
				pass
	# deal with multi-value parameter stuff
	if forceAttrLists or len(p.tuplet) > 1:
		for attr in LISTATTRS:
			if attr not in numAttrs and attr not in parAttrs:
				continue
			attrList = []
			for multiPar in p.tuplet:
				if attr == 'eval':
					val = multiPar.eval()
				else:
					val = getattr(multiPar, attr)
				attrList.append(serializeTDData(val, attr == 'eval' and
								isinstance(val,(Cell, Channel, Par))))
			if forceAttrLists:
				makeList = True
			else:
				# if we have any differing values, store all as list
				makeList = False
				for i in range(len(attrList) - 1):
					if attrList[i] != attrList[i+1]:
						makeList = True
						break

			if forceAttrLists or makeList:
				jDict['val' if attr == 'eval' else attr] = attrList
	return jDict

def pageToJSONDict(page, extraAttrs=None, forceAttrLists=False):
	"""
	Convert a page of parameters to a jsonable python dict.
		Format: {parameter name: {parameter attributes, ...}, ...}
	extraAttrs is a list or tuple of par attribute names that are not normally
		stored. For example, 'val' and 'order'. Can also be a string: '*'
		indicating all properties of the parameter.
	forceAttrLists: If True, all attributes will be stored in a list with the
		length of the tuplet
	"""
	jPage = dict()
	for p in page.pars:
		# make sure we only do first par in each tuplet
		# and you must test by name otherwise it defaults to value tests
		if p.name == p.tuplet[0].name:
			jPage[p.tupletName] = parameterToJSONPar(p, extraAttrs,
													 forceAttrLists)
	return jPage

def opToJSONOp(op, extraAttrs=None, forceAttrLists=False,
			   includeCustomPages=True, includeBuiltInPages=False):
	"""
	Convert parameter pages to a jsonable python dict. Format:
		{page name: {parameter name: {parameter attributes, ...}, ...}, ...}
	extraAttrs is a list or tuple of par attribute names that are not normally
		stored. For example, 'val' and 'order'. Can also be a string: '*'
		indicating all properties of the parameter.
	forceAttrLists: If True, all attributes will be stored in a list with the
		length of the tuplet
	includeCustomPages: If True, include custom par pages
	includeBuiltInPages: If True, include builtin pages
	"""
	jOp = dict()
	if includeBuiltInPages:
		for page in op.pages:
			jOp[page.name] = pageToJSONDict(page, extraAttrs,
											forceAttrLists)
	if includeCustomPages:
		for page in op.customPages:
			jOp[page.name] = pageToJSONDict(page, extraAttrs,
											forceAttrLists)
	return jOp

def addParameterFromJSONDict(comp, jsonDict, replace=True, setValues=True,
							 ignoreAttrErrors=True, fixParNames=True,
							 setBuiltIns=False):
	"""
	Add a parameter to comp as defined in a parameter JSON dict. To set values,
	expressions, or bind expressions, provide 'val', 'expr', or 'bindExpr' in
	JSON.
	If replace is False, will error out if the parameter already exists
	If setValues is True, values will be set to provided default
	If ignoreAttrErrors is True, no exceptions for bad attrs in json
	If fixParNames is True, names will be automatically capitalized
	If setBuiltIns is True, if par name matches a builtin par, change par's 
		settings to match instead of creating a new par

	returns a list of newly created parameters
	"""
	requiredKeys = {'page', 'style', 'name'}
	# issubset checks par dict for the required keys of the set requiredKeys
	if requiredKeys.issubset(jsonDict) and \
									all([jsonDict[k] for k in requiredKeys]):
		pStyle = jsonDict['style']
		parName = jsonDict['name']
		pageName = jsonDict['page']
	else:
		raise ValueError ('Parameter definition missing required '
						  'attributes. (' + str(requiredKeys) + ')',
						  jsonDict)

	label = jsonDict.get('label', parName)
	size = jsonDict.get('size', 1)
	# check if we can just replace an already exising parameter
	newPars = None
	if replace:
		def checkForPars(checkName):
			retPars = None
			if size > 1 or len(Page.styles[pStyle].suffixes) > 1:
				# special search for multi-value pars
				checkPars = comp.pars(checkName + '*')
				if checkPars:
					checkPar = checkPars[0]
					if checkPar.tupletName == checkName and \
							checkPar.style == pStyle \
							and (len(checkPar.tuplet) == size 
									or checkPar.style not in ('Int', 'Float')):
						retPars = checkPar.tuplet
			elif hasattr(comp.par, checkName) and \
								getattr(comp.par, checkName).style == pStyle\
					and len(getattr(comp.par, checkName).tuplet) == 1:
				retPars = getattr(comp.par, checkName).tuplet
			return retPars
		if setBuiltIns:
			newPars = checkForPars(parName)
			if newPars is None and fixParNames:
				parName = parName.capitalize()
				newPars = checkForPars(parName)
		else:
			if fixParNames:
				parName = parName.capitalize()
			newPars = checkForPars(parName)
	# set up page if necessary
	page = None
	for cPage in comp.customPages:
		if cPage.name == pageName:
			page = cPage
			break
	if page is None and parName == parName.capitalize():
		page = comp.appendCustomPage(pageName)
	if parName == parName.capitalize():
		try:
			appendFunc = getattr(page, 'append' + pStyle )
		except:
			raise ValueError("Invalid parameter type in JSON dict", pStyle)			
	# create parameter and stash newly created parameter(s) if necessary
	if newPars is None:
		if pStyle in ['Int', 'Float'] and size != 1:
			newPars = appendFunc(parName, label=label, size=size,
								 								replace=replace)
		else:
			newPars = appendFunc(parName, label=label, replace=replace)
	elif parName == parName.capitalize():
		newPars[0].label = label
		newPars[0].page = page

	# set additional attributes if they're in parDict
	# can have multi-vals:

	listAttributes = LISTATTRS
	for index, newPar in enumerate(newPars):
		# go through other attributes
		if setValues and not jsonDict.get('val') \
											and not newPar.style == 'Python':
			try:
				try:
					newPar.val = jsonDict['default']
				except:
					newPar.val = newPar.default
			except:
				if ignoreAttrErrors:
					pass
				else:
					raise
		for attr, value in list(jsonDict.items()) + \
				([('mode', jsonDict['mode'])] if 'mode' in jsonDict else []):
			if attr in ['style', 'name', 'label', 'size', 'page']:
				continue
			if attr in ['expr', 'bindExpr'] and not value:
				value = ''
			if attr in ['val', 'default'] and newPar.style == 'Python':
				continue
			try:
				# apply attributes that can contain an item or a list
				if attr in listAttributes:
					if isinstance(value, (list, tuple)):
						if attr == 'mode':
							if value[index] != 'EXPORT':
								setattr(newPar, attr,
											getattr(ParMode, value[index]))
						elif attr in ['expr', 'bindExpr'] and not value[index]:
							setattr(newPar, attr, '')
						else:
							try:
								setattr(newPar, attr, value[index])
								if setValues and attr == 'default' \
													and 'val' not in jsonDict:
									newPar.val = value[index]
							except:
								if not ignoreAttrErrors:
									debug('addPar error:', newPar, attr, value)
									raise
					elif attr == 'mode':
						if value != 'EXPORT':
							newPar.mode = getattr(ParMode, value)
					else:
						try:
							setattr(newPar, attr, value)
						except:
							if ignoreAttrErrors:
								pass
							else:
								raise
						if setValues and attr == 'default' \
													and 'val' not in jsonDict:
							newPar.val = value

				# apply standard attributes
				else:
					setattr(newPar, attr, value)

			except:
				if ignoreAttrErrors:
					pass
				else:
					raise
		# default menu labels to menu names
		if 'menuNames' in jsonDict and 'menuLabels' not in jsonDict:
			newPar.menuLabels = jsonDict['menuNames']
	return newPars

addParameterFromJSONPar = addParameterFromJSONDict

def addParametersFromJSONList(comp, jsonList, replace=True, setValues=True,
							  destroyOthers=False, newAtEnd=True,
							  ignoreAttrErrors=True, fixParNames=True,
							  setBuiltIns=False):
	"""
	Add parameters to comp as defined in list of parameter JSON dicts.
	If replace is False, will cause exception if the parameter already exists
	If setValues is True, values will be set to parameter's defaults.
	If destroyOthers is True, pars and pages not in jsonList will be destroyed
	If newAtEnd is True, new parameters will be sorted to end of page. This
		should generally be False if you are using 'order' attribute in JSON
	If ignoreAttrErrors is True, no exceptions for bad attrs in json
	If fixParNames is True, names will be automatically capitalized
	If setBuiltIns is True, if par name matches a builtin par, change par's 
		settings to match instead of creating a new par	
	"""
	parNames = []
	pageNames = set()
	for jsonPar in jsonList:
		newPars = addParameterFromJSONDict(comp, jsonPar, replace, setValues,
								ignoreAttrErrors, fixParNames, setBuiltIns)
		if newPars is not None:
			parNames += [p.name for p in newPars]
			pageNames.add(newPars[0].page.name)
	if destroyOthers:
		destroyOtherPagesAndParameters(comp, pageNames, parNames)
	if newAtEnd:
		sortNewPars(comp, pageNames, parNames)
	return parNames, pageNames

def addParametersFromJSONDict(comp, jsonDict, replace=True, setValues=True,
							  destroyOthers=False, newAtEnd=True,
							  ignoreAttrErrors=True, fixParNames=True,
							  setBuiltIns=False):
	"""
	Add parameters to comp as defined in dict of parameter JSON dicts.
	If replace is False, will error out if the parameter already exists
	If setValues is True, values will be set to parameter's defaults.
	If destroyOthers is True, pars and pages not in jsonDict will be destroyed
	If newAtEnd is True, new parameters will be sorted to end of page. This
		should generally be False if you are using 'order' attribute in JSON
	If ignoreAttrErrors is True, no exceptions for bad attrs in json
	If fixParNames is True, names will be automatically capitalized
	If setBuiltIns is True, if par name matches a builtin par, change par's 
		settings to match instead of creating a new par. 
	"""
	parNames = []
	pageNames = set()
	for jsonPar in jsonDict.values():
		newPars = addParameterFromJSONDict(comp, jsonPar, replace, setValues,
										   ignoreAttrErrors, fixParNames,
										   setBuiltIns)	
		if newPars is not None:
			parNames += [p.name for p in newPars]
			pageNames.add(newPars[0].page.name)
	if destroyOthers:
		destroyOtherPagesAndParameters(comp, pageNames, parNames)
	if newAtEnd:
		sortNewPars(comp, pageNames, parNames)
	return parNames, pageNames

def addParametersFromJSONOp(comp, jsonOp, replace=True, setValues=True,
							  destroyOthers=False, newAtEnd=True,
							ignoreAttrErrors=True, fixParNames=True,
							setBuiltIns=False):
	"""
	Add parameters to comp as defined in dict of page JSON dicts.
	If replace is False, will error out if the parameter already exists
	If setValues is True, values will be set to parameter's defaults.
	If destroyOthers is True, pars and pages not in jsonOp will be destroyed
	If newAtEnd is True, new parameters will be sorted to end of page. This
		should generally be False if you are using 'order' attribute in JSON
	If ignoreAttrErrors is True, no exceptions for bad attrs in json
	If fixParNames is True, names will be automatically capitalized
	If setBuiltIns is True, if par name matches a builtin par, change par's 
		settings to match instead of creating a new par	
	"""
	parNames = []
	pageNames = set()
	for jsonPage in jsonOp.values():
		newParNames, newPages = addParametersFromJSONDict(comp, jsonPage,
										replace, setValues, newAtEnd=newAtEnd,
										ignoreAttrErrors=ignoreAttrErrors,
										fixParNames=fixParNames,
										setBuiltIns=setBuiltIns)
		parNames += newParNames
		pageNames.update(newPages)
	if destroyOthers:
		destroyOtherPagesAndParameters(comp, pageNames, parNames)
	if newAtEnd:
		sortNewPars(comp, pageNames, parNames)
	return parNames, pageNames

def destroyOtherPagesAndParameters(comp, pageNames, parNames):
	"""
	Destroys all custom pages and parameters on comp that are not found in
	pageNames or parNames
	"""
	for p in comp.customPars:
		try:
			if p.name not in parNames:
				p.destroy()
		except Exception as e:
			# already destroyed
			# debug(e)
			continue
	for page in comp.customPages:
		if page.name not in pageNames:
			try:
				page.destroy()
			except:
				# already destroyed
				continue

def sortNewPars(comp, pageNames, parNames):
	"""
	Sorts the new parameters in added order at end of page
	"""
	pageDict = {page.name:{'oldPars':[], 'newPars':[]}
												for page in comp.customPages}
	for parName in parNames:
		par = getattr(comp.par, parName)
		if not par.isCustom:
			continue
		if par.tupletName not in pageDict[par.page.name]['newPars']:
			pageDict[par.page.name]['newPars'].append(par.tupletName)
	for page in comp.customPages:
		info = pageDict[page.name]
		if not info['newPars']:
			continue
		for par in page.pars:
			if par.tupletName not in info['newPars']:
				if par.tupletName not in info['oldPars']:
					info['oldPars'].append(par.tupletName)
		page.sort(*(info['oldPars'] + info['newPars']))