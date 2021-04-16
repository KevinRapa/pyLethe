from Player import Player
from Item import Item, Note
from Room import Room
import AudioPlayer
from Furniture import Furniture, Gettable, SearchableFurniture
from Names import SHOVEL, SOIL, TROWEL, HAND_TORCH
import re

"""
   This type of furniture can't be interacted with if the player doesn't hold 
   a torch.
"""
class Aarc_Furniture(SearchableFurniture):
    TOO_DARK = "The room is pitch black. You cannot see a thing."
    
    def __init__(self, itemList=[]):
        super(Aarc_Furniture, self).__init__(itemList)

    def getDescription(self):
        return self.checkForTorch(self.description)
       
    def getSearchDialog(self):
        return self.checkForTorch(self.searchDialog)

    def interact(self, key):              
        return self.checkForTorch(self.actDialog)

    def useEvent(self, item):
        return self.checkForTorch(self.useDialog)
     
    def checkForTorch(self, dialog):
        if Player.hasItem(HAND_TORCH):
            return dialog
        else:
            return Aarc_Furniture.TOO_DARK

class Aarc_Algae(Aarc_Furniture, Gettable):
    def __init__(self, ref):
        super(Aarc_Algae, self).__init__()
        
        self.ALGAE_REF = ref
        self.searchable = False
        self.addActKeys(Furniture.GETPATTERN, Furniture.FEELPATTERN, "lick")
        self.addNameKeys("algae")

    def interact(self, key):
        if key == "lick" or re.match(Furniture.FEELPATTERN, key):
            return "Gross... slimy."
        else:
            return self.getIt()
   
    def getIt(self):
        if Player.getInv().add(self.ALGAE_REF):
            return "You scrape off some of the algae. Yuck."
        else:
            return Furniture.NOTHING

class Aarc_Books(Aarc_Furniture, Gettable):
    def __init__(self, ref, itemList=[]):
        super(Aarc_Books, self).__init__(itemList)
        
        self.BOOK_REF = ref      
        self.addNameKeys("books?")
        self.addActKeys(Furniture.GETPATTERN, "read")
   
    def interact(self, key):
        return (self.actDialog if key == "read" else self.getIt())
   
    def getIt(self):
        if Player.getInv().add(self.BOOK_REF):
            return "You take one of the books, not giving much thought about it."
        else:
            return Furniture.NOTHING

class Aarc_Chandelier(Aarc_Furniture):
    def __init__(self):
        super(Aarc_Chandelier, self).__init__()
        self.searchable = False
        self.addNameKeys("(?:unlit )?(?:iron )?(?:chandelier|light)")
        self.addUseKeys(HAND_TORCH)
        self.addActKeys("light", "swing", "hang")
      
    def interact(self, key):
        return (self.actDialog if key == "light" else "That's a very immature thing to do.")

class Aarc_Desk(Aarc_Furniture):
    def __init__(self, itemList=[]):
        super(Aarc_Furniture, self).__init__(itemList)

        self.addActKeys(Furniture.JOSTLEPATTERN)
        self.addNameKeys("(?:old )?(?:wooden )?(?:drawered )?desk", "drawers?")

class Aarc_Floor(Aarc_Furniture):
    def __init__(self, itemList=[]):
        super(Aarc_Floor, self).__init__(itemList)
        self.addUseKeys(SHOVEL, TROWEL)
        self.addNameKeys("floor", "ground", "sinkhole", SOIL,
                         "(?:slightly raised )?(?:stone )?platform")

    def useEvent(self, item):
        AudioPlayer.playEffect(34)
        return self.actDialog

"""
   Contains a key to the Keepers chamber and a note hinting where the Factum is.
   Connects to Cis3
"""
class Aarc(Room):    
    def __init__(self, name, ID):
        super(Aarc, self).__init__(name, ID)

    def getDescription(self):
        if Player.hasItem(HAND_TORCH):
            return super(Aarc,self).getDescription()
        else:
            return ("You are in a pitch black room. You can't sense a thing " +
                    "but the smell of wilt and a wet floor.")



class Aarc_Shelves(Aarc_Furniture):
    def __init__(self, itemList=[]):
        super(Aarc_Shelves, self).__init__(itemList)
        self.addNameKeys("(?:old )?(?:broken )?(?:fallen )?(?:book)?shel(?:f|ves)")

class Aarc_Wall(Aarc_Furniture):
    def Aarc_Wall(self):
        super(Aarc_Wall, self).__init__()
        self.searchable = False
        self.addNameKeys("(?:cobblestone )?walls?")

class Aarc_Wood(Aarc_Furniture, Gettable):
    def __init__(self, ref):
        super(Aarc_Wood, self).__init__()
        
        self.WOOD_PIECE = ref
        self.searchable = False
       
        self.addActKeys(Furniture.GETPATTERN)
        self.addNameKeys("(?:piles of )?wood(?:en)?(?: rubble)?",
                         "(?:wood(?:en)? )?piles?")
    
    def interact(self, key):
        return self.getIt()
    
    def getIt(self):
        if Player.getInv().add(self.WOOD_PIECE):
            return "You take one of the books, not giving much thought about it."
        else:
            return Furniture.NOTHING
