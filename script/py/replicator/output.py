from _stubs import *
iName = 'renderselect'
iWireName = 'cache'

def onRemoveReplicant(comp, replicant):
	selectn = op(iName + str(replicant.digits))
	cachen = op(iWireName + str(replicant.digits))
	selectn.bypass = True
	cachen.bypass = True
	replicant.destroy()
	
	return

def onReplicate(comp, allOps, newOps, template, master):

	for c in allOps:
		selectn = op(iName + str(c.digits))
		cachen = op(iWireName + str(c.digits))
		selectn.bypass = False
		cachen.bypass = False
		digit = template[c.digits, 0].val[-1:]
		c.color = parent().parGroup['Outputscolor' + str(digit)]
		c.inputConnectors[0].connect(op(iWireName + str(c.digits)).outputConnectors[0])
		c.bypass = False
		if template[c.digits, 'hide'] == 1 and c.type != 'nullTOP':
			c.changeType(nullTOP)
		elif c.type != 'outTOP':
			n = c.changeType(outTOP)
			n.par.label.expr = f"parent().par.Outputsoutputname{digit}"
		pass

	return