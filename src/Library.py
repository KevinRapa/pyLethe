# -*- coding: utf-8 -*-
from Player import Player
from Mechanics import Button 
from GUI import GUI
from Inventory import Inventory
from Structure_gen import Window, Balcony, Column, Staircase
import re
from Things import Candelabra, Statue, Fireplace, WallArt
from Room import Room
from Furniture import Furniture, Moveable, SearchableFurniture 
import Direction, AudioPlayer
from Names import SHOES, LEATHER_SHOES, CRYSTAL_ORB, BIBLE, DANTES_INFERNO, ILIAD, ODYSSEY, PARADISE_LOST, CANDLE
from Item import Clothing, Item, Book

class Lib2_Button(Button):
    def __init__(self, ID, ID2):
        super(Lib2_Button,self).__init__()
        self.description = ("You look closely at the small stone button scorched " +
                           "from the heat of the fire. It's definitely a button.")
        self.FRPLC_ID = ID
        self.STAT_ID = ID2

    def interact(self, key):
        return self.event(key)

    def event(self, key):
        if Player.getRoomObj(Id.LIB2).getFurnRef(self.FRPLC_ID).isLit():
            AudioPlayer.playEffect(39, 30)
            return ("Ouch! There is fire in the way!")
        else:
            AudioPlayer.playEffect(11)
            return Player.getRoomObj(Id.LIB3).getFurnRef(self.STAT_ID).lightEye('l')



class Lib2_Fireplace(Fireplace):
    def __init__(self, bckt):       
        super(Lib2_Fireplace,self).__init__(bckt)

        self.descLit = ("The roaring fire from the large granite fireplace casts " +
                       "flickering shadows over the whole room. Like in the " +
                       "vestibule, you see a protrusion in the back. You guess " +
                       "fireplaces make good places to hide buttons. There's a " +
                       "small puddle of water in front of the fireplace.")
        self.descUnlit = self.descUnlit + " There's a small button in the back."
        
        self.searchDialogUnlit = ("You can't see much but ash. There looks to be a " +
                                 "small button in the back though.")


class Lib2(Room):
    def __init__(self, name, ID):
        super(Lib2,self).__init__(name, ID)

    def getBarrier(self, direct):
        AudioPlayer.playEffect(6)
        
        if direct == Direction.WEST or direct == Direction.EAST:
            return ("There's a bookshelf in the way.")
        else:
            return self.WALL_BARRIER


        
class Lib2_ShoeRack(SearchableFurniture, Moveable):
    def __init__(self, itemList=[]):
        super(Lib2_ShoeRack,self).__init__(itemList)
        self.description = ("It's a two-level low shoe rack.")
        self.searchDialog = ("You browse the shoe collection.")
        self.addNameKeys("shoe rack", "rack", "rack of shoes")



class Lib2_Statue(Statue):
    def __init__(self):
        super(Lib2_Statue,self).__init__()
        self.description = ("It's a Greek statue depicting a diplomatic male. " +
                           "Below, a small engraving reads \"Odysseus\".")



class Lib2_VoyageShelf(SearchableFurniture):
    def __init__(self, ID, ID2, ID3, ID4, itemList=[]):
        super(Lib2_VoyageShelf,self).__init__(itemList)
        
        self.WARFARE = ID
        self.CREATION = ID2
        self.PERDITION = ID3
        self.BANISHMENT = ID4
        
        self.actDialog = ("You push against the shelf, but it doesn't budge.")
        self.description = ("The tall bookshelf bears a plaque on the top reading " +
                           "\"Voyage\". At its base on the right, you notice " +
                           "consistent arched scratches on the floor.")
        self.searchDialog = ("You peruse its shelves.")
        self.addNameKeys("voyage", "(?:west|left) (?:(?:book)?shelf|one)")
        self.addActKeys(Furniture.MOVEPATTERN)

    def interact(self, key): 
        lib2 = Player.getRoomObj(Id.LIB2)
        wrfr = lib2.getFurnRef(self.WARFARE)
        crtn = Player.getRoomObj(Id.LIB3).getFurnRef(self.CREATION)
        perd = Player.getRoomObj(Id.LIB4).getFurnRef(self.PERDITION)
        bnsh = Player.getRoomObj(Id.LIB5).getFurnRef(self.BANISHMENT)
        
        if self.containsItem(self.ODYSSEY) and wrfr.containsItem(self.ILIAD) \
                and crtn.containsItem(self.BIBLE) and perd.containsItem(self.DANTES_INFERNO) \
                and bnsh.containsItem(self.PARADISE_LOST) and not lib2.isAdjacent(Id.LIB1):
            lib2.addAdjacent(Id.LIB1)
            AudioPlayer.playEffect(41)       
            return ("You push against the shelf. To your wonder, the shelf slowly " +
                "swivels clockwise on its center axis, revealing a hidden room.")
        else:
            return self.actDialog


        
