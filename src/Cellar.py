from Furniture import *
import Id, Direction, AudioPlayer
from Room import Room
from Names import *
from Player import Player
from Inventory import Inventory
from Item import Item
from Structure_gen import Column
import re

"""
    Drains the fountain in the rotunda.    
"""
class Cel_Valve(Furniture, Unmoveable):
    def __init__(self, ID):
        super(Cel_Valve, self).__init__()

        self.FNTN_ID = ID
        self.loosened, self.open = False, False
        
        self.useDialog = ("No progress is gained from hitting the valve.")
        self.searchDialog = ("There's nothing hidden near the valve. Honestly, " +
                  "you never expected to find anything.")
        self.description = ("It's a big rusty valve mounted to the wall. In the " +
                 "center is a metal bolt.")
        self.actDialog = ("You tighten back up the valve. ")
        
        self.addNameKeys("(?:big )?(?:rusty )?valve", "(?:metal )?bolt")
        self.addUseKeys(HAMMER, MONKEY_WRENCH)
        self.addActKeys(Furniture.VALVEPATTERN)

    def interact(self, key):
        self.open = not self.open 
        
        AudioPlayer.playEffect(17)
        rf = Player.getRoomObj(Id.ROTU).getFurnRef(self.FNTN_ID)

        if self.open:
            return ("You loosen the valve. " + rf.loosen(1))
        else: 
            return self.actDialog + rf.loosen(-1) 

    def useEvent(self, item):
        if str(item) == MONKEY_WRENCH:
            AudioPlayer.playEffect(17)
            self.loosened = True
            return ("You can loosen the bolt a little, though it does not " +
                  "seem too necessary at the moment.")
        else:
            AudioPlayer.playEffect(35)
            return self.useDialog

            

class Cel2_Shaft(Furniture, Unmoveable):
    def __init__(self):
        super(Cel2_Shaft, self).__init__()
        
        self.description = ("The smooth shaft is about two and a half feet wide and runs " +
                  "through two holes barely wider than itself in the floor and " +
                  "ceiling. It's stationary, and appears too heavy to move by hand.")
        self.actDialog = ("Climb to where, exactly?")
        
        self.addActKeys("climb")
        self.addNameKeys("(?:smooth )?(?:wide )?(?:wooden )?shaft")



