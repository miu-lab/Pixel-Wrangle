from LOAD_SETTINGS import *

jsonFile = None


def onValueChange(par, _):

    # Read file as Python dict
    with open(file, "r") as settings:
        jsonFile = json.load(settings)

    # Update Python dict
    jsonFile["vscodePath"] = par.eval()

    # Write modified Python dict as json
    with open(file, "w") as settings:
        json.dump(jsonFile, settings)
    return
