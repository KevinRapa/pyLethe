from Things import BurningBowl, WallArt
from Names import HAND_TORCH
import re
from Furniture import SearchableFurniture, Openable, Moveable, Gettable, Furniture
from Room import Room
import Direction, AudioPlayer

class Tomb_Casket(SearchableFurniture, Openable, Moveable):
    def __init__(self, itemList=[]):
        super(Tomb_Casket,self).__init__(itemList)
        
        self.description = ("The casket is just a decrepit wooden box with a " +
                           "couple hinges on one side. Its ominous, solemn presence " +
                           "in the forgotten chamber gives off a sinister vibe.")
        self.actDialog = ("What a morbid thought... are you not cozy enough in this room?")
        
        self.addActKeys(Furniture.SITPATTERN, "go")
        self.addNameKeys("(?:decrepit )?(?:standing )?(?:wooden )?(?:casket|box|tomb|coffin)")



class Tmb1_Bowl(BurningBowl):    
    def __init__(self):
        super(Tmb1_Bowl,self).__init__()
        self.description = ("The hanging steel bowl lights the room in a flickering dim light.")



class Tmb2_Casket(Tomb_Casket):
    def __init__(self, itemList=[]):
        super(Tmb2_Casket,self).__init__(itemList)
        self.searchDialog = ("You slowly swing open the casket lid. A faint, musty " +
                "odor escapes. Though not unexpected, you are surprised " +
                "to see a preserved, but degenerate body standing limp " +
                "in the casket on several layers of fabric. The body " +
                "is emaciated and wrinkled, but you can still make out " +
                "its features, including the eyes. The body is dressed " +
                "in blue robes, probably a luxury during its time. A " +
                "silky braided rope is tied around the robe at the waist. " +
                "It wears the hat of a scholar or academic and holds its " +
                "hands cupped at the waist. You look in its hands.")



class Tmb1_Casket(Tomb_Casket):
    def __init__(self, itemList=[]):
        super(Tmb1_Casket,self).__init__(itemList)
        self.searchDialog = ("You slowly swing open the casket lid. A faint, musty " +
                "odor escapes. Though not unexpected, you are surprised " +
                "to see a preserved, but degenerate body standing limp " +
                "in the casket on several layers of fabric. The body " +
                "is emaciated and wrinkled, but you can still make out " +
                "its features, including the eyes. The body is dressed " +
                "in plain linens as a monk would wear. The body wears " +
                "a crown made of simple dried grasses and twine. It " +
                "holds its hands cupped at its waist. You look in its hands.")



class Tmb1_Effigy(WallArt):    
    def __init__(self):
        super(Tmb1_Effigy,self).__init__()
        self.description = ("It is a goat or pig skull tied to some crossing " +
                           "bundles of dried grass. It's held together by a wooden frame. " +
                           "You aren't able to tell if this is a memorial or effigy...")

        self.addNameKeys("(?:unsettling )?(?:effigy|idol|totem)")



class Tmb2_Light(Furniture):
    def __init__(self):
        super(Tmb2_Light,self).__init__()
        
        self.description = ("The orb is blinding and is the only thing lighting " +
                           "the room. It has no source, nor any vessel to contain it...")
        self.actDialog = ("You attempt to touch the orb, but the orb just dodges " +
                         "you autonomously.")
        self.searchDialog = self.actDialog

        self.addNameKeys("(?:inexplicable )?(?:orb of |ball of )?(?:blinding )?light")
        self.addActKeys(Furniture.GETPATTERN, Furniture.FEELPATTERN)



class Tmb3_Casket(Tomb_Casket):
    def __init__(self, itemList=[]):
        super(Tmb3_Casket,self).__init__(itemList)
        self.searchDialog = ("You slowly swing open the casket lid. There is nobody inside. " +
                            "You look at the bottom of the casket.")



class Tmb3_Cndl(Furniture, Gettable):
    def __init__(self):
        super(Tmb3_Cndl,self).__init__()
        
        self.description = ("The candles stand in the wall niches without any base " +
                           "only a collection of melted wax at the bottoms holds them " +
                           "upright. Perplexingly, the candles still burn steadily, " +
                           "not appearing to melt the wax any further.")
        self.useDialog = ("The torch is already lit, despite having been in your pocket all this time.")
        self.actDialog = ("Ouch! Really hot! Why would you do that to yourself?")
        
        self.addUseKeys(HAND_TORCH)
        self.addActKeys(Furniture.GETPATTERN, Furniture.FEELPATTERN)
        self.addNameKeys("(?:standing )?(?:wax )?candles?")
    
    def interact(self, key):
        if re.match(Furniture.FEELPATTERN, key):
            return self.actDialog
        else:
            return self.getIt("The candles are melted to the surface. You can't pick any up.")



class Tmb3_Tapestry(WallArt):    
    def __init__(self):
        super(Tmb3_Tapestry,self).__init__()
        self.description = ("The tapestry is mainly just superficial designs. " +
                           "Woven in the center is a hexagram inside of a circle.")

        self.addNameKeys("(?:small )?(?:hanging )?(?:torn |ripped )?tapestry")



class Tmb_Vases(SearchableFurniture, Openable, Moveable):
    def __init__(self, itemList=[]):
        super(Tmb_Vases,self).__init__(itemList)

        self.description = ("The various clay vases and jars lying around the floor " +
                          "have collected a generous amount of dirt, dust, and cobwebs. " +
                           "They're decorated plainly, as if made by a peasant.")
        self.searchDialog = ("There aren't too many vases to search. You peek into them all.")
        self.addNameKeys("(?:clay )?(?:vases?|jars?)")



"""
    There are three tomb rooms in the catacombs with keys for the casket
    in the ancient tomb.
    These are Asterion and Rhadamanthus' tombs, and Eurynomos' empty tomb.
    Connects to catacombs.    
"""
class Tomb(Room):
    def __init__(self, ID):
        super(Tomb,self).__init__("Small tomb", ID)

    def getBarrier(self, direct):
        AudioPlayer.playEffect(6)
        return ("There is barely any room in which to move.")