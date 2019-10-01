import Direction, Id, AudioPlayer
from Room import Room
from Item import Item
from Names import WARHAMMER, BROKEN_WARHAMMER, CROWBAR, HAMMER, WEAPON
from Player import Player
import re
from Things import Skeleton
from Furniture import Furniture, Gettable

"""
    The player escapes the west wind by knocking down the wall in here with a warhammer.
    Haven't been able to invent a story that explains why this room is burnt up.
    Connects to Clos and Cou2.
"""
class Cous(Room):
    def __init__(self, name, ID):
        super(Cous,self).__init__(name, ID)

    def getBarrier(self, direct):
        if direct == Direction.WEST:
            AudioPlayer.playEffect(6)
            return ("The door here is boarded up.")
        elif direct == Direction.NORTH:
            return ("You're too stocky to fit through the fissure.")
        else:
            return self.bumpIntoWall()



class Sear_Ash(Furniture, Gettable):
    def __init__(self, ash):
        super(Sear_Ash,self).__init__()

        self.ASH_REF = ash
        self.description = ("The ash is scattered all over the floor.")
        self.searchDialog = ("Nothing here but more ash.")
        
        self.addActKeys(Furniture.GETPATTERN)
        self.addNameKeys("ash(?:es)?")

    def interact(self, key):
        return Furniture.getIt()

    def getIt(self):
        if Player.getInv().add(self.ASH_REF):
            return ("You take some ash.")
        else:
            return Furniture.NOTHING



class Sear_Door(Furniture):
    def __init__(self):
        super(Sear_Door,self).__init__()

        self.useDialog = ("...Do you intend to pick the lock with that? Well, " +
                         "perhaps you could, but then again, you are not learned " +
                         "of this skill. Yet another you yearn for at the moment.")
        self.description = ("The door is in even worse condition from this side. " +
                           "Whoever it is lying there was hitting it very " +
                           "forcefully with that crowbar to break it down.")
        self.actDialog = ("There's enough evidence here to suggest you can't go through there.")
        self.addUseKeys(Furniture.ANYTHING)
        self.addNameKeys("west door", "door")
        self.addActKeys("open|use|walk|go|close|kick", "knock|bang", "unlock|lock")

    def interact(self, key):
        if key == "close":
            return ("The door is already closed.")
        elif key == "kick":
            AudioPlayer.playEffect(40)
            return ("You thrust your boot into the door, but the door is too well-built to give.")
        elif key == "knock" or key == "bang":
            AudioPlayer.playEffect(55)
            return ("You give the door a knock. To your astonishment, your knock is left unanswered.")
        elif key == "lock" or key == "unlock":
            return ("That isn't how this game works. Read the directions!")
        else:
            return self.actDialog

    def useEvent(self, item):
        if item.getType() == WEAPON: 
            return ("The door is build too solidly and breaking it down is futile.")
        else:
            return self.useDialog


"""
    Player must use the warhammer on this to escape the west wing.    
"""
class Sear_Fissure(Furniture):
    def __init__(self):
        super(Sear_Fissure,self).__init__()

        self.searchDialog = ("It's just an empty hole.")
        self.description = ("The north wall has been damaged, and a resulting " +
                           "fissure in it leads outside through the wall into the front " +
                           "courtyard. Seems this was part of an escape plan.")
        self.useDialog = ("The wall gives way from the swing of the heavy " +
                         "warhammer, which snaps in half. You " +
                         "begin to think the wood ax is the only tool " +
                         "you know how to use without breaking.")
        self.actDialog = ("You couldn't manage to do that with your bare hands.")
        
        self.addActKeys("break", Furniture.JOSTLEPATTERN, "climb|go|walk")
        self.addNameKeys("fissure", "(?:north )?wall", "(?:empty )?hole")
        self.addUseKeys(WARHAMMER, CROWBAR, HAMMER)

    def useEvent(self, item):
        if str(item) == WARHAMMER:            
            Player.getPos().addAdjacent(Id.COU2)
            Player.getInv().remove(item)
            Player.getInv().add(Item(BROKEN_WARHAMMER, -30, use="Well, it's useless now."))
            AudioPlayer.playEffect(30)
            return self.useDialog
        elif not Player.getPos().isAdjacent(Id.COU2):
            AudioPlayer.playEffect(35)
            if str(item) == HAMMER:
                return ("You give it a swing, but this hammer is too " +
                       "small to break this wall. They must've been " +
                       "using something else.")
            else:
                return ("You give the crowbar a swing, but it just " +
                       "rebounds with a loud *THWANG*. They must've " +
                       "been hitting this with something else")
        else:
            return ("The fissure has been destroyed already!")

    def getDescription(self):
        if Player.getPos().isAdjacent(Id.COU2):
            return ("The hole leads outside. It's big enough to fit through.")
        else:
            return self.description 

    def interact(self, key):
        if key == "break":
            return self.actDialog
        elif re.match(Furniture.JOSTLEPATTERN, key):
            return ("That's sufficiently infeasible to do without a tool.")
        else:
            Player.move(Direction.NORTH)
            return Furniture.NOTHING



"""
    Holds a crowbar, to pry the panel in the ransacked room.    
"""  
class Sear_Skeleton(Skeleton):
    def __init__(self, itemList=[]):
        super(Sear_Skeleton,self).__init__(itemList)
        self.description = ("The scorched body lies against the boarded up door.")
        self.addNameKeys("(?:scorched )?body")

    def getDescription(self):
        if self.containsItem(CROWBAR):
            return (self.description + " There's a crowbar in its hand.")
        else:
            return self.description


        
class Sear_Wood(Furniture, Gettable):
    def __init__(self, wood):
        super(Sear_Wood,self).__init__()

        self.WOOD_REF = wood
        self.description = ("Bits of burnt wood are littered everywhere.")
        self.searchDialog = ("It's all just burnt wood.")
        self.addActKeys(Furniture.GETPATTERN)
        self.addNameKeys("(?:bits of )?(?:burnt )?wood")

    def interact(self, key):
        return self.getIt()

    def getIt(self):
        if Player.getInv().add(self.WOOD_REF):
            return ("You take a chunk of wood.")
        else:
            return Furniture.NOTHING