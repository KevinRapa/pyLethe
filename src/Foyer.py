from Names import WEAPON, PHYLACTERY, LOOT_SACK, PHASE_DOOR_POTION
from Furniture import SearchableFurniture, Moveable, Openable, Furniture, Unmoveable
from Mechanics import Button
from Structure_gen import Staircase, DoubleStaircase, Door
import re
import Id, Direction, AudioPlayer
from Room import Room
from Things import Chandelier, Carpet, Statue
from GUI import GUI
from Inventory import Inventory
from Player import Player
from Item import Item, Note


class Foy1_Armoire(SearchableFurniture, Openable, Moveable):
    def __init__(self, itemList=[]):
        super(Foy1_Armoire,self).__init__(itemList)
        
        self.description = ("The clean lavender armoire stands on four stubby legs " +
                           "near the south corner of the foyer. Double doors " +
                           "on its front conceal possibly endless riches hidden inside.")
        self.actDialog = ("The armoire moves a tad from your kick. A light screech " +
                         "echos from the feet rubbing against the stone floor.")
        self.searchDialog = ("You open up the armoire and look inside.")
        self.useDialog = ("Are we feeling bloodthirsty? Or perhaps you didn't realize " +
                         "that the armoire is unlocked?")

        self.addNameKeys("(?:clean )?(?:lavender )?(?:armoire|cabinet|double doors?)")
        self.addUseKeys(Furniture.ANYTHING)
        self.addActKeys(Furniture.JOSTLEPATTERN)
    
    def useEvent(self, item):
        if item.getType() == WEAPON:
            return self.actDialog
        else:
            return Furniture.DEFAULT_USE



class Foy1_Carpet(Carpet):
    def __init__(self):
        super(Foy1_Carpet,self).__init__()

        self.description = ("A thick red carpet. On top sits the large table.")
        self.searchDialog = ("To your great curiosity, lifting up the carpet " +
                            "reveals a second identical carpet underneath.")
        self.addNameKeys("(?:thick )?(?:red )?(?:carpet|rug)")



"""
    Superficial. 
    Contains a note enticing player to enter the vestibule
"""
class Foy1(Room):
    def __init__(self, name, ID):
        super(Foy1,self).__init__(name, ID)   

    def getDescription(self):
        return super(Foy1, self).getDescription().replace("%", self.descMode(), 1)

    def descMode(self):       
        if Player.getPos().isAdjacent(Id.FOYW): 
            return ("an opened gate leads into another room.")
        else:
            return "a closed gate blocks your way into another room."

    def triggeredEvent(self):
        if not Player.hasVisited(self.ID):
            GUI.out("As you enter the spacious foyer, you recieve only the " +
                    "greeting of a faint musty odor lingering in the air. " +
                    "You carefully listen for any signs of inhabitants, but " +
                    "only hear the wind whistling.")
                    
        return self.NAME

    def getBarrier(self, direct):
        if direct == Direction.WEST:
            AudioPlayer.playEffect(4)
            return ("The gate that way is closed.")
        elif direct == Direction.EAST:
            return ("You should be getting out of here...") # For end game.
        else:
            return self.bumpIntoWall()



class Foy1_Stairs(Furniture):
    def __init__(self):
        super(Foy1_Stairs,self).__init__()

        self.description = ("A winding stone staircase hugs the curved wall " +
                           "on the far north side of the room.")
        self.searchDialog = ("It's too far away to see anything.")
        self.actDialog = ("'There's no way I can walk up those from here,' you " +
                         "think to yourself. 'I will have to walk closer.'")
        self.addActKeys(Furniture.CLIMBPATTERN, "use", "walk")
        self.addNameKeys("(?:winding )?(?:stone )?(?:staircase|stairs|steps)")



