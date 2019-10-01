from Names import PLATE
from GUI import GUI
from Inventory import Inventory
import re
from Player import Player
from Item import Book, Item
from Things import Statue , WallArt
import Id, Menus, Direction, AudioPlayer
from Patterns import OBS_STATS_ONE_TO_EIGHT, OBS_SLOTS_A_TO_I
from Furniture import SearchableFurniture, Moveable, Openable, Furniture, Unmoveable
from Room import Room
from Structure_gen import Balcony, StaticWindow, Staircase, DoubleStaircase

class Obs13_Stairs(Staircase):
    def __init__(self, direction, dest):
        super(Obs13_Stairs,self).__init__(direction, dest, 14)
        self.description = ("The spiral staircase sits in a round alcove carved " +
                           "into the wall to the southeast and leads up to a long, " +
                           "wide balcony on the second floor.")
        self.addNameKeys("spiral stair(?:s|case)")

    def getDescription(self):
        if self.DIR == Direction.DOWN:
            return ("The straight set of wood steps lack supports and extend " +
                "from the north wall. They lead down to the low-eastern balcony.")
        else:
            return self.description



class Obs1_Lamp(Furniture, Unmoveable):
    def __init__(self):
        super(Obs1_Lamp,self).__init__()

        self.description = ("The tall Victorian-era lamp is topped with a large " +
                           "glass orb holding a light bulb. It's quite bright and " +
                           "manages to light most of the room.")
        self.actDialog = ("That light looks really hot...")

        self.addNameKeys("(?:standing )?(?:lamp|light)")
        self.addActKeys(Furniture.HOLDPATTERN)



class Obs1_Plate(Item):
    def __init__(self, name):
        super(Obs1_Plate,self).__init__(name, 30)
        self.type = PLATE



class Obs1_Seat(SearchableFurniture, Moveable):
    def __init__(self, itemList=[]):
        super(Obs1_Seat,self).__init__(itemList)
        
        self.description = ("The Victorian-era red leather seat curves slightly to " +
                           "match the wall's curvature. It looks stiff.")
        self.actDialog = ("You rest a moment on the seat, gazing out the window at " +
                         "the distant lighthouse, wondering if anyone sees you.")
        self.searchDialog = ("You look under the seat.")

        self.addNameKeys("(?:victorian-era )?(?:stiff )?(?:red )?(?:leather )?seat")
        self.addActKeys(Furniture.SITPATTERN)



"""
    Holds the brass plates for observatory statue puzzle.    
"""
class Obs1_Slot(SearchableFurniture):
    def __init__(self, NAME, correct, desc, itemList=[]):
        super(Obs1_Slot,self).__init__()
        self.CORRECT = correct
        self.description = desc
        self.searchDialog = ("This indentation in the floor reads, " + desc[:17] + ".")
        self.addNameKeys(NAME, NAME.lower())
        self.inv = Slt_Inv(itemList)

    def isCorrect(self):
        if self.inv.size() == 1:
            plateName = str(self.inv[0])[:14].replace("\"", Furniture.NOTHING)
            return re.match(plateName, self.CORRECT)
        else:
            return False

    def getSearchDialog(self):
        if self.inv.size() == 1 and self.searchable:
            return ("A plate has been fit into the slot.")
        else:
            return self.searchDialog

    def getDescription(self):
        if self.inv.size() == 1:
            return ("The " + str(self.inv[0]) + " has been fit into the slot.")
        else:
            return self.description

    def lock(self):
        self.searchable = False


class Slt_Inv(Inventory):
    def __init__(self, itemList=[]):
        super(Slt_Inv,self).__init__(itemList)
    
    def add(self, item):
        if self.isEmpty():
            if item.getType() == PLATE:
                AudioPlayer.playEffect(43)
                super(Slt_Inv,self).add(item)
                return True
            else:
                GUI.out("It doesn't seem like that belongs here.")
        else:
            GUI.out("There's already a plate in here.")
        
        return False



