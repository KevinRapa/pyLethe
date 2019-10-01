from Names import HAND_DRILL, WEAPON, CROWBAR
from Structure_gen import Ceiling, Staircase
import Direction
import re
from Things import Skeleton
from Furniture import Moveable, Openable, SearchableFurniture, Furniture, Unmoveable

class Gqua_Barrel(Furniture, Openable, Unmoveable):
    def __init__(self):
        super(Gqua_Barrel, self).__init__()

        self.description = ("It's a cask. You sure hope there's beer in there.")
        self.searchDialog = ("You can't get it open. You take a whiff from a crack in its surface. Disgusting!!")
        
        self.addUseKeys(Furniture.ANYTHING)
        self.addNameKeys("barrel", "cask")

    def useEvent(self, item):
        if item.getType() == WEAPON or str(item) == HAND_DRILL:
            return ("Whatever nasty liquid is in there, you definitely don't want it seeping out all over the place.")
        else:
            return Furniture.DEFAULT_USE



class Gqua_Ceiling(Ceiling):
    def __init__(self):
        super(Gqua_Ceiling, self).__init__()

        self.description = ("It's a low arched cobblestone ceiling supported by a few parallel wood trusses.")
        self.addNameKeys("(?:low )?(?:arched )?(?:cobblestone )?ceiling", "(?:parallel )?(?:wooden )?truss(?:es)?")



class Gqua_Ladder(Staircase):
    def __init__(self, direction, dest):
        super(Gqua_Ladder, self).__init__(direction, dest, 16)
        
        self.description = ("It's a sturdy wood ladder nailed to the wall. It " +
                           "leads " + str(self.DIR) + " a small hatch in the " + 
                ("floor" if direction == Direction.DOWN else "ceiling") + '.')
        
        self.NAMEKEYS = []
        self.addNameKeys("(?:sturdy )?(?:wood )?ladder")



"""
    Contains fertilizer, a required item.    
"""
class Gqua_Sacks(SearchableFurniture, Openable, Moveable):
    def __init__(self, itemList=[]):
        super(Gqua_Sacks, self).__init__(itemList)
        
        self.actDialog = ("The sacks are much too heavy to lift up.")
        self.description = ("Three large white cloth sacks sit carelessly tossed " +
                           "against the wall. They have names of various gardening " +
                           "materials on them.")
        self.searchDialog = ("You look into each of the sacks.")
        
        self.addUseKeys(Furniture.ANYTHING)
        self.addActKeys(Furniture.GETPATTERN)
        self.addNameKeys("(?:large )?(?:white )?(?:cloth )?sacks?")

    def useEvent(self, item):
        if item.getType() == WEAPON or str(item) == HAND_DRILL:
            return ("Don't be so reckless!")
        else:
            return Furniture.DEFAULT_USE



class Gqua_Shelf(SearchableFurniture, Unmoveable):
    def __init__(self, itemList=[]):
        super(Gqua_Shelf, self).__init__(itemList)

        self.description = ("A big hefty wooden shelving unit. Now that's what you call a shelf!")
        self.searchDialog = ("You look among the shelves.")
        self.actDialog = ("You give the big wooden shelf a jostle, but it shelf stands firmly in place letting off only a thick *knock*.")
        
        self.addNameKeys("(?:big )?(?:hefty )?(?:wooden )?(?:shelf|shelving unit)")
        self.addActKeys(Furniture.JOSTLEPATTERN)

    def interact(self, key):
        if re.match(Furniture.JOSTLEPATTERN, key):
            return ("You give it a kick. 'Wow, how sturdy! Truly a mark of artisan craftsmanship.'")
        else:
            return Furniture.DEFAULT_USE



"""
    Contains a crowbar, a required item.
"""
class Gqua_Skeleton(Skeleton):
    def __init__(self, itemList=[]):
        super(Gqua_Skeleton, self).__init__(itemList)

        self.description = ("The body lies face down on the floor.")

    def getDescription(self):
        if self.containsItem(CROWBAR): 
            return (self.description + " There's a crowbar in its hand.")
        else:
            return self.description



class Gqua_Stool(Furniture, Moveable):
    def __init__(self):
        super(Gqua_Stool, self).__init__()

        self.description = ("It's a puny three-legged stool.")
        self.actDialog = ("You sit in the tiny stool, feeling even more insecure about your mass.")
        self.addNameKeys("(?:puny |tiny )?(?:three-legged )?stool")
        self.addActKeys(Furniture.SITPATTERN)



"""
    Contains a screw, for constructing the red lens.    
"""        
class Gqua_Workbench(SearchableFurniture, Openable, Moveable):
    def __init__(self, itemList=[]):
        super(Gqua_Workbench, self).__init__(itemList)

        self.description = ("It's a poplar table with stuff on it.")
        self.searchDialog = ("You look through its various drawers and nooks.")
        self.actDialog = ("The workbench stands firmly in place, letting off only a thick-sounding *thud*.")
        
        self.addNameKeys("(?:poplar |wood(?:en)? )?(?:table|work ?bench)")
        self.addActKeys(Furniture.JOSTLEPATTERN)