class Foy1_Table(SearchableFurniture, Moveable):
    def __init__(self, itemList=[]):
        super(Foy1_Table,self).__init__(itemList)
        
        self.description = ("It's a long mahogany table. A respectable wood among " +
                           "lumberjacks, it's a durable and workable species. You " +
                           "nod your head in appreciation.")
        self.actDialog = ("You nudge the table. It stands firmly in place, without even " +
                         "letting a creak. 'What a magnificent table!' you think to " +
                         "yourself. You give it another knock, and to your delight, " +
                         "another solid woody *knock* caresses your ear.")
        self.searchDialog = ("You quickly scan the table.")
        
        self.addActKeys(Furniture.JOSTLEPATTERN)
        self.addNameKeys("(?:long )?(?:mahogany |wood(?:en)? )?table")



"""
    Contains a statue hiding a button which switches gates in the foyer.
"""
class Foy2_Alcove(Furniture):
    def __init__(self, ID):
        super(Foy2_Alcove,self).__init__()
        self.STAT_ID = ID
        
        self.description = ("A shallow domed alcove carved into the wall. " +
                           "A statue has been displayed inside of it.")
        self.searchDialog = ("The large statue makes searching difficult. You " +
                            "can't seem to find anything.")
        
        self.addNameKeys("(?:shallow )?(?:domed )?alcove")

    def getDescription(self):
        stat = Player.getRoomObj(Id.FOY2).getFurnRef(self.STAT_ID)
        
        if not stat.moved():
            return self.description
        else:
            return ("A shallow domed alcove carved into the wall. Behind " +
                        "the displaced statue is a small black button.")

    def getSearchDialog(self):
        stat = Player.getRoomObj(Id.FOY2).getFurnRef(self.STAT_ID)
        
        return (self.searchDialog if not stat.moved() else \
            "With the statue moved, you see a small black button in the back.")



"""
    Switches the gates in the foyer
"""        
class Foy2_Button(Button):
    def __init__(self, ID1, ID2):
        super(Foy2_Button,self).__init__()

        self.actDialog = ("The two gates in the foyer switch positions.")
        self.N_GATE_ID = ID2
        self.S_GATE_ID = ID1
        self.addNameKeys("(?:small )?(?:black )?button")

    # Public in order to allow access from FOYW and FOYB.
    def event(self, key):
        bba1 = Player.getRoomObj(Id.FOYB)
        want = Player.getRoomObj(Id.FOYW)
        foy1 = Player.getRoomObj(Id.FOY1)
        foy2 = Player.getRoomObj(Id.FOY2)
        
        if not want.isAdjacent(Id.FOY1):
            want.addAdjacent(Id.FOY1)
            foy1.addAdjacent(Id.FOYW)
            
            foy2.removeAdjacent(Id.FOYB)
            bba1.removeAdjacent(Id.FOY2)
        else:
            want.removeAdjacent(Id.FOY1)
            foy1.removeAdjacent(Id.FOYW)
            
            foy2.addAdjacent(Id.FOYB)
            bba1.addAdjacent(Id.FOY2)
        
        # Opens or closes gate.
        Player.getRoomObj(Id.FOY2).getFurnRef(self.N_GATE_ID).swtch()
        Player.getRoomObj(Id.FOY1).getFurnRef(self.S_GATE_ID).swtch()

        AudioPlayer.playEffect(28)
        
        return self.actDialog



class Foy2(Room):
    def __init__(self, name, ID):
        super(Foy2,self).__init__(name, ID)

    def getDescription(self):
        return super(Foy2,self).getDescription().replace("%", self.descMode(), 1)

    def descMode(self):       
        if Player.getPos().isAdjacent(Id.FOYB):
            return ("an opened gate leads into another room.")
        else:
            return ("a closed gate blocks your way into another room.")

    def getBarrier(self, direct):
        if direct == Direction.NORTH:
            AudioPlayer.playEffect(4)
            return ("The gate that way is closed.")
        else:
            return self.bumpIntoWall()