class Lib2_WarefareShelf(SearchableFurniture):
    def __init__(self, itemList=[]):
        super(Lib2_WarefareShelf,self).__init__(itemList)       
        self.actDialog = ("You push against the shelf, but it doesn't budge.")
        self.description = ("The tall bookshelf bears a plaque on the top reading \"Warfare\".")
        self.searchDialog = ("You peruse its shelves.")
        self.addNameKeys("warfare", "(?:east|right) (?:(?:book)?shelf|one)")
        self.addActKeys(Furniture.MOVEPATTERN)



class Lib2_Window(Window):
    def __init__(self):
        super(Lib2_Window,self).__init__()

        self.descClosed = ("Through the small stone window, you can see your " +
                          "village in the great distance to the east. Ahead " +
                          "is just an expanse of sea and fog.")
        self.descOpen = self.descClosed + " A light breeze flows in."
        


class Lib3_CreationShelf(SearchableFurniture):
    def __init__(self, itemList=[]):
        super(Lib3_CreationShelf,self).__init__(itemList)
        self.description = ("The tall bookshelf bears a plaque on the top reading \"Creation\".")
        self.actDialog = ("You push against the shelf, but it doesn't budge.")
        self.searchDialog = ("You peruse its shelves.")
        self.addNameKeys("creation", "(?:south )?(?:book)?shelf")
        self.addActKeys(Furniture.MOVEPATTERN)



class Lib3_Painting(WallArt):
    def __init__(self):
        super(Lib3_Painting,self).__init__()

        self.description = ("A large portrait of a man hangs above the south " +
                           "bookshelf. It is decorated with a thick, expensive " +
                           "looking frame. The man is dressed in black robes, " +
                           "shiny leather shoes, and holds a silver scepter. " +
                           "He resembles the man from the portrait in the study...")
        self.actDialog = ("The painting is too high up to do that.")
        self.searchDialog = self.actDialog

        self.addNameKeys("(?:huge |large )?(?:painting|portrait)")



class Lib3(Room):
    def __init__(self, name, ID):
        super(Lib3,self).__init__(name, ID)

    def getBarrier(self, direct):
        if direct == Direction.SOUTH:
            AudioPlayer.playEffect(6)
            return ("There's a bookshelf in the way.")
        else:
            return self.bumpIntoWall()

    def triggeredEvent(self):
        if not Player.hasVisited(self.ID):
            GUI.out("As you step foot into this room, you feel your IQ rise a few points.")
            
        return self.NAME



class Lib3_Statue(Statue):
    def __init__(self, itemList=[]):
        super(Lib3_Statue,self).__init__()
        
        self.inv = Inventory(itemList)
        self.leftEye, self.rightEye = False, False
        self.description = ("The towering statue reaches a bit over a story tall. " +
                           "On its boxy rectangular base stands a prancing horse. " +
                           "A small square seam on the statue's base piques your interest.")
        self.searchDialog = ("A small square seam on the statue's base piques your interest.")
        self.actDialog = ("Such an impressive work of artistry deserves not to be " +
                         "tainted by your touch.")
        self.addNameKeys("(?:impressive )?(?:horse )?statue", "horse")

    def getDescription(self):
        if not self.leftEye and not self.rightEye:
            return self.description
        elif self.leftEye and not self.rightEye:
            return (self.description + " Its left eye glows eerily.")
        elif not self.leftEye and self.rightEye:
            return (self.description + " Its right eye glows eerily.")
        else:
            return (self.description.replace(" small square seam", "n open compartment") + " Both of its eyes glow eerily.")

    def getSearchDialog(self):
        if self.searchable:
            return ("You look into the compartment inside the statue's base")
        else:
            return self.searchDialog

    def makeSearchable(self):
            AudioPlayer.playEffect(44)
            self.addNameKeys("compartment")
            self.searchable = True
            return (" Both of the horse's eyes now glow. You hear a faint grinding noise.")

    def lightEye(self):
        rep = ("You push the button. As soon as you turn around, you " +
                   "notice the horse's " + ("right" if eye == 'l' else "left") + " eye glowing.")
        
        if eye == 'r':
            self.rightEye = True
        else:
            self.leftEye = True

        if self.rightEye and self.leftEye and not self.searchable:
            rep += self.makeSearchable()
        
        return rep



