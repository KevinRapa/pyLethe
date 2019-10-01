from GUI import GUI
from Inventory import Inventory
from Player import Player
import MachineColor
from Gallery import Gal_LightMachine
from Names import HAND_TORCH, FOCUS
from Things import Carpet, Safe
from Item import Note
from Furniture import SearchableFurniture, Furniture, Unmoveable, Moveable, Openable
from Structure_gen import StaticWindow

"""
    Contains the blue lens for the gallery light puzzle. 
"""
class Lib1_Artifact(Gal_LightMachine):
    def __init__(self, itemList=[]):
        super(Lib1_Artifact,self).__init__()
        
        self.beam = MachineColor.COLOR_MAP[0b0010]
        
        self.description = ("The artifact is a stone head with a hollowed out " +
               "cranium. It's carved crudely. The face is eerily " +
               "expressionless and its eyes are blank. It seems " +
               "ancient. % shoots out a hole in " +
               "the top, reflecting off the ceiling mirror onto " +
               "the desk. You look around, but the head isn't " +
               "connected to anything. You can't determine the " +
               "light's source.")
        self.actDialog = ("The large stone head is too heavy to pick up.")
        self.searchDialog = ("You squint and peek inside the head.")
        
        self.inv = Art_Inv(self, itemList)  
        
        self.addActKeys(Furniture.GETPATTERN)
        self.addNameKeys("(?:strange )?artifact", "(?:stone )?head")

    def getDescription(self):      
        return self.description.replace("%", beam, 1)

    def useEvent(self, item):
        self.useDialog = ("You place the " + str(item) + " in the hole.")
        Player.getInv().give(item, self.inv)
        return self.useDialog

    def turnOn():
        return Furniture.NOTHING


class Art_Inv(Inventory):
    def __init__(self, ref, itemList=[]):
        super(Art_Inv,self).__init__(itemList)
        self.ARTIFACT_REF = ref

    def add(self, *item):
        if item.getType() == FOCUS:
            super(Art_Inv,self).add(item)
            self.ARTIFACT_REF.determineColor()
            GUI.out(beam + " emits from the top of the artifact.")
            return True
        GUI.out("The " + str(item) + " doesn't fit in.")
        return False

    def remove(self, removeThis):  
        self.CONTENTS.remove(removeThis)
        self.ARTIFACT_REF.determineColor()



class Lib1_Desk(SearchableFurniture, Openable, Moveable):
    def __init__(self, ID, itemList=[]):
        super(Lib1_Desk,self).__init__(itemList)
        self.ART_ID = ID
        self.searchDialog = ("You fan through the boring papers on the surface. " +
                            "Here's what you find interesting: ")
        self.addNameKeys("desk", "unkept desk")

    def getDescription(self):  
        return ("The desk is unkept and covered in various pieces of paper " +
               "and other knick knacks. The beam from the artifact casts " +
               "its surface in " + Player.getPos().getFurnRef(self.ART_ID).getBeam().lower() + '.')



class Lib1_Documents(Furniture):
    def __init__(self):
        super(Lib1_Documents,self).__init__()

        self.description = ("Various papers and scrolls litter the surfaces and shelves of the room.")
        self.actDialog = ("It would take at least a year to read all of these!")
        self.searchDialog = ("There are simply too many to search them all at once.")
        self.useDialog = ("Yes... burn it... burn it all to the ground... ")
        
        self.addUseKeys(HAND_TORCH)
        self.addNameKeys("documents?", "scrolls?", "papers?")
        self.addActKeys("read", Furniture.GETPATTERN)
        


class Lib1_Light(Furniture):
    def __init__(self):
        super(Lib1_Light,self).__init__()

        self.description = ("The beam of light is emitting out the top of the artifact.")
        self.addNameKeys("light", "beam of light")



class Lib1_Mirror(Furniture):
    def __init__(self):
        super(Lib1_Mirror,self).__init__()

        self.description = ("The round mirror on the ceiling is angled such that " +
                           "the light reflects onto the desk. Ingenuous.")
        self.addNameKeys("mirror", "ceiling mirror")



class Lib1_Rack(SearchableFurniture, Unmoveable):
    def __init__(self, itemList=[]):
        super(Lib1_Rack,self).__init__(itemList)
        
        self.description = ("The wood rack looks like it's meant to hold scrolls, " +
                           "but an equal assortment of scrolls and papers have " +
                           "been stuffed into its crevices.")
        self.searchDialog = ("You look through its various nooks and crannies. " +
                            "Here's what you find interesting: ")
        self.addNameKeys("(?:wood(?:en)? )?rack")



class Lib1_Rug(Carpet):
    def __init__(self):
        super(Lib1_Rug,self).__init__()

        self.description = ("A dusty Persian rug. Clearly an antique, but it looks surprisingly new.")
        self.searchDialog = ("To your great curiosity, lifting up the rug " +
                            "reveals a second identical rug underneath.")
        
        self.addNameKeys("(?:dusty )?(?:persian )?(?:rug|carpet)")



class Lib1_Safe(Safe):
    def __init__(self, combo, itemList=[]):
        super(Lib1_Safe,self).__init__(combo, itemList=[])
        self.description = ("The heavy, black, combination safe sits on the floor beneath the table.")



class Lib1_Table(SearchableFurniture, Unmoveable):
    def __init__(self, itemList=[]):
        super(Lib1_Table,self).__init__(itemList)
        self.description = ("The table is ornate, with curved legs, and bears " +
                           "a bizarre stone head emitting light from an unknown source.")
        self.searchDialog = ("You fan through the boring papers scattered around " +
                            "the artifact. Here's what you find interesting: ")
        self.actDialog = ("You give it a kick. A thick woody clunk inundates " +
                 "your ear holes, and you are enticed to hit it again.")
        
        self.addActKeys(Furniture.JOSTLEPATTERN)
        self.addNameKeys("(?:ornate )?table")



class Lib1_Window(StaticWindow):
    def __init__(self):
        super(Lib1_Window,self).__init__()

        self.description = ("The 16-paned window spans most of the wall. From it, " +
                           "you have a magnificent view of the sea. The sight of " +
                           "your village makes you feel so close, yet so far away.")