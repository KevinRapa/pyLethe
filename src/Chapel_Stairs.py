from Things import Statue
import Direction
from Room import Room
from Structure_gen import StaticWindow, Staircase


class Chs1_Stairs(Staircase):
    def __init__(self, direction, dest):
        super(Chs1_Stairs,self).__init__(direction, dest, 15)
        self.description = ("The wide spiral stairs wind many times around the " +
                           "tower's wall. A dark red carpet follows them up.")
        self.addNameKeys("(?:circular |spiral )?stair(?:s|case)")

    def getDescription(self):
        if self.DIR == Direction.DOWN:
            return ("The spiral stairs run a few stories downward to the first floor landing.")
        else:
            return self.description



class Chs1_Statue(Statue):
    def __init__(self):
        super(Chs1_Statue,self).__init__()

        self.description = ("The female statue wears a face of sorrow and stares " +
                           "directly at you. As you sway from side to side, it's " +
                           "almost as if her eyes follow you.")
        self.actDialog = ("That's not a very religious thing to do...")
        self.addNameKeys("female statue")


"""
    Serves as the entrance to the chapel.
    Superficial.
"""
class Chs3(Room):
    def __init__(self, name, ID):
        super(Chs3,self).__init__(name, ID)

    def getBarrier(self, direct):
        if direct == Direction.WEST:
            return ("The landing's railing protects you from tumbling three stories.")
        else:
            return self.bumpIntoWall()


class Chs_Windows(StaticWindow):
    def __init__(self, NAME):
        super(Chs_Windows,self).__init__()

        self.escapeDialog = ("You could probably use your weight to break through... but aren't too keen on the idea.")
        self.actDialog = ("These stained glass windows aren't designed that way.")
        self.description = ("The stained glass windows line the outer wall of the " +
                           "tower and follow the white spiral stairs. The moonlight " +
                           "penetrates their many colors and projects a dim array of " +
                           "hues against the inner tower wall.")
        self.addNameKeys("stained glass windows?")
