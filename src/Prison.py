from Things import Candelabra
import Id, Menus
from Patterns import ONE_TO_SIX
from Player import Player
from GUI import GUI
from Names import SHINY_WATCH, NL
from NonPlayerCharacter import NonPlayerCharacter
from Room import Room
from Furniture import SearchableFurniture, Unmoveable, Furniture, Openable, Moveable

class Pris_Cll(Furniture, Openable):
    def __init__(self, num, numWord, desc):
        super(Pris_Cll,self).__init__()
        self.description = ("The cell gate is locked. " + desc)
        self.addNameKeys("(?:gated )?(?:prison )?cell (?:" + num + "|" + numWord + ")")
    
    def getSearchDialog(self):
        return self.getDescription()


        
class Pris_Cabinet(SearchableFurniture, Openable, Moveable):  
    def __init__(self, itemList=[]):
        super(Pris_Cabinet,self).__init__(itemList)

        self.description = ("It's an old wood cabinet. The doors look ready to " +
                           "fall off their hinges.")
        self.searchDialog = ("You open up the cabinet.")

        self.addNameKeys("(?:old )?(?:wooden )?cabinet")



class Pris_Candelabra(Candelabra):
    def __init__(self, itemList):
        super(Pris_Candelabra,self).__init__(itemList)
        
        self.description = ("Scattered around the prison are several standing " +
                           "candelabras. Each one is rusted, the candles are " +
                           "heavily melted, and dried wax is seen dirtying " +
                           "every light. Still, the candles continue to burn.")
        self.addNameKeys("(?:rusted )?(?:standing )?(?:candelabras?|lights?)", 
                "(?:melt(?:ed|ing))?candles")



"""
    These can be searched to discover the solution to the Sew2 valve puzzle.    
"""
class Pris_Cells(Furniture, Openable, Unmoveable):
    def __init__(self):
        super(Pris_Cells,self).__init__()
        self.addNameKeys("(?:gated )?(?:prison )?cells?")
    
    def getDescription(self):
        GUI.out("There are 6 cells in this room. Each one is labeled with " +
                "a number. Inspect which one?")
        ans = GUI.askChoice(NL + "<#> Inspect", ONE_TO_SIX)
        return Player.getRoomObj(Id.PRIS).getCellDescription(int(ans))
    
    def getSearchDialog(self):
        return self.getDescription()



class Pris_Gates(Furniture, Openable):
    def __init__(self):
        super(Pris_Gates,self).__init__()

        self.searchDialog = ("The gate is locked.")
        self.description = ("Each cell is locked with an iron gate.")
        self.addNameKeys("(?:iron )?gates?")



