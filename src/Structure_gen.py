from Names import *
from Player import Player
from Inventory import Inventory 
from Names import RUBBER_HOSE, LOOPED_ROPE, LEATHER_HOSE, WEAPON, METAL_LADDER, FIXED_LADDER
from GUI import GUI 
import Menus, Direction, AudioPlayer
from Furniture import Furniture, Unmoveable, Climbable, SearchableFurniture
from Patterns import DESTROY_P, UP_DOWN_P

"""
    Represents a wall. 
    Superficial only. Would not make sense for game to say "there is no wall here"
"""
class Wall(Furniture, Unmoveable):
    def __init__(self, dsc): 
        super(Wall, self).__init__()

        self.description = dsc
        self.actDialog = "What do expect to find? A pork chop?"
        self.searchDialog = "The walls here are solid and couldn't hide anything."
        self.useDialog = "You whack the wall and jolt backwards. Well, that was productive."
        self.addActKeys("break", Furniture.CLIMBPATTERN, "push", "press", "lean")
        self.addUseKeys(Furniture.ANYTHING)
        self.addNameKeys("walls?")
    
    def useEvent(self, item): 
        if item.getType() == WEAPON: 
            AudioPlayer.playEffect(35)
            return self.actDialog
        elif str(item) == METAL_LADDER:
            return item.useEvent()
        else:
            return Furniture.DEFAULT_USE

    def interact(self, key): 
        if key == "break":
            return self.actDialog
        elif key == "push" or key == "press":
            return "The player makes an unsuccessful but commendable attempt at discovering a hidden door or panel."
        elif key == "lean":
            return "Your player leans on the wall, hoping to activate a camoflaged button, but to no avail."
        else:
            return "Suction cups would be pretty convenient right about now..."




class Balcony(Furniture, Unmoveable):
    def __init__(self):
        super(Balcony, self).__init__()

        self.actDialog = "That doesn't seem like a safe thing to do..."
        self.searchDialog = "The entire balcony? One thing at a time please."

        self.addNameKeys("(?:balcony )?railing", "balcony")
        self.addActKeys("lean", "jump", "vault", Furniture.HOLDPATTERN)
       
    def interact(self, key):              
        if key =="lean":
            return self.actDialog
        elif key == "jump" or key == "vault":
            return "Are we flirting with death now?"
        else:
            return "You grab the balcony railing, but surely you'd never fall over by accident."



class Ceiling(Furniture, Unmoveable):
    DESC = "There's nothing too exciting about the ceiling here."
    
    def __init__(self, desc=DESC):
        super(Ceiling, self).__init__()

        self.description = desc
        self.actDialog = "It's too high up to do that. Also, why?"
        self.searchDialog = "There exists no evidence of something being hidden there."
        self.useDialog = "You poke the ceiling with the long object."

        self.addNameKeys("ceiling", "roof")
        self.addUseKeys(POLEARM, "wooden spear", "silver spear")
        self.addActKeys(Furniture.FEELPATTERN)



class Column(Furniture, Unmoveable):
    def __init__(self):
        super(Column, self).__init__()

        self.actDialog = ("You aren't very skilled at climbing vertical " +
                         "surfaces with your hands.")
        self.searchDialog = "There's nothing interesting on the column."
        self.useDialog = "What are you trying to do? Bring the whole castle down?"

        self.addUseKeys(Furniture.ANYTHING)
        self.addActKeys(Furniture.CLIMBPATTERN)

    def useEvent(self, item):
        if item.getType() == WEAPON:
            return self.useDialog
        elif str(item) == FIXED_LADDER or str(item) == METAL_LADDER:
            return "That'll get you up there, sure, but it's really not going to GET you anywhere..."
        else:
            return Furniture.DEFAULT_USE



# Represents a generic exterior wall.
class ExteriorWall(Wall):     
    def __init__(self):
        super(ExteriorWall, self).__init__("A fortress-like granite brick wall.")
        self.searchDialog = "The walls here are solid and couldn't hide anything."



