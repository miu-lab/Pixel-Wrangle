import manager_exec

def onValueChange(_, __):
    manager_exec.set_target_operators()
    manager_exec.update()
    return
