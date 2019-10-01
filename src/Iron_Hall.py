from Names import POLEARM
from Player import Player
import Id, Direction, AudioPlayer
from Mechanics import Lever
from Room import Room
from GUI import GUI
from Inventory import Inventory
from Furniture import SearchableFurniture, Furniture, Gettable, Moveable
from Things import BurningBowl
from Structure_gen import StaticWindow

class Iha1_Armor(Furniture, Moveable):
    def __init__(self):
        super(Iha1_Armor,self).__init__()

        self.description = ("It's plate armor holding a polearm. It stands gazing out the window.")
        self.actDialog = ("You will probably get hurt trying to do that.")
        self.searchDialog = ("You find a long polearm, but the gauntlet is gripping it too tightly to be pried open.")
        self.addActKeys("equip|wear", "pry|open", Furniture.GETPATTERN)
        self.addNameKeys("(?:suit (?:of )?|plate )?armor", POLEARM, 
                "(?:armor )?suit|gauntlet|hand")

    def interact(self, key):
        if key == "equip" or key == "wear":
            return self.actDialog
        else:
            return ("The suit's grip is too firm to do that.")



class Iha1_Bowl(Furniture):
    def __init__(self, ID, ref):
            super(Iha1_Bowl,self).__init__()

            self.jabbed = False
            self.FLOOR_ID = ID
            self.WOWKEY_REF = ref
            
            self.description = ("It's an unlit steel bowl hanging from the ceiling by a " +
                               "chain. A draft from the outside causes it to swing " +
                               "gently. As it rocks, you hear it rattle a little.")
            self.searchDialog = ("It's too high up to see if there's anything inside.")
            self.actDialog = ("It's too high up to do that with your hands.")
            self.useDialog = ("You give the hanging bowl a jab with the pole. " +
                             "A small piece of metal falls out onto the floor.")
            
            self.addUseKeys(POLEARM)
            self.addActKeys(Furniture.JOSTLEPATTERN, "poke", "jab")
            self.addNameKeys("(?:hanging )?(?:steel )?bowl")

    def useEvent(self, item):
        if not self.jabbed:
            Player.getPos().getFurnRef(self.FLOOR_ID).getInv().add(self.WOWKEY_REF) 
            AudioPlayer.playEffect(27)
            self.jabbed = True
            return self.useDialog
        else:
            return ("You jab the bowl, but nothing falls out.")



class Iha1_Lever(Lever):
    def __init__(self):
        super(Iha1_Lever,self).__init__()
        
        self.description = ("Next to the door is a big iron lever.")
        self.searchDialog = ("This is just a plain iron lever...")
        self.addNameKeys("(?:big )?(?:iron )?lever")

    def event(self, key):
        Player.getRoomObj(Id.ROTU).rotate()
        return ("you hear a loud rumble.")



class Iha1(Room):
    def __init__(self, name, ID):
        super(Iha1,self).__init__(name, ID)

    def getBarrier(self, direct):
        if direct == Direction.NORTH:
            AudioPlayer.playEffect(6)
            return ("The door is missing!")
        else:
            return self.bumpIntoWall() 



class Iha2_Armor(SearchableFurniture, Gettable, Moveable):
    def __init__(self, ref):
        super(Iha2_Armor,self).__init__()

        self.PLRM_REF = ref
        self.searchable = False
        self.inv = Armor_Inventory([ref])
        self.description = ("It's a suit of armor holding a polearm. Its gauntlet " +
                           "is wrapped around it, but awkwardly as if the gauntlet " +
                           "had been pried opened and then closed repeatedly.")
        self.searchDialog = ("The suit of armor is holding a polearm, but its " +
                            "gauntlet is wrapped around it awkwardly.")
        self.actDialog = ("You will probably get hurt trying to do that.")
        
        self.addActKeys("equip|wear", "pry|open", Furniture.GETPATTERN)
        self.addNameKeys("(?:suit (?:of )?|plate )?armor", POLEARM, 
                "(?:armor )?suit|gauntlet|hand")

    def getDescription(self):
        if self.containsItem(POLEARM):
            return self.description
        else:
            return "It's a suit of armor. It's gauntlets are empty."

    def getSearchDialog(self):
        if self.searchable:
            return "You look in the armor's gauntlet."
        else:
            return self.searchDialog 

    def interact(self, key):
        if key == "equip" or key == "wear":
            return self.actDialog
        elif key == "pry" or key == "open":
            if not self.searchable:
                self.searchable = True
                return ("You manage to pry the gauntlet open.")
            else:
                return ("The gauntlet is already open.")
        else:
            return self.getIt()

    def getIt(self):
        if not self.containsItem(POLEARM):
            return ("The suit of armor isn't holding a polearm anymore.")
        elif self.searchable:
            if self.inv.give(self.PLRM_REF, Player.getInv()):
                return ("You slide the weapon from the suit's gauntlet.")
            else:
                return Furniture.NOTHING
        else:
            return self.searchDialog


class Armor_Inventory(Inventory):
    def __init__(self, itemList=[]):
        super(Armor_Inventory,self).__init__(itemList)
    
    def add(self, item):
        if self.size() == 0 and str(item) == POLEARM:
            super(Armor_Inventorym,self).add(item)
            Player.getPos().addPolearm()
            return True # Only polearms may be added to self.
        else:
            GUI.out("The " + str(item) + " doesn't fit in.")
            return False
    
    def remove(self, removeThis):  
        # Item must be a polearm.
        self.CONTENTS.remove(removeThis)
        Player.getPos().removePolearm()



class Iha2_Bowl(BurningBowl):
    def __init__(self):
        super(Iha2_Bowl,self).__init__()

        self.description = ("It's a steel bowl of fire hanging from the ceiling " +
                           "by a chain. It burns steadily, lighting your end of " +
                           "the hallway. A draft from the outside causes it to " +
                           "swing gently.")



"""
    Updates description whenever polearm is taken or removed from armor.    
"""
class Iha2(Room):
    def __init__(self, name, ID):
        super(Iha2,self).__init__(name, ID)
        self.hasPolearm = True

    def removePolearm(self):
        self.hasPolearm = False

    def addPolearm(self):
        self.hasPolearm = True

    def getDescription(self):
        if self.hasPolearm:
            return super(Iha2,self).getDescription()
        else:
            return super(Iha2,self).getDescription().replace(" It holds a polearm in its gauntlet.", "")

    def getBarrier(self, direct):
        if direct == Direction.SOUTH:
            return "You should be getting out of here..." # For end game.
        else:
            return self.bumpIntoWall()



class Iha_Window(StaticWindow):
    def __init__(self):
        super(Iha_Window,self).__init__()
        self.escapeDialog = ("That won't do any good. It leads right back out into the courtyard. It's all barred up anyway.")
        self.description = ("Through the window, you can see the dilapidated moonlit courtyard.")