"""
    Represents the floor or ground in a room.
    Superficial, though items may be stored here if needed.
"""
class Floor(SearchableFurniture, Unmoveable):
    def __init__(self, desc, itemList=[]):
        super(Floor, self).__init__(itemList)

        self.description = desc
        self.searchDialog = "You crouch down and scan the ground."
        self.actDialog = "You jam the spade into the floor. Your body jolts and you stagger back. The floor is undefeated."
        self.useDialog = "There's no reason to stand the ladder up in here."
        self.addActKeys("dig", SHOVEL, MOP, "clean")
        self.addUseKeys(FIXED_LADDER, SHOVEL, BUCKET_OF_WATER, TROWEL, MOP, "sweep")
        self.addNameKeys("floor", "ground", "walkway")
    
    def interact(self, key):      
        if key == "clean":
            return "Oh yes, you're sure the owner of this castle would love that."
        elif key == MOP or key == "sweep": 
            if Player.hasItem(MOP): 
                mop = Player.getInv().get(MOP)
                return self.useEvent(mop)
            else:
                return ("You have nothing mop the floor with. " +
                       "Do you really want to do that anyway? " +
                       "One less thing you need is a slippery floor.")
        else:
            if Player.hasItem(SHOVEL) or Player.hasItem(TROWEL): 
                i = Player.getInv().get(SHOVEL)
                
                if i == Inventory.NULL_ITEM:
                    i = Player.getInv().get(TROWEL)
                
                return self.useEvent(i)
            else:
                return "You have nothing with which to dig."
         
    def useEvent(self, item): 
        if str(item) == FIXED_LADDER:
            return self.useDialog
        elif str(item) == MOP:
            return "Yes, let's just make this a game about cleaning some madman's castle."
        elif str(item) == BUCKET_OF_WATER: 
            Player.getInv().remove(item)
            Player.getInv().add(Item(name=METAL_BUCKET, score=25))
            return "You dump the bucket of water out."
        else:
            AudioPlayer.playEffect(35)
            return self.actDialog



class Railing(Furniture, Unmoveable):
    def __init__(self):
        super(Railing, self).__init__()

        self.actDialog = ("You lean against the railing and rest a bit. All this " +
                         "walking has nearly bested you.")
        self.useDialog = ("Hopefully you aren't thinking that you can just climb " +
                         "down with something that short...")

        self.addNameKeys("railing")
        self.addUseKeys(LOOPED_ROPE, LEATHER_HOSE, RUBBER_HOSE)
        self.addActKeys(Furniture.HOLDPATTERN, "lean", "vault|jump|climb")
       
    def interact(self, key):              
        if key == "lean":
            return self.actDialog
        elif key == "jump" or key == "climb":
            return "Why are you trying to kill yourself?"
        else:
            return "You grab the railing. There's no fear of falling over, right?"



"""
    Defines generic attributes and methods for a staircase.
"""
class Staircase(Furniture, Unmoveable, Climbable):         
    def __init__(self, direction, dest, sound):
        super(Staircase, self).__init__()

        self.DIR = direction # If it is an up or down staircase.
        self.SOUND = sound # Sound this makes when walked on.
        self.DEST = dest # Room to which this leads.
        self.addActKeys(Furniture.CLIMBPATTERN, "use", "walk", "go")
        self.addNameKeys("stair(?:s|case)|steps?", "banister", "railing")
    
    def interact(self, key):      
        Player.setOccupies(self.DEST)
        AudioPlayer.playEffect(self.SOUND)
        return "You climb " + str(self.DIR) + " the stairs."    

    def getDir(self):
        return self.DIR



"""
    Some rooms have two sets of stairs or a switchback staircase.
    Allow the player to interact with either one and avoid problems of ambiguity.
"""
class DoubleStaircase(Staircase):
    def __init__(self, dest, dest2, sound): 
        super(DoubleStaircase, self).__init__(Direction.BOTH, dest, sound)
        self.DEST_2 = dest2 # Up destination
       
    def interact(self, key): 
        if key == Direction.UP or key == Direction.DOWN: 
            AudioPlayer.playEffect(self.SOUND)
            Player.setOccupies(self.DEST_2 if key == "up" else self.DEST)
            return "You climb " + key + " the stairs."   
        else:
            ans = GUI.askChoice(Menus.DOUBLE_ST, UP_DOWN_P)
            
            if not ans:
                return Furniture.NOTHING
            else:
                AudioPlayer.playEffect(self.SOUND) 

            if ans == "up" or ans == "u":
                Player.setOccupies(self.DEST_2)
                return "You climb up the stairs."
            else:
                Player.setOccupies(self.DEST) # Z coordinate modifier.
                return "You climb down the stairs."
               

