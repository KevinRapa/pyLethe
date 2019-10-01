from Item import Item
from Names import PHYLACTERY, COPPER_PAN, COPPER_POT, HAND_TORCH
from Player import Player
import re
import Direction
from Room import Room
from Furniture import *
from GUI import GUI
from Inventory import Inventory
from Things import Torch_Holder
from Structure_gen import StaticWindow

class Kitc_Barrels(SearchableFurniture, Openable, Unmoveable): 
    def __init__(self, itemList=[]):
        super(Kitc_Barrels,self).__init__(itemList)
        self.description = ("The two barrels are open and filled with stale barley and rye.")
        self.searchDialog = ("You look into the barrels.")
        self.addNameKeys("barrels?")



class Kitc_Cntr(SearchableFurniture, Openable, Unmoveable):
    def __init__(self, itemList=[]):
        super(Kitc_Cntr,self).__init__(itemList)
        self.description = ("The dark oak counters have a nice polished granite " +
                       "surface. Beautiful! There is a storage area underneath the counter.")
        self.searchDialog = ("You open the doors under the counter.")
        self.addNameKeys("counters?")



class Kitc_FrtPhy(Item):
    def __init__(self, name, score):
        super(Kitc_FrtPhy,self).__init__(name, score)
        self.type = PHYLACTERY
        self.description = ("This red, clean, shiny apple looks perfect! Huh... It has almost a glow to it.")



class Kitc_Hearth(SearchableFurniture, Unmoveable):
    def __init__(self, itemList=[]):
        super(Kitc_Hearth,self).__init__(itemList)
  
        self.description = ("The hearth is a simple square pit lined with mortared cobblestone.")
        self.searchDialog = ("You look inside the pit.")
        self.actDialog = ("You really could use a steak or ham right now.")
        self.useDialog = ("You try lighting the wood, but they are too rotted and moist from the coastal air to light.")
        
        self.addNameKeys("(?:unlit )?hearth", "(?:square )?pit")
        self.addActKeys("cook")
        self.addUseKeys(HAND_TORCH)



class Kitc_Pantry(SearchableFurniture, Openable, Moveable):
    def __init__(self, itemList=[]):
        super(Kitc_Pantry,self).__init__(itemList)

        self.description = ("A disgusting odor seeps out of the tall pantry.")
        self.searchDialog = ("The pantry creaks as you slowly open it.")
        self.addNameKeys("(?:tall )?pantry")



class Kitc_Pots(SearchableFurniture, Gettable):
    def __init__(self, pot, pan, itemList=[]):
        super(Kitc_Pots,self).__init__()
        
        self.inv = PotRack_Inventory(itemList)
        self.PAN_REF = pan
        self.POT_REF = pot
        
        self.description = ("A bunch of old copper pots and pans hang from the ceiling")
        self.searchDialog = ("You inspect the rack of pots.")
        self.actDialog = ("That's very loud!")
        self.useDialog = ("You store it.")
        
        self.addUseKeys(COPPER_POT, COPPER_PAN)
        self.addActKeys(Furniture.GETPATTERN)
        self.addActKeys(Furniture.JOSTLEPATTERN, "rattle")
        self.addNameKeys("(?:old )?(?:copper )?(?:pots?|pans?)", "pots and pans", "(?:pot|pan) rack")

    def interact(self, key):              
        if re.match(Furniture.JOSTLEPATTERN, key) or key == "rattle":
            if self.inv.isEmpty():
                return ("You jostle the rack and mildly amuse yourself.")
            else:
                return self.actDialog
        else:
            return self.getIt()

    def useEvent(self, item):
        Player.getInv().give(item, self.inv)
        return self.useDialog

    def getIt(self):
        if not self.inv.isEmpty():
            if self.inv.contains(str(self.POT_REF)) and Player.getInv().add(self.POT_REF):
                self.inv.remove(self.POT_REF)
                return ("You take a pot off.")
            elif self.inv.contains(str(self.PAN_REF)) and Player.getInv().add(self.PAN_REF):
                self.inv.remove(self.PAN_REF)
                return ("You take a pan off.")
            else:
                return ("You already have one of those.")
        else:
            return ("The rack is empty.")

     
