from Names import *
from GUI import GUI 
from Inventory import Inventory 
from Player import Player
from Furniture import *
import Menus, AudioPlayer
from random import randint

class BurningBowl(Furniture, Gettable):
    def __init__(self):
        super(BurningBowl, self).__init__()

        self.searchDialog = ("Whatever important item might have been there has " +
                             "likely burned away at self.point.")
        self.actDialog = "Jabbing a burning bowl isn't a very good idea."
        self.useDialog = self.actDialog

        self.addNameKeys("(?:hanging )?(?:steel )?bowl(?: of fire)?", 
                "(?:hanging )?(?:steel )?burning bowl", "fire", "light")
        
        self.addUseKeys(Furniture.ANYTHING)
        self.addActKeys(Furniture.GETPATTERN, Furniture.JOSTLEPATTERN, "jab", "poke")

    def useEvent(self, item):
        if item.getType() == WEAPON:
            return self.useDialog
        elif str(item) == HAND_TORCH:
            return "The torch is already lit, despite having been in your pocket for so long."
        else:
            return "What good would that serve?"

    def interact(self, key):
        if key == "jab" or key == "poke" or re.match(Furniture.JOSTLEPATTERN, key):
            return self.actDialog
        else:
            return self.getIt()



class Candelabra_Inventory(Inventory): 
    def __init__(self, itemList): 
        super(Candelabra_Inventory, self).__init__(itemList)
    
    def add(self, item):
        if str(item) == CANDLE: 
            return super(Candelabra_Inventory,self).add(item)
        else:
            GUI.out("Candelabras are not meant to hold such things.")
            return False



class Candelabra(SearchableFurniture, Gettable, Moveable):
    def __init__(self, itemList):
        super(Candelabra, self).__init__()
        
        self.actDialog = "That does not cause anything interesting."
        self.searchDialog = "The candelabra holds some candles."
        self.useDialog = ("The torch is already lit, despite having been kept in " +
                         "your pocket self.whole time.")

        self.addNameKeys("candles?", "fire")
        self.addUseKeys(HAND_TORCH, CANDLE)
        self.addActKeys(Furniture.GETPATTERN, "touch", "light")
        self.inv = Candelabra_Inventory(itemList)
    
    def getDescription(self):
        if self.inv.contains(CANDLE):
            return super(Candelabra, self).getDescription()
        else:
            return "The candelabra holds no more candles."
    
    def useEvent(self, item): 
        if str(item) == CANDLE:
            Player.getInv().remove(item)
            self.inv.add(item)
            return "You store a candle."
        else:
            return self.useDialog
    
    def getSearchDialog(self): 
        if self.inv.contains(CANDLE):
            return self.searchDialog
        else:
            return "The candelabra holds no more candles."
    
    def interact(self, key):               
        if key == "touch": 
            if self.inv.contains(CANDLE):
                return self.actDialog
            else:
                return ("You touch it. Thankfully, the candelabra lacks any " +
                        "burning candles, and thus you avoid burning.")
        elif key == "light":
            return "Lighting the candelabra gets you no closer to freedom."
        else:
            return self.getIt()
    
    def getIt(self):
        if self.inv.contains(CANDLE):
            if self.inv.give(self.inv.get(CANDLE), Player.getInv()):
                return "You take a candle from the candelabra."
            else:
                return Furniture.NOTHING
        else:
            return "The candelabra holds no more candles."



class Carpet(Furniture, Gettable):
    def __init__(self):
        super(Carpet, self).__init__()
        
        self.actDialog = ("You take some valuable time to admire the carpet. Yes, " +
                         "what a wonderfully woven piece of artwork. It really " +
                         "would be a shame to get self.dirty. What a fantastic rug.")
        self.useDialog = "That would most certainly ruin it."
        self.searchDialog = "There's nothing interesting under the carpet."

        self.addUseKeys(ACETONE, ASH, SOIL, "sand|.  dye", ".  (?:wine|vinegar)")
        self.addActKeys(Furniture.MOVEPATTERN, Furniture.GETPATTERN, "admire", "lift|raise", "roll")
   
    def interact(self, key):              
        if re.match(Furniture.MOVEPATTERN, key) or key == "lift" or key == "raise":
            return self.searchDialog
        elif key == "roll":
            return "You're really not intending to take that with you, right?"
        elif key == "admire":
            return self.actDialog
        else:
            return self.getIt("A foolish attempt is made. Carpets are much heavier than they look.")