class Lib3_Window(Window):
    def __init__(self):
        super(Lib3_Window,self).__init__()
        
        self.descClosed = ("Through the small stone window, you can see your " +
                          "village in the great distance. A light fog rolls " +
                          "through the air.")
        self.descOpen = ("Through the small stone window, you can see your " +
                        "village in the great distance. A light fog rolls " +
                        "through the air. In flows a small breeze.")



class Lib4_Button(Button):
    def __init__(self, ID, ID2):
        super(Lib4_Button,self).__init__()
        self.description = ("You look closely at the small stone button scorched " +
                           "from the heat of the fire. It's definitely a button.")
        self.FRPLC_ID = ID
        self.STAT_ID = ID2

    def interact(self, key):
        return self.event(key)

    def event(self, key):
        if Player.getRoomObj(Id.LIB4).getFurnRef(self.FRPLC_ID).isLit():
            AudioPlayer.playEffect(39, 30)
            return ("Ouch! There is fire in the way!")
        else:
            s = Player.getRoomObj(Id.LIB3).getFurnRef(self.STAT_ID)
            AudioPlayer.playEffect(11)
            return s.lightEye('r')



class Lib4_Globe(Furniture, Moveable):
    def __init__(self):
        super(Lib4_Globe,self).__init__()
 
        self.description = ("The globe looks antique, but on a closer look, it " +
                           "seems fairly modern. Early 1920s you guess.")
        self.actDialog = ("You think to yourself, 'when I get out of here, I'd like " +
                      "to stay this adventurous but be three times as safe.' You " +
                      "spin the globe and blindly stop it on a country, intending " +
                      "to take take a well-earned vacation after this ordeal is " +
                      "through. You stop on the Soviet Union. 'Well, maybe I'll " +
                      "wait a few years for all that nonsense to end over there'.")
        self.addNameKeys("globe", "large globe")
        self.addActKeys("spin", "rotate", "turn")



class Lib4_PerditionShelf(SearchableFurniture):
    def __init__(self, itemList=[]):
        super(Lib4_PerditionShelf,self).__init__(itemList)
        self.description = ("The tall bookshelf bears a plaque on the top reading \"Perdition\".")
        self.actDialog = ("You push against the shelf, but it doesn't budge.")
        self.searchDialog = ("You peruse its shelves.")
        self.addNameKeys("perdition", "(?:west )?(?:book)?shelf")
        self.addActKeys(Furniture.MOVEPATTERN)



class Lib4(Room):
    def __init__(self, name, ID, tbl):
        super(Lib4,self).__init__(name, ID)
        self.REF = tbl

    def getBarrier(self, direct):
        if direct == Direction.WEST:
            AudioPlayer.playEffect(6)
            return ("There's a bookshelf in the way.")
        else:
            return self.bumpIntoWall()

    def getDescription(self):
        if not self.REF.containsItem(CRYSTAL_ORB):
            return re.sub(r" A glimmering.+them\.", "", super(Lib4,self).getDescription())
        else:
            return super(Lib4,self).getDescription()



class Lib4_Statue(Statue):
    def __init__(self):
        super(Lib4_Statue,self).__init__()
        self.description = ("It's a statue depicting some kind of horned demon. " +
                           "Below, a small engraving reads \"Lucifer\".")



class Lib4_Table(SearchableFurniture, Moveable):
    def __init__(self, itemList=[]):
        super(Lib4_Table,self).__init__(itemList)

        self.description = ("The low table sits between the couch and the " +
                          "fireplace. On its surface is something glinting.")
        self.searchDialog = ("You look on the table.")
        self.actDialog = ("The table resists any give from the kick you give it. " +
                         "It is a solidly built piece of artistry.")
        
        self.addActKeys(Furniture.JOSTLEPATTERN)
        self.addNameKeys("(?:low )?table", "(?:glimmering )?object")

    def getDescription(self):
        if not self.containsItem(CRYSTAL_ORB):
            return ("The low table sits between the couch and the fireplace.")
        else:
            return self.description



class Lib5_BanishmentShelf(SearchableFurniture):
    def __init__(self, itemList=[]):
        super(Lib5_BanishmentShelf,self).__init__(itemList)

        self.description = ("The tall bookshelf bears a plaque on the top reading \"Banishment\".")
        self.actDialog = ("You push against the shelf, but it doesn't budge.")
        self.searchDialog = ("You peruse its shelves.")
        self.addNameKeys("banishment", "(?:south )?(?:book)?shelf")
        self.addActKeys(Furniture.MOVEPATTERN)



