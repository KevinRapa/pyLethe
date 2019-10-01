from Names import SHROUDED_SHOES
from Player import Player
from GUI import GUI
import Id
from Things import PottedPlant
from Furniture import Furniture, SearchableFurniture, Openable, Moveable
from Room import Room
from Structure_gen import StaticWindow
from Item import Note

class Bha1_Horizon(Furniture):    
    def __init__(self):
        super(Bha1_Horizon, self).__init__()

        self.description = ("The floor of the hallway warps downwards paradoxically. " +
                           "You cannot see beyond perhaps twenty feet down the hallway, " +
                           "for the floor's curvature forms a horizon.")
        self.searchDialog = ("A horizon is too abstract a concept to search.")
        self.addNameKeys("horizon")



class Bha1_Plant(PottedPlant):     
    def __init__(self, soil, gift):
        super(Bha1_Plant, self).__init__(soil, gift)

        self.description = ("The plant doesn't seem to be in good shape. Though " +
                           "drooping a bit, it's still alive.")


"""
    Hides a brass plate for the observatory statue puzzle.
"""
class Bha1_Table(SearchableFurniture, Openable, Moveable):     
    def __init__(self, itemList=[]):
        super(Bha1_Table, self).__init__(itemList)
        
        self.useDialog = ("This table clearly has all four legs intact, you oaf.")
        self.description = ("A petite drawered end table.")
        self.searchDialog = ("You slide open the drawer and look inside.")
        self.actDialog = ("Jostling the table a little, you find its " +
                         "craftsmanship impressive. The carvings on it are " + 
                         "equally as such.")
        
        self.addUseKeys("broken table leg")
        self.addNameKeys("(?:drawered )?(?:end )?table")
        self.addActKeys(Furniture.JOSTLEPATTERN)



"""
   Contains a note and key to assist in the finding of the brass plates needed
   to solve the observatory puzzle.
"""
class Bha2_Frame(SearchableFurniture):    
    def __init__(self, itemList=[]):
        super(Bha2_Frame, self).__init__(itemList)
        
        self.description = ("The picture frame is charred but still intact.")
        self.searchDialog = ("You flip it over and look inside the frame.")
        self.addNameKeys("(?:charred )?(?:picture )?frame")



"""
    Sends player back to BHA1 if the player is not wearing the enchanted shoes.
    Supposed to generate the illusion that the hallway is infinitely long.
    Connects to Bha1 and Bha2
"""
class Bha2(Room):    
    def __init__(self, name, ID):
        super(Bha2, self).__init__(name, ID)

    def triggeredEvent(self):
        if not Player.getShoes() == SHROUDED_SHOES:
            if Player.getLastVisited() == Id.BHA1:
                Player.setOccupies(Id.BHA1)
            else:
                Player.setOccupies(Id.BHA3)
            
            GUI.out("You start pacing down the hallway in a state of vertigo. " +
                    "The hallway paradoxically continues to extend onward and warp " +
                    "downwards past a nearby horizon. After a short while, you stop and look behind you, " +
                    "seeing the door you just entered still only several feet away.")
            return str(Player.getPos())
        else:
            GUI.out("You pace lightly down the hallway almost effortlessly. You " +
                    "break free from your state of vertigo. Before long, " +
                    "you feel as though you have reached the room's center.")
            return self.NAME



class Bha3_Window(StaticWindow):
    def __init__(self):
        super(Bha3_Window, self).__init__()
        
        self.description = ("You peer out the window and see an expanse of ocean " +
                           "meeting the foot of the cliff on which the castle rests. " +
                           "You puzzle at the fact, thinking you were much farther " +
                           "from the castle at this point.")