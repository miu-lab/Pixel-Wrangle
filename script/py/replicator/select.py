from _stubs import *
glsln = op('glsl1')
table = op('SELECT_REPLICATOR/OUT_ACTIVE_INPUTS')
outNodesTable = op('SELECT_REPLICATOR/OUT_OUTPUT_NODES')

# Callbacks
def onRemoveReplicant(comp, replicant):
	replicant.destroy()
	return

def onReplicate(comp, allOps, newOps, template, master):
	for i,c in enumerate(allOps):
		tarn = op(template[i+1, 0].val)
		tarnType = tarn.type 
		if template[i+1, 'type'].val != 'custom' and template[i+1, 'fallback'].val == 'none':
			c.destroy()
		elif template[i+1, 'type'].val != 'custom' and template[i+1, 'fallback'].val != 'none':
			c.par.top = f"{parent.Comp.path}/BUILTINS_INIT/{template[i+1, 'fallback'].val}"
			if tarnType != 'in': 
				pass
			else:
				c.outputConnectors[0].connect(tarn.inputConnectors[0])
		else:
			c.par.top = template[i+1, 'custom'].val
			if tarnType != 'in': 
				pass
			else:
				c.outputConnectors[0].connect(tarn.inputConnectors[0])
	return
