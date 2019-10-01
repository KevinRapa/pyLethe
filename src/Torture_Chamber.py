from Player import Player
import re
from Names import SCYTHE
from Room import Room
import Id, Names, AudioPlayer
from Inventory import Inventory
from Item import Weapon, Item
from Furniture import *

"""
    This item must be used in SEW4 to give access to the metal pipe in order to
    replace the missing piece.
    
    When this item is used, it places itself as furniture in the room and removes
    itself from the player inventory. When said furniture is picked up, it removes
    itself from the room and is placed in the player's inventory.
"""
class Metal_Ladder(Item):
    def __init__(self, name):
        super(Metal_Ladder,self).__init__(name, 0, use="You stand the ladder up in the room.")

        self.LADDER_FURNITURE = Metal_Ladder_Furniture(self)
    
    def useEvent(self):
        Player.getInv().remove(self)
        Player.getPos().addFurniture(self.LADDER_FURNITURE)
        Player.printInv()
        
        if not Player.getPosId() == Id.SEW4:
            return self.useDialog
        else:
            return ("You extend the ladder and lean it up against the tunnel wall. " +
                   "It just reaches the top.")

    
class Metal_Ladder_Furniture(Furniture):
    def __init__(self, ref):
        super(Metal_Ladder_Furniture,self).__init__()
        
        self.LADDER_ITEM = ref
        self.description = ("The old metal ladder stands in the center of the room, going nowhere.")
        self.actDialog = ("You climb up the ladder. \"There's really not much " +
                         "need to be up here,\" you think to yourself, and climb down.")

        self.addNameKeys("(?:old )?(?:metal )?ladder")
        self.addActKeys(Furniture.CLIMBPATTERN, Furniture.GETPATTERN, "use")
    
    def interact(self, key): 
        if re.match(Furniture.CLIMBPATTERN, key) or key == "use":
            AudioPlayer.playEffect(47)
            if not Player.getPosId() == Id.SEW4:
                return self.actDialog
            else:
                return ("You climb high up the ladder to the pipe on the ceiling.")
        elif Player.getInv().add(self.LADDER_ITEM):
            Player.getPos().removeFurniture(self.getID())
            return ("You pick up the ladder.")
        else:
            return Furniture.NOTHING
    
    def getDescription(self):
        if not Player.getPosId() == Id.SEW4:
            return self.description
        else:
            return ("The metal ladder stands extended against the tunnel wall. " +
                   "It just reaches the pipe at the top.")



class Torc_Cages(SearchableFurniture, Openable):
    def __init__(self, itemList=[]):
        super(Torc_Cages,self).__init__(itemList)
        
        self.description = ("The small, thick-barred cages hang by chains from " +
                           "the ceiling. There is a small door in each. On the " +
                           "base of one of them sit a pile of bones.")
        self.searchDialog = ("You open up one of the cages.")
        self.actDialog = ("That would be uncomfortably cozy...")
         
        self.addActKeys("go", "climb", Furniture.SITPATTERN)
        self.addNameKeys("(?:small )?(?:hanging )?(?:thick-barred )?cages?")



"""
    Holds a metal ladder that the player needs to replace the pipe in SEW4 and
    a scythe for the statue in the crypt.
    Connects to Cry1 and Pris    
"""
class Torc(Room):
    def __init__(self, name, ID):
        super(Torc,self).__init__(name, ID)

    def getDescription(self):
        if not Player.getPos().hasFurniture(SCYTHE):
            return super(Torc,self).getDescription().replace(" below a large scythe", "", 1)
        else:
            return super(Torc,self).getDescription()



class Torc_Rack(SearchableFurniture, Moveable):
    def __init__(self, itemList=[]):
        super(Torc_Rack,self).__init__(itemList)
        
        self.description = ("It's a plain wooden table, about 8 feet long, with " +
                           "no intricacies. At one end of the table is a roller " +
                           "of sorts with a crank on one side and a couple ropes " +
                           "tied around it. Along the table are several long leather " +
                           "straps and buckles. At the opposite end are two more " +
                           "short ropes.")
        self.actDialog = ("The macabre idea of laying on the table dances in your " +
                         "head. You let off a sarcastic chuckle and try to forget " +
                         "about it.")
        self.searchDialog = ("You look on the table.")

        self.addNameKeys("(?:plain )?(?:wooden )?(?:table|rack)")
        self.addActKeys(Furniture.SITPATTERN)



"""
    This furniture holds the metal ladder needed to place the metal pipe in SEW4.
    
    TORC also has a dummy furniture can Torc_Ladder which may be interacted with
    to get the ladder as well.
"""
class Torc_Sawhorses(Furniture, Resetable, Moveable):
    def __init__(self, torc, itemList=[]):
        super(Torc_Sawhorses,self).__init__()
        
        self.METAL_LADDER = Metal_Ladder(Names.METAL_LADDER)
        self.TORC_LDDR = Torc_Lddr(self)
        self.inv = Sawhorse_Inventory(self, self.METAL_LADDER)
        self.searchable = True
        
        torc.addFurniture(self.TORC_LDDR)
        
        self.description = ("The two sawhorses are spread apart about 8 feet.")
        self.searchDialog = ("The sawhorses are holding up a ladder-like metal device.")
        self.useDialog = ("You place the metal ladder back on the sawhorses.")

        self.addNameKeys("(?:two )?sawhorses?", "(?:long )?(?:metal )?device")
        self.addUseKeys(Names.METAL_LADDER)
    
    def getDescription(self):
        if self.hasLadder():
            return (self.description + " They are holding up " +
                  "a device resembling two parallel 10-foot long metal poles attached " +
                  "together via many shorter perpendicular metal poles.")
        else:
            return self.description
    
    def getSearchDialog(self):
        return (self.searchDialog if self.hasLadder() else "You check around the sawhorses.")
    
    def useEvent(self, item):
        self.inv.add(item)
        Player.getRoomObj(Id.TORC).addFurniture(self.TORC_LDDR)
        return self.useDialog
    
    def reset(self):
        if Player.hasItem(Names.METAL_LADDER):
            self.inv.add(self.METAL_LADDER)
            Player.getInv().remove(self.METAL_LADDER)
            Player.getRoomObj(Id.TORC).addFurniture(self.TORC_LDDR)
    
    def hasLadder(self):
        return self.containsItem(Names.METAL_LADDER)
    
    
