from _stubs import *
glsln = op('glsl1')
table = op('FEEDBACK_REPLICATOR/OUT_ACTIVE_INPUTS')
outNodesTable = op('FEEDBACK_REPLICATOR/OUT_OUTPUT_NODES')


# Functions
def getOutNodes(table):
	outNodes = table.rows()
	del outNodes[0]
	nodes = []
	for n in outNodes:
		nodes.append(op(n[1].val))
	return nodes

def disconnectAll(node):
	op_ins = node.inputConnectors
	for i in range(len(op_ins)-1):
		op_ins[i].disconnect()
	return

# Callbacks
def onRemoveReplicant(comp, replicant):
	glsln.inputConnectors[table.numRows-1].disconnect()
	replicant.destroy()
	return

def onReplicate(comp, allOps, newOps, template, master):
	outs = getOutNodes(outNodesTable)
	for i,c in enumerate(allOps):
		inputn = op(template[i+1, 0].val)
		try:
			c.inputConnectors[0].connect(inputn.outputConnectors[0])
		except:
			pass
		try:
			c.outputConnectors[0].connect(glsln.inputConnectors[i])
		except:
			pass
		if template[i+1, 'type'] != 'feedback':
			c.destroy()
		else:
			for j, node in enumerate(outs):
				if outNodesTable[j+1,'out_name'] == template[i+1, 3].val:
					c.par.top = node.name
					c.par.reset.mode = ParMode.BIND
					c.par.resetpulse.mode = ParMode.BIND
					c.par.reset.bindExpr = f'parent.Comp.par.Inputsinputfeedbackreset{str(int(i+1))}'
					c.par.resetpulse.bindExpr = f'parent.Comp.par.Inputsinputfeedbackreset{str(int(i+1))}'
					c.bypass = False
					break
	return