"""
    Before being able to move the statues in the observatory, the player
    must find 8 brass plates and fit them in their correct spots.    
"""
class Obs1_Slots(Furniture):
    def __init__(self, hlsPlt, stats):
        super(Obs1_Slots,self).__init__()

        self.SLOTS = (
            Obs1_Slot("I", "Sol",       "Inside the slot: \"Helios\""),
            Obs1_Slot("A", "Mercury",   "Inside the slot: \"Hermes\""),
            Obs1_Slot("B", "Venus",     "Inside the slot: \"Aphrodite\""),
            Obs1_Slot("C", "Terra",     "Inside the slot: \"Gaea\""),
            Obs1_Slot("D", "Mars",      "Inside the slot: \"Ares\""),
            Obs1_Slot("E", "Jupiter",   "Inside the slot: \"Zeus\""),
            Obs1_Slot("F", "Saturn",    "Inside the slot: \"Kronos\""),
            Obs1_Slot("G", "Caelus",    "Inside the slot: \"Uranus\""),
            Obs1_Slot("H", "Neptune",   "Inside the slot: \"Posiedon\"")
        )

        self.MAP = {
            'i' : 0, 'a' : 1, 'b' : 2, 'c' : 3, 'e' : 5, 'f' : 6, 'g' : 7, 'h' : 8, 'd' : 4
        }
        
        self.SLOTS[0].getInv().forceAdd(hlsPlt)
        
        self.description = ("It's an array of brass indentations on the floor. " +
                           "Each one bears an inscription.")
        self.searchDialog = ("You inspect the array of slots.")
        self.useDialog = ("There are eight slots here. Perhaps you should search among " +
                   "them the one in which to place that.")
        self.STATS_REF = stats
        
        self.addUseKeys(Furniture.ANYTHING)
        self.addNameKeys("(?:brass )?(?:slots?|indentations?)")

    def useEvent(self, item):
        if item.getType() == PLATE:
            return self.useDialog
        else:
            return "That doesn't belong there."

    def getDescription(self):
        choice = " "
        
        while choice:
            GUI.out(self.getArray() + "\t\t\t\t\t\t" + self.description) 

            choice = GUI.askChoice(Menus.OBS_SLOT_EX, OBS_SLOTS_A_TO_I)
           
            if choice:
                GUI.descOut(self.SLOTS[self.MAP[choice[0]]].getDescription())
        
        Player.describeRoom()
        return Furniture.NOTHING

    def getSearchDialog(self):
        rep = ""
        choice = " "
    
        while choice:
            GUI.out(self.getArray() + "\t\t\t\t\t\t" + self.description) 

            choice = GUI.askChoice(Menus.OBS_SLOT_SE, OBS_SLOTS_A_TO_I)
           
            if choice:
                slot = self.SLOTS[self.MAP[choice[0]]]
                Player.trySearch(slot)
                
                if self.checkSolved() and not self.areSlotsLocked():
                    rep = ("A luminescence from an unknown source begins seeping through the seams " +
                          "in the floor and under each statue. You hear a click. Something has been activated.")
                    self.lockSlots()
                    choice = Furniture.NOTHING
                elif self.areSlotsLocked():
                    rep = ("The " + slot + " has locked itself in place.")
                    choice = Furniture.NOTHING

            Player.printInv()
        
        return rep

    def getArray(self):
        a = self.SLOTS[1]
        b = self.SLOTS[2]
        c = self.SLOTS[3]
        d = self.SLOTS[4]
        e = self.SLOTS[5]
        f = self.SLOTS[6]
        g = self.SLOTS[7]
        h = self.SLOTS[8]
        i = self.SLOTS[0]
        
        return ("\t\t\t\t\t     {"+a+"}   " +
               "\t\t        {"+h+"}       {"+b+"} " +
               "\t\t         \t\t           " +
               "{"+g+"}    {"+i+"}    {"+c+"} " +
               "\t\t\t     \t             " +
               "{"+f+"}       {"+d+"} " +
               "                    {"+e+"}")

    def getIndex(self, stat):
        current = 0

        for i in self.SLOTS:
            if not re.match(stat, str(i)):
                current += 1
            else:
                break
             
        return current

    def checkSolved(self):
        isSolved = True
        
        for s in self.SLOTS: 
            if not s.isCorrect():
                isSolved = False
        
        if isSolved:
            self.STATS_REF.unlock() 
        
        return isSolved

    def lockSlots(self):
        AudioPlayer.playEffect(43)
        
        for s in self.SLOTS:
            s.lock()

    def areSlotsLocked(self):
        return not self.SLOTS[0].isSearchable()



