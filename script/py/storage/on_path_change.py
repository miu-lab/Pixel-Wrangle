
from PRESET_UTILS import buildPreset
from TDJSON import opToJSONOp


def onPathChange(changeOp):
    oldStorage = op.pwstorage.storage
    comp = parent.Comp
    curOPID = changeOp.id
    curOPPATH = changeOp.path
    inputs = [
        {
            "index": x.index,
            "op": x.connections[0].owner.path if len(x.connections) >= 1 else None,
        }
        for x in comp.inputConnectors
    ]
    outputs = [
        {
            "index": x.index,
            "op": x.connections[0].owner.path if len(x.connections) >= 1 else None,
        }
        for x in comp.outputConnectors
    ]
    for k, v in oldStorage.items():
        if int(v["opid"]) == curOPID:
            op.pwstorage.unstore(k)
            lastState = buildPreset(comp)
            op.pwstorage.store(
                curOPPATH,
                {
                    "opid": curOPID,
                    "lastState": lastState,
                    "connections": {"inputs": inputs, "outputs": outputs},
                },
            )
            return


def onWireChange(changeOp):
    onPathChange(changeOp)
