# Stubs BEGIN
try:
	op
except NameError:
	from _stubs import *
# Stubs END

def resetKeys(opTable):
	rows = n.rows()
	rows.pop(0)
	for i,row in enumerate(rows):
		oppath = n[i+1, "path"].val
		curOP = op(oppath)
		curOP.par.clear.pulse(1, frames=1)
	return
	
n = op("KEYBOARDS")
resetKeys(n)