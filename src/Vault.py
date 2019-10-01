from Names import GLOWING_CHALICE, PHYLACTERY
from Room import Room
from Things import BurningBowl
from Item import Item
from Furniture import SearchableFurniture, Moveable, Openable, Unmoveable, Furniture
from GUI import GUI
import Id, Menus, Direction, AudioPlayer
from Patterns import VAUE_DOOR_COORDS_P
from Player import Player
import re

"""
    Contains the fourth phylactery.
    Connects to Vau2.    
"""
class Vau1(Room):
    def __init__(self, name, ID, tbl):
        super(Vau1,self).__init__(name, ID)
        self.Vau1_Tbl = tbl

    def getBarrier(self, direct):
        if direct == Direction.EAST or direct == Direction.WEST:
            return ("The ceiling slopes down to the floor to the east and west.")
        else:
            return self.bumpIntoWall()

    def getDescription(self):
        if self.Vau1_Tbl.containsItem(GLOWING_CHALICE):
            return super(Vau1,self).getDescription() + " Standing on the table is a glowing object."
        else:
            return super(Vau1, self).getDescription()



class Vau1_Table(SearchableFurniture, Moveable):    
    def __init__(self, itemList=[]):
        super(Vau1_Table,self).__init__(itemList)
        
        self.description = ("It's a clean marble table resting on two short columns. A satin tablecloth is draped over it")
        self.searchDialog = ("You look on the table.")
        self.addNameKeys("(?:clean )?(?:marble )?table")
    
    def getDescription(self):
        if self.containsItem(GLOWING_CHALICE):
            return self.description + ", and a glowing chalice rests on its surface."
        else:
            return self.description + "."



"""
    Connects to Vau1 and Vaue.    
"""
class Vau2(Room):
    def __init__(self, name, ID, tbl):
        super(Vau2,self).__init__(name, ID)
        self.Vau1_Tbl = tbl

    def getBarrier(self, direct):
        if direct == Direction.EAST or direct == Direction.WEST:
            return ("The ceiling slopes down to the floor to the east and west.")
        else:
            return self.bumpIntoWall()

    def getDescription(self):
        if self.Vau1_Tbl.containsItem(GLOWING_CHALICE):
            return super(Vau2,self).getDescription() + " Standing on a table at the far end is a glowing object."
        else:
            return super(Vau2,self).getDescription()



class Vau_Bowls(BurningBowl):
    def __init__(self):
        super(Vau_Bowls,self).__init__()

        self.description = ("The steel bowls hang from chains and burn. They hang " +
                           "low, as the ceiling itself is quite low too, and you " +
                           "must take care avoiding them.")

class Vau_Ceiling(Furniture):
    def __init__(self):
        super(Vau_Ceiling,self).__init__()

        self.description = ("The ceiling is sandstone like the rest of the room. " +
                           "It arches only feet above your head and gradually " +
                           "slopes down on either side of you meeting the floor.")
        self.addNameKeys("(?:low )?(?:arched )?ceiling")



"""
    The fourth phylactery, found on a table.    
"""
class Vau_ChalicePhylactery(Item):
    def __init__(self, name, score):
        super(Vau_ChalicePhylactery,self).__init__(name, score, "The enigmatic, jewel-encrusted chalice glows a light blue and emits a deep hum.")
        self.type = PHYLACTERY



class Vau_Chsts(SearchableFurniture, Openable, Moveable):
    def __init__(self, itemList=[]):
        super(Vau_Chsts,self).__init__(itemList)
        
        self.description = ("Scattered around the room are several wooden chests.")
        self.searchDialog = ("You pick a few chests and look inside them.")
        self.addNameKeys("(?:wooden )?chests?")
    
    def moveIt(self):
        AudioPlayer.playEffect(44)
        return ("You move the chest over a bit... Nope, just more treasure underneath.")



class Vaue_Door(Furniture, Unmoveable):
    ON = ("[o]")
    OFF = ("[ ]")
    BUTTONS = ((ON,ON,OFF,ON), (OFF,OFF,OFF,ON), (ON,ON,ON,OFF), (OFF,ON,OFF,OFF))
    
    def __init__(self):
        super(Vaue_Door,self).__init__()

        self.description = ("Standing before you is an interesting wall resembling " +
                           "a sliding door. On it is a 4 by 4 grid of buttons. Drawn " +
                           "on each is a dark circular rune")
        self.searchDialog = ("The only curiosity is the grid of buttons on the front.")
        
        self.addNameKeys("buttons?", "(?:sliding )?door", "(?:interesting |curious )?wall")
        self.addActKeys("push", "activate", "solve", "open")
    
    def interact(self, key):            
        ans = " "
        
        while ans:
            GUI.out(self.printButtons())
            ans = GUI.askChoice(Menus.VAEU_DOOR, VAUE_DOOR_COORDS_P)
            
            if ans:
                crds = re.split(" ?, ?", ans)
                self.switchButtons(int(crds[0]) - 1, 4 - int(crds[1]))
            
            if self.solved():
                Player.getRoomObj(Id.VAU2).setLocked(False)
                Player.getPos().removeFurniture(self.getID())
                AudioPlayer.playEffect(37)
                return ("As you push the last button, all the runes become lit. " +
                       "The wall recedes into the floor slowly. " +
                       "As the dust settles, a long room filled with treasure is revealed.")

        return self.actDialog
    
    def printButtons(self):
        row = 4
        b = ("\t\t\t\t\t")

        for i in Vaue_Door.BUTTONS:
            b += str(row)
            row -= 1
            
            for j in i:
                b += str(j)
            
            b += "\t\t\t"
        b += "  1  2  3  4 \t\t\t"
        
        return b
    
    def switchButtons(self, x, y):
        self.flip(x, y)
        self.flip(x + 1, y)
        self.flip(x - 1, y)
        self.flip(x, y + 1)
        self.flip(x, y - 1)
        AudioPlayer.playEffect(43)
    
    def flip(self, x, y):
        try:
            if Vaue_Door.BUTTONS[y][x] == Vaue_Door.ON:
                Vaue_Door.BUTTONS[y][x] = Vaue_Door.OFF
            else:
                Vaue_Door.BUTTONS[y][x] = Vaue_Door.ON
        except:
            pass
    
    def solved(self):
        for i in Vaue_Door.BUTTONS:
            for j in i:
                if j == Vaue_Door.OFF:
                    return False
        
        return True 