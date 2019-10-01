from Furniture import SearchableFurniture, Moveable, Furniture
from Player import Player
from Inventory import Inventory
from Item import Item

class Dkch_Axle(Furniture):
    def __init__(self):
        super(Dkch_Axle,self).__init__()

        self.actDialog = ("That is dangerous and unecessary.")
        self.description = ("The wooden axle spins only a couple feet from your head.")

        self.addActKeys("stop")
        self.addNameKeys("(?:wooden )?(?:spinning )?(?:axle|shaft|driveshaft)")



class Dkch_Bed(SearchableFurniture, Moveable):
    def __init__(self, itemList=[]):
        super(Dkch_Bed,self).__init__(itemList)
        
        self.description = ("A cheap spring bed with no sheets, only a plain dirty mattress.")
        self.actDialog = ("Whoever owns this probably doesn't want you doing that...")
        self.searchDialog = ("You look under the bed.")

        self.addNameKeys("(?:cheap )?(?:spring )?bed", "(?:plain )?(?:dirty )?mattress")
        self.addActKeys(Furniture.SITPATTERN)



class Dkch_Ceiling(Furniture):
    def __init__(self):
        super(Dkch_Ceiling,self).__init__()

        self.description = ("The low ceiling arches to the floor on the chamber's east side.")
        self.addNameKeys("(?:arched )?ceiling")



class Dkch_Desk(SearchableFurniture, Moveable):
    def __init__(self, itemList=[]):
        super(Dkch_Desk,self).__init__(itemList)
        
        self.description = ("The plain wooden table has no drawers and only " +
                           "bears some papers and gadgets on the surface. " +
                           "The chair sits pushed in under it.")
        self.searchDialog = ("You look on the desk and chair surfaces.")

        self.addNameKeys("(?:plain )?(?:wooden )?(?:desk|chair|table)")



class Kampe_Box(Item):
    def __init__(self, itemList=[]):
        super(Kampe_Box,self).__init__("shoebox", 5, 
                "It resembles a large plain shoebox. Something rattles inside.", 
                use="You remove as much as you can.")
        
        self.EMPTY_BOX = Item("empty shoebox", 5, use="It's now empty.")
        self.BOX_INV = Inventory(itemList)
    
    def useEvent(self):
        while not self.inv.isEmpty():
            if not self.inv.give(self.inv.get(0), Player.getInv()):
                break
        
        if self.inv.isEmpty():
            Player.getInv().remove(self)
            Player.getInv().add(self.EMPTY_BOX)
        
        Player.printInv()
        return self.useDialog
