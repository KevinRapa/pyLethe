from GUI import GUI
import Menus, Direction
from Player import Player
from Room import Room
from Patterns import SEARCH_P
from Furniture import SearchableFurniture, Furniture

class Hades(Room):
    def __init__(self, name, ID):
        super(Hades,self).__init__(name, ID)
        
        self.END_DIALOG = \
            ("An echoing voice thunders through the crimson skies. It " +
            "is directed at you. \"Another adventurer comes! Welcome " +
            "to the land of the dead, where you may spend life eternal " +
            "among your intrepid kindred. Judgement awaits, and you " +
            "shall be judged not by your cunning and intellect, but " +
            "by the fruits of them, for only the wealthy live " +
            "comfortably here...\"")

    def getBarrier(self, direct):
        if direct == Direction.EAST:
            return ("Some invisible force prevents you from passing through the gate.")
        else:
            return self.bumpIntoWall()

    def triggeredEvent(self):
        if not Player.hasVisited(self.ID):
            GUI.roomOut(self.NAME)
            GUI.clearDialog()
            GUI.descOut(self.END_DIALOG)
            GUI.menOut(Menus.ENTER)
            GUI.promptOut()
            GUI.descOut(self.calculateScore(Player.getScore()))
            GUI.promptOut()
            GUI.toMainMenu()
            Player.describeRoom()
        
        return self.NAME

    def calculateScore(self, score):
        if score >= 15000:
            return \
                ("\"You are drenched in greed, my son. Undaunted by risk, " +
                "in pursuit of only the unquenchable thirst for wealth. " +
                "You are a master adventurer a True idol among idols, " +
                "surpassing even me. You shall live comfortably for all " +
                "eternity in Tartarus, in constant labor with frequent " +
                "coffee breaks.\"")
        if score >= 13500:
            return \
                ("\"You are drenched in greed, my son. Undaunted by risk, " +
                "in pursuit of only the unquenchable thirst for wealth. " +
                "You are a master adventurer a True idol among idols, " +
                "except among me, for I have traveled to these lands " +
                "before, and even back. You shall live comfortably for " +
                "all eternity in Tartarus, in constant labor with " +
                "occasional coffee breaks.\"")
        if score >= 10000:
            return \
                ("\"You have the True spirit of an adventurer, yet you " +
                "also lived as a prisoner, and ultimately strayed from " +
                "your path to freedom to embrace death's cold grasp. " +
                "You have moderate wealth, impressive to many, but not " +
                "to all. You will be sent to live eternally in the " +
                "flaming river Phlegethon with other aspired adventurers, " +
                "interrupted occasionally with short breaks for leisurely " +
                "activities.\"")
        if score >= 5000:
            return \
                ("\"You have the True spirit of an adventurer, yet you " +
                "also lived as a prisoner, and ultimately strayed from " +
                "your path to freedom to embrace death's cold grasp. " +
                "You have some wealth, impressive to the commonfolk, " +
                "Yet deserve not to live amongst kings. You will be " +
                "sent to live eternally in the flaming river Phlegethon " +
                "with opportunities to earn credits, supposing you wish " +
                "to vacation from hellfire a couple times a month.\"")
        if score >= 0:
            return \
                ("\"Your wealth is sparse, and your accomplishments " +
                "laughable. Though perhaps you have a good spirit " +
                "and the sound ethics of a hard worker, you will " +
                "be forgotten eventually and fade into obscurity. " +
                "You shall be sent to Lethe, where you will spend " +
                "forever swimming in a state of dementia.\"")
        else: 
            return \
                ("\"Your wealth is null, and your accomplishments " +
                "laughable. Though perhaps you have a good spirit " +
                "and the sound ethics of a hard worker, you will " +
                "be forgotten and fade into obscurity. You shall " +
                "be sent Cocytus, where you shall swim in " +
                "lamentation for all eternity.\"")



class Hads_Corpses(SearchableFurniture):
    def __init__(self, itemList=[]):
        super(Hads_Corpses,self).__init__(itemList)
        
        self.description = self.actDialog = ("You can't do even that.")
        self.searchDialog = ("You fan through the pile of corpses.")
        self.addActKeys(Furniture.ANYTHING)
        self.addNameKeys("(?:pile of )?(?:mangled )?(?:corpses?|bodies)")
    
    def interact(self, key):
        if SEARCH_P.match(key):
            Player.trySearch(self)
            return Furniture.NOTHING
        else:
            return self.actDialog



class Hads_Gateway(Furniture):
    def __init__(self):
        super(Hads_Gateway,self).__init__()
        
        self.description = self.actDialog = \
        self.searchDialog = ("You can't do even that.")
        self.addActKeys(Furniture.ANYTHING)
        self.addNameKeys("(?:large )?(?:open )?gate(?:way)?")



class Hads_Spirits(Furniture):
    def __init__(self):
        super(Hads_Spirits,self).__init__()
        
        self.description = self.actDialog = \
        self.searchDialog = ("You can't do even that.")
        
        self.addActKeys(Furniture.ANYTHING)
        self.addNameKeys("(?:evil )?(?:jeering )?spirits")



class Hads_Voices(Furniture):
    def __init__(self):
        super(Hads_Voices,self).__init__()
        
        self.description = self.actDialog = \
        self.searchDialog = ("You can't do even that.")
        
        self.addActKeys(Furniture.ANYTHING)
        self.addNameKeys("(?:thousands of )?(?:lamenting )?voices?")