class Chandelier(Furniture):
    def __init__(self):
        super(Chandelier, self).__init__()

        self.searchDialog = "You are pretty sure you can't jump that high."
        self.useDialog = "The chandelier is lit already."
        self.actDialog = "That would not be a very civilized thing to do."
        
        self.addNameKeys("chandelier")
        self.addUseKeys(HAND_TORCH)
        self.addActKeys("swing", "pull", "hang", "light")

    def interact(self, key):           
        if key == "pull":
            return ("It suffices to say the chandelier is mounted solidly " +
                    "to the ceiling and isn't unusual in any way.")
        elif key == "light":
            return self.useDialog
        else:
            return self.actDialog



"""
    Represents a fireplace with lit and unlit states.
    The bucket of water may be used on a fireplace to extinguish it.
"""
class Fireplace(Furniture, Gettable, Unmoveable):
    def __init__(self, bckt):        
        super(Fireplace, self).__init__()
        
        self._isLit = True
        self.BCKT_REF = bckt
        
        self.searchDialogLit = "Ouch! That's hot!"
        self.descUnlit = "It's a smoldering, unlit fireplace."
        self.useDialog = "You douse the flames with the water."
        
        self.addActKeys("warm", "douse|extinguish", "use", Furniture.GETPATTERN, "relax")
        self.addNameKeys("fireplace", "hearth", "fire|flames?")
        self.addUseKeys(BUCKET_OF_WATER)

    def getSearchDialog(self):  
        if self._isLit: 
            AudioPlayer.playEffect(39, 0.3)
            return self.searchDialogLit
        else:
            return self.searchDialogUnlit

    def getDescription(self):
        return self.descLit if self.isLit() else self.descUnlit

    def isLit(self):
        return self._isLit

    def extinguish(self):
        AudioPlayer.playEffect(39, 0.3)
        self._isLit = False

    def interact(self, key):   
        if key == "extinguish" or key == "douse": 
            if Player.hasItem(BUCKET_OF_WATER):
                bucket = Player.getInv().get(BUCKET_OF_WATER)
                return self.useEvent(bucket)
            else:
                return "You have nothing to douse the flames with."
        elif re.match(Furniture.GETPATTERN, key):
            return self.getIt()
        elif self.isLit(): 
            return "You warm your hands for a second, but you are still cold."
        else:
            return "There's not much you can do to an unlit fireplace." 
    

    def useEvent(self, water): 
        Player.getInv().remove(water)
        Player.getInv().add(BCKT_REF)

        if not self._isLit: 
            return ("You toss the water on, although there was never a fire to " +
                   "begin with. It's good that you get paid to chop, not think.")
        else:
            self.extinguish() 
            return self.useDialog



"""
    Represents a locked container (Cabinet, chest, etc.) That requires a key to
    to be opened. These keys have a unique type that do not match any room ID.
    Container is opened by 'unlocking' or 'opening' it with the corresponding
    key in possession. This is otherwise unsearchable before being unlocked.
"""
class LockedContainer(SearchableFurniture, Openable, Moveable): 
    def __init__(self, key, itemList=[]):
        super(LockedContainer, self).__init__(itemList)
        
        self.KEY = key          # ID of the key (type) used to unlock self.
        self.searchable = False # Starts locked, need a key to make searchable.

        self.addActKeys("unlock")
     
    def getSearchDialog(self): 
        if self.searchable:
            return "You open it and look inside."
        elif Player.hasKey(self.KEY):
            return self.unlock()
        else:
            return self.denyEntry()
     
    def interact(self, key):
        if self.searchable:
            return "Seems that you have already unlocked it."             
        else: 
            return self.getSearchDialog()
     
    def unlock(self): 
        self.searchable = True 
        AudioPlayer.playEffect(13)
        return self.actDialog
     
    def denyEntry(self):
        AudioPlayer.playEffect(4)
        return self.searchDialog



