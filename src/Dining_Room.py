from Structure_gen import Balcony, Column, Door, Staircase, StaticWindow
from Things import Chandelier, Carpet, WallArt
import Direction, Id, AudioPlayer
from GUI import GUI
from Room import Room
from Player import Player
from Furniture import Furniture, SearchableFurniture, Moveable
import re

class Din1_Balcony(Balcony):
    def __init__(self):
        super(Din1_Balcony,self).__init__()

        self.description = ("The second-floor balcony bows out into the room. Up " +
                           "on the south wall, you see the source of the noise.")

        self.addNameKeys("(?:second[- ]floor )?balcony(?: railing)?")



class Din1_Carpet(Carpet):
    def __init__(self):
        super(Din1_Carpet,self).__init__()

        self.description = ("The clean lavender carpet lies under the table and " +
                           "chairs, covering most of the cold stone floor.")
        self.searchDialog = ("To your great curiosity, lifting up the carpet " +
                            "reveals a second identical carpet underneath.")
        
        self.addNameKeys("(?:clean )?(?:lavender )?(?:carpet|rug)")



class Din1_Chairs(Furniture, Moveable):
    def __init__(self):
        super(Din1_Chairs,self).__init__()

        self.description = ("The chairs are boxy with lavender upholstery. The " +
                           "hickory wood is meticulously carved. 'They can " +
                           "carve a chair worth double my life, but not one " +
                           "worth 5 minutes of sitting in!'")
        self.searchDialog = ("You look underneath, but find nothing.")
        self.actDialog = ("You pick out a chair to sit in and stare out the window " +
                         "on the east end. For a moment, you feel free of worry.")
        
        self.addActKeys(Furniture.SITPATTERN)
        self.addNameKeys("chairs?")



class Din1_Chandelier(Chandelier):
    def __init__(self):
        super(Din1_Chandelier,self).__init__()

        self.useDialog = ("The chandlier is too high up.")
        self.description = ("The chandelier shimmers in the moonlight. Its candles " +
                "are unlit, which at this point seems odd to you. Still, " +
                "the room is well lit from the light shining in.")



class Din1_Columns(Column):
    def __init__(self):
        super(Din1_Columns,self).__init__()

        self.description = ("The row of six Doric columns bows out following the " +
                           "curve of the balcony's edge. They are all clean white marble.")
        
        self.addNameKeys("(?:doric )?columns?")



"""
    Holds an observatory plate.
    Discovered by looking behind tapestry.    
"""
class Din1_Crevice(SearchableFurniture):
    def __init__(self, itemList=[]):
        super(Din1_Crevice,self).__init__(itemList)

        self.description = ("It's a small indentation carved right into the wall!")
        self.searchDialog = ("You look in the hole")
        self.addNameKeys("(?:small )?(?:indentation|crevice|hole(?: in the wall)?)")



class Din1_Door(Door):
    def __init__(self, direct):
        super(Din1_Door,self).__init__(direct)
        
        self.description = ("The backside of the door to this room looks as " +
                           "complicated as you imagined. Many plates, hinges, " +
                           "and springs cover its back.")



class Din1_Moonlight(Furniture):
    def __init__(self):
        super(Din1_Moonlight,self).__init__()

        self.description = ("The skies are clear and the full moon is bright tonight.")
        self.searchDialog = ("Don't be ridiculous.")
        self.addNameKeys("moonlight")



"""
    Superficial, except that one plate needed for the observatory puzzle is here.    
"""
class Din1(Room):
    def __init__(self, name, ID):
        super(Din1,self).__init__(name, ID)

    def triggeredEvent(self):
        if not Player.hasVisited(self.ID):
            AudioPlayer.playEffect(8)
            GUI.out("As you enter, you hear a door above you swing shut.")
        return self.NAME



class Din1_Stairs(Staircase):
    def __init__(self, direction, dest):
        super(Din1_Stairs,self).__init__(direction, dest, 15)
        self.description = ("The stone staircase leads straight up to the " +
                           "balcony. A lavender carpet runs its surface.")
        self.searchDialog = ("In searching the stairs, you find it as clean " +
                            "as the rest of this room.")

    def getDescription(self):
        if self.DIR == Direction.DOWN:
            return ("The stone staircase leads straight down to the first floor. " +
                   "A lavender carpet runs its surface.")
        else:
            return self.description


        
class Din1_Table(SearchableFurniture):
    def __init__(self, itemList=[]):
        super(Din1_Table,self).__init__(itemList)
        
        self.description = ("The table must be twenty feet long! A scarlet tablecloth coats its dark polished surface.")
        self.actDialog = ("You give the table a nudge. It gives only slightly the table is formidable.")
        self.searchDialog = ("You look on the table's surface.")
        
        self.addActKeys(Furniture.MOVEPATTERN)
        self.addActKeys(Furniture.JOSTLEPATTERN)
        self.addNameKeys("(?:long )?table")

    def interact(self, key):              
        if re.match(Furniture.MOVEPATTERN, key):
            AudioPlayer.playEffect(41)
            return ("Gathering some momentum, you push into the table, sliding it some.")
        else:
            return self.actDialog



class Din1_Tapestry(WallArt):
    def __init__(self, ref):
        super(Din1_Tapestry,self).__init__()

        self.CRVC_REF = ref
        self.description = ("A large, renaissance-era tapestry. A well-dressed male " +
                           "and female sit together on a log in a grove. Between " +
                           "them is a chalice bearing an unexplainable blue glow.")
        self.searchDialog = ("Lifting the tapestry, you discover a crevice in the wall behind it.")
        self.actDialog = self.searchDialog
        self.addNameKeys("(?:large )?tapestry")

    def getSearchDialog(self):
        if not Player.getRoomObj(Id.DIN1).hasFurniture("crevice"):
            Player.getRoomObj(Id.DIN1).addFurniture(self.CRVC_REF)
            return self.searchDialog
        else:
            return ("Yes, the hole in the wall is still there")

    def interact(self, key):
        if key == "admire":
            return ("Yes, what a beautiful piece of artwork. You take a moment " +
                   "to soak in the creative essence. Yes...")
        else:
            return self.getSearchDialog()



class Din1_Window(StaticWindow):
    def __init__(self):
        super(Din1_Window,self).__init__()
        
        self.escapeDialog = ("You could probably use your weight to break through... but aren't too keen on the idea.")
        self.description = ("From the great window, you can see all of the east. The " +
                           "sea extending from the castle's cliff terminates at the " +
                           "shore before your village. Past the village, a thin " +
                           "forest coats the hills that roll far out into the distance " +
                           "before graduating into a mountain range on the horizon.")



class Din2_Painting(WallArt):
    def __init__(self):
        super(Din2_Painting,self).__init__()
        
        self.description = ("The wide painting illustrates a view of a long dinner " +
                           "table. A single man sits at the center of the table. " +
                           "He looks right at you with a serious, almost malevolent " +
                           "stare. 'Why would anyone hang this in their house?' You " +
                           "ask yourself.")
        self.addNameKeys("(?:long |wide )?painting")



"""
    Superficial.
    Entrance to drawing room.    
"""
class Din2(Room):
    def __init__(self, name, ID):
        super(Din2,self).__init__(name, ID)

    def getBarrier(direct):
        if direct == Direction.EAST:
            return ("There's a railing that way.")
        else:
            return self.bumpIntoWall()