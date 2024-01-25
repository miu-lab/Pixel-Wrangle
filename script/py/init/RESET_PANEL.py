

op(f"{parent.Comp}/KEYBOARDS_SHORTCUTS/panel5").bypass = False
mode = parent.Comp.par.Glmode.val
if mode == "compute":
    parent.Comp.par.Glmode.pulse(0, frames=4)
else:
    parent.Comp.par.Glmode.pulse(1, frames=4)

op("Preset_Manager/POP_PRESET").par.Close.pulse(1, frames=1)
op("Function_Manager/POP_FUNCTION").par.Close.pulse(1, frames=1)
