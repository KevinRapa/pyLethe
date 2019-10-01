import Id, Direction, AudioPlayer
from Player import Player
from Names import HAND_TORCH, WEAPON, WOOD_LOG, BATTERING_RAM
from Structure_gen import Door
import re
from Room import Room
from Things import LockedContainer
from Item import Item

class Sha1_Door(Door):
    def __init__(self, ram, brRam, ID):
        super(Sha1_Door,self).__init__(Direction.WEST)
        self.RAM_REF = ram
        self.BRKNRAM_REF = brRam
        self.GEN_DR_ID = ID
        
        self.description = ("It's a small wooden door a bit taller than you. " +
                           "The doorknob on it is missing.")
        self.actDialog = ("The doorknob is gone!!")
        self.useDialog = ("You give the door a good bang with the ram. It gives " +
                         "from its hinges and falls to the floor. But the frayed " +
                         "rope you're holding the ram with snaps in half. Good " +
                         "thing that worked on the first try.")

    def useEvent(self, item):
        if str(item) == BATTERING_RAM:
            AudioPlayer.playEffect(40)
            Player.getRoomObj(Id.SHA1).addAdjacent(Id.SHAR) # Make SHAR accessible.
            Player.getRoomObj(Id.SHA1).removeFurniture(self.getID()) # Remove this door from the room.
            Player.getRoomObj(Id.SHA1).removeFurniture(self.GEN_DR_ID)
            Player.getInv().remove(self.RAM_REF) # Take ram from player.
            Player.getInv().add(self.BRKNRAM_REF) # Add broken ram to player.
            return self.useDialog        
        elif str(item) == WOOD_LOG:
            return ("What appears to be a battering ram is missing anything " +
                   "with which to hold. You can't obtain a firm enough grip.")
        elif item.getType() == WEAPON:
            AudioPlayer.playEffect(40)
            return ("While a worthwile attempt, the door is build a bit too " +
                   "solidly to be knocked down with that.")
        elif str(item) == HAND_TORCH:
            return ("Unfortunately, the door is coated in what could only " +
                   "be recognized (by you at least) as fire-proof varnish.")
        else:
            return Furniture.DEFAULT_USE

    def interact(self, key):
        if re.match("open|use|walk|go|close", key):
            return self.actDialog
        else:
            return super(Sha1_Door, self).interact(key)



"""
    Adjacent to the Ransacked Quarters, where the study key is.
    Connects to Sha2, Wow1, and Rqua    
"""
class Sha1(Room):
    def __init__(self, name, ID):
        super(Sha1,self).__init__(name, ID)

        self.DESC_2 = (super(Sha1,self).getDescription().replace("a small door", "an open doorway", 1) \
            if super(Sha1,self).getDescription() else None)

    def getBarrier(self, direct):   
        if direct == Direction.WEST:
            return ("This door's knob is missing.")
        else:
            return self.bumpIntoWall()

    def getDescription(self):
        if not self.hasFurniture("west door"):
            return self.DESC_2
        else:
            return super(Sha1,self).getDescription()



class Sha2_Cabinet(LockedContainer):
    def __init__(self, itemList=[]):
        super(Sha2_Cabinet,self).__init__(Id.CBNT, itemList)
        
        self.description = ("It's a large wooden double-door cabinet. It looks " +
                           "plain and cheap. It must just house tools for the servants.")
        self.actDialog = ("The tiny metal key fits perfectly. You turn it and the " +
                          "cabinet makes a satisfying *click*.")
        self.searchDialog = ("The cabinet is locked. Maybe one of the servants had a key...")

        self.addNameKeys("(?:large )?(?:wood(?:en)? )?(?:double-door )?cabinet")



class Sha_Door(Door):
    def __init__(self, direct):
        super(Sha_Door,self).__init__(direct)
        self.description = ("It's a small wooden door a bit taller than you.")