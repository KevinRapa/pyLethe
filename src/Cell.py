from Furniture import *
import re
import Id, Patterns, Direction, AudioPlayer
from Player import Player
from GUI import GUI
from Room import Room
from Things import Torch_Holder
from Item import Item, Weapon
from Names import METAL_BAR
from Tunnels import Sew_Door

class Intr_Door(Sew_Door):
    def __init__(self):
        super(Intr_Door,self).__init__(Direction.EAST)
        
        self.description = ("The metal door offers a view to the outside through " +
                           "a small barred opening. You can " +
                           "see into a larger room with a pool in the center. A vortex " +
                           "of water in the pool spins a water wheel attached to a " +
                           "driveshaft going into the ceiling. You can see a door " +
                           "on the far opposite side and a small black grate in the " +
                           "room's corner. You can't locate the source of the discomforting " +
                           "noise though.")

        self.addActKeys("pry", "cut")
        self.addNameKeys("(?:small )?window", "(?:metal )?bars?")
    
    def interact(self, key):
        if key == "pry":
            return ("The bars are too thick to pry.")
        elif key == "cut":
            return ("Cut the bars with... what though?")
        else:
            return super(Intr_Door, self).interact(key)
    
    def useEvent(self, item):
        if str(item) == METAL_BAR: 
            return ("The bars are too thick to pry. Fitting yourself through the " +
                      "opening seems far-fetched as well.")
        else:
            return super(Intr_Door, self).useEvent(item)



class Intr_Gears(Furniture, Gettable, Unmoveable):
    def __init__(self):
        super(Intr_Gears, self).__init__()

        self.description = ("Many gears and axles of different sizes spin on the " +
                           "walls. They must generate power for something.")
        self.actDialog = ("You don't think sticking your hand in there is a good idea.")
        self.useDialog = ("You thrust the bar into the gears. The bar bounces off, ineffective. Your body jolts back.")
        self.searchDialog = ("You search around the machinery but cannot find anything useful.")

        self.addNameKeys("(?:spinning )?gears?", "machinery", "axles")
        self.addActKeys(Furniture.GETPATTERN, "touch|feel|stop")
        self.addUseKeys(METAL_BAR)
    
    def interact(self, key):
        if re.match("touch|feel|stop", key):
            return self.actDialog
        else:
            return self.getIt()



"""
    The player must move this grate with a metal bar found in the noisy room
    in order to escape.
    
    
"""
class Intr_Grate(Furniture, Resetable, Gettable, Climbable):
    MOVED_GRATE = ("You've already moved the grate!")
    
    def __init__(self):
        super(Intr_Grate, self).__init__()
        
        self.description = ("The water in the room drains through this grate here. " +
                           "Squinting though it, you spot what you believe to be " +
                           "the top rung of a ladder.")
        self.actDialog = ("It's too heavy. You can't open it.")
        self.useDialog = ("With a lot of strength, you manage to move the grating out of the way.")
        self.searchDialog = ("There's nothing unusual... Though squinting through the grate, " +
                            "you see what looks like the top rung of a ladder.")

        self.addNameKeys("(?:metal )?(?:grate|ladder|drain)", "hole")
        self.addActKeys("jump", Furniture.CLIMBPATTERN, Furniture.MOVEPATTERN, "pry", "open", "lift")
        self.addActKeys(Furniture.GETPATTERN)
        self.addUseKeys(METAL_BAR)
    
    def getDescription(self):
        if self.opened:
            return ("The open hole in the floor reveals a simple ladder leading downwards.")
        else:
            return self.description
    
    def getSearchDialog(self):
        if self.opened: 
            return ("The ladder goes down a ways you estimate about 30 feet.")
        else:
            return self.searchDialog
    
    def interact(self, key):  
        if re.match(Furniture.MOVEPATTERN, key) or key == "open" or key == "lift": 
            return (Intr_Grate.MOVED_GRATE if self.opened else self.actDialog)
        elif key == "pry":
            if Player.hasItem(METAL_BAR): 
                return self.useEvent(None)
            else:
                return "You have nothing good to pry with."
        elif key == "jump" or re.match(Furniture.CLIMBPATTERN, key):
            if self.opened:
                AudioPlayer.playEffect(47)
                Player.setOccupies(Id.ESC1)
                return ("You climb down the ladder a ways into a small noisy tunnel.")
            else:
                return ("You aren't going anywhere with that grate closed.")
        elif Patterns.KEY_P.match(key):
            Player.setOccupies(key)
            return ("You climb down the ladder a ways into a small noisy tunnel.")
        else:
            return self.getIt()

    def useEvent(self, item):
        if not self.opened:
            AudioPlayer.playEffect(48)
            self.opened = True
            return self.useDialog
        else:
            return Intr_Grate.MOVED_GRATE
    
    def reset(self):
        self.opened = False
    
    def getDir(self):
        return Direction.DOWN