class Foy2_Staircase(Staircase):
    def __init__(self, direction, dest):
        super(Foy2_Staircase,self).__init__(direction, dest, 15)
        self.description = ("A winding staircase run with red carpet all the way " +
                           "up. Looking straight " + str(direction) + ", it winds around " +
                           "until terminating at the " + 
                            ("third" if direction == Direction.UP else "first") + 
                            " floor, where it leads back to the south. Halfway " + 
                            str(direction) + " is a second floor landing to the north.")
        self.searchDialog = ("In searching the stairs, you find it as clean and " +
                            "bare as the rest of this room.")



"""
    Player must move this to discover a button.    
"""
class Foy2_Stat(Statue):
    def __init__(self, ref):
        super(Foy2_Stat,self).__init__()
        self.isMoved = False
        self.LVR_REF = ref
        self.description = ("A white marble statue. It depicts a woman holding " +
                           "a vessel of water on her shoulder. At its base, " +
                           "there appears to be some skid markings on the floor.")
        self.searchDialog = ("The statue appears to hide nothing, although, you can see " +
                            "streaks on the floor beginning at the statue's base.")
        self.addNameKeys("(?:skid )?markings")

    def interact(self, key):
        if re.match(Furniture.MOVEPATTERN, key):
            if not self.isMoved:
                Player.getPos().addFurniture(self.LVR_REF)
                AudioPlayer.playEffect(41)
                self.isMoved = True
                return ("You push the statue and manage to displace it a bit. " +
                       "In the alcove, behind the statue, you discover a small black button.")
            else:
                return ("You have moved the statue as far as you can.")
        else:
            return super(Foy2_Stat,self).interact(key)

    def moved(self):
        return self.isMoved



class Foy34_Carpet(Carpet):
    def __init__(self):
        super(Foy34_Carpet,self).__init__()
        
        self.description = ("The thick red carpet runner follows up and down the foyer staircase.")
        self.addNameKeys("(?:thick )?(?:red )?(?:carpet|rug)(?: runner)?")



"""
    Second floor landing of the foyer stairs.    
"""
class Foy3(Room):
    def __init__(self, name, ID):
        super(Foy3,self).__init__(name, ID)

    def getBarrier(self, direct):
        if direct == Direction.WEST:
            return "You should be getting out of here..." # For end game.
        elif direct == Direction.SOUTH:
            return "You aren't sure whether to go up or down."
        else:
            return self.bumpIntoWall()



class Foy3_Stairs(DoubleStaircase):
    def __init__(self):
        super(Foy3_Stairs,self).__init__(Id.FOY2, Id.FOY4, 15)
        self.description = ("From the second floor switchback, the stairs lead " +
                           "to a top floor landing.")
        self.searchDialog = ("In searching the stairs, you find it as clean and " +
                            "bare as the rest of this room.")



class Foy4_Door(Door):
    def __init__(self, direct):
        super(Foy4_Door,self).__init__(direct)

        self.description = ("The door has an engraving of a chalice on it.")



class Foy4(Room):
    def __init__(self, name, ID):
        super(Foy4,self).__init__(name, ID)

    def getBarrier(self, direct):
        if direct == Direction.WEST:
            return ("The staircase banister is that way.")
        else:
            return self.bumpIntoWall()



class Foy_Chandelier(Chandelier):
    def __init__(self):
        super(Foy_Chandelier,self).__init__()

        self.description = ("It's a huge iron chandelier. Its forged iron frame " +
                           "curves intricately. It holds numerous candles at " +
                           "least thirty. You are stunned by its majesty. At the " +
                           "same time, you ponder who has the time to maintain " +
                           "so many candles.")
        
        self.addNameKeys("(?:huge )?(?:iron )?(?:chandelier|light)")



