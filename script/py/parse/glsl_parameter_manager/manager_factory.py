import manager_classes

GL_PAGE_TO_CLASS = {
    "UI": manager_classes.GLUIItem,
    "VECTOR": manager_classes.GLVectorPageItem,
    "ARRAY": manager_classes.GLArrayPageItem,
    "MATRIX": manager_classes.GLMatrixPageItem,
    "CONSTANT": manager_classes.GLConstantPageItem,
}


class ManagerFactory:
    def __init__(self, ownerComp: COMP, host: COMP, glslTOP: glslTOP):
        self.owner = ownerComp
        self.current_items = {}
        self.host = host
        self.glslTOP = glslTOP
        self.actions = {}

    def set_actions(self, actions: dict) -> dict:
        self.actions = actions
        return self

    def run(self):
        self.__run_actions()

    def __run_actions(self):
        for item in self.actions["destroy"]:
            self.__destroy_item(item)

        for item in self.actions["create"]:
            self.__create_item(item)

        for item in self.actions["update"]:
            self.__update_item(item)

    def __create_item(self, item: dict):
        print(f"CREATE : {item['item']['gl_page']}")

    def __destroy_item(self, item: dict):
        pass

    def __update_item(self, item: dict):
        pass
