from Inventory import Inventory
from Names import W_DIR, SEP
import re, pickle, random
import Main, AudioPlayer

"""
  Furniture is ANY object that can be examined, interacted with, and searched.
  Furniture may also be interacted with in the Inventory USE sub-prompt
   
  SearchableFurniture (a sub-class) have inventories. Items may be traded between
  searchable furniture and the player during a search.
   
  Furniture is referenced by the player by entering a string matching a string
  in NAMEKEYS, which is generally a regex pattern.

  Any method in furniture that sends text through GUI.out or
  GUI.roomOut can return an empty string which will be ignored.
"""
class Furniture(object):
    count = 0 # Used as a unique ID for this 

    HOLDPATTERN = "grab|hold|touch"
    CLIMBPATTERN = "climb|scale|ascend|descend"
    GETPATTERN = "get|take|acquire|grab|scoop"      
    SITPATTERN = "sit|relax|lay|use|sleep"
    JOSTLEPATTERN = "kick|hit|jostle|nudge|bump|knock|bang"
    VALVEPATTERN = "turn|rotate|spin|twist|open|close"
    MOVEPATTERN = "move|slide|displace|push|pull|spin|rotate"
    FEELPATTERN = "feel|touch|poke"
    DEFAULT_USE = "An interesting but far-fetched proposition."
    NOTHING_HERE = "There's nothing hiding here."
    ANYTHING = ".+"
    NOTHING = "" # Returning NOTHING will be ignored by GUI
    
    
    """
      A set of all verbs that the game accepts. If the player enters in just a
      verb, the game will prompt the player for more information.
    """
    ALL_ACTION_KEYS = set()
    
    try:
        with open(W_DIR + SEP + "data" + SEP + "verbs.txt", "r") as allVerbs:
            while True:
                verb = allVerbs.readline().strip("\n")
                
                if verb:
                    ALL_ACTION_KEYS.add(verb)
                else:
                    break
    except:
        print("Could not finds verbs to add.")
    
    """
      Constructor for furniture.
      Many attributes are overwritten in furniture sub-classes.
    """
    def __init__(self):
        self.searchable = False
        self.inv = None
        self.ID = Furniture.count
        Furniture.count += 1
        
        self.NAMEKEYS, self.USEKEYS, self.ACTKEYS = [], [], []
        
        self.description = Furniture.NOTHING
        self.actDialog = Furniture.DEFAULT_USE
        self.useDialog = Furniture.DEFAULT_USE
        self.searchDialog = Furniture.NOTHING_HERE
    
    """
        Used to check if this piece contains a certain item.
        Removes titles from books.
        @param name The name of an item.
        @return If this piece contains an item with the name.
    """
    def containsItem(self, name):
        if self.inv:
            return self.inv.contains(name)
        else:
            return False
 
    def getDescription(self):
        return self.description 
    
    def getSearchDialog(self):
        return self.searchDialog 
    
    def getID(self):
        return self.ID
    
    def isSearchable(self):
        return self.searchable # Item's can be traded with searchable furniture.
    
    def getInv(self):
        if not self.inv:
            # To be safe. This shouldn't be called if this isn't searchable.
            print("Hm... that furniture shouldn't be searchable.")
            return Inventory()
        else:
            return self.inv
    
    def __str__(self):
        return str(self.NAMEKEYS[0])

    """
      Invoked when the player interacts with this piece using a correct action.
      The map reference may be used in overwritten version of this method.
      @param key The name of an action.
      @return A string that prints when this piece is interacted with.
    """
    def interact(self, key):              
        return self.actDialog
    
    """
        This method is invoked when an item is used on this piece.
        @param item The object reference to the item used on self.
        @return String that prints when the item is used on self.
    """
    def useEvent(self, item):
        return self.useDialog
    
    def actKeyMatches(self, verb):
        for i in range(len(self.ACTKEYS)):
            pattern = self.ACTKEYS[i]

            if pattern.match(verb):
                if i > 0:
                    self.ACTKEYS[i] = self.ACTKEYS[0]
                    self.ACTKEYS[0] = pattern
                return True

        return False
    
    def useKeyMatches(self, itemName):
        for useKey in self.USEKEYS:
            if useKey.match(itemName):
                return True
        return False
    
    """
        Checks if any pattern in this furniture's list matches the string.
        If a match is found, moves it to the front of the list, assuming the
        same pattern will be used again in the future.
        @param furnName A string the player typed.
        @return If a matching pattern is found.
    """
    def nameKeyMatches(self, furnName):
        for i in range(len(self.NAMEKEYS)):
            pattern = self.NAMEKEYS[i]
            
            if pattern.match(furnName):
                if i > 0:
                    self.NAMEKEYS[i] = self.NAMEKEYS[0]
                    self.NAMEKEYS[0] = pattern
                return True
        
        return False
    
    """
          Adds a list of use keys to this furniture.
          @param keys A list of use keys.
    """
    def addUseKeys(self, *keys):
        for key in keys:
            self.USEKEYS.append(re.compile(key))
    
    """
          Adds a list of name keys to this furniture.
          @param keys A list of name keys.
    """
    def addNameKeys(self, *keys):
        for key in keys:
            self.NAMEKEYS.append(re.compile(key))
    
    """
      Adds a list of action keys to this furniture.
      @param keys A list of action keys.
    """
    def addActKeys(self, *keys):
        for key in keys:
            self.ACTKEYS.append(re.compile(key))    



"""
    Made so that not ALL furniture have inventories, just one's that can hold items.
"""
class SearchableFurniture(Furniture):
    def __init__(self, itemList=[]):
        super(SearchableFurniture, self).__init__()
        self.inv = Inventory(itemList)
        self.searchable = True



"""
    If a furniture implements this, then the action "open" will search it.
    For instance open cabinet.
"""
class Openable(object):
    def __init__(self):
        pass



"""
    Objects marked as moveable will give dialog if the player types "move *this*'
"""
class Moveable(object):
    def moveIt(self):
        AudioPlayer.playEffect(44)
        return "You manage to displace it a little, but nothing out of the ordinary is revealed."



class Unmoveable(Moveable):
    MESSAGES = (
        "You are by all means a strongly-willed man, but you know your limits.",
        "It appears most unmoveable.", 
        "In an incredible feat, you trip over your own shoes.",
        "The stories of you moving that will surely echo through the fields of Elysium.",
        "You pull a nerve a short duration into the attempt.",
        "The player is thwarted in the ridiculous attempt."
    )
    
    # Randomly displays one of the messages.
    def moveIt(self):
        return random.choice(Unmoveable.MESSAGES)



"""
    Marker interface, used to signify that it can be climbed but isn't stairs.
    Used when player types 'climb up', 'climb down', 'up', 'down', etc.
"""
class Climbable(object):
    def getDir(self):
        pass # Must be implemented. Returns which direction it takes you.



"""
    Represents furniture on which the player may type a Get word to get an item
    from it.

    Furniture representing certain divisible, heavy, etc. objects implement
    the default method.
"""
class Gettable(object):
    def getIt(self, dialog="You cannot pick that up with your hands..."):
        return dialog



"""
    Represents furniture that is reset if the player is caught by the monster.
"""
class Resetable(object):
    def reset(self):
        pass