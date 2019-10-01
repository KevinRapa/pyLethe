from Furniture import SearchableFurniture, Furniture, Unmoveable
from Player import Player
from Structure_gen import Balcony, Door, Floor, Staircase, StaticWindow
from Item import Item
from Names import FIXED_LADDER, WHEEL_SPOKE, CROWBAR
from GUI import GUI
from Room import Room
import Id, Direction, AudioPlayer
from Things import Fireplace

class Wow1_Cart(SearchableFurniture):
    def __init__(self, itemList=[]):
        super(Wow1_Cart,self).__init__(itemList)
        self.description = ("It's a large wooden cart with a wheel sitting off of " +
                           "its axle on the floor.")
        self.useDialog = ("The spoke is probably of more use to you off of the wheel.")
        self.searchDialog = ("It looks like most of everything has been removed.")
        self.actDialog = ("What are you trying to do? The cart is clearly broken.")
        
        self.addUseKeys(WHEEL_SPOKE)
        self.addActKeys("ride|use", "fix|repair")
        self.addActKeys(Furniture.MOVEPATTERN)
        self.addNameKeys("(?:large )?(?:wooden )?cart", "wheel")

    def interact(self, key):
        if key == "fix" or key == "repair":
            return ("You aren't really learned enough in the school of cart fixing...")
        else:
            return self.actDialogf



class Wow1_Shelves(SearchableFurniture, Unmoveable):
    def __init__(self, itemList=[]):
        super(Wow1_Shelves,self).__init__(itemList)
        self.description = ("The shelves are stocked with many chemicals and tools.")
        self.searchDialog = ("You look on the shelves.")
        self.actDialog = ("So many tools! You are overwhelmed with choice, " +
                  "while lightly dabbing some sweat off your forehead.")
        
        self.addActKeys(Furniture.GETPATTERN)
        self.addNameKeys("shelf|shelves|jars|(?:cleaning )?tools|brushes|liquids")



class Wow2_Armor(Furniture):
    def __init__(self):
        super(Wow2_Armor,self).__init__()

        self.description = ("It's a suit of armor with its gauntlets pried open.")
        self.searchDialog = ("It's not holding anything anymore.")
        self.actDialog = ("You will probably get hurt trying to do that.")
        self.useDialog = ("The suit of armor must be tired of holding things.")
        self.addNameKeys("(?:suit (?:of )?|plate )?armor", "(?:armor )?suit|gauntlet|hand")
        self.addUseKeys(Furniture.ANYTHING)
        self.addActKeys("wear", "equip")

    def useEvent(self, item):
        if item.getType() == Names.WEAPON:
            return self.useDialog
        elif str(item) == Names.BROKEN_WARHAMMER:
            return ("The suit of armor is quite angry that you broke its warhammer.")
        else:
            return Furniture.DEFAULT_USE



class Wow2_Balcony(Balcony):
    def __init__(self, wow2Strs, lddr):
        super(Wow2_Balcony,self).__init__()

        self.STRS_REF = wow2Strs
        self.LDDR_REF = lddr
        self.description = ("You can't see much from down here. The balcony " +
                           "is small and crowded. You can see a door up there " + 
                           "against the east wall. You also spot what appears " +
                           "to be a rope on a shelf.")

        self.useDialog = ("You lean the ladder against the balcony. It's just tall enough.")
        
        self.addNameKeys("(?:small )?(?:crowded )?balcony", "wall")
        self.addUseKeys(FIXED_LADDER)

    def useEvent(self, item):
        Player.getPos().addFurniture(self.STRS_REF) # Add the ladder to WOW2.
        Player.getInv().remove(self.LDDR_REF) # Remove the ladder from player inventory.
        return self.useDialog



class Wow2_Door(Door):
    def __init__(self, direct):
        super(Wow2_Door,self).__init__(direct)
        self.description = ("It's in horrible condition. It's boarded shut, and " +
                          "numerous gashes and splinters cover it. A hole in " +
                           "the door is big enough to see through.")
        self.useDialog = ("You've been in there already and it's not worth the energy.")
        self.actDialog = ("Not even someone as burly as yourself could pull these boards off.")
        self.addNameKeys("hole", "(?:wood(?:en)?)?boards?")
        self.addActKeys("pry", "remove")

    def interact(self, key):
        if key == "pry" or key == "remove":
            return self.actDialog
        else:
            return super(Wow2_Door,self).interact(key)

    def useEvent(self, item):
        if str(item) == CROWBAR:
            return self.useDialog
        else:
            return super(Wow2_Door,self).useDialog



class Wow2_Floor(Floor):
    def __init__(self, wow2Strs, lddr, itemList=[]):
        super(Wow2_Floor,self).__init__("A sandstone tiled floor.", itemList=[])
        
        self.STRS_REF = wow2Strs
        self.LDDR_REF = lddr
        self.useDialog = ("You stand the ladder on the floor leaning against the balcony.")
    
    def useEvent(self, item):
        Player.getPos().addFurniture(self.STRS_REF) # Add the ladder to WOW2.
        Player.getInv().remove(self.LDDR_REF) # Remove the ladder from player inventory.
        return self.useDialog



class Wow2_Hole(Furniture):
    def __init__(self):
        super(Wow2_Hole,self).__init__()

        self.description = ("You peek through the hole. The room next door is " +
                           "ash-filled and burnt to a crisp! In the far corner " +
                           "of the room, you see a ladder leading up.")
        self.searchDialog = ("The hole is but empty space. You have nothing to search.")
        self.addNameKeys("hole")



