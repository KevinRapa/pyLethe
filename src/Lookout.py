from Furniture import Furniture, Unmoveable, Climbable
import Direction, Id, AudioPlayer
from Room import Room
from Structure_gen import Railing, Door
from Player import Player
import re

class Look_Cliff(Furniture, Unmoveable):
    def __init__(self):
        super(Look_Cliff,self).__init__()

        self.description = ("The winding cliff forms the shoreline to the south " +
                           "and terminates at the distant lighthouse.")
        self.searchDialog = ("The cliff is too far away to do that.")
        self.actDialog = ("What are you talking about? The cliff is nearly a mile away!")
        
        self.addActKeys("jump", Furniture.CLIMBPATTERN)
        self.addNameKeys("(?:winding )?cliff")



class Look_Lighthouse(Furniture, Unmoveable):
    def __init__(self):
        super(Look_Lighthouse,self).__init__()

        self.description = ("A classic red and white striped lighthouse. Its " +
                           "beacon illuminates northwards. You wish it would maybe spot you.")
        self.searchDialog = ("The lighthouse is absolutely too far away to do that.")
        self.actDialog = ("You consider yourself a decent swimmer, but that doesn't " +
                         "seem very feasible to do.")
        
        self.addActKeys("walk", "swim", "go")
        self.addNameKeys("(?:classic )?(?:red and white )?(?:striped )?lighthouse")



"""
    Location of the valve that drains the rotunda fountain.
    Connects to Rotu
"""
class Look(Room):
    def __init__(self, name, ID):
        super(Look,self).__init__(name, ID)

    def getBarrier(self, direct):
        if direct == Direction.WEST:
            return ("There's a couple hundred foot drop right there.")
        elif direct == Direction.EAST:
            AudioPlayer.playEffect(6)
            return ("The door is missing!")
        else:
            return self.bumpIntoWall()



class Look_Railing(Railing):
    def __init__(self):
        super(Look_Railing,self).__init__()
        
        self.description = ("A wide, sturdy granite railing.")
        self.addNameKeys("(?:wide )?(?:sturdy )?(?:granite )?(?:balcony )?railing", "balcony")



class Look_TrapDoor(Door, Climbable):
    def __init__(self):
        super(Look_TrapDoor,self).__init__(Direction.DOWN)
        
        self.LADDER_NAME = re.compile("(?:metal )?ladder")
        self.isOpen = False
        self.description = ("The wooden trap door is %.")
        self.actDialog = ("You descend down the ladder for about 20 feet.")

        self.NAMEKEYS = []
        self.addNameKeys("(?:wooden )?trap ?door")
        self.addActKeys(Furniture.CLIMBPATTERN)
    
    def getDescription(self):
        return self.description.replace("%", \
            ("open, revealing a metal ladder leading down" if self.isOpen else "closed"), 1)
    
    def interact(self, key):              
        if re.match("open|use|walk|go", key):
            if self.isOpen:
                return ("The trap door is open already!")
            else:
                self.isOpen = True
                self.addNameKeys(self.LADDER_NAME)
                return "You open the trap door"
        elif re.match(Furniture.CLIMBPATTERN, key):
            if self.isOpen:
                AudioPlayer.playEffect(47)
                Player.setOccupies(Id.CEL1)
                return self.actDialog
            else:
                return ("The trap door is closed. There's nothing to take you there.")
        elif key == "close":
            if self.isOpen:
                self.isOpen = False
                self.NAMEKEYS.remove(self.LADDER_NAME)
                return ("You close the trap door.")
            else:
                return ("The trap door is closed already!")
        else:
            return super(Look_TrapDoor,self).interact(key)
    
    def getDir(self):
       return Direction.DOWN