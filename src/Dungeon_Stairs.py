from Furniture import Furniture
import Id, Direction
from Player import Player
from Room import Room
from Tunnels import DungeonMonster
from Structure_gen import Staircase
        
class Dst1_Lantern(Furniture):
    def __init__(self):
        super(Dst1_Lantern,self).__init__()

        self.description = ("The old oil lantern is still lit and gives off a dim luminescence.")
        self.actDialog = ("The lantern is just out of your reach.")
        self.addActKeys(Furniture.GETPATTERN)
        self.addNameKeys("(?:hanging )?(?:oil )?(?:lantern|light)")



"""
    The only walkable way to dungeon.
    The player cannot use these stairs unless the SEW0 has been entered.
    ATT1 responsible for sending player to the lower level the first time.    
"""
class Dst1(Room):
    def __init__(self, name, ID):
        super(Dst1,self).__init__(name, ID)

    """
        Turns the monster around when player climbs the stairs in SEW0.
        Allows player to escape the creature if cornered in SEW0. 
    """
    def triggeredEvent(self):      
        if not DungeonMonster.isInactive() and Player.getLastVisited() == Id.SEW0:
            DungeonMonster.turnMonsterAround()
        return self.NAME



class Dst1_Stairs(Staircase):
    def __init__(self):
        super(Dst1_Stairs,self).__init__(Direction.DOWN, Id.SEW0, 15)
        self.description = ("The mossy stone spiral staircase winds down into the unknown.")
        self.actDialog = ("The sense of dread is overwhelming. " +
                      "You can't bring yourself to climb down them.")

    def interact(self, key):
        if Player.hasVisited(self.DEST):
            # Sets the room that the player is in.
            super(Dst1_Stairs, self).interact(key)
            
            return ("You circle down the steps. You can't sense how many levels, " +
                   "but it is not just one. After a short while, you reach a dark landing.")
        else:
            return self.actDialog