class Cel3_Crate(SearchableFurniture, Gettable, Moveable, Openable):
    def __init__(self, itemList=[]):
        super(Cel3_Crate, self).__init__(itemList)
        
        self.searchable = False
        self.description = ("The large wooden crate is about 3 feet on all sides " +
                  "and appears reinforced. Several nails all over the crate " +
                  "seal the lid shut.")
        self.actDialog = ("You have nothing effective to pry it with.")
        self.searchDialog = ("You peer inside the pried open crate.")
        self.useDialog = ("That seems like an interesting idea, considering " +
                  "the crate is open already.")

        self.addNameKeys("(?:large )?(?:wooden )?crate", "nails?", "screws?")
        self.addUseKeys(Furniture.ANYTHING)
        self.addActKeys("pry", "break", Furniture.GETPATTERN, Furniture.JOSTLEPATTERN)
    
    def getDescription(self):
        if self.searchable:
            return "The wooden crate has been opened by the astute player."
        else:
            return self.description
    
    def getSearchDialog(self):
        if self.searchable: 
            return self.searchDialog
        else: 
            return ("The wooden crate is sealed shut and offers no view inside.")
    
    def interact(self, key):              
        if key == "pry":
            if self.searchable:
                return ("The crate is apparently open already.")
            elif Player.hasItem(CROWBAR):
                return self.useEvent(Player.getInv().get(CROWBAR))
            else:
                return self.actDialog
        elif key == "break":
            if self.searchable:
                return ("The crate is apparently open already.")
            else:
                return ("Doing that by hand would be quite painful and regretable.")
        elif key == Furniture.GETPATTERN:
            return self.getIt()
        else:
            AudioPlayer.playEffect(40)
            return ("You kick the crate out of frustration, but what " +
                     "does not destroy the crate only makes it stronger.")
    
    def useEvent(self, item):
        name = str(item)
        
        if name == CROWBAR or name == SCREWDRIVER:
            if self.searchable: 
                return self.useDialog
            else:
                self.searchable = True
                
                if name == SCREWDRIVER:
                    AudioPlayer.playEffect(33)
                
                if name == CROWBAR:
                    return ("The crate snaps open under the leverage of the superior crowbar.")
                else:
                    return ("The screwdriver is super-effective against the rogue screws. ")
        elif name == HAND_TORCH:
            return ("The room's humidity prevents you from burning the crate open.")
        elif name == HAMMER:
            if self.searchable: 
                return self.useDialog
            else:
                return ("What appeared to be nails holding the crate shut are, to the player's dismay, " +
                    "heavy-duty screws. They cannot be pried with a common hammer.")
        elif name == BOTTLE_OF_VINEGAR:
            return ("How ingenious, attempting to dissolve the crate with acid. Unbeknownst " +
                    "to the player, acetic acid is weak and could not dissolve even a " +
                    "marshmallow. Actually, perhaps it could, but this game contains no marshmallows.")
        elif name == GLUE_BOTTLE:
            return ("Gluing the crate together? Isn't that the opposite of what we're " +
                      "trying to accomplish here?")
        elif name == MONKEY_WRENCH or name == METAL_BAR:
            AudioPlayer.playEffect(40)
            if self.searchable:
                return self.useDialog
            else:
                return ("The small blunt object is not powerful enough to break into the crate.")
        elif item.getType() == WEAPON:
            if self.searchable:
                return self.useDialog
            else:
                return ("You succeed in only making small gashes and slices in the powerful crate.")
        else:
            return Furniture.DEFAULT_USE



class Cel3_Valve(Cel_Valve):
    def __init__(self, ID, ref):
        super(Cel3_Valve, self).__init__(ID)
        
        self.WRENCH_REF = ref
        self.addActKeys("loosen")
    
    def interact(self, key):    
        if key == "loosen":
            if Player.getInv().contains(str(self.WRENCH_REF)):
                return self.useEvent(self.WRENCH_REF)
            else:
                return ("That sounds quite ambitious to do by hand.")
        elif self.loosened:
            return super(Cel3_Valve, self).interact(key)
        else:
            return ("Applying all the brawn you can muster fails to " +
                 "budge the valve. It's stuck.")

    def useEvent(self, item):
        if str(item) == MONKEY_WRENCH:
            if not self.loosened:
                self.loosened = True
                AudioPlayer.playEffect(17)
                return ("You loosen the bolt some with the wrench.")
            else:
                return ("Let's not go crazy here. The bolt is plenty loose.")
        else:
            return super(Cel3_Valve, self).useEvent(item)



class Cel4_Bed(SearchableFurniture, Moveable):    
    def __init__(self, itemList=[]):
        super(Cel4_Bed, self).__init__(itemList)
        
        self.description = ("The simple bed is nothing but a rudimentary metal " +
                  "frame and plain white mattress. It appears heavily used, " +
                  "though there is no one here.")
        self.actDialog = ("It's really not the time for sleeping now.")
        self.searchDialog = ("You crouch down and look under the bed.")

        self.addNameKeys("(?:rudimentary | simple )?bed")
        self.addActKeys(Furniture.SITPATTERN)