"""
    Furniture type for the observatory statue puzzle.    
"""
class Obs1_Statue(Statue):
    def __init__(self, NAME, desc, position):
        super(Obs1_Statue,self).__init__()
        self.description = desc
        self.NAMEKEYS = []
        self.addNameKeys(NAME)



""" 
    The observatory statue puzzle. 
    Player must first find 8 brass plates around the castle and fit them into
    their respective indentation. On each plate reads a Greek diety, and its
    respective latinized equivalent is spelled in an indentation.
    
    Then, player must manipulate statue positions until each statue is in
    front of its name. A book on the second floor observatory describes each diety.
    
    SOLUTION
        5
     2     0
    6       1
     3     4
        7

    PLATE LOCATIONS
    Under the cushion in the Parlor.
    On a shelf in the parlor.
    Dig a hole with a shovel in Cou4 to find another.
    Behind tapestry in dining room.
    In trophy room cabinet.
    Chest in observatory.
    In back hall end table.
    Under plaque in Garden.
"""
class Obs1_Statues(Furniture):
    def __init__(self, ID):
        super(Obs1_Statues,self).__init__()

        self.solved = False
        self.locked = True
        self.actDialog = ("As the statue settles in place, a bright " +
                         "array of light forms on the floor. The chandelier " +
                         "high up at the third level descends.")
        self.description = ("An array of statues arranged in a circle. In the " +
                           "center stands an additional larger statue looking " +
                           "upwards.")
        self.searchDialog = ("They don't seem to be hiding anything unusual. " +
                            "An inspection of the floor around them reveals " +
                            "fine seams in the floor connecting them in various ways.")
        self.CHNDLR_ID = ID
        
        self.SOLUTION = ("5", "0", "1", "4", "7", "3", "6", "2")
        self.STATS = (
            Obs1_Statue("0", "A beautiful woman stands on this base. She stands with long hair and no clothing on a large sea-shell.", 3),
            Obs1_Statue("1", "The statue depicts a pregnant short-haired female figure holding a newborn.", 2),
            Obs1_Statue("2", "On this statue stands a towering older male figure. He wears a glorious beard and poses triumphantly holding a trident.", 1),
            Obs1_Statue("3", "This statue shows a glorious sitting bearded male. He is well-built and dressed in a heavy robe. He holds a scythe.", 4),
            Obs1_Statue("4", "It shows a tall male figure dressed in soldier's garb. He wears a tall galea helmet and holds a spear and shield.", 5),
            Obs1_Statue("5", "On its base stands a male figure of average build. He wears sandals, a heavy cloak, and a winged helmet.", 6),
            Obs1_Statue("6", "A male wearing light armor stands on this base. He holds a staff in his left hand.", 7),
            Obs1_Statue("7", "This statue depicts a glorious bearded male striding forward holding a lightning bolt. You cannot contain your tears.", 8),
            Obs1_Statue("8", "The statue displays a monumental male figure crowned with a radiating halo. He rides in a chariot pulled by four steeds.", 0)
        )   

        self.addNameKeys("statues?", "ring(?: of statues)?", "gods?", "goddess(?:es)?")
        self.addActKeys(Furniture.MOVEPATTERN, "turn|spin", "admire")

    def getDescription(self):
        rep = Furniture.NOTHING
        choice = " "
        
        GUI.out(self.description + " ")
        
        while choice:
            GUI.out(self.getArray() + "\t\t\t\t\t\t" + rep)    
            choice = GUI.askChoice(Menus.OBS_STATS, OBS_STATS_ONE_TO_EIGHT)
            
            if choice:
                rep = getStatRef(choice).getDescription()
        
        return Furniture.NOTHING

    def interact(self, key):
        rep = Furniture.NOTHING

        if key == "admire":
            return "What otherworldly beauty!"
        elif not self.locked and not self.solved:
            choice = " "
            statNum = 0

            while choice:         
                GUI.out(self.getArray())
                GUI.menOut(Menus.OBS_STAT_MEN)
                choice = re.split(" ?", GUI.promptOut())

                try:
                    action = choice[0]
                    slot = choice[0]
                    statNum = int(slot)

                    if action == "r" and 0 <= statNum < 8:       
                        self.rotateStat(slot)
                    elif action == "m" and 0 <= statNum < 8:
                        self.moveStat(slot)
                    elif action == "r" or action == "m" and statNum == 8:
                        self.spinArray()
                    else:
                        GUI.out("That's not a valid choice.")           
                except:
                    if choice:
                        GUI.out("Type an action and a statue number.") 

                if self.checkSolved():
                    Player.getRoomObj(Id.OBS3).getFurnRef(self.CHNDLR_ID).lower()
                    rep = self.actDialog
                    self.solved = True
                    choice = Furniture.NOTHING
        elif self.locked:
            AudioPlayer.playEffect(6)
            rep = ("The statues budge only a slight amount. Something might " +
                      "be locking them in place")
        else:
            AudioPlayer.playEffect(6)
            rep = ("The statues have locked in place once again.")
        
        return rep

    def getArray(self):
        a = str(self.STATS[0])
        b = str(self.STATS[1])
        c = str(self.STATS[2])
        d = str(self.STATS[3])
        e = str(self.STATS[4])
        f = str(self.STATS[5])
        g = str(self.STATS[6])
        h = str(self.STATS[7])
        i = str(self.STATS[8])
        
        return ("\t\t\t\t\t     {"+a+"}--\\" +
               "\t\t        {"+h+"}       {"+b+"} " +
               "\t\t        /\t\t           " +
               "{"+g+"}    {"+i+"}    {"+c+"} " +
               "\t\t\t    /\t             " +
               "{"+f+"}       {"+d+"} " +
               "                 \\__{"+e+"}")

    def moveStat(self, stat):
        AudioPlayer.playEffect(44)
        
        if self.getIndex(stat) in (0, 2, 4, 6):
            self.moveThese(0, 2, 4, 6)
        else:
            self.moveThese(1, 3, 5, 7)    

    def rotateStat(self, stat):
        AudioPlayer.playEffect(44)
        i = self.getIndex(stat)

        if i == 0 or i == 1:
            self.switchThese(0, 1)
        elif i == 2 or i == 3:
            self.switchThese(2, 3)
        elif i == 4 or i == 5:
            self.switchThese(4, 5)
        elif i == 6 or i == 7:
            self.switchThese(6, 7)

    def getIndex(self, stat):
        current = 0

        for i in self.STATS:
            if not re.match(stat, str(i)):
                current += 1
            else:
                return current
             
        return -1

    # Swaps two adjacent statues that are connected.
    def switchThese(self, first, second):
        temp = self.STATS[first]
        self.STATS[first] = self.STATS[second]
        self.STATS[second] = temp

    # Moves every other statue starting from first to the right.
    def moveThese(self, first, second, third, fourth):
        temp = self.STATS[first]
        self.STATS[first] = self.STATS[fourth]
        self.STATS[fourth] = self.STATS[third]
        self.STATS[third] = self.STATS[second]
        self.STATS[second] = temp 

    # Rotates every statue one to the right
    def spinArray(self):
        AudioPlayer.playEffect(44)
        temp = self.STATS[0]
        self.STATS[0] = self.STATS[7]

        for count in range(7, 1, -1):
            self.STATS[count] = self.STATS[count - 1]

        self.STATS[1] = temp 

    def checkSolved(self):
        for index in range(8):
            if not re.match(self.SOLUTION[index], str(STATS[index])):
                return False
        return True

    def unlock(self):
        self.locked = False

    def getStatRef(self, name):
        for s in self.STATS:
            if str(s) == name:
                return s
        
        return None # Shouldn't happen because name must be a number from 0 to 8from Furniture import SearchableFurniture, Unmoveable



