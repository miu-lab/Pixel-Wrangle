from _stubs import *
glsln = op('glsl1')
feedbacksRep = op('FEEDBACK_REPLICATOR')
outNodesTable = op('FEEDBACK_REPLICATOR/OUT_OUTPUT_NODES')

def getOutNodes(table):
	outNodes = table.rows()
	del outNodes[0]
	nodes = []
	for n in outNodes:
		nodes.append(op(n[1].val))
	return nodes

def onRemoveReplicant(comp, replicant):
	# replicant.disconnect()
	replicant.destroy()
	return

def onReplicate(comp, allOps, newOps, template, master):
	outs = getOutNodes(outNodesTable)

	inputs = []
	for i,c in enumerate(allOps):
		try:
			inOP = c.inputConnectors[0].owner.parent().inputConnectors[i].connections[0].owner 
			inputs.append({"name":template[i+1, 'name'].val, "inputOP": inOP})
		except:
			continue

	for i,c in enumerate(allOps):
		digit = int(template[i+1, 'name'].val[-1:])
		inOP = None
		c.color = parent().parGroup['Inputscolor' + str(digit)]
		inittype = template[i+1, 'inittype'].val
		
		# Check OP type
		if template[i+1, 'type'].val != 'feedback':
			if c.type != 'inTOP':
				n = c.changeType(inTOP)
				n.par.label.mode = ParMode.EXPRESSION
				n.par.label.expr = f"parent().par.Inputsinputname{str(digit)}"
			else:
				n = c
				n.par.label.mode = ParMode.EXPRESSION
				n.par.label.expr = f"parent().par.Inputsinputname{str(digit)}"

		if template[i+1, 'type'].val == 'feedback':
			if inittype == 'direct':
				n = c.changeType(inTOP)
				n.par.label.mode = ParMode.EXPRESSION
				n.par.label.expr = f"parent().par.Inputsinputname{str(digit)}"
				# n.inputConnectors[0].connect(op(f"selectInputsactive{digit}").outputConnectors[0])
				
			elif inittype == 'builtin':
				n = c.changeType(selectTOP)
				builtinPath = template[i+1, 'initbuiltinpath'].val
				n.par.top.val = f"BUILTINS_INIT/{builtinPath}"
			elif inittype == 'output':
				n = c.changeType(selectTOP)
				outputName = template[i+1, 'initoutputname'].val
				for j, node in enumerate(outs):
					if outNodesTable[j+1,'out_name'] == outputName:
						n.par.top = node.name
			elif inittype == 'custom':
				n = c.changeType(selectTOP)
				customPath = template[i+1, 'initcustompath'].val
				n.par.top.val = f"../{customPath}"

	feedbacksRep.par.recreatemissing.pulse(1, frames=4)
	for i,c in enumerate(newOps):
		# Init ids, set color and connect to out
		digit = int(template[i+1, 'name'].val[-1:])
		index = i
		c.outputConnectors[0].connect(glsln.inputConnectors[index])

	
	## Rewiring
	for i,c in enumerate(allOps):
		for input in inputs:
			if c.name == input["name"]:
				tarOP = input["inputOP"]
				c.inputConnectors[0].owner.parent().inputConnectors[i].connect(tarOP.outputConnectors[0])
	
	return
