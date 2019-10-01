import Direction, Id, AudioPlayer
from GUI import GUI
from Room import Room
from Names import *
from Player import Player
from Structure_gen import Window, Door
from Furniture import Furniture, Moveable, SearchableFurniture
from Things import Chandelier, PottedPlant

class Mha1_Door(Door):
    def __init__(self, direct):
        super(Mha1_Door,self).__init__(direct)
        self.description = ("The door is painted white and accented in gold. Nailed in " +
                          "the center is a gold cross.")
        self.addNameKeys("(?:gold )?cross")



"""
    Connects to Mha2 and Gal2    
"""
class Mha1(Room):
    def __init__(self, name, ID):
        super(Mha1,self).__init__(name, ID)

    def triggeredEvent(self):
        if not Player.hasVisited(self.ID):
            GUI.out("As soon as you enter, you catch a glimpse of a white " +
                   "figure passing through a door in the middle of the hallway.")
        return self.NAME



class Mha1_Window(Window):
    def __init__(self):
        super(Mha1_Window,self).__init__()

        self.descClosed = ("The window is tall and arched at the top. Through its " +
                          "many glass panes, you can see the north end of the " +
                          "courtyard. A small headless statue stands in the center.")
        self.descOpen = ("The window is open and its two shutters open outwards. " +
                        "You can see the north end of the courtyard. A small " +
                        "headless statue stands in the center.")
        self.addNameKeys("(?:tall )?window")



"""
    Leads to the dining room- player must locate 3 medallions and use them
    on this door in order to unlock the room.
    
    Angel medallion, in right angel statue in marble hall
    Horse medallion, inside the horse statue in the library
    Soldier medallion, in the courtyard 5 fountain with the soldier statue
"""
class Mha2_Door(Door):
    def __init__(self, direct):
        super(Mha2_Door,self).__init__(dir)
        
        self.angSolHrs = 0
        self.numEmpty = 3
        self.description = ("The double doors here are locked tight. Four round " +
                   "sockets are built into the door's surface. One already " +
                   "contains a gold disk with an engraving of an angel on it. " +
                   "In the other three sockets you make out a second engraving " +
                   "of an angel, an engraving of a soldier, and an engraving " +
                   "of a horse.")
        
        self.addNameKeys("(?:double )?doors", "(?:door )?(?:sockets?|slots?)")
        self.addUseKeys(STONE_DISK, ANGEL_MEDALLION, HORSE_MEDALLION)

    def useEvent(self, item):
        name = str(item)
        res = None
        
        if name in (STONE_DISK, ANGEL_MEDALLION, HORSE_MEDALLION): 
            res = ("You press the " + name + " into its socket.")
            AudioPlayer.playEffect(43)

            if name == STONE_DISK:
                angSolHrs |= 0b010 
            elif name == ANGEL_MEDALLION:
                angSolHrs |= 0b100 
            elif name == HORSE_MEDALLION:
                angSolHrs |= 0b001 

            Player.getInv().remove(item)
            self.numEmpty -= 1

            if self.numEmpty == 0:
                Player.getRoomObj(Id.DIN1).setLocked(False)
                return res + " With the last medallion in place, the door *clicks* loudly."
            else:
                return res
        elif name == CROWBAR:
            return ("The medallion is wedged in tightly and can't be pried out.")
        else:
            return super(Mha2_Door,self).useEvent(item)

    def getDescription(self):    
        res = ("The doors remain locked. ")
        
        if self.numEmpty == 1: 
            if self.angSolHrs == 0b110:
                return res + "The socket with the horse engraving remains empty."
            elif self.angSolHrs == 0b101:
                return res + "The socket with the soldier engraving remains empty."
            elif self.angSolHrs == 0b011:
                return res + "The socket with the angel engraving remains empty."
        elif self.numEmpty == 2:
            if self.angSolHrs == 4:
                return res + "The sockets with the soldier and horse engravings remain empty."
            elif self.angSolHrs == 2:
                return res + "The sockets with the angel and horse engravings remain empty."
            elif self.angSolHrs == 1:
                return res + "The sockets with the angel and soldier engravings remain empty."
        elif self.numEmpty == 0:
            return ("All of the door's medallions have been returned. The door is unlocked.")
        else:
            return self.description

    def getSearchDialog(self):
        return ("You can't seem to dig the disk out by hand." \
            if self.numEmpty == 3 else "You can't seem to dig the medallions out by hand.")



class Mha2_LeftStatue(SearchableFurniture):
    def __init__(self):
        super(Mha2_LeftStatue,self).__init__()
        self.description = ("The angel poses majestically with an indifferent " +
                          "gaze upwards. It holds a silver spear in its hand " +
                          "and points it upwards over the right angel. In its " +
                          "hollow base is an open compartment.")
        self.searchDialog = ("You look into the compartment inside its base.")
        self.useDialog = ("You start jamming it into the angel's hand " +
                        "before realizing that the angel is already holding a spear.")
        self.actDialog = ("Such an impressive work of artistry deserves not to be " +
                        "tainted by your touch.")
        
        self.addNameKeys("left (?:statue|one|angel|hand|palm)", "(?:left )?(?:open )?compartment", 
                "left (?:statue|angel|one)(?:'s)? (?:hand|palm)")
        self.addActKeys(Furniture.HOLDPATTERN)
        self.addUseKeys(Furniture.ANYTHING)

    def useEvent(self, item):
        if item.getType() == WEAPON:
            return self.useDialog
        else:
            return ("It doesn't seem like that belongs there.")