class Obs1_Telescope(SearchableFurniture, Unmoveable):
    def __init__(self, itemList=[]):
        super(Obs1_Telescope,self).__init__(itemList)
        self.description = ("The large old heavy telescope sits as an antique " +
                           "against the west wall. It looks to be made of mostly " +
                           "aluminum, bronze, and wood. A small eyepiece connects to a 1 " +
                           "foot-wide lens near the top. Many various gears and other " +
                           "parts comprise it as well.")
        self.searchDialog = ("You carefully look through its various intricacies.")
        self.actDialog = ("You look into the eyepiece and see nothing but black.")

        self.addNameKeys("(?:large )?(?:old )?(?:heavy )?(?:antique )?telescope")
        self.addActKeys("use", "look", "gaze", "view")



"""
    Holds a book which helps with the observatory puzzle.    
"""
class Obs2_BkShlf(SearchableFurniture):
    def __init__(self, itemList=[]):
        super(Obs2_BkShlf,self).__init__(itemList)
        
        self.description = ("The tall dark brown bookshelf rests on small curved feet.")
        self.searchDialog = ("You look on the shelves.")

        self.addNameKeys("(?:tall )?(?:brown )?(?:shelf|bookshelf)", "books")



class Obs2_Chair(Furniture, Moveable):
    def __init__(self):
        super(Obs2_Chair,self).__init__()

        self.description = ("The tall lavender lounge chair looks quite comfortable to sit in.")
        self.actDialog = ("You sit down for a moment, pondering various worldly mysteries. " +
                         "The chair is as comfortable as it looks, and you feel almost at home.")
        self.searchDialog = ("The chair isn't hiding anything unusual.")

        self.addNameKeys("(?:tall )?(?:lavender )?(?:lounge )?chair")
        self.addActKeys(Furniture.SITPATTERN)



