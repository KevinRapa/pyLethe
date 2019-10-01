from Names import ITEM, BREAKABLE, LIQUID, WEAPON, CLOTHING, READABLE, INGREDIENT, FOCUS, NL, W_DIR, SEP
from GUI import GUI
import Menus, AudioPlayer
from Patterns import YES_NO_P

"""
    Represents an object that can be stored in an inventory.

    s are generally simple objects instantiated directly in the main class.
    Many items are significant in that they are tied with certain furniture that
    are used by the item defined in USEKEYS. 

    s may be combinable, in that they have a non-zero THRESHOLD,
    FORMS and PRODUCT. s with these matching values
    are a set and thus may be combined to form a new item.
"""
class Item(object):   
    USE_DEFAULT = "You will need to be more specific."
            
    def __init__(self, name="NO NAME", score=0, useID=2, thresh=0, use=USE_DEFAULT, forms=None):
        self.NAME = name
        self.FORMS = forms  #  given to player after a combine.
        self.description = None # Displayed when item is inspected.
        self.useID = useID if use == Item.USE_DEFAULT else 1 # 1: used on itself | 2: enters sub-prompt
        self.score = score # However many points this is worth.
        self.type = ITEM # Useful to certain inventories.
        self.THRESHOLD = thresh # Does not combine
        self.useDialog = use # Displayed when items with Id 1 are used.

    def __str__(self):               
        return self.NAME

    """
        Returns what type of item this is.
        Items can have difference types that determine how they are used.
        For example, phylacteries cannot be put down.
        Keys have types corresponding to the ID of the room they unlock.
        @return This item's type.
    """
    def getType(self):
        return self.type 

    def getDesc(self):
        if not self.description:
            with open(W_DIR + SEP + "data" + SEP + "desc" + SEP + "ITEMS.txt", "r") as items:
                while not self.description:
                    line = items.readline().strip('\n')
                    # TABS ARE #
                    # newlines are $
                    if not line:
                        self.description = "Description not found."
                    elif self.NAME == line:
                        self.description = items.readline().strip('\n')

        return self.description 

    def forms(self):
        return self.FORMS 

    def getUseID(self):
        return self.useID 

    def getThreshold(self):
        return self.THRESHOLD 

    def getScore(self):
        return self.score

    """
        This method is called when an item with useID 1 is used by the player.
        @return A string that prints when this item is used.
    """
    def useEvent(self):
        return self.useDialog



"""
    Keys are not used on anything, they only allow access to locked rooms.
    Keys and your key ring are special. Keys are not meant to be stored.
    Keys are never added to your inventory, only to your key ring. 

    The key type is matched to a room ID; the room that the key 'unlocks'

    
"""
class Key(Item):  
    def __init__(self, name, ID):
        super(Key, self).__init__(name)
        self.type = ID

"""
    Represents an item that can be destroyed. 
    This can render the game unbeatable.
"""
class BreakableItem(Item):
    def __init__(self, name="NO NAME", score=0, useID=2, thresh=0, use=Item.USE_DEFAULT, forms=None):
        super(BreakableItem, self).__init__(name, score, useID, thresh, use, forms)
        self.type = BREAKABLE

"""
    Something with which the player may type 'drink' [this name] at the main prompt.
"""
class Liquid(Item):
    def __init__(self, name, score, use=Item.USE_DEFAULT, thresh=0, forms=None):
        super(Liquid, self).__init__(name, score, thresh=thresh, forms=forms, use=use)
        self.type = LIQUID

"""
    Used to decide certain kinds of dialog.
"""
class Weapon(Item):
    def __init__(self, name, score, use=Item.USE_DEFAULT):
        super(Weapon, self).__init__(name, score, use=use)
        self.type = WEAPON

"""
    Represents a class of items that are used by themselves, and that the player
    may type "'wear' clothing name" to use them from the main prompt.
"""
class Clothing(Item):
    def __init__(self, name, score, use):
        super(Clothing, self).__init__(name, score, use=use)
        self.type = CLOTHING

"""
    Used in the laboratory.
    Ingredients can be added to the florence flask in the laboratory.
"""
class Ingredient(Item):
    def __init__(self, name, score, desc):
        super(Ingredient,self).__init__(name, score)
        self.type = Names.INGREDIENT

        # Ingredients can have variable names depending on volume. These cannot all be accounted for in a file.
        self.persistentDesc = desc

    def getDesc(self):
        return self.persistentDesc

"""
    Represents a piece of paper with writing on it. 
    Plays a paper noise when inspected or used.
"""
class Note(Item):    
    def __init__(self, name, desc=""):
        super(Note, self).__init__(name, 0, desc)
        self.type = READABLE
        self.useID = 1
   
    def getDesc(self):
        AudioPlayer.playEffect(2)
        return super(Note,self).getDesc()

"""
    A note that the player writes. Saves its description.
"""
class NotepadNote(Note):
    def __init__(self, name, desc):
        super(NotepadNote,self).__init__(name)
        self.persistentDesc = desc

    def getDesc(self):
        AudioPlayer.playEffect(2)
        return self.persistentDesc

"""
    This item is used in the light machine puzzle.
    Only foci may be put in light machines.
"""
class Focus(Item):
    def __init__(self, name):
        super(Focus,self).__init__(name, 50)
        self.type = FOCUS


 
"""
    Represents a book with one or more pages.
 
    Interacting with a book will take the player to sub prompt where the player
    may turn pages to read further or close the book.
"""
class Book(Note): 
    def __init__(self, name, file): 
        super(Book, self).__init__(name)
        self.useDialog = "You close the book."
        self.FILE = file
       
    def getDesc(self): 
        self._read()
        GUI.clearDialog()
        return self.useDialog 
              
    def useEvent(self): 
        return self.getDesc()

    """
        Repeatedly asks player to flip through pages in the book until 'no'
        or a blank string is entered. Closes the book at end of pages.
    """
    def _read(self):
        filepath = W_DIR + SEP + "data" + SEP + "desc" + SEP + "books" + SEP + self.FILE

        with open(filepath, "r") as pages:
            while True:
                AudioPlayer.playEffect(2)
                GUI.clearDialog()
                GUI.resetScroll()
                GUI.out(pages.readline())
                nextline = pages.readline() # Should be blank or EOF

                if nextline: 
                    choice = GUI.askChoice(Menus.BOOK, YES_NO_P)

                    if choice == "yes" or choice == "y": 
                        page += 1
                    else:
                        return
                else:
                    GUI.menOut(NL + NL + "< > Close the book")
                    GUI.promptOut() 
                    return