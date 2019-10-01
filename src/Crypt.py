from Furniture import *
import Id, Main, Menus, AudioPlayer
from Player import Player
from Things import Statue
import re, random
from Room import Room
from GUI import GUI
from Inventory import Inventory
from Names import BRAIN, SCYTHE
from Patterns import ONE_TO_HUNDRED_P
from Item import Liquid

class Cry1_Carving(Furniture, Gettable, Unmoveable):    
    def __init__(self):
        super(Cry1_Carving,self).__init__()
        
        self.description = ("Carved into the wall is a mural of sorts. In the center " +
                           "is a standing cloaked figure resembling a skeleton. It " +
                           "holds a scythe and stands elevated among many unclothed " +
                           "people piled up onto each other crawling towards it, " +
                           "perhaps wishing to embrace the figure. " +
                           "Many clouds gather high above the skeleton.")
        self.actDialog = ("Something so morbid hardly seems admirable...")
        
        self.addActKeys("admire")
        self.addNameKeys("(?:wall )?(?:carving|engraving)", 
                "(?:death )?depiction", "art", "mural(?: of sorts)?")



class Cry1_Statue(Statue, Resetable):
    def __init__(self, ref):
        super(Cry1_Statue,self).__init__()
        
        self.hasScythe, self.eyesGlowing = False, False
        self.SCYTHE_REF = ref
        
        self.useDialog = ("You place the scythe into the statue's left hand.")
        self.description = ("The tall statue stands in the center of this side " +
                           "of the room. The statue is cloaked with a skull for " +
                           "a head and stares at you. It holds one of its boney hands up as if it were " +
                           "grasping something, though its palm is empty. With the other " +
                           "palm it reaches out openly towards you.")
        
        self.addNameKeys("(?:tall )?(?:stone )?(?:cloaked )?statue", "(?:statue(?:'s)? )?(?:bone?y )?(?:hand|palm)")
        self.addUseKeys(SCYTHE)
        self.addActKeys("shake|embrace|greet|hold|grasp|push|pull|move|turn|twist")
    
    def getDescription(self):
        result = None
        
        if not self.hasScythe:
            result = self.description
        else:
            result = self.description.replace(
                    "one of its boney hands up as if it were grasping something, though its palm is empty", 
                    "a scythe in one hand", 1)
        
        if self.eyesGlowing:
            return (result + " It's eyeholes glow with an orange light.")
        else:
            return result
    
    def getSearchDialog(self):
        return self.getDescription()
    
    def interact(self, key): 
        if re.match("shake|embrace|greet|hold|grasp|push|pull|move|turn|twist", key):
            if self.hasScythe:
                self.eyesGlowing = True
                return ("You grasp the statue's right hand and twist. An orange " +
                       "light glows deep in the statue's eyes.")
            else:
                return ("You grasp the statue's right hand and twist. Nothing happens.")
        else: 
            return super(Cry1_Statue,self).interact(key)
    
    def useEvent(self, item):
        Player.getInv().remove(item)
        self.hasScythe = True
        return self.useDialog
    
    def reset(self):
        if self.hasScythe:
            Player.getRoomObj(Id.TORC).addFurniture(self.SCYTHE_REF)
            self.hasScythe = False

        self.eyesGlowing = False
    
    def isSolved(self):
        return self.eyesGlowing



class Cry2_Altar(SearchableFurniture, Unmoveable):
    def __init__(self, itemList=[]):
        super(Cry2_Altar,self).__init__(itemList)
        self.description = ("The altar is essentially a stone table adorned with " +
                           "many lit candles and dried flora. A few pieces of " +
                           "jewelry are distributed about the surface.")
        self.actDialog = ("You really aren't part of whatever religion this is for.")
        self.searchDialog = ("You look on the altar.")

        self.addNameKeys("altar", "(?:stone )?table(?: surface)?", 
                         "candles?", "flora", "effigy", "surface")
        self.addActKeys("worship", "kneel", "sacrifice", "pray")



class Cry2_Engraving(Furniture, Moveable):
    def __init__(self):
        super(Cry2_Engraving,self).__init__()
        self.description = ("The tall coffin resembles a large stone box with " +
                           "a lid, but something is holding it closed. The lid " +
                           "of the coffin is artfully decorated with a carving of " +
                           "a boney cloaked figure wearing a halo. Around it is " +
                           "an engraving resembling a doorway. The engraving " +
                           "depicts two grooved columns holding up a roof.")
        self.actDialog = ("You can't pry it open. Something is holding the coffin tightly closed.")
        
        self.addNameKeys("(?:wall )?(?:engraving|carving)", "(?:stone )?(?:box|coffin|casket|lid)",
                "(?:(?:artfully )?decorated)?lid")
        self.addActKeys("open", "pry")
    
    def getDescription(self):
        if Player.getPos().isAdjacent(Id.CAS1):
            return ("The engraving frames a metal door in the center of it. The stone " +
                   "coffin stands off to the side.")
        else:
            return self.description
    
    def moveIt(self):
        if Player.getPos().isAdjacent(Id.CAS1):
            return ("There really is no reason. The coffin has already been moved.")
        else:
            return ("As hard as you try, you cannot manage to budge it even a small distance.")



