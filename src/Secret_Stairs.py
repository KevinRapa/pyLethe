from Structure_gen import Balcony, Staircase, StaticWindow, Door
import Direction

class Sst_Door(Door):
    def __init__(self, direct):
        super(Sst_Door,self).__init__(direct)
        self.description = ("This door is weathered and merely just vertical wood " +
                           "slats accompanied by a plain black iron doorknob.")



class Sst_Landing(Balcony):
    def __init__(self):
        super(Sst_Landing,self).__init__()

        self.description = ("The stairs lead up to the small landing. It's held up " +
                           "only by several old wood planks and looks just big " +
                           "enough to stand on.")

        self.addNameKeys("(?:small )?(?:landing|balcony)")



class Sst_Stairs(Staircase):
    def __init__(self, direction, dest):
        super(Sst_Stairs,self).__init__(direction, dest, 14)
        self.description = ("The rickety U-shaped wooden staircase wraps around " +
                           "the room to a small second-floor landing. It looks " +
                           "only partially stable.")
        self.addNameKeys("(?:rickety )?(?:wooden )?(?:stair(?:s|case)|steps)")

    def getDescription(self):
        if self.DIR == Direction.DOWN:
            return ("The rickety wooden stairs lead back down to the second floor.")
        else:
            return self.description



class Sst_Window(StaticWindow):
    def __init__(self):
        super(Sst_Window,self).__init__()
        self.description = ("The circular vented window lets in a small amount of moonlight.")
        self.actDialog = ("You can't reach the window from here.")
        self.addNameKeys("light", "(?:circular )?(?:vented )?window")