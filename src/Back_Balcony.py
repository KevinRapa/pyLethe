from Room import Room
import Direction, AudioPlayer
from Structure_gen import Door, Column, Railing
from Furniture import SearchableFurniture, Moveable, Furniture, Unmoveable
from Item import Note

"""
    Contains a note which directs player to the first key.
    Mainly superficial, for flavor. Offers view of the village the player left
    from. 
    Named Foyb in order to avoid door noise.
    Connects to Foy2 and Foyc.
"""
class Bba1(Room):
    def __init__(self, name, ID):
        super(Bba1, self).__init__(name, ID)

    def getBarrier(self, direct):
            if direct == Direction.NORTH:
                return ("There's a couple hundred foot drop right there.")
            elif direct == Direction.SOUTH:
                AudioPlayer.playEffect(4)
                return ("The gate that way is closed.")
            else:
                return self.bumpIntoWall()



class Bba2_Door(Door):        
    def __init__(self, direct):
        super(Bba2_Door, self).__init__(direct)
        
        self.description = ("This door looks different from the other doors in " +
                           "the castle. It is carved very artfully. At its center, " +
                           "a bearded face is carved into the wood.")



"""
    Contains a note which directs player to the first key.
    Mainly superficial, for flavor. Offers view of the village the player left
    from.
    Named Foyc in order to avoid door sound.
    Connected to Gal1 and Foyb
"""
class Bba2(Room):    
    def __init__(self, name, ID):
        super(Bba2, self).__init__(name, ID)

    def getBarrier(self, direct):
        if direct == Direction.NORTH:
            return ("There's a couple hundred foot drop right there.")
        elif direct == Direction.SOUTH:
            return "You should be getting out of here..." # For end game.
        else:
            return self.bumpIntoWall()


class Bba_Bench(SearchableFurniture, Moveable):    
    def __init__(self, itemList=[]):
        super(Bba_Bench, self).__init__(itemList)

        self.description = ("It's a stone bench with carvings of birds around the edge. ")
        self.searchDialog = ("You look on the bench.")
        self.actDialog = ("You sit down for a moment and let the salty breeze hit your face.")
        self.addActKeys(Furniture.SITPATTERN)
        self.addNameKeys("(?:stone )?bench")

    def getDescription(self):
        if self.containsItem("note from a visitor"):
            return (self.description + "A note is laying on its surface.")
        else:
            return self.description



class Bba_Cliff(Furniture):    
    def __init__(self):
        super(Bba_Cliff, self).__init__()
        self.description = ("The cliff has a steep incline. To your discomfort, " +
                           "you spot an eerie body in a pocket of rocks on it.")
        self.actDialog = ("You haven't reached that point yet. Hang in there!")
        self.searchDialog = ("You aren't jumping down there like that last person did.")
        
        self.addActKeys("jump", "climb", "vault")
        self.addNameKeys("cliff", "drop")

    def interact(self, key):
        if key == "jump":
            return self.actDialog
        else:
            return ("You're too heavy for that, and the cliff is too vertical. Good idea though.")



class Bba_Columns(Column):    
    def __init__(self):
        super(Bba_Columns, self).__init__()

        self.description = ("The granite columns are wide and bulging.")
        self.addNameKeys("(?:granite )?(?:columns?|pillars?)")



class Bba_Rlng(Railing):    
    def __init__(self):
        super(Bba_Rlng, self).__init__()

        self.description = ("A thick granite railing. Past it is a huge, treacherous " +
                           "drop into the black sea.")
        self.addNameKeys("(?:thick )?(?:stone |granite )?railing")



class Bba_Sconce(Furniture, Unmoveable):
    def __init__(self):
        super(Bba_Sconce, self).__init__()

        self.description = ("It's a copper metal sconce holding a glass bulb. It dimly " +
                           "lights the wall with a flickering orange glow.")
        self.actDialog = ("Ouch! That's hot!")
        self.addActKeys(Furniture.HOLDPATTERN)
        self.addNameKeys("(?:copper )?(?:metal )?(?:sconce|light)")

    def moveIt():
        return ("Solidly mounted to the wall. No hidden lever here.")



class Bba_Sea(Furniture):
    def __init__(self):
        super(Bba_Sea, self).__init__()
        
        self.description = ("Just an endless black expanse.")
        self.actDialog = ("Well, if you were to jump down there, your problems would be gone in a way..")
        self.searchDialog = ("If your friends jumped off a cliff, would you too?")
        self.addNameKeys("sea", "ocean", "waves")
        self.addActKeys("drink", "swim")



class Bba_Shoreline(Furniture):
    def __init__(self):
        super(Bba_Shoreline, self).__init__()

        self.description = ("It's a long, distant shoreline running in front of the small village.")
        self.searchDialog = ("There's no way you are getting over there.")
        self.actDialog = self.searchDialog
        self.addActKeys("get", "go", "walk", "fly", "jump")
        self.addNameKeys("shore ?(?:line)?")



class Bba_Village(Furniture):   
    def __init__(self):
        super(Bba_Village, self).__init__()
        self.description = ("You gaze at its still silhouette and tiny flickering " +
                           "lights. You calmly reminisce about your life in that " +
                           "village, wondering if you will ever return.")
        self.searchDialog = ("Don't be silly.")
        self.actDialog = ("Do you really think you can do that?")
        self.addActKeys("visit", "return", "go")
        self.addNameKeys("village", "town")
