
from PRESET_UTILS import buildPreset
from EXPORTER import setContainer


def initStorage():
    try:
        op.pwstorage.valid
    except Exception:
        parent = op("/").create(baseCOMP, "storage")
        tarn = parent.create(baseCOMP, "Pixel_Wrangle")
        tarn.par.opshortcut = "pwstorage"


def onTableChange(dat):
    comp = parent.Comp
    opid = comp.id
    oppath = comp.path
    inputs = op.pwstorage.fetch(oppath)["connections"]["inputs"]
    outputs = op.pwstorage.fetch(oppath)["connections"]["outputs"]
    initStorage()
    lastState = buildPreset(comp)
    op.pwstorage.store(
        oppath,
        {
            "opid": opid,
            "lastState": lastState,
            "connections": {
                "inputs": inputs,
                "outputs": outputs
            },
        },
    )
    return
