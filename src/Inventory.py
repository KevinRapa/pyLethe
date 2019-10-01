from Names import NL
from Item import Item
import Patterns, GUI
import re

class Inventory(object):
    NULL_ITEM = Item(name="null item", useID=0)

    def __init__(self, itemList=[]):
        self.CONTENTS = itemList
    
    """
        Returns an item in the inventory with as close a name as possible to
        itemName.
        Exact matches are searched for first. If nothing is found, looks for
        something containing the word in itemName.
        If passed an digit, the inventory at that index is returned.
        @param name The name of an item to search for.
        @return Matching item. Returns a NULL_ITEM if nothing is found.
    """
    def get(self, name):
        if type(name) == int:
            if name < self.size() and name >= 0:
                return self.CONTENTS[name]
        elif Patterns.ANY_DIGIT_P.match(name):
            return self.get(int(name) - 1) # Player used a slot number.
        else:
            for item in self.CONTENTS:
                if str(item) == name:
                    return item
            
            try:
                # If player types anything that evaluates to an invalid regex, this prevent crashing.   
                p = re.compile('(?:' + name + ')(?:[-,": ]|$)', re.IGNORECASE)

                for item in self.CONTENTS: # Checks for a close match.
                    if p.search(str(item)):
                        return item
            except:
                pass
            
        return Inventory.NULL_ITEM # Item wasn't found. Always check for this!!
    
    def contains(self, itemName):
        for item in self.CONTENTS:
            if str(item) == itemName:
                return True
        
        return False
    
    def isEmpty(self):
        return not len(self.CONTENTS)
    
    def size(self):
        return len(self.CONTENTS)
    
    def clear(self):
        self.CONTENTS = []
    
    """
        Adds an item to the inventory.
        To be overridden for specific kinds of inventories.
        @param item An item to add to this inventory's contents.
        @return If the add was successful. 
    """
    def add(self, item):
        self.CONTENTS.append(item)
        return True
    
    """
        Always adds the item.
        Not to be overridden.
        @param item An item to add into self.
    """
    def forceAdd(self, item):
        self.CONTENTS.append(item)
    
    def remove(self, item):  
        name = str(item)
        
        for i in range(len(self.CONTENTS)):
            if str(self.CONTENTS[i]) == name:
                self.CONTENTS.pop(i)
                break
        else:
            print("Item " + str(item) + " not found.")
    
    """
        Removes an item from this inventory and gives it to another.
        @param item The item to give.
        @param giveToThis The inventory to add the item to.
        @return It the add was successful
    """
    def give(self, item, giveToThis):
        if giveToThis.add(item):
            self.remove(item)
            return True
        else:
            return False
    
    """
        Displays a formatted string representation of this for the player.
        The items in this are accompanied with a number which the player uses
        to reference items in the inventory.
        @return A string representation of this inventory's contents.
    """
    def __str__(self):
        if not self.isEmpty():
            result = ""
            slot = 1

            for i in self.CONTENTS:
                result += '<' + str(slot) + '> ' + str(i).title() + '\n'
                slot += 1
                    
            return result
        else:
            return "   nothing." + NL
