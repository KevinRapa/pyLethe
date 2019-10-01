from GUI import GUI
import Id, Menus, AudioPlayer
from Player import Player
from Names import PHASE_DOOR_POTION, LOOT_SACK
from Tunnels import DungeonMonster
from Room import Room
from Furniture import SearchableFurniture, Moveable, Openable, Furniture
from Structure_gen import StaticWindow, Ceiling

"""
    The player is captured in ATT1 after creating the phase door potion.
"""
class Att1(Room):    
    def __init__(self, name, ID, cbntNum):
        super(Att1, self).__init__(name, ID)

        self.PRIS_CBNT_ID = cbntNum

    def triggeredEvent(self):
        if Player.hasItem(PHASE_DOOR_POTION) and not Player.hasVisited(Id.INTR):
            cbntInv = Player.getRoomObj(Id.PRIS).getFurnRef(self.PRIS_CBNT_ID).getInv()
            
            self._dialog()
            
            for i in Player.getInv(): 
                if str(i) == LOOT_SACK and i.getInv().contains(PHASE_DOOR_POTION):
                    i.getInv().remove(PHASE_DOOR_POTION)
                if str(i) != PHASE_DOOR_POTION:
                    cbntInv.add(i)
            
            Player.getInv().clear()
            Player.updateScore(0)
            Player.setShoes("")
            Player.setOccupies(Id.INTR)
            Player.getRoomObj(Id.EOW1).setLocked(True)
            DungeonMonster.startMovement()
            AudioPlayer.playEffect(8, 80)
            Player.printInv()
            return ""

        return self.NAME

    def _dialog():
        GUI.menOut(Menus.ENTER)
        GUI.clearDesc()
        GUI.invOut("")
        GUI.out("As you exit the laboratory, you are startled to see a hideous, decrepit " +
                "bald male wearing black robes standing among the shadows in the center of the attic. " +
                "You freeze, unable to move. Several seconds pass...")
        GUI.promptOut()
        GUI.out("   ...")
        GUI.promptOut()
        GUI.out("Several more seconds pass. Before you can realize, you are unconscious...")
        GUI.promptOut()
        GUI.out("   ... ... ...")
        GUI.promptOut()



"""
    The player is captured in ATT1 after creating the phase door potion.
"""
class Att2(Room):    
    def __init__(self, name, ID):
        super(Att2, self).__init__(name, ID)

    def triggeredEvent(self):
        if not Player.hasVisited(Id.ATT2):
            AudioPlayer.playEffect(52)
            GUI.out("You feel an unnerving presence here. You shutter and look " +
                    "around, but see only darkness.")

        return self.NAME



class Att_Boxes(SearchableFurniture, Openable, Moveable):
    def __init__(self, itemList=[]):
        super(Att_Boxes, self).__init__(itemList)
        
        self.description = ("There are plenty of old cardboard boxes scattered " +
                           "around the room. They seem to be filled with various curios and science equipment.")
        self.searchDialog = ("In an excited manner reminiscent of a small child " + 
            "in a toy store, you rummage joyfully through the myterious boxes.")
        self.actDialog = ("You really aren't very good at folding.")
        
        self.addActKeys("fold", Furniture.GETPATTERN)
        self.addNameKeys("(?:cardboard )?box(?:es)?", "pile")
          
    def interact(self, key):
        if key == "fold":
            return self.actDialog
        else:
            return ("The boxes are too large and heavy to simply put in your pocket.")



class Att_Cases(SearchableFurniture, Openable, Moveable):
    def __init__(self, itemList=[]):
        super(Att_Cases, self).__init__(itemList)
        
        self.description = ("Various suitcases of different sizes lie stacked up around the attic. They seem to be filled with just clothes.")
        self.actDialog = ("How greedy you are. Surely you couldn't carry all of these suitcases around.")
        self.searchDialog = ("You pick through the various suitcases scattered about.")

        self.addNameKeys("(?:suit)?cases?", "piles")
        self.addActKeys(Furniture.GETPATTERN)



class Att_Ceiling(Ceiling):
    def __init__(self):
        super(Att_Ceiling, self).__init__()
        
        self.description = ("The ceiling here is just the underside of a gabled " +
                           "roof, reinforced with many gray wooden slats.")

        self.addNameKeys("(?:gray )?(?:wooden )?slats", "gabled roof", "sloped ceiling")



class Att_Vents(StaticWindow):
    def __init__(self):
        super(Att_Vents, self).__init__()
        
        self.actDialog = ("They're too high up to reach.")
        self.escapeDialog = ("You couldn't possibly fit your huge body between those slats.")
        self.description = ("So many times thus far you have felt so close to " +
                           "the outside of this castle. The thought taunts you. " +
                           "You feel as though days have passed, but it's been " +
                           "just a few hours.")

        self.addNameKeys("vents?", "moonlight")