class Sawhorse_Inventory(Inventory):
    def __init__(self, ref, itemList=[]):
        super(Sawhorse_Inventory, self).__init__(itemList)
        self.SAWHORSES_REF = ref
    
    def remove(self, removeThis):      
        super(Sawhorse_Inventory,self).remove(removeThis)

        if str(removeThis) == Names.METAL_LADDER: 
            Player.getRoomObj(Id.TORC).removeFurniture(self.SAWHORSES_REF.TORC_LDDR.getID())
    
    def add(self, item):
        if str(item) == Names.METAL_LADDER: 
                Player.getRoomObj(Id.TORC).addFurniture(self.SAWHORSES_REF.TORC_LDDR)

        return super(Sawhorse_Inventory,self).add(item)
    

class Torc_Lddr(Furniture):
    def __init__(self, ref):
        super(Torc_Lddr, self).__init__()

        self.SAWHORSES_REF = ref
        self.description = ("The ladder-like object sits horizontally across the sawhorses.")
        self.actDialog = ("You take the metal device off from the sawhorses.")
        
        self.addNameKeys("(?:metal )?ladder", "two parallel 10-foot long metal poles attached " +
                         "together via many shorter perpendicular metal poles")
        self.addActKeys(Furniture.GETPATTERN)
    
    def interact(self, key):  
        if self.SAWHORSES_REF.getInv().give(self.SAWHORSES_REF.METAL_LADDER, Player.getInv()):
            Player.getPos().removeFurniture(self.getID())
            return self.actDialog
        else:
            return Furniture.NOTHING



"""
    Gives player the scythe for the crypt puzzle.    
"""
class Torc_ScytheFurniture(Furniture, Resetable):
    # SEWP needs to access this, so this cannot be removed from the room when
    # player takes it. Instead, all names from this object are deleted. This
    # therefore needs to remember its name.
    def __init__(self):
        super(Torc_ScytheFurniture,self).__init__()

        self.searchDialog = ("It's just a big scythe on the wall.")
        self.description = ("It's a sharp black scythe hanging sideways on the wall. Decoration... perhaps?")
        self.actDialog = ("You reach up and take the scythe off the wall.")
        self.SCYTHE = Weapon(Names.SCYTHE, 80)
        self.NAME_KEY = "(?:large )?scythe"
        self.addNameKeys(self.NAME_KEY)
        self.addActKeys(Furniture.GETPATTERN)
    
    def interact(self, key):
        if Player.getInv().add(self.SCYTHE):
            self.NAMEKEYS = [] # Furniture 'disappears' from room.
            return self.actDialog
        else:
            return Furniture.NOTHING
    
    """
        Replaces scythe if player has it. 
    """
    def reset(self):
        if Player.hasItem(Names.SCYTHE):
            Player.getInv().remove(self.SCYTHE)
            self.addNameKeys(self.NAME_KEY) # This 're-appears' in room.from Furniture import Furniture



class Torc_Tools(Furniture):    
    def __init__(self):
        super(Torc_Tools,self).__init__()
        
        self.description = ("You are trying your best not to think of what these were used for.")
        self.actDialog = ("You don't know how to use these, and nor do you want to.")
        self.searchDialog = ("You aren't sure which one to search.")

        self.addNameKeys("(?:sinister )?(?:tools?|instruments?|apparatus(?:es)?)")
        self.addActKeys("use", "play")



class Torc_Wheel(SearchableFurniture, Unmoveable):
    def __init__(self):
        super(Torc_Wheel,self).__init__()
        
        self.description = ("The large wooden wheel is about 6 feet in diameter. " +
                           "The wheel has many small nicks and gashes on its " +
                           "surface, and many pegs stick out towards you around its " +
                           "edge. It is suspended from a stand and looks rotatable.")
        self.actDialog = ("You give the wheel a spin. It squeaks as it turns and " +
                         "quiets down slowly as the wheel comes to a halt.")
        self.searchDialog = ("You look behind the wheel.")

        self.addNameKeys("(?:large )?(?:vertical )?(?:wooden )?wheel", "pegs?")
        self.addActKeys("rotate", "spin", "turn")



class Torc_Wood(Furniture):    
    def __init__(self):
        super(Torc_Wood,self).__init__()

        self.description = ("The two square wooden beams are tied at the " +
                           "center and edges with rope. Both are bloodied. " +
                           "Below the center of the device, on the floor, is a drain.")
        self.addNameKeys("(?:square )?(?:wooden )?beams?", "drain")