"""
    Created from the wooden rod, broken ladder, and wooden spoke.    
"""
class Wow2_Ladder(Staircase):
    def __init__(self, direction, dest):
        super(Wow2_Ladder,self).__init__(direction, dest, 16)
        self.searchDialog = ("The ladder hides nothing.")
        self.description = ("The ladder rests against the upper balcony, but it's unstable from the debris.")
        
        self.NAMEKEYS = []
        self.addNameKeys("ladder", FIXED_LADDER)

    def interact(self, key):     
        super(Wow2_Ladder,self).interact(key)
        return Furniture.NOTHING



"""
    Player must use the fixed ladder on the floor or balcony to reach Wow3    
"""
class Wow2(Room):
    def __init__(self, name, ID):
        super(Wow2,self).__init__(name, ID)

    def getBarrier(self, direct): 
        AudioPlayer.playEffect(6)
        
        if direct == Direction.EAST:
            return ("The door here is battered and boarded up.")
        else:
            return Room.WALL_BARRIER

    def getDescription(self):
        if self.hasFurniture("ladder"):
            return super(Wow2,self).getDescription().replace("you. There's", 
                    "you. A ladder now rests against the lip of the balcony. There's a boarded " +
                   "up door on the east wall of this room. There's", 1)
        else:
            return super(Wow2,self).getDescription()

    def triggeredEvent(self):
        if not Player.hasVisited(self.ID):
            GUI.out("A comfortable ambient-warmth swarms around you as " +
                     "you enter this lofty two-story chamber.")
        
        return self.NAME



class Wow2_Stairs(SearchableFurniture):
    def __init__(self):
        super(Wow2_Stairs,self).__init__()

        self.description = ("The remnants of the stairs lie crumbled all over the floor.")
        self.searchDialog = ("There's nothing among all these rocks but more rocks.")
        self.actDialog = ("Don't be ridiculous. The stairs are crumbled down.")
        self.addNameKeys("staircase", "stairs", "steps")
        self.addActKeys(Furniture.CLIMBPATTERN, "walk", "use")
        
        rock = Item("rubble", -15)
        self.inv.add(rock) 
        self.inv.add(rock) 
        self.inv.add(rock)



class Wow3_Door(Door):
    def __init__(self, direct):
        super(Wow3_Door,self).__init__(direct)
        self.description = ("To your immediate right is a wooden door with vertical " +
                        "slats. The door looks beaten up just like the door below you.")



class Wow3_NorthDoor(Furniture):
    def __init__(self):
        super(Wow3_NorthDoor,self).__init__()

        self.description = ("The door is hopelessly blocked by the large shelf.")
        self.actDialog = self.description

        self.addNameKeys("north door")
        self.addActKeys("open", "use")



class Wow3(Room):
    def __init__(self, name, ID, wow2lddr, ID2, Ilddr):
        super(Wow3,self).__init__(name, ID)
        
        self.WOW3LDDR_REF = Wow2_Ladder(Direction.DOWN, Id.WOW2)
        self.WOW2LDDR_ID = ID2
        self.LDDRITEM_REF = Ilddr
        self.FLR_ID = ID

    def getBarrier(self, direct):
        if direct == Direction.NORTH:
            AudioPlayer.playEffect(6)
            return ("There's a rather large shelf in the way.")
        elif direct == Direction.WEST:
            return ("There's a railing there, and that drop looks intimidating.")
        else:
            return self.bumpIntoWall()

    def triggeredEvent(self):
        if Player.getLastVisited() == Id.WOW2:
            if Player.hasVisited(self.ID):
                if not self.hasFurniture(self.WOW3LDDR_REF.getID()):
                    self.addFurniture(self.WOW3LDDR_REF)
                
                GUI.out("The ladder creaks with instability. You were more " +
                        "careful in scaling the ladder this time.")
            else:
                wow2 = Player.getRoomObj(Id.WOW2)
                wow2.removeFurniture(self.WOW2LDDR_ID)
                wow2.getFurnRef(FLR_ID).getInv().add(self.LDDRITEM_REF)
                AudioPlayer.playEffect(31)
                GUI.out("You successfully scale the ladder, but you accidentally " +
                        "knock it down with your final step, you uncoordinated oaf.")
        
        return self.NAME



class Wow3_Shelf(SearchableFurniture):
    def __init__(self, itemList=[]):
        super(Wow3_Shelf,self).__init__(itemList)
        self.description = ("A big hefty wooden shelving unit. Now that's what you call a shelf!")
        self.searchDialog = ("You look among the shelves.")
        self.actDialog = ("This is way too heavy to move. There's not much space to move this to anyway.")
        self.addNameKeys("(?:large )?(?:wood )?shelf")
        self.addActKeys("move", "push", "pull")



class Wow_Hearth(Fireplace):
    def __init__(self, bckt):       
        super(Wow_Hearth,self).__init__(bckt)
        self.descLit = ("A large arched hearth made of clay brick. The hearth " +
                       "was undoubtedly designed for drying linens.")



class Wow_Window(StaticWindow):
    def __init__(self):
        super(Wow_Window,self).__init__()
        self.description = ("Through the window, you can see out the front of the " +
                           "castle into the forest you walked through to get here. " +
                           "The forest gradually follows the slope of the hill " +
                           "downward and winds to the west along the foothills of " +
                           "a distant mountain.")