class PotRack_Inventory(Inventory):
    def __init__(self, itemList=[]):
        super(PotRack_Inventory,self).__init__(itemList)
    
    def add(self, item):
        if str(item) == COPPER_POT or str(item) == COPPER_PAN:
            return super(PotRack_Inventory,self).add(item)
        else:
            GUI.out("That doesn't belong there!")
            return False



class Kitc(Room):
    def __init__(self, name, ID, ID2):
        super(Kitc,self).__init__(name, ID)
        self.TORCH_ID = ID

    def getBarrier(self, direct):
        i = Player.getPos().getFurnRef(self.TORCH_ID).getInv()
        
        if direct != Direction.WEST and i.isEmpty():
            return ("It's too dark to see anything, and you don't want to trip and fall.")
        else:
            return self.bumpIntoWall()

    def getDescription(self):
        if Player.getPos().getFurnRef(self.TORCH_ID).getInv().isEmpty(): 
            return ("This room is pitch black and fetid. All that's visible is an " +
                   "empty mounted holder on the wall next to you and a thin " +
                   "slitted window on the east end of the room.")
        else:
            return super(Kitc,self).getDescription()

    def triggeredEvent(self):
        if not Player.hasVisited(self.ID):
            GUI.out("As you step in, a fetid stench immediately infiltrates your senses. " +
                    "You gag a few times before attuning your yourself to the wretched odor.")
            
        if not Player.getPos().getFurnRef(self.TORCH_ID).getInv().isEmpty():
            return self.NAME
        else:
            return "Pitch black room"



class Kitc_Rack(SearchableFurniture):
    def __init__(self, itemList=[]):
        super(Kitc_Rack,self).__init__(itemList)
        self.description = ("It's a rack of hooks used to hold keys.")
        self.searchDialog = ("You look among the hooks.")
        self.addNameKeys("(?:key )?(?:rack|hooks?)")



class Kitc_Shelf(SearchableFurniture, Unmoveable):
    def __init__(self, itemList=[]):
        super(Kitc_Shelf,self).__init__(itemList)
        self.description = ("The tall shelf is filled with old wines.")
        self.searchDialog = ("You peruse the wine selection.")
        self.actDialog = ("Do you really want wine and broken glass everywhere?")
        
        self.addActKeys(Furniture.JOSTLEPATTERN)
        self.addNameKeys("shelf of wine", "wine(?: shelf| rack)?", "shelf")



"""
    Player must add a torch to this to light the room.
    Begins empty.    
"""
class Kitc_Torch(Torch_Holder):
    def __init__(self, torch):
        super(Kitc_Torch,self).__init__(torch)
        self.useDialog = ("You slide the torch into the steel holder, lighting the room.")
        self.inv = KitcHolderInventory()

    def interact(self, key):
        if key == "pull":
            return super(Kitc_Torch,self).interact(key)
        elif self.inv.contains(str(self.TORCH)):
            if self.inv.give(self.TORCH, Player.getInv()):
                Player.describeRoom()
                return self.actDialog
            else:
                return Furniture.NOTHING
        else:
            return ("The holder is empty you bumbling oaf.")

    def useEvent(self, item):
        if self.inv.contains(str(self.TORCH)):
            return ("The holder already bears a torch you bumbling oaf.")
        else:
            Player.getInv().give(item, self.inv)
            return self.useDialog 



class KitcHolderInventory(Inventory):      
    def __init__(self):
        super(KitcHolderInventory,self).__init__()

    def add(self, item): 
        if str(item) == HAND_TORCH and not self.size():
            Player.describeRoom()
            GUI.roomOut("Kitchen")
            return super(KitcHolderInventory,self).add(item)
        else:
            GUI.out("The " + str(item) + " doesn't fit in.")
            return False

    def remove(self, removeThis):      
        super(KitcHolderInventory,self).remove(removeThis)
        Player.describeRoom()
        GUI.roomOut("Pitch black room")



class Kitc_Window(StaticWindow):
    def __init__(self):
        super(Kitc_Window,self).__init__()
        self.actDialog = ("This window is just an open slit in the wall.")
        self.description = ("Looking through the foot-wide slit in the wall, you " +
                           "can see only the distant landscape of shoreline, trees, " +
                           "and mountains on the horizon.")