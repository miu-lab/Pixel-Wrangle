
from utils import *


def onDestroy():
    for source in sourcesn:
        source.par.syncfile = 0
        source.par.file = ""
    return
