from _stubs import *
from utils import *

def onDestroy():
	for i, source in enumerate(sourcesn):
		source.par.syncfile = 0
	return
