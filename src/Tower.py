import Direction
from Structure_gen import Window, Door, Balcony
from Furniture import Furniture, Unmoveable, SearchableFurniture
from Item import Item
from GUI import GUI
from Inventory import Inventory
from Names import DAMPENING_STAFF, GLOWING_SCEPTER, PHYLACTERY
from Player import Player
from Lichs_Quarters import Lich_Room
from Patterns import TOW1_SPHERE_P
import re

class AtriumDoor(Door):
    def __init__(self, direct):
        super(AtriumDoor,self).__init__(dir)
        
        self.description = ("The double doors are symmetrical and decorated with " +
                           "a fine lattice embossing. A carving of a snake curves " +
                           "around the edge of each door.")

        self.addNameKeys("(?:imposing )?(?:black )?(?:iron )?(?:double-?)?doors?")



"""
    Contains the scepter phylactery- player must have the dampening staff to obtain self.    
"""
class Tow1_Pedestal(SearchableFurniture):
    def __init__(self, itemList=[]):
        super(Tow1_Pedestal,self).__init__()
        
        self.inv = Pedestal_Inventory(itemList)
        self.searchable = False
        
        self.description = ("It's a solid gray stone platform with two brass extensions on the top.")
        self.searchDialog = ("You try to approach the pedestal, but some sort of repelling force is preventing you.")
        self.useDialog = ("You naively wave the staff in an arbitrary pattern. Nothing happens.")

        self.addNameKeys("(?:solid )?(?:gray )?(?:stone )?(?:pedestal|platform)", 
                "(?:silver )?(?:glowing )?(?:object|scepter)", "(?:brass )?extensions?")
        self.addUseKeys(DAMPENING_STAFF)
    
    def getDescription(self):
        if self.containsItem(GLOWING_SCEPTER):
            return self.description + " The extensions support a silver glowing object."
        else:
            return self.description
    
    def getSearchDialog(self):
        self.searchable = Player.hasItem(DAMPENING_STAFF)
        return ("You approach the pedestal" if self.searchable else self.searchDialog)
    

class Pedestal_Inventory(Inventory):
    def __init__(self, itemList=[]):
        super(Pedestal_Inventory,self).__init__(itemList)

    def add(item):
        if str(item) != DAMPENING_STAFF: 
            GUI.out("You may not want to leave that there, unless you never want it back.")
        
        return super(Pedestal_Inventory,self).add(item)



"""
    Contains the fifth phylactery.
    Connects to Bls1 and Foy4.
    Accessed from a key found in Vau2 with the fourth phylactery.    
"""
class Tow1(Lich_Room):
    def __init__(self, name, ID, pedestal):
        super(Tow1,self).__init__(name, ID)
        self.TOW_PEDESTAL = pedestal

    def getDescription(self):
        result = super(Tow1,self).getDescription() + self.TOW_PEDESTAL.getDescription()
        
        if not self.lichDead:
            return TOW1_SPHERE_P.sub(" You see a magnificent sphere of light hovering in the apex. ", 
                result, 1)
        else:
            return result

    def triggeredEvent(self):
        if not Player.hasVisited(self.ID):
            GUI.out("As you enter the room, your head begins to throb slightly.")
            
        return self.NAME



class Tow2_NorthDoor(Door):
    def __init__(self, direct):
        super(Tow2_NorthDoor,self).__init__(direct)
        
        self.description = ("The metal double doors are incised with many curved " +
                           "decorative etchings. Five circular etchings arranged pentagonally " +
                           "weave themselves in with the numerous other etchings. " +
                           "A stream of blue light fills ")

        self.addNameKeys("(?:imposing )?(?:glowing )?(?:metal )?(?:double-?)?doors?", "(?:door )?etchings?")
    
    def getDescription(self):
        numPhyl = Player.getInv().countPhylacteries()
        
        if numPhyl == 0:
            return self.description + "none of the circular etchings." 
        elif numPhyl == 5:
            return self.description + "all of the circular etchings." 
        else:
            return self.description + str(numPhyl) + " of the circular etchings."



"""
    Contains the source of the player's luring to the castle.
    Connects to Lqu1, Bls2, and Tbal    
"""
class Tow2(Lich_Room):
    def __init__(self, name, ID):
        super(Tow2,self).__init__(name, ID)

    def getDescription(self):
        if not self.lichDead:
            return super(Tow2,self).getDescription() + (" You see a magnificent glowing sphere of " +
                            "light hovering in the highest area of the tower. ")
        else:
            return super(Tow2,self).getDescription()

    def triggeredEvent(self):
        if not Player.hasVisited(self.ID):
            GUI.out("The throbbing in your head becomes quite uncomfortable.")

        if self.lichDead: 
            GUI.out("The glowing sphere of light has disappeared...")
        
        return self.NAME



class Tow_Balcony(Balcony):
    def __init__(self):
        super(Tow_Balcony,self).__init__()
        
        self.description = ("The long circular balcony wraps around the inner " +
                           "perimeter of the upper tower floor. A black metal " +
                           "railing guards the balcony's inner edge.")
        self.addNameKeys("(?:long )?(?:circular )?balcony", "(?:black )?(?:metal )?railing")



"""
    The fifth phylactery.    
"""
class Tow_ScepterPhylactery(Item):
    def __init__(self, name, score):
        super(Tow_ScepterPhylactery,self).__init__(name, score)
        self.type = PHYLACTERY
        self.description = ("It's a glimmering silver scepter holding a large opal " +
                        "at the top. The handle resembles a snake wrapped around a stick.")




"""
    The source of the player's luring to the castle. 
    It has an enticing glow and sound.    
"""
class Tow_Sphere(Furniture):
    def __init__(self):
        super(Tow_Sphere,self).__init__()

        self.description = ("The ball of bright yellow light pulses every few seconds and emits " +
                           "a dizzying low pitch. The sphere just hovers, still, high up in the center " +
                           "of the tower. The throbbing in your head exacerbates as you look. " +
                           "You are compelled to keep staring, but you pull your eyes away.")
        self.searchDialog = ("The sphere is too high to inspect more closely.")

        self.addNameKeys("(?:hovering )?(?:glowing |pulsing )?(?:yellow )?(?:sphere|ball|light)(?: of (?:yellow )?light)?")



class Tow_Windows(Window):    
    def __init__(self):
        super(Tow_Windows,self).__init__()

        self.descOpen = self.descClosed = ("From the wide paned windows, you can " +
                  "see far over and beyond the castle. The forest is much bigger " +
                  "than you imagined, and the amount of effort to trek here was " +
                  "far more than the amount you would ever naturally commit.")

        self.addNameKeys("(?:wide )?(?:paned )?windows?")