"""
    Potted plants give special items when watered.
"""
class PottedPlant(SearchableFurniture, Gettable, Moveable):
    def __init__(self, soil, gift): 
        super(PottedPlant, self).__init__()
        
        self.watered = False
        self.GIFT = gift # When watered for the first time, this is given to the player.
        self.SOIL_REF = soil
        
        self.actDialog = ("You pour a bit of the water on the plant. " +
                         "The plant trembles some and a bit of life springs back into it. ")
        self.searchDialog = "You fan through the soil."
        self.useDialog = ("Pouring that on the plant is definitely not going to " +
                         "be good for it, you monster.")

        self.addNameKeys("dirt", SOIL, "(?:potted )?plants?")
        self.addUseKeys(Furniture.ANYTHING)
        self.addActKeys(Furniture.GETPATTERN, "water", "dig")
        
        for i in range(3):
            self.inv.add(soil) 
    
    def interact(self, key):               
        if key == "water":
            if Player.hasItem(BUCKET_OF_WATER): 
                if self.watered: 
                    return self.actDialog
                else:
                    self.inv.add(GIFT)
                    self.watered = True
                    return self.actDialog + "A small object rises from the soil and now rests on top."
            else:
                return "You have nothing to water the plant with."
        elif key == "dig": 
            if Player.hasItem(SHOVEL) or Player.hasItem(TROWEL): 
                AudioPlayer.playEffect(34)
                return "Digging in the plant reveals nothing unusual."
            else:
                return "You have nothing sufficient to dig with, and your stocky hands are terrible for digging."
        else:
            return getIt()
    
    def useEvent(self, item): 
        if str(item) == BUCKET_OF_WATER:
            return self.interact("water")
        elif item.getType() == LIQUID:
            return self.useDialog
        elif item.getType() == WEAPON:
            return "Attacking the plant isn't going to solve any of your problems."
        elif str(item) == SHOVEL or str(item) == TROWEL: 
            AudioPlayer.playEffect(34)
            return "Digging in the plant reveals nothing unusual."
        elif str(item) == SOIL: 
            Player.getInv().remove(item)
            return "You return the soil to the plant."
        else:
            return DEFAULT_USE
    
    def getIt(self): 
        if Player.getInv().add(self.SOIL_REF):
            return "You scoop up some of the dirt."
        else:
            return "You already have some dirt."



"""
    A combination safe that can be unlocked by entering the right combination.
    Player may interact with or search this for an open attempt.
"""
class Safe(SearchableFurniture, Openable, Moveable): 
    def __init__(self, combo, itemList=[]):
        super(Safe, self).__init__(itemList)

        self.COMBO = combo
        self.DIALS = [randint(0, 9), randint(0, 9), randint(0, 9)]

        self.actDialog = "The safe is still locked."
        self.useDialog = "They didn't design safes to break open that easily."
        self.searchDialog = self.actDialog
        self.searchable = False
        self.addUseKeys(Furniture.ANYTHING)
        self.addActKeys("use|spin|twist", "smash|break")
        self.addNameKeys("(?:combination )?safe", "strongbox")

    def getSearchDialog(self):
        if not self.searchable:
            GUI.out("The safe has a combination lock.")
            self.openSub()

        if self.searchable:
            return "The safe is unlocked!"
            
        return self.searchDialog

    def openSub(self):
        GUI.menOut(Menus.SAFE_MENU)
        
        while True:
            GUI.out("\t  [" + str(self.DIALS[0]) + "][" + str(self.DIALS[1]) + "][" + str(self.DIALS[2]) + "]")      
            action = GUI.promptOut()

            if re.match("[123]", action):        
                if self.turnDial(int(action) - 1):
                    self.searchable = True
                    AudioPlayer.playEffect(43)
                    GUI.menOut("You here a click.") 
                else:
                    self.searchable = False
                    GUI.menOut(Menus.SAFE_MENU)
            elif not action:
                break

    def turnDial(self, i):
        AudioPlayer.playEffect(10)
        self.DIALS[i] = (self.DIALS[i] + 1) % 10
        return self.COMBO == (self.DIALS[0] * 100) + (self.DIALS[1] * 10) + self.DIALS[2]

    def interact(self, key):              
        if key == "break" or key == "smash":
            return "Now you WOULD like to do that, wouldn't you?"
        elif not self.searchable:
            GUI.out("The safe has a combination lock.")
            self.openSub()
            
            if self.searchable:
                return "The safe is unlocked!"
        else:
            return "The safe is already open. Perhaps you should search it."
        
        return self.actDialog

    def useEvent(self, item):
        return (useDialog if item.getType() == WEAPON else DEFAULT_USE)
 
    def moveIt(self):
        return "It budges only a small amount before you're out of breath. This is much too heavy."



class Skeleton(SearchableFurniture, Moveable):
    def __init__(self, itemList=[]):
        super(Skeleton, self).__init__(itemList)
        
        self.actDialog = ("\"Hello? Are you okay? Do you know a way out?\" You repeatedly ask the skeleton. " +
                         "The skeleton lies silently, motionless, rudely ignoring your inquiry.")
        self.searchDialog = "You crouch down."

        self.addNameKeys("skeleton|body")
        self.addActKeys("eat", "speak|talk|converse|chat|greet|listen")

    def interact(self, key):
        if key == "eat":
            return "The thought of that makes you shutter..."
        else:
            return self.actDialog

    def moveIt(self):
        return "This skeleton is most likely dead at this point. May as well let it rest."