"""
    Player must find the silver spear located in the rack in Eow2 to open up
    this statue's compartment, revealing the angel medallion.    
"""
class Mha2_RightStatue(SearchableFurniture):
    def __init__(self, itemList=[]):
        super(Mha2_RightStatue,self).__init__(itemList)
        
        self.searchable = False
        self.description = ("The angel poses majestically with an indifferent " +
                          "gaze upwards. It's a mirror-image of the left " +
                          "statue, though its hand is empty.")
        self.searchDialog = ("There looks to be no compartment on this one.")
        self.useDialog = ("You slide the spear back into the angel's grasp. The " +
                        "divines will be pleased with you. A compartment " +
                        "reveals itself at the statue's base.")
        self.actDialog = ("Such an impressive work of artistry deserves not to be " +
                             "tainted by your touch.")
        self.addNameKeys("right (?:statue|one|angel|hand|compartment|palm|base)", 
                "right (?:statue|angel|one)(?:'s)? (?:hand|palm)")
        self.addActKeys(Furniture.HOLDPATTERN)
        self.addUseKeys(Furniture.ANYTHING)

    def useEvent(self, item):
        if str(item) == SILVER_SPEAR:
            self.searchable = True
            Player.getInv().remove(item)
            AudioPlayer.playEffect(44)
            self.addNameKeys("compartment", "open compartment")
            return self.useDialog
        else:
            return ("It doesn't seem like that belongs there.")

    def getDescription(self):
        if self.searchable:
            return ("The angel poses majestically with an indifferent " +
                  "gaze upwards. It's a mirror-image of the left " +
                  "statue. In its right hand is a silver spear.")
        else:
            return self.description

    def getSearchDialog(self):
        if self.searchable:
            return ("You look into the compartment inside the statue's base.")
        else:
            return self.searchDialog



"""
    Resolves ambiguity from there being two statues in this room.    
"""
class Mha2_Statues(Furniture):
    def __init__(self, ID):
        super(Mha2_Statues,self).__init__()
        
        self.R_STAT_ID = ID
        self.searchDialog = self.useDialog = "You aren't sure which. Specify 'left statue' or 'right statue'"
        
        self.description = ("The pair of statues are mirror images of each other. " +
                           "Each leans toward the other while gazing nonchalantly " +
                           "towards the ceiling. The only differences are that the " +
                           "left statue holds a spear while the right one does not " +
                           "and the left statue's base is hollow with an open " +
                           "compartment inside. Choose a specific statue by " +
                           "specifying 'left statue' or 'right statue'.")
        self.actDialog = ("Such impressive works of artistry deserve not to be " +
                      "tainted by your touch.")
        self.addNameKeys("(?:angel )?statues?", "angels?", "hands?")
        self.addActKeys(Furniture.HOLDPATTERN)
        self.addUseKeys(Furniture.ANYTHING)

    def getDescription(self):
        if Player.getPos().getFurnRef(self.R_STAT_ID).isSearchable():
            return ("The pair of statues are mirror images of each other. " +
                   "Each leans toward the other while gazing nonchalantly " +
                   "towards the ceiling. They each hold a silver spear " +
                   "over the other.")
        else:
            return self.description



class Mha3_Door(Door):
    def __init__(self, direct):
        super(Mha3_Door,self).__init__(direct)

        self.description = ("The door to the east is small and arched, made of " +
                           "cheap wood with black iron hinges. It looks as if " +
                           "it hasn't been opened in a very long time. The door " +
                           "to the south is large and heavy.")



class Mha3_Window(Window):
    def __init__(self):
        super(Mha3_Window,self).__init__()
        
        self.isOpen = True
        self.escapeDialog = ("That won't do any good. It leads right back out into the courtyard.")
        self.descClosed = ("The window is tall and arched at the top. Through its " +
                          "many glass panes, you can see the south end of the " +
                          "courtyard. The ruined fountain with the soldier statue " +
                          "sits in the center.")
        self.descOpen = ("The window is open and its two shutters open outwards. " +
                        "You can see the south end of the courtyard. The ruined " +
                        "fountain with the soldier statue sits in the center.")



class Mha_Chair(Furniture, Moveable):
    def __init__(self):
        super(Mha_Chair,self).__init__()

        self.description = ("The chair's frame is glorious rosewood. What you " +
                           "wouldn't give to chop down a towering Dalbergia. " +
                           "Its cushioning is a dark green diamond pattern " +
                           "which you don't care for.")
        self.searchDialog = ("You look underneath but find nothing.")
        self.actDialog = ("You sit down in the chair, noting its marvelous polish.")
        self.addNameKeys("(?:rosewood )?chairs?")
        self.addActKeys(Furniture.SITPATTERN)



class Mha_Chandelier(Chandelier):
    def __init__(self):
        super(Mha_Chandelier,self).__init__()

        self.description = ("The silver chandelier hangs many feet above you. Its " +
                "intricacy gives it a classical feel, unlike the black " +
                "iron one in the foyer. It holds many candles at least " +
                "twenty. 'Who keeps these lit?' You think to yourself.")
        
        self.addNameKeys("(?:silver )?(?:chandelier|light)")



class Mha_Door(Door):
    def __init__(self, direct):
        super(Mha_Door,self).__init__(direct)
        self.description = ("A white regal door accented with gold lining.")



class Mha_Plant(PottedPlant):
    def __init__(self, soil, gift):
        super(Mha_Plant,self).__init__(soil, gift)

        self.description = ("The potted plant is in okay shape, but could afford a bit more care. " +
                  "It sits in a fancy white vase.")