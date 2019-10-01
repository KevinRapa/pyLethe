from GUI import GUI
import Id
from Names import HAND_TORCH, METAL_BAR
from Player import Player
from Tunnels import Dungeon_Tunnel
from Furniture import Furniture, Unmoveable, Resetable, Gettable
from East_Outer_Wall import Water

class Sewp_Ceiling(Furniture):    
    def __init__(self):
        super(Sewp_Ceiling,self).__init__()

        self.description = ("The ceiling is stone brick just like the rest of the room.")
        self.addNameKeys("ceiling")



"""
    The grate the player climb out of in escaping the cell.
    The player is not allowed to go backwards.    
"""
class Sewp_Grate(Furniture, Gettable):
    def __init__(self):
        super(Sewp_Grate,self).__init__()

        self.useDialog = ("Why would you want to cover that back up?")
        self.description = ("It's an open metal grate with the ladder descending " +
                           "into the hole that you escaped out of.")
        self.actDialog = ("You've just escaped! No need to back into the dangerous tunnel.")

        self.addUseKeys(METAL_BAR)
        self.addNameKeys("(?:metal )?(?:ladder|grate)")
        self.addActKeys(Furniture.CLIMBPATTERN, Furniture.GETPATTERN)
    
    def interact(self, key):
        if re.match(Furniture.CLIMBPATTERN, key):
            return self.actDialog
        else:
            return self.getIt()



"""
    Player emerges into this room from the ladder in escape tunnel
    Connects to Dkch and Sew3    
"""
class Sewp(Dungeon_Tunnel):
    def __init__(self, name, ID, ID2, resetables, ids):
        super(Sewp,self).__init__(name, ID)
        self.RESETABLES = resetables
        self.IDS = ids
        self.PRIS_CBNT_ID = ID2

    def resetAllObjects(self):
        for i in range(len(self.RESETABLES)):
            Player.getRoomObj(self.IDS[i]).getFurnRef(self.RESETABLES[i]).reset()
        
        Player.getRoomObj(Id.CIS1).reset()
        
        for i in Player.getInv():
            if not str(i) == HAND_TORCH and not str(i) == METAL_BAR:
                Player.getRoomObj(Id.PRIS).getFurnRef(self.PRIS_CBNT_ID).getInv().add(i)
        
        Player.getInv().clear()
        Player.setShoes("")
        Player.printInv()

    def triggeredEvent(self):
        if not Player.hasVisited(self.ID):
            GUI.out("You climb up the ladder into the room outside your cell. " +
                    "Looking north, you peer down a short thin tunnel into " +
                    "a larger area which you believe to be the source of the " +
                    "unsettling noise.")
            
        return self.NAME



class Sewp_Tunnel(Furniture, Unmoveable):
    def __init__(self):
        super(Sewp_Tunnel,self).__init__()

        self.description = ("To the north is a short way to a large open tunnel " +
                           "running to the west and east.")
        self.searchDialog = ("You will need to go over there to do that.")
        self.addNameKeys("(?:large )?(?:open )?tunnel")



class Sewp_Water(Water):
    def __init__(self, bckt):
        super(Sewp_Water,self).__init__(bckt)

        self.description = ("The water circles rapidly around the pool turning " +
                           "the wheel in the center. The driveshaft must be powering " +
                           "something. The water drains down a hole at the pool's bottom.")
        self.actDialog = ("It's probably not a good idea to step near that pool.")
        self.searchDialog = ("Anything that fell in there is long gone at this point.")

        self.addNameKeys("(?:large )?pool", "(?:vortex of )?water", "driveshaft", 
                "(?:submerged )?(?:water )?wheel")