class Cel4_Coal(Furniture, Gettable, Unmoveable):
    def __init__(self, ref):
        super(Cel4_Coal, self).__init__()
        
        self.COAL_REF = ref
        self.description = ("It's a simple mound of coal.")
        self.actDialog = ("How most imprudent. Besides, you have nothing to set it ablaze.")
        self.searchDialog = ("Searching the coal mound reveals only coal.")
        self.useDialog = ("That is not prudent.")

        self.addNameKeys("(?:coal )?mound", "coal")
        self.addUseKeys(SHOVEL, TROWEL, HAND_TORCH)
        self.addActKeys(Furniture.GETPATTERN, "burn", SHOVEL, "dig")
    
    def interact(self, key):              
        if key == "burn":
            if Player.hasItem(HAND_TORCH): 
                return self.useDialog
            else:
                return self.actDialog
        elif key == SHOVEL or key == "dig":
            if Player.hasItem(SHOVEL) or Player.hasItem(TROWEL):
                i = Player.getInv().get(SHOVEL)
                
                if i == Inventory.NULL_ITEM:
                    i = Player.getInv().get(TROWEL)
                
                return self.useEvent(i)
            else:
                return ("You have nothing to dig the coal with. Of course, you " +
                       "could simple take one.")
        else:
            return self.getIt()

    def useEvent(self, item):
        if str(item) == SHOVEL or str(item) == TROWEL:
            AudioPlayer.playEffect(34)
            return self.getIt()
        else:
            return self.useDialog
    
    def getIt(self):
        if Player.getInv().add(self.COAL_REF):
            return ("You take a piece of coal.")
        else:
            return Furniture.NOTHING



class Cel5_Furnace(SearchableFurniture, Unmoveable, Gettable, Openable): 
    def __init__(self):
        super(Cel5_Furnace,self).__init__()
        
        self.lit = False
        self.description = ("A ramshackle tin furnace. It is unlit. A tin pipe " +
                  "feeds out the top and into the ceiling.")
        self.actDialog = ("You have nothing to light the furnace with.")
        self.searchDialog = ("You open up the furnace.")
        self.useDialog = ("You stick the torch in and light it ablaze. The warmth is quite comforting to you.")

        self.addNameKeys("(?:ramshackle )?(?:cylindrical )?(?:metal |tin )?furnace")
        self.addUseKeys(HAND_TORCH, COAL, METAL_BUCKET, BUCKET_OF_WATER)
        self.addActKeys("light", Furniture.GETPATTERN)
    
    def getDescription(self):
        if self.lit:
            return self.description.replace("un", "", 1) 
        else:
            self.description
    
    def getSearchDialog(self):
        self.searchable = not self.lit
         
        if self.searchable:
            return self.searchDialog
        else:
            return ("Best not do that while the furnace is lit.")
    
    def interact(self, key):              
        if key == "light":
            if Player.hasItem(HAND_TORCH):
                torch = Player.getInv().get(HAND_TORCH)
                return self.useEvent(torch)
            else:
                return self.actDialog
        else:
            return self.getIt()
    
    def useEvent(self, item):
        name = str(item)
        
        if name == HAND_TORCH:
            if self.lit:
                return ("The furnace is lit already!")
            elif self.containsItem(COAL):
                self.lit = True
                return self.useDialog
            else:
                return ("The furnace is empty of coal.")
        elif name == COAL:
            Player.getInv().give(item, self.inv)
            return ("You toss the lump of coal in the furnace.")
        elif name == BUCKET_OF_WATER:
            if self.lit:
                self.lit = False
                AudioPlayer.playEffect(39, 30)
                return ("You pour a bit of water on, extinguishing the fire.")
            else:
                return ("The furnace isn't even lit right now!")
        else:
            return ("You toss some of... ah, hold on, the player immediately " +
                   "realizes at this moment that the bucket was empty this whole time.")



