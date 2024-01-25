import os
import platform
import subprocess

def open_file(path):
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])

def onPulse(par):
	path = parent.Comp.par.Codelibrarypath.eval()
	open_file(path)
	return