target = op(f"{parent.Comp}/glsl1")


def onValueChange(par, prev):
    if par.eval() == 0:
        try:
            op("time").destroy()
        except Exception:
            pass

    elif op("time") is None:
        setTimeOP()
    return

def setTimeOP():
    timen = parent().create(timeCOMP, "time")
    timen.par.play.bindExpr = "parent.Comp.par.Inputsplay"
    timen.par.rate.expr = "cookRate()"
    timen.par.start.bindExpr = "op('/local/time').par.start"
    timen.par.end.bindExpr = "op('/local/time').par.end"
    timen.par.rangelimit.bindExpr = "op('/local/time').par.rangelimit"
    timen.par.rangestart.bindExpr = "op('/local/time').par.rangestart"
    timen.par.rangeend.bindExpr = "op('/local/time').par.rangeend"
    timen.par.resetframe.bindExpr = "op('/local/time').par.resetframe"
    timen.par.signature1.bindExpr = "op('/local/time').par.signature1"
    timen.par.signature2.bindExpr = "op('/local/time').par.signature2"
    timen.par.tempo.bindExpr = "op('/local/time').par.tempo"
    timen.par.independent = True
