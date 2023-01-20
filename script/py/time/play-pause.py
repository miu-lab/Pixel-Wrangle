target = op(f'{parent.Comp}/glsl1')

def onValueChange(par, prev):
	
	seconds = absTime.seconds
	frames = absTime.frame
	step = absTime.stepSeconds
	
	if par.eval() == 0:
		target.par.value0x = seconds
		target.par.value0y = frames 
		target.par.value0z = step
	else:
		 target.par.value0x.expr = 'absTime.seconds'
		 target.par.value0y.expr = 'absTime.frame'
		 target.par.value0z.expr = 'absTime.stepSeconds'
	
	return