class Obs2_Lamp(Furniture, Moveable):
    def __init__(self):
        super(Obs2_Lamp,self).__init__()

        self.description = ("The electric lamp looks like it's made of clay. It lights " +
                           "the chair's vicinity just enough in order to read comfortably.")
        self.addNameKeys("(?:electric )?(?:table )?(?:lamp|light)")



class Obs2_Painting(WallArt):
    def __init__(self):
        super(Obs2_Painting,self).__init__()
        self.description = ("The small, thick-framed painting depicts a ship " +
                          "sailing during a storm on thrashing waves.")
        self.addNameKeys("(?:thick-framed )?painting")



"""
    Holds a book describing dieties of Greek polytheism
"""
class Obs2(Room):
    def __init__(self, name, ID):
        super(Obs2,self).__init__(name, ID)

    def getBarrier(self, direct):
        if direct == Direction.WEST:
            return ("The balcony railing is that way.")
        else:
            return self.bumpIntoWall()



class Obs2_Railing(Furniture):
    def __init__(self):
        super(Obs2_Railing,self).__init__()

        self.description = ("The railing is quite thin, and does not appear as " +
                           "though it can take much weight. Certainly not your " +
                           "weight, that is.")
        self.actDialog = ("That is really not a very safe thing to do.")
        self.addNameKeys("(?:balcony )?railing")
        self.addActKeys("lean")