class Cel5_Grate(Furniture, Gettable):
    def __init__(self):
        super(Cel5_Grate, self).__init__()
        
        self.moved = False
        self.CEL5_LDDR = Cel_Ladder(Id.CEL6, Direction.DOWN)
        
        self.description = ("The thick grate is about two and a half feet across " +
                "and covers what you can only assume to be the top rung " +
                "of a ladder. The grate looks just light enough to lift, " +
                "however the grate is locked down with a padlock.")
        self.actDialog = ("You can almost lift it, but a rogue padlock is sabotaging your attempt.")
        self.searchDialog = ("All that is of interest is a padlock and the metal rung below the grate.")
        self.useDialog = ("A sharp vibration propels through your body from the " +
                         "impact. Quite an impulse and futile decision.")

        self.addNameKeys("(?:thick )?(?:metal )?grate")
        self.addUseKeys(Furniture.ANYTHING)
        self.addActKeys(Furniture.MOVEPATTERN, Furniture.GETPATTERN, "open")
    
    def getDescription(self):
        if not self.moved:
            if Player.getPos().hasFurniture("padlock"):
                return re.sub(",.+", ".", self.description, count=1)
            else:
                return self.description
        else:
            return ("The metal grate has been moved out of the way.")
    
    def getSearchDialog(self):
        if Player.getPos().hasFurniture("padlock"):
            return self.searchDialog
        else:
            return Furniture.NOTHING_HERE
    
    def interact(self, key):              
        if Player.getPos().hasFurniture("padlock"):
            return self.actDialog 
        else:
            return self.getIt()
    
    def getIt(self):
        self.moved = not self.moved
        AudioPlayer.playEffect(48)
        
        if self.moved:
            Player.getPos().addFurniture(self.CEL5_LDDR)
            return ("You pull the grate out of the way, yielding entrance into the hole.")
        else:
            Player.getPos().removeFurniture(self.CEL5_LDDR.getID())
            return ("The player confusingly decides to place the grate back over the hole.")
    
    def useEvent(self, item):
        if item.getType() == Names.WEAPON:
            AudioPlayer.playEffect(35)
            return self.useDialog
        else:
            return Furniture.DEFAULT_USE



class Cel5_Lock(Furniture, Gettable):
    def __init__(self):
        super(Cel5_Lock, self).__init__()

        self.description = ("The small padlock connects the grate to a metal " +
                          "reinforcment around its rim.")
        self.actDialog = ("If only you had a fitting key for such a simple task.")
        self.searchDialog = ("Searching it yields only tiny lock parts.")
        self.useDialog = ("Smacking it with the % obliterates the lock. " +
                  "It falls into the abyss down below before apparently smacking the ground.")

        self.addNameKeys("padlock", "lock")
        self.addUseKeys(Furniture.ANYTHING)
        self.addActKeys("pick", "unlock|lock", Furniture.GETPATTERN, "break|destroy|hit|bang")
    
    def interact(self, key):              
        if key == "unlock":
            return self.actDialog
        elif key == "lock":
            return ("Isn't that the opposite of what we're trying to accomplish?")
        elif key == "pick":
            return ("Prepare for disappointment, for our protagonist is not skilled in that trade.")
        elif re.match(Furniture.GETPATTERN, key):
            return self.getIt("An astute proposition. Interestingly, the padlock is... well... locked.")
        else:
            return ("That would be too painful and ineffective to do by hand.")
    
    def useEvent(self, item):
        if item.getType() == WEAPON:
            AudioPlayer.playEffect(35)
            AudioPlayer.playEffect(31, 10)
            Player.getPos().removeFurniture(self.getID())
            return self.useDialog.replace("%", str(item), 1)
        else:
            return ("Do you intend to pick the lock with that? Prepare for " +
                   "disappointment, for our protagonist is not skilled in the trade.")



class Cel6_Columns(Column):
    def __init__(self):
        super(Cel6_Columns, self).__init__()
        
        self.description = ("A couple huge, wide columns standing perhaps 40 feet away are nearly blanketed by the darkness.")
        self.useDialog = self.actDialog = self.searchDialog = ("They are unreachable from here.")

        self.addNameKeys("(?:huge )?(?:distant )?(?:wide )?columns?")