"""
    Player wakes up trapped in here after laboratory puzzle.
    Player must take the torch, lift the grate, climb down the ladder
    to escape through small tunnels into the strange pool.
    
    If the player is captured, the torch and grate in here are reset.
    
    Connects to Esc1
"""
class Intr(Room):
    def __init__(self, name, ID, *furniture):
        super(Intr, self).__init__(name, ID)

    def triggeredEvent(self):
        if not Player.hasVisited(self.ID):
            GUI.out("An unknown amount of time passes. You awake with your head " +
                    "against a cold, wet rock floor. You manage to stand with " +
                    "some effort, and then take notice of a rattling noise. " +
                    "There's something, some kind of creature, wandering the halls outside...")
        
        return self.NAME



class Intr_Torch(Torch_Holder, Resetable):
    def __init__(self, torch):
        super(Intr_Torch, self).__init__(torch)
    
    def reset(self):
        if not self.inv.contains(str(self.TORCH)):
            self.inv.add(self.TORCH)
    
    def interact(self, key):
        if key == "pull":
            return ("Nope, nothing. Of all the torches you wanted " +
                   "to be a disguised lever, this was the one.")
        else:
            return super(Intr_Torch, self).interact(key)



class Intr_Water(SearchableFurniture, Resetable):
    METAL_BAR_REF = Weapon(METAL_BAR, 0)
    
    def __init__(self):
        super(Intr_Water, self).__init__()
        
        self.searchDialog = ("You look in the shallow stream, near the wheel.")
        self.description = ("The small river of water flows through a dip under the " +
                           "door. The square channel is only a couple feet wide.")
        self.actDialog = ("The river is too small for your frame, and the current " +
                         "looks strong. There must be another way out.")

        self.inv.add(Intr_Water.METAL_BAR_REF)
        self.addNameKeys("(?:shallow )?dip", "(?:river of )?water", "(?:square )?channel")
        self.addActKeys("drink", "jump", "swim", "escape")
    
    def interact(self, key):              
        if key == "drink":
            return ("You take a sip. The water is cool and tastes a little strange, but you haven't much of a care for now.")
        else:
            return self.actDialog
    
    def reset(self):
        if not self.inv.contains(str(Intr_Water.METAL_BAR_REF)):
            self.inv.add(Intr_Water.METAL_BAR_REF)



class Intr_Wheel(Furniture, Unmoveable):
    def __init__(self):
        super(Intr_Wheel,self).__init__()

        self.description = ("The large horizontal axle spins at about shoulder " +
                           "height in the room. It must be somehow connected to " +
                           "these other gears. Be careful, you wouldn't want to " +
                           "bump your head on this thing.")
        
        self.actDialog = ("You could never muster the strength to stop the wheel.")
        self.useDialog = ("You thrust the bar into the wheel attempting to stop " +
                       "it. The bar jolts back along with your body.")
        self.searchDialog = ("You search around the machinery but cannot find anything useful.")

        self.addUseKeys(METAL_BAR)
        self.addNameKeys("(?:large )?(?:spinning )?(?:horizontal )?(?:(?:water )?wheel|axle)")
        self.addActKeys(Furniture.GETPATTERN, "stop")