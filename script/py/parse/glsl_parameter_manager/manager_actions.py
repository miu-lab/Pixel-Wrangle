class ManagerActions:
    def __init__(self, items: dict, host: COMP, glslTOP: glslTOP):
        self.glslTOP = glslTOP
        self.host = host
        self.items = items

    def eval_actions(self):
        actions = {"update": [], "create": [], "destroy": []}
        self.__eval_destroy_actions(actions)
        self.__eval_create_update_actions(actions)
        return actions

    def __eval_destroy_actions(self, actions):
        for par in self.host.customPars:
            if par.name not in self.items:
                self.__set_destroy_action(actions, par)

    def __eval_create_update_actions(self, actions):
        for k in self.items:
            if isinstance(self.host.par[k], Par):
                self.__set_update_action(actions, k)
            else:
                self.__set_create_action(actions, k)

    def __set_destroy_action(self, actions, parK):
        print(f"Destroy parameter {parK.name}")
        actions["destroy"].append({"item": None, "par": parK})

    def __set_create_action(self, actions, k):
        print(f"Create parameter {k}")
        actions["create"].append({"item": self.items[k], "par": None})

    def __set_update_action(self, actions, k):
        print(f"Update parameter {k}")
        actions["update"].append({"item": self.items[k], "par": self.host.par[k]})