"""
    The player must speak this furniture's name before the coffin in the crypt
    in order to access the catacombs.
    Serves as a dummy furniture.
"""
class Cry2_Password(Furniture):
    def __init__(self, ID):
        super(Cry2_Password,self).__init__()
        
        self.CRY1_STAT_ID = ID

        self.actDialog = ("As you speak the phrase before the stone coffin, it " +
                         "slides to the side with a rumble, revealing a metal door.")
        self.searchDialog = self.description = self.useDialog = ("There is nothing with that name here.")

        self.addNameKeys(r"it is i,? friend,? welcome me\.?", r"is i,? friend,? welcome me\.?")
        self.addUseKeys(Furniture.ANYTHING)
        self.addActKeys("talk", "speak", "say", "announce", "whisper", "it")
    
    def interact(self, key):    
        s = Player.getRoomObj(Id.CRY1).getFurnRef(self.CRY1_STAT_ID)
                
        if s.isSolved() and not Player.getPos().isAdjacent(Id.CAS1):
            Player.getPos().addAdjacent(Id.CAS1)
            Player.getRoomObj(Id.CAS1).addAdjacent(Id.CRY2)
            AudioPlayer.playEffect(50)
            return self.actDialog
        else:
            return ("You speak before the coffin with no effect.")



class Cry2(Room):
    def __init__(self, name, ID):
        super(Cry2,self).__init__(name, ID)

    def getDescription(self):
        if Player.getPos().isAdjacent(Id.CAS1):
            return super(Cry2,self).getDescription().replace(\
                    "Standing against the west wall is a tall stone coffin with an engraving on the wall framing it.", 
                    "To the west is a metal door framed by an engraving. The stone coffin stands next to it.", 1)
        else:
            return super(Cry2, self).getDescription()



"""
    The player can search any of the cabinets, but only one of them has
    the brain in a jar.
    This drawer is selected randomly when a new game is made.
"""
class Cry_Drawers(Furniture, Openable):
    def __init__(self):
        super(Cry_Drawers,self).__init__()

        self.DRAWERS = [None] * 100
        self.BRAIN_REF = Liquid(BRAIN, 10)
        self.DRAWER_NUM = random.randint(1,100) 
        
        for i in range(100):
            self.DRAWERS[i] = Inventory()

        self.DRAWERS[self.DRAWER_NUM - 1].add(self.BRAIN_REF)
        
        self.description = ("The drawers are most likely being used to hold the " +
                           "dead. Who exactly, you don't know. The drawers are " +
                           "each labeled a with a number from 1 to 100.")
        
        self.searchDialog = ("You pull the knob on the drawer. The door swings " +
                            "open revealing a dessicated corpse inside.")

        self.addActKeys("slide", "pull", "remove")
        self.addNameKeys("drawers?", "knobs?", "numerous drawers")
    
    def interact(self, key):
        return self.getSearchDialog()
    
    def getSearchDialog(self):
        GUI.out("The drawers are labeled from 1 to 100. Search which drawer?")
        ans = GUI.askChoice(Menus.CRY_DRWRS, ONE_TO_HUNDRED_P)

        if ans:
            GUI.out(self.searchDialog)
            Player.search(self.DRAWERS[int(ans) - 1]) 
        
        return Furniture.NOTHING



"""
    Serves as a dummy furniture to display input whenever the player speaks
    in the crypt.    
"""
class Cry_Dummy(Furniture):
    def __init__(self):
        super(Cry_Dummy,self).__init__()

        self.description = self.searchDialog = self.useDialog = "There is nothing with that name here."
        self.actDialog = ("You speak the words, but nothing happens")
        
        self.addNameKeys(Furniture.ANYTHING)
        self.addUseKeys(Furniture.ANYTHING)
        self.addActKeys("talk", "speak", "say", "announce", "whisper")



class Cry_Lights(Furniture):
    def __init__(self):
        super(Cry_Lights,self).__init__()

        self.description = ("From the wall extend boney arms, palms up, holding " +
                           "small dishes. The surfaces of the dishes burn and give " + 
                           "off the smell of brimstone.")
        self.actDialog = ("You can't do that. They are attached to the wall.")

        self.addNameKeys("(?:boney )?arms", "(?:burning )?(?:platters?|dish(?:es)?)", 
                "torch(?:es)?", "protrusions?")
        self.addActKeys(Furniture.GETPATTERN)