"""
    Defines generic attributes of a statue.
"""
class Statue(Furniture):
    MOVE_DIAL = ("With a burst of almost super-human adrenaline, you " +
                 "passionately thrust yourself into the statue, moving " +
                 "it a small distance. You discover nothing interesting.")

    def __init__(self): 
        super(Statue, self).__init__()
        
        self.actDialog = "You brush your hand against the statue and marvel at its detail."
        self.searchDialog = "You look around the statue but find nothing of interest."

        self.addNameKeys("statues?")
        self.addActKeys("speak|talk|converse|chat|greet|listen")
        self.addActKeys(Furniture.MOVEPATTERN, Furniture.FEELPATTERN, Furniture.GETPATTERN, "admire")
    
    def interact(self, key):               
        if re.match(Furniture.MOVEPATTERN, key): 
            AudioPlayer.playEffect(41)
            return Statue.MOVE_DIAL
        
        elif key == "admire":
            return ("The statue's smooth and chiseled features trap your gaze " +
                   "in mesmerisation. Its delicate curves.. ehhh... it's " +
                   "a rock someone banged with a hammer and chisel a bunch of times. " +
                   "Woodworking! Now that's a refined art.")
        elif re.match(Furniture.FEELPATTERN, key):
            return self.actDialog
        elif re.match(Furniture.GETPATTERN, key):
            return "This is much too large to take."
        else:
            return ("\"Hello? Doth thou hast knowledge of an escape? Per chance " +
                   "be you the owner? Hello?\" You redundantly make your inquiry, " +
                   "but the statue stands motionless, nonchalant, and with a mark of disinterest.")



class HolderInventory(Inventory):  
    def __init__(self, itemList=[]):
        super(HolderInventory,self).__init__(itemList)

    def add(item): 
        if str(item) == HAND_TORCH and self.size() == 0:
            self.CONTENTS.append(item)
            return True
        else:
            GUI.out("The " + str(item) + " doesn't fit in.")
            return False



"""
    Represents a wall-mounted torch that can be taken.
    Torches are useful for a few things.
"""
class Torch_Holder(SearchableFurniture):
    def __init__(self, torch):
        super(Torch_Holder,self).__init__()
        self.TORCH = torch
        self.inv = HolderInventory(torch)
        
        self.description = ("Sitting in a steel holder is a burning wall torch " +
                           "giving off an orange glow.")
        self.searchDialog = "You look in the mounted steel holder."
        self.actDialog = "You slide the torch out of its holder and take it."
        self.useDialog = "You slide the torch into the steel holder."
        
        self.addActKeys(Furniture.GETPATTERN, "pull")
        self.addNameKeys("(?:wall )?torch(?:es)?", "(?:steel )?holders?")
        self.addUseKeys(HAND_TORCH)

    def interact(self, key):
        if key == "pull":
            return "If you expected the torch holder to be a disguised lever, be thoroughly disappointed."
        elif self.inv.contains(str(self.TORCH)):
            if self.inv.give(self.TORCH, Player.getInv()):
                return self.actDialog
            else:
                return NOTHING
        else:
            return "The holder is empty you bumbling oaf."
  
    def useEvent(self, item):
        if self.inv.contains(str(self.TORCH)):
            return "The holder already bears a torch you bumbling oaf."
        else:
            Player.getInv().give(item, self.inv)
            return self.useDialog

    def getDescription(self):
        if not self.containsItem(HAND_TORCH):
            return "The mounted steel holder is empty."
        else:
            return self.description

    def getSearchDialog(self):
        return self.getDescription()



"""
    Represents any type of wall art, e.g. paintings, tapestries.
    
"""
class WallArt(Furniture):  
    def __init__(self):  
        super(WallArt, self).__init__()

        self.actDialog = "You lift it only to reveal a blank wall."
        self.searchDialog = self.actDialog
        self.useDialog = "You can't bring yourself to destroy such an expensive object."
        
        self.addActKeys(Furniture.GETPATTERN)
        self.addActKeys("move", "lift", "slide", "admire")
        self.addUseKeys(HAND_TORCH, ACETONE, CANDLE, BOTTLE_OF_VINEGAR, BOTTLE_OF_WINE)
        
    def interact(self, key):                
        if key == "admire":
            return ("Yes, what a beautiful piece of artwork. You take a moment " +
                    "to soak in the creative essence. Yes...")
        else:
            return self.actDialog