"""
    Open and closeable gate toggled by a button in Foy2.
    Two of these in the foyer. Only one is ever open at a time.
"""
class Foy_Gate(Door, Unmoveable):
    def __init__(self, isOpen, direct):
        super(Foy_Gate,self).__init__(direct)
        
        self.description = ("An arched black iron gate barely taller than you. " +
                           "It looks like this kind lifts upward by a hidden pulley or chain.")
        self.DESCOPEN = ("With the gate retracted, there is only an open doorway.")
        self.searchDialog = ("You aren't sure what you'd search for on a gate.")
        self.SRCHOPEN = ("It's just an empty doorway.")
        self.DIALOPEN = ("It's just empty space. Maybe you should go through it?")
        self.actDialog = ("You try to lift the bars, but they are much too heavy.")
        self.isOpen = isOpen
        
        self.addActKeys("open", "lift")
        self.addNameKeys("gate", str(direct) + " gate")

    def getDescription(self):
        return (self.DESCOPEN if self.isOpen else self.description)

    def getSearchDialog(self):
        return (self.SRCHOPEN if self.isOpen else self.searchDialog)

    def swtch(self):
        self.isOpen = not self.isOpen

    def interact(self, key):
        if key == "close":
            if self.isOpen:
                return ("That would only impede your progress.")
            else:
                return ("The gate is closed already!")
        elif self.isOpen:
            return self.DIALOPEN
        elif key == "open" or key == "lift":
            return self.actDialog
        else:
            return super(Foy_Gate, self).interact(key)



"""
    The loot sack is a special item with its own inventory. As the player
    collects items, he or she may put them in the sack. This adds points
    to the player's score as a secondary objective.
    
    To access this item's inventory, it must be cast. Caution.
"""
class LootSack(Item):
    def __init__(self):
        super(LootSack, self).__init__(LOOT_SACK, 0, "An elegent black velvet sack with a rope " +
                  "wrapped around the top. A reddish aura coats its surface.")
        self.INV = SackInventory(self)
        self.type = LOOT_SACK
    
    def useEvent(self):
        AudioPlayer.playEffect(1)
        Player.search(self.INV)
        
        if Player.hasItem(LOOT_SACK):
            return ""
        else:
            return ("You stuff the sack inside itself and pull the string. " +
                    "All of the sudden, the sack is gone. You stand there, " +
                    "empty-handed, and confused.")
    
    def getInv(self):
        return self.INV
    
    # Returns the number of phylacteries in here.
    def countPhylacteries(self):
        result = 0
        
        for i in self.INV.CONTENTS:
            if i.getScore() == 2000 or i.getScore() == 3000:
                result += 1
        
        return result
    
    # Returns the number of special treasures in here.
    def countTreasures(self):
        result = 0
        
        for i in self.INV.CONTENTS:
            j = i.getScore()
            if j == 500 or j == 1000 or j == 1500:
                result += 1
        
        return result
    
    def isFull(self):
        return self.INV.isFull()
    
    def getWorth(self):
        return self.INV.getWorth()
    
class SackInventory(Inventory):
    def __init__(self, ref):
        super(SackInventory,self).__init__([Note("notice")])
        self.MAX_SIZE = 20
        self.worth = 0
    
    def isFull(self):
        return len(self.CONTENTS) >= self.MAX_SIZE
    
    def add(self, item):
        if len(self.CONTENTS) < self.MAX_SIZE:
            self.worth += item.getScore()
            Player.updateScore(self.getWorth())
            super(SackInventory, self).add(item)
            
            # The player may humorously put the sack inside itself.
            if item.getType() == LOOT_SACK:
                GUI.out("What paradoxical sin of nature are you trying to " +
                        "commit? You better take that back out before " +
                        "you break the universe.")
            elif item.getType() == PHYLACTERY:
                GUI.out("What sinful greed! Don't you realize we need to " +
                        "destroy those? The aether-dwellers look down " +
                        "shamefully upon you.")
            else:
                GUI.out("You stuff the " + str(item) + " inside the sack.")

            return True
        else:
            GUI.out("You can't fit anything more inside!")
            return False
    
    def remove(self, item):
        self.worth -= item.getScore()
        Player.updateScore(self.worth)
        super(SackInventory,self).remove(item)

    def getWorth(self):
        return self.worth