class Cel6_Lights(Furniture):
    def __init__(self):
        super(Cel6_Lights,self).__init__()
        
        self.description = ("You cannot gauge their distance from you. A rough " +
                  "guess would be about 100 feet. They flicker, and appear to rest on a wall.")
        self.actDialog = self.searchDialog = self.useDialog = ("They are unreachable from here.")

        self.addNameKeys("lights?")
        self.addActKeys(Furniture.GETPATTERN)



class Cel6_Pipe(Furniture, Gettable):
    def __init__(self):
        super(Cel6_Pipe, self).__init__()
        
        self.description = ("The metal pipe feeding all the way down the shaft " +
                  "drains here into the blackness.")
        self.actDialog = ("You will need to turn the valve to do that.")
        self.useDialog = ("Hitting the pipe is futile.")

        self.addUseKeys(Furniture.ANYTHING)
        self.addNameKeys("(?:metal )?pipe")
        self.addActKeys(Furniture.GETPATTERN, "open")
    
    def interact(self, key):              
        if key == "open":
            return self.actDialog
        else:
            return self.getIt()
    
    def useEvent(self, item):
        if item.getType() == WEAPON:
            AudioPlayer.playEffect(35)
            return self.useDialog
        else:
            return Furniture.DEFAULT_USE



class Cel6_Platform(Furniture, Unmoveable):
    def __init__(self):
        super(Cel6_Platform, self).__init__()
        
        self.description = ("The mesh iron platform you stand on hangs from " +
                  "four poles connected to the ceiling. Surrounding " +
                  "you is just a black void except for the glow of " +
                  "what appear to be torches far below.")
        self.actDialog = ("That cannot possibly be a safe thing to do right now.")
        
        self.addActKeys("break|destroy", "jump")
        self.addNameKeys("(?:metal )?(?:iron )?(?:bars|railing|platform)")
    
    def interact(self, key):
        if key == "jump":
            return ("What an adventurous way to commit suicide...")
        else:
            return self.actDialog



class Cel6(Room):
    def __init__(self, name, ID):
        super(Cel6, self).__init__(name, ID)

    def getBarrier(self, direct):
        return ("There's nothing but a railing separating you from the black unknown.")



class Cel_Ladder(Furniture, Climbable):
    def __init__(self, ID, direct):
        super(Cel_Ladder, self).__init__()
        
        self.DIR = direct
        self.DEST = ID
        
        self.description = ("It's a metal ladder with rudimentary rungs attached " +
                           "directly to the stone wall.")
        self.actDialog = ("You climb " + str(direct) + " the long ladder.")

        self.addNameKeys("(?:metal )?ladder", "rungs?")
        self.addActKeys("use", Furniture.CLIMBPATTERN)
    
    def interact(self, key):      
        AudioPlayer.playEffect(47)
        Player.setOccupies(self.DEST)
        return self.actDialog
    
    def getDir(self):
        return self.DIR



class Cel_Lantern(Furniture):
    def __init__(self):
        super(Cel_Lantern, self).__init__()
        
        self.description = ("The small octagonal gas lamp hangs from a chain " +
                  "connected to the ceiling. It lights the area in a dim orange hue.")
        self.actDialog = ("The lantern is connected to a chain on the ceiling and can't be moved.")

        self.addNameKeys("(?:small )?(?:octogonal )?(?:hanging )?(?:lantern|lamp)")
        self.addActKeys(Furniture.GETPATTERN)



class Cel_Pipe(Furniture, Unmoveable):
    def __init__(self):
        super(Cel_Pipe,self).__init__()
        
        self.description = ("The metal pipe is about 6 inches wide. It does not " +
                "sound as though anything is running through it.")
        self.actDialog = ("For shame. That pipe did no harm unto you.")

        self.addNameKeys("(?:metal )?pipe")
        self.addUseKeys(Furniture.ANYTHING)
        self.addActKeys("bust", "break")
    
    def interact(self, key):              
        return self.actDialog
    
    def useEvent(self, item):
        return (self.actDialog if item.getType() == WEAPON else Furniture.DEFAULT_USE)