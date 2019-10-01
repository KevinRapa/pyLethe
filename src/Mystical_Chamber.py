from Structure_gen import Ceiling, Staircase
from Names import IRIDESCENT_JEWEL
from Player import Player
import Direction, Id, AudioPlayer
from Furniture import Furniture, Unmoveable
from Room import Room
from Caves import Cave

class My18_Ceiling(Ceiling):
    def __init__(self):
        super(My18_Ceiling,self).__init__()

        self.description = ("It's a domed sandstone ceiling only about 2 feet above your head.")
        self.addNameKeys("(?:domed )?(?:sandstone )?ceiling")



"""
    Adds furniture to its room if the iridescent jewel is used on self.
    Iridescent jewel is somewhere in the catacombs- determined randomly.
    Its location is written on a note in the Ancient Tomb in a casket.    
"""
class My18_Pedestal(Furniture, Unmoveable):
    def __init__(self):
        super(My18_Pedestal,self).__init__()

        self.hasStone = False
        self.description = ("The pedestal has a globular indentation in the center.")
        self.searchDialog = ("There's nothing interesting about the pedestal.")
        self.useDialog = ("That doesn't fit in the indentation.")
        self.STAIRS = My18_Stairs(Direction.DOWN, Id.CV18)
        
        self.addNameKeys("(?:sandstone )?pedestal")
        self.addUseKeys(Furniture.ANYTHING)
    
    def getDescription(self):
        return ("The iridescent stone sits flush into the indentation." \
            if self.hasStone else self.description)
    
    def useEvent(self, item):
        if str(item) == IRIDESCENT_JEWEL:
            self.hasStone = True
            AudioPlayer.playEffect(37)
            Player.getPos().addFurniture(self.STAIRS)
            Player.getInv().remove(item)
            Player.getPos().updateDesc()

            return ("The stone fits perfectly into the indentation. Immediately, the " +
                   "ground begins to shake lightly. You step back. The seams in the floor " + 
                   "begin to cascade downward forming a spiral staircase descending " +
                   "downwards into darkness.")
        else:
            return self.useDialog



"""
    Provides access to the caves once the player finds the iridescent jewel and
    uses it on a pedestal in here.
    Connects to Catacombs and Caves.    
"""
class My18(Room):
    def __init__(self, name, ID):
        super(My18,self).__init__(name, ID)
        self.hasJewel = False

    def updateDesc(self):
        self.hasJewel = True

    def getDescription(self):
        return ("You stand at the rim of the circular chamber before " +
                "the descending set of spiral stairs wrapping around " +
                "the center pillar on which the pedestal still stands." \
                if self.hasJewel else super(My18,self).getDescription())

    def triggeredEvent(self):
        if Player.getLastVisited() == Id.CV18:
            Cave.stopClip()
        
        return self.NAME



class My18_Stairs(Staircase):
    def __init__(self, direction, dest):
        super(My18_Stairs,self).__init__(direction, dest, 15)
        self.description = ("The sandstone spiral staircase wraps around the central pillar " + \
            ("down into a dark void." if direction == Direction.DOWN else "up into the round chamber."))

        self.addNameKeys("(?:sandstone )?spiral stair(?:s|case)")
