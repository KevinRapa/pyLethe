from Names import METAL_BUCKET, EMPTY_VIAL, GLASS_BOTTLE, HOLY_WATER, FACTUM, MOP
import Id
from Player import Player
from Things import Carpet, Candelabra
from Structure_gen import Ceiling, StaticWindow
from Item import Note
from Furniture import *
import re

class Cha1_Candelabra(Candelabra):
    def __init__(self, *item):
        super(Cha1_Candelabra, self).__init__(item)
        
        self.description = ("The silver standing candelabras burn calmly and quietly.")
        self.addNameKeys("(?:silver )?(?:standing )?(?:lit )?candelabras?")



class Cha1_Cylix(Furniture, Moveable):
    def __init__(self):
        super(Cha1_Cylix, self).__init__()

        self.description = ("The cylix resembles a wide brass bowl decorated with many angular etchings.")
        self.actDialog = ("The cylix isn't portable enough to simply take.")
        self.useDialog = ("You begin banging the container against the bowl, but the " +
                         "bowl isn't fitting inside...")
        self.searchDialog = ("If your logic holds as well as this bowl holds water, " +
                            "you'd guess this vessel was filled with the holy kind. " +
                            "You can't pick up the water with your hands though.")
        
        self.addActKeys(Furniture.GETPATTERN, "drink")
        self.addNameKeys("(?:wide )?(?:brass )?(?:cylix|bowl)")
        self.addUseKeys(EMPTY_VIAL, METAL_BUCKET, GLASS_BOTTLE)

    def interact(self, key):
        if key == "drink":
            return ("You can't imagine that holy water is very palatable.")
        else:
            return self.actDialog



"""
    Contains holy water that the player needs to grow the mandragora for the
    enchanted bottle.    
"""
class Cha1_Water(Furniture, Gettable):
    def __init__(self, ref):
        super(Cha1_Water, self).__init__()

        self.REF_HOLY_WATER = ref
        self.description = ("It's seems to be just water, but it's most likely the holy kind.")
        self.searchDialog = ("You can't pick this up with your bare hands.")
        self.useDialog = ("You fill the small vial with a sample of holy water.")
        
        self.addActKeys("drink", "swim", Furniture.GETPATTERN)
        self.addNameKeys("water", HOLY_WATER, "clear water")
        self.addUseKeys(METAL_BUCKET, EMPTY_VIAL, GLASS_BOTTLE)

    def useEvent(self, item):
        if str(item) == EMPTY_VIAL:
            Player.getInv().remove(item)
            Player.getInv().add(self.REF_HOLY_WATER)
            return self.useDialog
        elif str(item) == METAL_BUCKET:
            return ("The bucket is too large to dip into the cylix.")
        else:
            return ("The bottle is small enough to fit in, but too wide to submerge the neck.")

    def interact(self, key): 
        if key == "swim":
            return ("How in the world are you going to fit in there??")
        elif key == "drink":
            return ("This water isn't for drinking.")
        else:
            return self.getIt()

    def getIt(self):
        if Player.hasItem(EMPTY_VIAL):
            i = None # Vial must be in inventory at this point.
            
            for j in Player.getInv():
                if str(j) == EMPTY_VIAL:
                    i = j
            
            Player.getInv().remove(i)
            Player.getInv().add(self.REF_HOLY_WATER)
            return ("You dip the vial in and collect some holy water.")
        elif Player.hasItem(METAL_BUCKET) or Player.hasItem(GLASS_BOTTLE):
            return ("The vessel you're carrying is too big to fit in the cylix.")
        else:
            return ("You have nothing suitable in which to hold the holy water.")



class Cha2_Altar(SearchableFurniture, Gettable, Unmoveable):
    URN_DESC = (" In the center sits a decorated stone and gold urn.")
    
    def __init__(self, itemList=[]):
        super(Cha2_Altar, self).__init__(itemList)
        
        self.description = ("The altar rests atop a small riser in front of the " +
                           "rows of pews. The altar is a tan marble table bearing " +
                           "a row of lit candles.")
        self.actDialog = ("No hitting things! This is a sacred place.")
        self.searchDialog = ("You look on the chapel altar.")
        self.useDialog = ("You've just moved...")

        self.addActKeys(Furniture.JOSTLEPATTERN, Furniture.GETPATTERN, "pray")
        self.addNameKeys("(?:tan )?(?:marble )?altar", "(?:lit )?candles?")
        self.addUseKeys(FACTUM)
    
    def interact(self, key):
        if key == "pray":
            return ("Praying fails to teleport you anywhere.")
        elif re.match(Furniture.JOSTLEPATTERN, key):
            return self.actDialog
        else:
            return self.getIt("You attempt to blow the flame off one candle before taking it, " +
              "but the flame refuses to die, thwarting your attempt.")
    
    def getDescription(self):
        if self.containsItem("gold urn"):
            return self.description + Cha2_Altar.URN_DESC
        else:
            return self.description
    
    def useEvent(self, item):
        Player.setOccupies(Id.VAUE)
        return self.useDialog



class Cha_Carpet(Carpet):
    def __init__(self):
        super(Cha_Carpet,self).__init__()
        
        self.description = ("The long red carpet runs in between the pews. Small " +
                           "puffs of smoke rise up with each step you take on it.")

        self.addNameKeys("(?:long )?(?:red )?carpet(?: runner)?")



class Cha_Ceiling(Ceiling):
    def __init__(self):
        super(Cha_Ceiling, self).__init__()

        self.description = ("The chapel ceiling is high and arched.")
        self.addNameKeys("(?:high )?(?:arched )?ceiling")



class Cha_Haze(Furniture, Gettable):
    def __init__(self):
        super(Cha_Haze,self).__init__()
        
        self.description = ("Though the room seems clean, a thin blanket of dust " +
                           "coats everything, and an ambient haze floats in the calm air.")
        self.actDialog = self.useDialog = ("You aren't a maid!")
        
        self.addUseKeys(MOP)
        self.addActKeys("clean", "sweep")
        self.addActKeys(Furniture.GETPATTERN)
        self.addNameKeys("(?:dusty )?haze", "dust")
    
    def interact(self, key):
        if key == "clean" or key == "sweep":
            return self.actDialog
        else:
            return self.getIt()



class Cha_Pews(SearchableFurniture, Moveable):
    def __init__(self, itemList=[]):
        super(Cha_Pews, self).__init__(itemList)

        self.description = ("Ten rows of uncomfortable pews fill the chapel nave. " +
                           "A walkway splits the rows in the room's center.")
        self.actDialog = ("These look quite uncomfortable though...")
        self.searchDialog = ("You walk up and down the aisle, scanning the pews.")

        self.addNameKeys("(?:uncomfortable )?(?:wood(?:en)? )?pews?")
        self.addActKeys(Furniture.SITPATTERN)



class Cha_Windows(StaticWindow):
    def __init__(self):
        super(Cha_Windows,self).__init__()

        self.description = ("The high stained glass windows tint the moonlight " +
                           "a calm bluish hue as it penetrates the glass. The " +
                           "windows do not depict anything in particular.")

        self.addNameKeys("stained glass windows?")