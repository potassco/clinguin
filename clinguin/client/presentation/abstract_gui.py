

class AbstractGui:

    def __init__(self):
        print("Abstract Solver")

    def window(self, id, parent, attributes, callbacks):
        print("WINDOW: " + str(id) + "::" + str(parent))

    def container(self, id, parent, attributes, callbacks):
        print("CONTAINER: " + str(id) + "::" + str(parent))

    def dropdownmenu(self, id, parent, attributes, callbacks):
        print("DROPDOWNMENU: " + str(id) + "::" + str(parent))

    def dropdownmenuitem(self, id, parent, attributes, callbacks):
        print("DROPDOWNMENUITEM: " + str(id) + "::" + str(parent))

    def label(self, id, parent, attributes, callbacks):
        print("LABEL: " + str(id) + "::" + str(parent))

    def button(self, id, parent, attributes, callbacks):
        print("BUTTON: " + str(id) + "::" + str(parent))


    def draw(self):
        print("DRAW")