# Represents a static window that can't be opened or closed.
class StaticWindow(Furniture, Unmoveable):
    def __init__(self):
        super(StaticWindow, self).__init__()
        self.escapeDialog = ("And fall to your death? You are a man of morals. " +
                            "Stave off the morbid thoughts!")
        self.actDialog = "This is a plain window. It has no moving parts."
        self.addActKeys("open|close", "exit|climb|jump|escape")
        self.addNameKeys("(?:barred )?window")

    def interact(self, key):
        return (self.actDialog if key in ("open", "close") else self.escapeDialog)



"""
    Represents a window that can be opened and closed.'
    Mainly for decoration. A few windows in the game are significant, however.
"""
class Window(Furniture, Unmoveable):   
    def __init__(self): 
        super(Window, self).__init__()

        self.isOpen = False
        self.escapeDialog = "And fall to your death?"
        self.descOpen = "It's an open stone arched window. In the distance, you see an expanse of sea."                    
        self.descClosed = "It's a closed stone arched window."
        self.addActKeys("open|close", "climb|exit|jump|escape")
        self.addNameKeys("window")
    
    def getDescription(self) :
        return (self.descOpen if self.isOpen else self.descClosed)

    def isOpen(self): 
        return self.isOpen

    def open(self): 
        self.isOpen = True
    
    def close(self): 
        self.isOpen = False
        
    def interact(self, key): 
        if key == "open" or key == "close": 
            if self.isOpen and key == "close": 
                AudioPlayer.playEffect(26)
                self.close()
                return "You close the window." 
            elif not self.isOpen and key == "open": 
                AudioPlayer.playEffect(26)
                self.open()
                return "You open the window." 
            else:
                return "The window is already " + ("open!" if key == "open" else "closed!")
        else:
            return self.escapeDialog



class Door(Furniture):   
    def __init__(self, direct):
        super(Door, self).__init__();
        self.DIR = direct
        self.useDialog = ("...Do you intend to pick the lock with that? Well, " +
                         "perhaps you could, but then again, you are not learned " + 
                         "of this skill. Yet another you yearn for at the moment.")
        self.searchDialog = "You aren't sure what you'd search for on a door."
        self.description = "It looks like a heavy wooden door."
        
        self.addUseKeys(Furniture.ANYTHING)
        self.addActKeys("open|use|walk|go|close", 
                "kick|bash|break|obliterate|destroy", "knock|bang", "unlock|lock", "pick")
        self.addNameKeys(str(direct) + " door", "(?:heavy )?(?:wooden )?door", "(?:door )?lock")
        
        if dir == Direction.EAST:
            self.addNameKeys("right door")
        elif dir == Direction.WEST:
            self.addNameKeys("left door")
    
    def interact(self, key):
        if key == "close":
            return "The door is already closed."
        elif DESTROY_P.match(key) or key == "kick" or key == "bash": 
            AudioPlayer.playEffect(40)
            return "You thrust your boot into the door, but the door is too well-built to give."
        elif key == "knock" or key == "bang":
            AudioPlayer.playEffect(55)
            return "You give the door a knock. To your astonishment, your knock is left unanswered."
        elif key == "lock" or key == "unlock":
            return "That isn't how this game works. Read the directions!"
        elif key == "pick":
            return "Lock picking is a skill you have always yearned for."
        else:
            Player.move(self.DIR)
            return Furniture.NOTHING

    def useEvent(self, item): 
        if item.getType() == WEAPON: 
            return "The door is build too solidly and breaking it down is futile."
        else:
            return self.useDialog



"""
    A generic door, used when a room has multiple doors.
    If the player specifies a 'door' in a room with many doors, self furniture
    is accessed. Though all Door objects contain the valid name key 'door', self
    object, being FIRST in the furnishings list, will be accessed first if the
    player types 'door'.
"""
class GenDoor(Furniture):
    def __init__(self):
        super(GenDoor, self).__init__()
        
        self.description = "There are several doors here. Use <direction 'door'>"
        self.searchDialog = self.description
        self.useDialog = ("...Do you intend to pick the lock with that? Well, " +
                         "perhaps you could, but then again, you are not learned " +
                         "of self skill. Yet another you yearn for at the moment.")
        self.actDialog = self.description

        self.addUseKeys(Furniture.ANYTHING)
        self.addNameKeys("door")
        self.addActKeys(Furniture.ANYTHING)

    def useEvent(self, item):
        if item.getType() == WEAPON: 
            return "The door is build too solidly and breaking it down is futile."
        else:
            return self.useDialog