class Pris_Ghost(NonPlayerCharacter):
    def __init__(self):
        super(Pris_Ghost,self).__init__()

        self.pleased = False    
        self.description = ("The apparition resembles a middle-aged bald male with a long beard. " +
                           "his eyes are blank, and he sits passively in the corner. He looks " +
                           "at you funny. \"Do you have a habit of staring?\" He asks.")
        self.actDialog = ("\"Now that I have my watch, I do not have any more reason " +
                         "to stay. I suppose I will find peace somewhere else in " +
                         "a little while.\"")
        self.searchDialog = ("The ghost looks to not have anything interesting.")
        self.addNameKeys("(?:spooky )?(?:sitting )?(?:blue )?(?:ghost|figure|person|apparition)", "him")
    
    def useEvent(self, item):
        if str(item) == SHINY_WATCH:
            Player.getInv().remove(item)
            return self.converse2()
        elif not self.pleased: 
            if self.firstTime:
                return "\"What is this? This isn't mine... I mean, I appreciate the gesture, but I'm looking for something else.\""
            else:
                return "\"I'm pretty sure that isn't it. Don't worry, I have all the time in the world.\""
        else:
            return "\"I appreciate the continued gifts, but I'm fine. Thank you.\""
    
    def interact(self, key):   
        if re.match(NonPlayerCharacter.ATTACK_PATTERN, key):
            return NonPlayerCharacter.ATTACK_DIALOG
        elif self.firstTime: 
            return self.converse1()
        elif not self.pleased:
            return ("\"Did you find something that might be it? " +
                      "Hand it over and let me see...\"")
        else:
            return ("\"I do understand that the Treasure is hidden in the caves " +
                "beneath this castle. I have watched Eury travel through " +
                "here many times, into the crypt, frustrated. The Treasure " +
                "does not want to be here, and desires only to be close to " +
                "where it was created. You should find the treasure where " +
                "the stench of hell is the strongest.\"")

    def converse1(self):
        firstTime = False
        
        GUI.menOut(Menus.ENTER)
        GUI.out("\"... ... ... You aren't Kampe. You better tread " +
                "carefully, or Kampe will lock you up as he did " +
                "me. It is not a wise decision to be here, stranger. " +
                "If you are down here to find Eury's Treasure, then " +
                "you have not descended far enough.\"")
        GUI.promptOut()
        
        GUI.out("\"I was foolish enough to try. Kampe's only job is " +
                "to guard the Treasure by walking these tunnels, " +
                "although the location of the Treasure has been " +
                "forgotten, even to Kampe. Most everyone who lives " +
                "here has either left or slipped into madness.\"")
        GUI.promptOut()
        
        GUI.out("\"This river here... you'd expect it to empty into " +
                "the surrounding sea. But it does not. This river " +
                "empties to a place much deeper, the place which " +
                "birthed the Treasure. If you seek it, I cannot help, " +
                "but you may find something in Kampe's quarters.\"")
        GUI.promptOut()
        
        
        GUI.out("\"In addition, Kampe took something from me. Ordinarily, " +
                "he would have locked my possessions in the cabinet next " +
                "to these cells. Be he took something special of mine, a " +
                "family heirloom, that I suspect is captive in his " +
                "quarters. Bring it to me, and I can offer more " +
                "information on the Treasure.\"")
        GUI.promptOut()
        
        return ("\"Ehhhh... ... No, I cannot remember what it is to tell " +
               "the truth. My mind is weakening on account of the water, " + 
               "but do not worry. I do not suffer here, for I do not " +
               "know the word's meaning any longer. All I know of myself " + 
               "is my name, Hypnos.\"")
    
    def converse2(self):
        self.pleased = True
        
        GUI.menOut(Menus.ENTER)
        GUI.out("\"Ah yes! I do believe this is it, a valuable watch handed " +
                "down to me from my mother. I would never leave this place " +
                "without it. Thank you, sir of the woods, knower of the " +
                "species', speaker to the birds.\"")
        GUI.promptOut()
        
        GUI.out("\"I do understand that the Treasure is hidden in the caves " +
                "beneath this castle. I have watched Eury travel through " +
                "here many times, into the crypt, frustrated. The Treasure " +
                "does not want to be here, and desires only to be close to " +
                "where it was created. You should find the treasure where " +
                "the stench of hell is the strongest.\"")
        GUI.promptOut()
        
        GUI.out(actDialog)
        GUI.promptOut()

        return ("\"... No I couldn't have just walked through the bars and " +
               "into Kampe's quarters. Ghosts do not work that way! Now " +
               "thank you, my friend.\"")



"""
    Holds a clue for solving the valve puzzle, contains the oubliette key.
    Oubliette key is not a necessary item.
    Connects to Sew3, Torc, and Sew5.
"""
class Pris(Room):
    CELLS = (
        Pris_Cll("1", "one", "You see a pair of wall shackles and a metal bucket on the floor."),
        Pris_Cll("2", "two", "Sitting in this cell is a spooky blue ghost " +
                  "a scruffy bald male with a long beard and primitive clothing."),
        Pris_Cll("3", "three", "This cell has the remains of a skeleton in it. It " +
                     "lacks anything below the pelvis, and one of its arms is shackled."),
        Pris_Cll("4", "four", "Nothing but a bucket and a few bones. There is a carving on the wall:" +
                  "                     __ " +
                  "                        _/// " +
                  "                      _///  " +
                  "               _______///   " +
                  "                \\\\\\\\\\\\\\or   " +
                  "                       or|     " +
                  "                     or|____  " +
                  "                    or|\\\\\\\\\\ " +
                  "                            "),
        Pris_Cll("5", "five", "You see a pair of wall shackles and a metal bucket on the floor."),
        Pris_Cll("6", "six", "The back wall here has caved in somewhat " +
                     "and the cell has filled with dirt.")
    )

    def __init__(self, name, ID):
        super(Pris,self).__init__(name, ID)

        for f in Pris.CELLS:
            self.addFurniture(f)

    def getCellDescription(self, i):
        return self.CELLS[i - 1].getDescription()



class Pris_Table(SearchableFurniture, Unmoveable):
    def __init__(self, itemList=[]):
        super(Pris_Table,self).__init__(itemList)
        
        self.description = ("It's a heavy wooden dining table sitting in the " +
                           "center of the room. It's exceedingly intricate for " +
                           "a place like this and does not suit this room.")
        self.searchDialog = ("You look on the table.")
        self.addNameKeys("(?:heavy )?(?:wooden )?(?:dining )?table")