class Lib5_Candelabra(Candelabra):
    def __init__(self, *item):
        super(Lib5_Candelabra,self).__init__(item)

        self.description = ("The intricate iron candelabra sits in the corner holding 5 candles.")
        self.addNameKeys("(?:intricate )?(?:iron )?(?:standing )?candelabra")



class Lib5(Room):
    def __init__(self, name, ID):
        super(Lib5,self).__init__(name, ID)

    def getBarrier(self, direct):
        if direct == Direction.SOUTH:
            AudioPlayer.playEffect(6)
            return ("There's a bookshelf in the way.")
        elif direct == Direction.EAST:
            return ("The balcony railing is that way.")
        else:
            return self.bumpIntoWall()



class Lib_Balcony(Balcony):
    def __init__(self):
        super(Lib_Balcony,self).__init__()

        self.description = ("The second-floor balcony follows the east wall and " +
                           "around to the south wall. On the balcony against the " +
                           "south wall is another bookshelf.")

        self.addNameKeys("(?:second[- ]floor )?balcony")



class Lib_BookShelf(Furniture):
    def __init__(self):
        super(Lib_BookShelf,self).__init__()

        self.description = ("There are a couple of bookshelves in here. You will " +
                           "need to be a bit more specific.")
        self.searchDialog = self.description
        self.actDialog = self.description
        self.addNameKeys("(?:book)?shel(?:f|ves)")
        self.addActKeys(Furniture.MOVEPATTERN)



class Lib_Couch(SearchableFurniture, Moveable):
    def __init__(self):
        super(Lib_Couch,self).__init__()

        self.description = ("A red gothic-era couch. It looks way more fancy " +
                           "than comfortable. Its frame is a glorious rosewood.")
        self.searchDialog = ("You look underneath the couch.")
        self.actDialog = ("You relax on the couch for a moment. You feel like your " +
                      "IQ has just risen a couple points.")
        self.addNameKeys("(?:red )?(?:gothic-era )?(?:couch|sofa)")
        self.addActKeys(Furniture.SITPATTERN)



class Lib_Pillar(Column):
    def __init__(self):
        super(Lib_Pillar,self).__init__()

        self.description = ("The fat Corinthian pillar stands in the corner of " +
                           "where the stairs meet the second floor.")

        self.addNameKeys("(?:fat )?(?:corinthian )?(?:pillar|column)")



class Lib_Sconces(Furniture):
    def __init__(self):
        super(Lib_Sconces,self).__init__()

        self.description = ("Copper metal sconces holding glass bulbs. They dimly " +
                           "light the wall with a flickering orange glow.")
        self.actDialog = ("Ouch! That's hot!")
        self.addNameKeys("(?:electric )?(?:copper )?(?:metal )?(?:sconces?|lights?)")
        self.addActKeys(Furniture.HOLDPATTERN, Furniture.FEELPATTERN, Furniture.GETPATTERN)



class Lib_Stairs(Staircase):
    def __init__(self, direct, dest):
        super(Lib_Stairs,self).__init__(direct, dest, 14)
        
        ups = ("second", "up", "northern second-floor")
        downs = ("first", "down", "southern first-floor")
        use = ups if (direct == Direction.UP) else downs
        
        self.searchDialog = ("You begin the search, but as soon as you touch the " +
                    "stairs, they flatten down to the floor before popping back up again.")
        
        self.actDialog = ("You successfully climb the stairs to the " + use[0] + " floor.")
        
        self.description = ("The stairs are a gray stone with salmon-colored " +
                         "marble steps. They lead " + use[1] + " to the " +
                         use[2] + " area of the library.")

    def interact(self, key):     
        if Player.getShoes() == LEATHER_SHOES:
            super(Lib_Stairs,self).interact(key)
            return self.actDialog        
        else:
            AudioPlayer.playEffect(40)
            
            if self.DIR == Direction.UP:
                return ("As soon as your foot touches the bottom step, the staircase " +
                      "flattens against the floor. You remove your foot, and the " +
                      "staircase pops back up again. 'How irritating!' you exclaim.")
            else:
                return ("As your foot touches the top step, the stairs flatten down " +
                    "against the floor. You jump back and avoid falling to the first floor.")



class Shoes(Clothing):
    def __init__(self, name, score, use):
        super(Shoes,self).__init__(name, score, use)
        self.type = SHOES

    def useEvent(self):
        if not Player.getShoes() == self.NAME:
            Player.setShoes(self.NAME)
            return self.useDialog
        else:
            Player.setShoes("")
            return ("You remove them and put your old shoes back on.")
