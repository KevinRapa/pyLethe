import Direction, AudioPlayer
from Furniture import *
from Structure_gen import Balcony, Door, Staircase
from Room import Room
from Player import Player
from Names import METAL_BUCKET, EMPTY_VIAL, TEST_TUBE
from Item import Ingredient, Item        


class Eow1_Basket(SearchableFurniture, Openable, Moveable):
    def __init__(self, itemList=[]):
        super(Eow1_Basket,self).__init__(itemList)
        
        self.description = ("It's a tall wicker basket.")
        self.searchDialog = ("You take a look in the basket.")
        self.addNameKeys("(?:tall )?(?:wicker )?basket")



class Eow1_Door(Door):
    def __init__(self, direct):
        super(Eow1_Door,self).__init__(direct)
        self.description = ("Carved on a metal plaque in its center is a jawless " +
                           "skull. The door is arched, pointed, and many other " +
                           "metal plates decorate the surface.")



class Eow1_Rack(SearchableFurniture, Moveable):
    def __init__(self, itemList=[]):
        super(Eow1_Rack,self).__init__(itemList)

        self.description = ("It's a plain weapon rack.")
        self.searchDialog = ("You take a look at its contents.")
        self.actDialog = ("Are we being lazy and not searching the rack first?")
        self.addActKeys(Furniture.GETPATTERN)
        self.addNameKeys("(?:plain )?(?:weapon )?rack", "weapons?")



class Eow2_Balcony(Balcony):
    def __init__(self):
        super(Eow2_Balcony,self).__init__()

        self.description = ("The second-floor balcony follows the north wall to the west and ends at a door.")
        self.addNameKeys("(?:small )?(?:second[- ]floor )?balcony")



class Eow2_Cabinet(SearchableFurniture, Openable, Moveable):
    def __init__(self, itemList=[]):
        super(Eow2_Cabinet,self).__init__(itemList)

        self.description = ("It's a tall pine utility cabinet.")
        self.searchDialog = ("You open the cabinet.")
        self.addNameKeys("(?:tall )?(?:pine |wood(?:en)? )?(?:utility )?cabinet")



"""
    Superficial, but justifies the presence of water in the room for filling the metal bucket.    
"""
class Eow2_Fountain(SearchableFurniture, Unmoveable):
    def __init__(self):
        super(Eow2_Fountain,self).__init__()

        self.description = ("The fountain is running smoothly with clear water. " +
                           "In its center is a tall statue of a helmed woman " +
                           "holding a staff and shield. It reminds you of the " +
                           "soldier statue in the ruined courtyard fountain. " +
                           "Now that you think about it, it's the same fountain.")
        self.searchDialog = ("Peering into the water-filled basin...")
        self.actDialog = ("Now is NOT the time for a swim, though it's tempting. You " +
                         "don't even have a change of clothes, and you aren't wearing "+
                         "servant's garb.")
        self.addActKeys("jump", "swim")
        self.addNameKeys("(?:great )?fountain", "(?:soldier )?statue")



class Eow2_Stairs(Staircase):
    def __init__(self, direction, dest):
        super(Eow2_Stairs,self).__init__(direction, dest, 15)
        self.description = ("The curved sandstone stairs lead to a small balcony " +
                           "above. It's a wonder why these didn't crumble like " +
                           "those in the west outer wall.")

    def getDescription(self):
        if self.DIR == Direction.DOWN:
            return ("The curved sandstone stairs lead down to the first floor. " +
                   "It's a wonder why these didn't crumble like those in " +
                   "the west outer wall.")
        else:
            return self.description



"""
    Entrance to the workshop.    
"""
class Eow4(Room):
    def __init__(self, name, ID):
        super(Eow4,self).__init__(name, ID)

    def getBarrier(self, direct):
        if direct == Direction.SOUTH:
            return ("The balcony railing is that way.")
        else:
            return self.bumpIntoWall()



class Water(Furniture, Gettable):
    def __init__(self, ref):
        super(Water,self).__init__()
        
        self.BUCKET_REF = ref
        self.description = ("Clean, sparkling water.")
        self.searchDialog = ("Just clean H2O here.")
        self.actDialog = ("Now is NOT the time for a swim, though it's tempting. You " +
                         "don't even have a change of clothes, and you aren't wearing " +
                         "servant's garb.")
        self.useDialog = ("You dip the bucket in and fill it with water.")
        
        self.addActKeys(Furniture.GETPATTERN)
        self.addActKeys("drink", "swim", "jump", "dive")
        self.addNameKeys("water", "clear water", "H20", "water (?:sink|fountain)") 
            # 'water sink' is so that "get ___ from the sink" works.
        self.addUseKeys(METAL_BUCKET, EMPTY_VIAL, TEST_TUBE)

    def useEvent(self, item):
        Player.getInv().remove(item)
        
        if str(item) == METAL_BUCKET:
            AudioPlayer.playEffect(42)
            Player.getInv().add(self.BUCKET_REF)
            return self.useDialog
        else:
            Player.getInv().add(Ingredient("H2O 50mL", 0, "The vial holds a small amount of H2O"))
            return ("You dip it under the water, uncontrollably filling it to the brim.")

    def interact(self, key): 
        if key == "swim" or key == "jump" or key == "dive":
            return self.actDialog
        elif key == "drink":
            return ("You take a sip of water and feel refreshed. Carrying " +
                   "all that stuff around has tired you.")
        else:
            return self.getIt()

    def getIt(self):
        if Player.hasItem(METAL_BUCKET):
            return self.useEvent(Player.getInv().get(METAL_BUCKET))
        elif Player.hasItem(EMPTY_VIAL):
            return self.useEvent(Player.getInv().get(EMPTY_VIAL))
        elif Player.hasItem(TEST_TUBE):
            return self.useEvent(Player.getInv().get(TEST_TUBE))
        else:
            return ("You'll need an empty bucket...")