class Obs2_Stairs(DoubleStaircase):
    def __init__(self):
        super(Obs2_Stairs,self).__init__(Id.OBS1, Id.OBS3, 14)
        self.description = ("On each end of the balcony is a set of spiral stairs. " +
                           "One to the north leads to a third-floor balcony. The other " +
                           "to the south leads back down.")
        self.addNameKeys("spiral stair(?:s|cases?)")



"""
    Holds a ruby, one item needed in the Jade Hall puzzle.
"""
class Obs3_Chandelier(SearchableFurniture):
    def __init__(self, NAME, itemList=[]):
        super(Obs3_Chandelier,self).__init__(itemList)
        self.searchable = False
        self.description = ("The curved brass chandelier hangs high up from a " +
                           "chain extending through a hole in the ceiling. " +
                           "Secured in its center is a red jewel encompassed " +
                           "by the chandelier's many candles.")
        self.searchDialog = ("The chandelier is too high up.")
        self.actDialog = ("You would most certainly fall to your death...")
        
        self.addActKeys("swing", "hang")
        self.addNameKeys("(?:curved )?(?:brass )?(?:chandelier|light)")

    def getDescription(self):
        if self.searchable: 
            return ("The brass chandelier's chain, having extended from " +
                   "the ceiling, suspends the chandelier now level with the " +
                   "observatory's top floor. It's just within reach.")
        else:
            return self.description

    def getSearchDialog(self):
        return ("The chandelier is just within reach." if self.searchable else self.searchDialog)

    def lower(self):
        self.searchable = True



class Obs3_Chest(SearchableFurniture, Openable, Moveable):    
    def __init__(self, itemList=[]):
        super(Obs3_Chest,self).__init__(itemList)
        self.description = ("It's a wooden chest. 'Looks like the kind with " +
                           "treasure in it,' you think to yourself.")
        self.searchDialog = ("To your surprise, the chest is unlocked. You open it.")

        self.addNameKeys("(?:wooden )?chest")



class Obs3(Room):
    def __init__(self, name, ID):
        super(Obs3,self).__init__(name, ID)
    
    def getBarrier(self, direct):
        if direct == Direction.EAST:
            return ("The balcony railing is that way.")
        else:
            return self.bumpIntoWall()



class Obs3_Telescopes(Furniture, Moveable):    
    def __init__(self):
        super(Obs3_Telescopes,self).__init__()

        self.description = ("The telescopes have many different copper parts and " +
                           "intricate carvings. One of them is pointed at the " +
                           "lighthouse along the cliff in the distance.")
        self.actDialog = ("You gaze through the telescope pointed at the lighthouse. " +
                         "As the beacon rotates in your direction, the blinding glare " +
                         "forces your eye away.")
        self.searchDialog = ("They look like just plain telescopes. Expensive though.")

        self.addNameKeys("telescopes?")
        self.addActKeys("use", "look", "gaze", "view")



class Obs_Balcony(Balcony):
    def __init__(self):
        super(Obs_Balcony,self).__init__()
        self.description = ("One balcony to the east on the second level serves " +
                           "as the sole access point to the third floor. The " +
                           "third floor balcony starts at the northeast and curves " +
                           "around the west side of the room against the window.")
        self.addNameKeys("balcony", "balconies")



class Obs_Window(StaticWindow):
    def __init__(self):
        super(Obs_Window,self).__init__()
        self.escapeDialog = ("You could probably use your weight to break through... but aren't too keen on the idea.")
        self.description = ("Through the huge window, you can see a cliff far to the " +
                           "south rolling into the western fog. Farther away, you can " +
                           "see a lighthouse at the cliff's edge overlooking the sea.")
        self.addNameKeys("(?:three story )?(?:paned )?window")