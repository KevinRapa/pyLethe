from Player import Player
from Names import HAND_TORCH, ROCK
import Direction
from Structure_gen import Floor, Door
from Item import Item
from Room import Room
from Furniture import SearchableFurniture
import random, re

"""
    The catacombs comprise a maze of similar tunnels.
    Each catacomb generates its own description, and will be described
    differently depending on if the player is holding a torch.    
"""
class Catacomb(Room):
    ITEM_LIST = (Item("dirt", -50), Item("bone", -50), Item("dirty rock", -50))

    def __init__(self, ID, wall, ceiling):
        super(Catacomb, self).__init__("Catacombs", ID)
        
        builder = ("The torch offers a small radius of light to see. You " +
                "are in a thin rocky tunnel with scattered crevices dug " +
                "into the walls. These are definitely graves. You shudder, " +
                "perhaps from the cold...                              " +
                "                                       To your ")
        
        """
           Builds the lit description of the room. Here, the constructor figures
           out what is in each direction of the catacombs. The description will
           reflect if there if empty space or a door in any direction.
       """
        X, Y = self.COORDS[2], self.COORDS[1] # X and Y coordinates of this room.

        # List of X and Y coordinates of the adjacent catacomb rooms.
        adjCatacombCoords = []
        
        # The X and Y coordinates of a non-catacomb room adjacent to self.
        adjOtherCoords = None
        
        # Holds directions to append to descLit.
        dirs = []

        for i in self.ADJ:
            coords = (int(i[2]), int(i[3]))

            if re.match(r"CT\d{2}", i): # Is a catacomb tunnel.
                adjCatacombCoords.append(coords)
            else:                      # Is a side room.
                adjOtherCoords = coords

        # Figures out the directions in which there are more catacombs.
        for j in adjCatacombCoords:
            if j[0] == Y - 1:
                dirs.append("NORTH")
            elif j[0] == Y + 1:
                dirs.append("SOUTH")
            elif j[1] == X - 1:
                dirs.append("WEST")
            elif j[1] == X + 1:
                dirs.append("EAST")

        # Appends the correct directions to descLit.
            if len(dirs) == 1:
                builder += dirs[0]
            elif len(dirs) == 2:
                builder += dirs[0] + " and " + dirs[1]
            else:
                i = 0 
                
                while i < len(dirs) - 1:
                    builder += (dirs[i] + ", ")
                    i += 1

                builder += "and " + dirs[i]
        
        builder += ", the tunnel veers into darkness. "
        
        # Appends additional information if a non-catacomb room is adjacent.
        # Adds a door to room.
        door = None
        
        if adjOtherCoords:
            if adjOtherCoords[0] == Y - 1:
                builder += "To the NORTH"
                door = Ct_Door(Direction.NORTH)
            elif adjOtherCoords[0] == Y + 1:
                builder += "To the SOUTH"
                door = Ct_Door(Direction.SOUTH)
            elif adjOtherCoords[1] == X - 1:
                builder += "To the WEST"
                door = Ct_Door(Direction.WEST)
            else:
                builder += "To the EAST"
                door = Ct_Door(Direction.EAST)
            
            builder += ", erected unevenly into the tunnel wall is an ancient door."

        self.descLit = builder
        
        # Puts a crevice furniture objects in here and adds items to it randomly.
        catGrv = Ct_Grave()
        catF = Floor("It's a damp, rocky, dirty floor.")
        numTimes = random.randint(0, 4) + 3
        
        for i in range(1, numTimes + 1): 
            catGrv.getInv().add(Catacomb.ITEM_LIST[random.randint(0,2)])

        # Important that catGrv is FIRST ITEM ADDED, iridescent jewel needs to be added to it.
        self.addFurniture(catGrv, catF, wall, ceiling)
        
        if door:
            self.addFurniture(door)

    def getDescription(self):
        if Player.hasItem(HAND_TORCH): 
            return self.descLit
        else:
            return super(Catacomb, self).getDescription()

    def triggeredEvent(self):
        return (self.NAME if Player.hasItem(HAND_TORCH) else "???")


class Ct_Door(Door):
    def __init__(self, direct):
        super(Ct_Door, self).__init__(direct)
        
        self.description = ("The door is ramshackle, held together with old dark boards nailed together and a rusty handle.")
        self.addNameKeys("(?:ancient |old |ramshackle )?(?:wooden )?(?:boarded )?door")

"""
    One of these holds the iridescent jewel.
"""
class Ct_Grave(SearchableFurniture):    
    def __init__(self, itemList=[]):
        super(Ct_Grave, self).__init__(itemList)
        
        self.description = ("Passed the wall, the crevice looks dug down somewhat. It seems to be filled with dirt and some rocks...")
        self.searchDialog = ("Apprehensively, you inspect the crevice, shallowly digging through the dirt with your hand.")
        self.addNameKeys("(?:scattered )?(?:crevices?|graves?|holes?)")
