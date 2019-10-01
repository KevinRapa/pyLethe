from Names import WEAPON
from Player import Player
from Item import Item
from Id import GCBT
from Things import LockedContainer, Chandelier
from Furniture import SearchableFurniture, Moveable, Openable, Furniture, Gettable

class Cobweb(Furniture, Gettable):
    def __init__(self):
        super(Cobweb,self).__init__()

        self.COBWEB = Item("cobweb ball", -30, use="What good would a balled-up cobweb serve?")
        self.description = ("It's a sticky mess of cobwebs, thankfully without the spiders.")
        self.actDialog = ("You grab some of the sticky matter.")
        self.searchDialog = ("The cobwebs aren't hiding anything...")
        self.useDialog = ("You ball up some of the cobwebs with it, but their are still a lot in this room.")

        self.addNameKeys("cobwebs?")
        self.addUseKeys(Furniture.ANYTHING)
        self.addActKeys(Furniture.GETPATTERN)
    
    def interact(self, key):              
        return self.getIt()
    
    def getIt(self):
        if Player.getInv().add(self.COBWEB):
            return self.actDialog
        else:
            return ("You already have all the cobweb you will ever need.")
    
    def useEvent(self, item):
        return (self.useDialog if item.getType() == WEAPON else Furniture.DEFAULT_USE)



class Gal5_Cabinet(LockedContainer):
    def __init__(self, itemList=[]):
        super(Gal5_Cabinet,self).__init__(GCBT, itemList)

        self.actDialog = ("The tiny gold key fits perfectly. You turn it and the " +
                              "cabinet makes a satisfying *click*.")
        self.description = ("It's a large wooden double-door cabinet. It is fancily " +
                           "carved and looks as though it holds something valuable.")
        self.searchDialog = ("The cabinet is locked. Looks like you'll need a key.")
        self.addNameKeys("(?:large )?(?:wood(?:en)? )?(?:double-door )?(?:curio )?cabinet")



class Gal5_Ceiling(Furniture):
    def __init__(self):
        super(Gal5_Ceiling,self).__init__()

        self.description = ("The ceiling in this room is low and arched, and dips " +
                           "down in the middle to hold the chandelier.")
        self.actDialog = ("You extend your arm and poke the ceiling.")
        self.addActKeys("touch", "poke")
        self.addNameKeys("ceiling")
        


class Gal5_Chandelier(Chandelier):
    def __init__(self):
        super(Gal5_Chandelier,self).__init__()

        self.description = ("The chandelier holds only a few melted candles. It's " +
                           "covered in cobwebs. This light has not been lit for a while.")
        self.searchDialog = ("The low-hanging chandelier is within reach, " +
                  "but contains nothing interesting.")
        self.useDialog = ("The candles are all too melted and old to light.")



class Gal5_Display(SearchableFurniture, Openable, Moveable):
    def __init__(self, itemList=[]):
        super(Gal5_Display,self).__init__(itemList)
        self.description = ("The hinged glass case is dusty and cloudy.")
        self.searchDialog = ("Dramatic music queues, you slowly open the display case.")
        self.addNameKeys("(?:hinged )?(?:glass )?(?:display|case)")