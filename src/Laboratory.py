import Menus, AudioPlayer
from Patterns import YES_NO_P, ONE_TO_SIX, LABO_BURET_ONE_OR_TWO
from Names import *
from Item import Item, Ingredient, Liquid, Book
from Inventory import Inventory
from Furniture import *
import re, time
from Player import Player
from Room import Room
from GUI import GUI
from threading import Timer, Thread

class Labo_Beaker(Furniture):        
    EMPTY = ("nothing.")
    GEN_POTION = ("A mystery liquid.")
    PHASE_DOOR = ("the phase door potion.")
    
    def __init__(self, beakerItem):
        super(Labo_Beaker,self).__init__()
        
        self.mode = Labo_Beaker.EMPTY
        
        self.BEAKER_REF = beakerItem
        self.PHASE_POTION = Liquid(PHASE_DOOR_POTION,  150,
                        use="You don't know the duration. Better get out to the front gate before drinking this!!")
        self.GENERIC_POTION = Liquid(POTION_OF_SCIENCE, 0, 
                        use="You really aren't sure enough about the safety of doing that...")
        self.description = ("The beaker contains ")
        self.searchDialog = Furniture.NOTHING
        self.useDialog = ("That's not it's proper function right now!")
        self.actDialog = ("You take the beaker off of the contraption.")

        self.addUseKeys("\\w+ \\d{1,2}mL")
        self.addNameKeys(BEAKER)
        self.addActKeys(Furniture.GETPATTERN)
        self.addActKeys("drink")
    
    def getDescription(self):
        return self.description + self.mode
    
    def getSearchDialog(self):
        return self.getDescription()
    
    def interact(self, key):              
        if key == "drink":
            return ("You can't do that while it's still on the table!")
        elif not Player.getInv().isFull():
            Player.getPos().removeFurniture(self.getID())
            
            if self.mode == Labo_Beaker.EMPTY:
                Player.getInv().add(self.BEAKER_REF)
            elif self.mode == Labo_Beaker.GEN_POTION:
                Player.getInv().add(self.GENERIC_POTION)
            elif self.mode == Labo_Beaker.PHASE_DOOR:
                Player.getInv().add(self.PHASE_POTION)

            self.mode = Labo_Beaker.EMPTY
            return self.actDialog
        else:
            return ("You are already carrying too much!")
    
    def setMode(self, mode):
        if self.mode != Labo_Beaker.EMPTY:
            self.mode = Labo_Beaker.GEN_POTION
        elif self.mode == 0:
            self.mode = Labo_Beaker.GEN_POTION
        else:
            self.mode = Labo_Beaker.PHASE_DOOR



"""
    Used to titrate wine and vinegar for the phase door potion.
    Uses titrator task. 
"""
class Labo_Burette(Furniture):
    EMPTY = ("nothing ") # Shouldn't be dispensed ever.
    WINE = ("wine ")
    VINEGAR = ("vinegar ")
    HOLYWATER = ("holy water ")
    ACETONE = ("acetone ")
    WATER = ("H2O ")
    GLUE = ("glue ")
    CLEANER = ("cleaning solution ")

    def __init__(self, emptyVial, testTube):
        super(Labo_Burette,self).__init__()

        self.mode = Labo_Burette.EMPTY
        self.VIAL_REF = emptyVial
        self.TUBE_REF = testTube
        self.description = ("It's a tall glass tube for dispensing particular quantities of liquids. " +
                           "On the top is an opening to pour a liquid. On the bottom is a nozzle " +
                           "and stopcock for dispensing it. Make sure you have a vial or " +
                           "test tube to catch the liquid with. The burette has ")
        self.actDialog = ("You need a vial or test tube to dispense into!")

        self.addNameKeys("(?:glass )?buret(?:te)?", "buret(?:te)? stopcock")
        self.addUseKeys(BOTTLE_OF_WINE, BOTTLE_OF_VINEGAR, TEST_TUBE, EMPTY_VIAL, 
                HOLY_WATER, ACETONE, BUCKET_OF_WATER, CLEANING_SOLUTION, GLUE_BOTTLE)
        self.addActKeys("use", Furniture.VALVEPATTERN, "dispense", "drain", "empty", "titrate")
    
    def getDescription(self):
        return (self.description + self.mode + "in it.")
    
    def getSearchDialog(self):
        return self.interact("use")
    
    def useEvent(self, item):
        s = str(item)

        if s == TEST_TUBE and not s == EMPTY_VIAL and self.mode == Labo_Burette.EMPTY:
            return ("The burette has liquid in it already!")

        if s == BOTTLE_OF_VINEGAR:
            self.mode = Labo_Burette.VINEGAR 
        elif s == BOTTLE_OF_WINE:
            self.mode = Labo_Burette.WINE       
        elif s == HOLY_WATER:
            self.mode = Labo_Burette.HOLYWATER  
        elif s == ACETONE:
            self.mode = Labo_Burette.ACETONE    
        elif s == BUCKET_OF_WATER:
            self.mode = Labo_Burette.WATER      
        elif s == CLEANING_SOLUTION:
            self.mode = Labo_Burette.CLEANER    
        elif s == GLUE_BOTTLE:
            self.mode = Labo_Burette.GLUE                             

        return self.interact("use")
    
    def interact(self, key):   
        if key == "empty" or key == "drain":
            self.mode = Labo_Burette.EMPTY
            return ("The burette is now empty.")
        elif self.mode != Labo_Burette.EMPTY:
            GUI.out("Would you like to titrate the " + mode + "or empty the burette?")

            ans = GUI.askChoice(Menus.LABO_BURET, LABO_BURET_ONE_OR_TWO)

            if ans:
                if ans == "1":
                    self.mode = Labo_Burette.EMPTY
                    return ("You empty everything out of the burette.")
                else:
                    return self.dispenseDialog()
            else:
                return Furniture.NOTHING
        else:
            return ("The burette is currently empty.")
    
    def dispenseDialog(self):
        if Player.hasItem(TEST_TUBE):
            Player.getInv().remove(self.TUBE_REF)
            Player.getInv().add(self.dispense())
            return Furniture.NOTHING
        elif Player.hasItem(EMPTY_VIAL):
            Player.getInv().remove(self.VIAL_REF)
            Player.getInv().add(self.dispense())
            return Furniture.NOTHING
        else:
            return self.actDialog
    
    def dispense(self):
        GUI.out(self.mode + "will be dispensed in 5 mL increments. Press " +
                  "enter to start titrating and then a second time to stop titrating.")
        GUI.menOut(Menus.ENTER)
        GUI.promptOut()
        
        volume = TitrationTask.titrate()

        return Ingredient(mode + volume + "mL", 0, "The vial holds a small amount of " + mode + ".")



class Labo_Condenser(Furniture, Moveable):
    def __init__(self, beakerItem):
        super(Labo_Condenser,self).__init__()
        
        self.flapOpen = False
        self.BEAKER_REF = Labo_Beaker(beakerItem)
        
        self.description = ("This half of the contraption consists of a long, curved " +
                           "glass tube on a stand. The glass tube has a switch attached to a stopper inside the tube. " +
                           "The tube(from the condenser and ends hanging above a ")
        self.actDialog = ("You toggle the switch attached to the stopper. It's now ")
        self.searchDialog = ("The contraption is comprised of many alchemical components. " +
                            "Though they're alien to you, you note nothing out of the ordinary.")
        self.useDialog = ("You place the beaker on top of the drain, under the glass tube.")

        self.addNameKeys("condenser", "(?:glass )?tubes?|stopper|switch|drain")
        self.addUseKeys(BEAKER, TEST_TUBE, FLORENCE_FLASK, EMPTY_VIAL, "copper (?:pot|pan)")
        self.addActKeys("flick", "turn", "toggle", "rotate")
    
    def getDescription(self):
        return self.description + ("beaker." if Player.getPos().hasFurniture(BEAKER) else "drain on the table.")
    
    def interact(self, key): 
        self.flapOpen = not self.flapOpen 
        return self.actDialog + ("open." if self.flapOpen else "closed.")
    
    def useEvent(self, item):
        if not str(item) == BEAKER:
            return ("That type of vessel was not designed for collecting chemicals! Put it down before you poke your eye out.")
        else:
            Player.getInv().remove(item)
            Player.getPos().addFurniture(self.BEAKER_REF)
            return self.useDialog
    
    def condense(self, chemical):
        result = ("You strike the top of the burner. For a minute, it burns against the flask's bottom, " +
                       "boiling the insides aggressively. % After a minute, the flame dies out.")
        
        if self.flapOpen:
            if Player.getPos().hasFurniture(self.BEAKER_REF.getID()):
                self.BEAKER_REF.setMode(chemical)
                GUI.out(result.replace("%", "The chemical condenses into the beaker on the other side.", 1))
            else:
                GUI.out(result.replace("%", "You watch in horror as the chemical condenses into the glass tube and " +
                        "flows down the drain under the condenser.", 1))
            return True
        else:
            GUI.out(result.replace("%", "The liquid evaporates up into the glass tube, but starts dripping back " +
                    "out into the florence flask. You scratch your head.", 1))

            return False 

    def moveIt(self):
        return ("The contraption looks pretty fragile. You think it best to leave it where it is.")



class Labo_Contraption(Furniture, Moveable):    
    def __init__(self):
        super(Labo_Contraption,self).__init__()

        self.description = ("The large contraption seems to be composed of two parts. " + 
                           "The left half has a bunsen burner under a rack for a flask. " +
                           "Above it is an inch-wide glass tube bridging over. The " +
                           "right half consists of the glass tube emptying out over a " +
                           "drain in the counter. There's a switch connected to a stopcock on the tube.")
        self.actDialog = ("You have no idea what to do. Maybe there's something in here to help.")
        self.searchDialog = ("This giant thing is alien to you, yet nothing seems out of the ordinary.")
        self.useDialog = self.actDialog

        self.addNameKeys("(?:complicated )?(?:alchemical )?contraption")
        self.addActKeys("use")
        self.addUseKeys(BEAKER, FLORENCE_FLASK)
    
    def moveIt(self):
        return ("The contraption looks pretty fragile. You think it best to leave it where it is.")



class Labo_Counter(SearchableFurniture, Openable, Unmoveable):
    def __init__(self, itemList=[]):
        super(Labo_Counter,self).__init__(itemList)
        
        self.description = ("The counter has a black top and two drawers on the bottom. " +
                           "On the surface of the counter, to the left, is a metal sink " +
                           "next to the large contraption on the right.")
        self.searchDialog = ("You look inside the drawers.")

        self.addNameKeys("counter", "drawers?")



class Labo_Devices(Furniture):
    def __init__(self):
        super(Labo_Devices,self).__init__()

        self.description = ("You are overwhelmed with science. You have never been " +
                           "in a laboratory before. All you see are many colors, " +
                           "valves and pipes.")
        self.actDialog = ("You have no idea what to do.")
        self.searchDialog = self.useDialog = self.actDialog

        self.addNameKeys("(?:alchemical )?devices?")
        self.addUseKeys(Furniture.ANYTHING)
        self.addActKeys(Furniture.ANYTHING)



"""
    Dispenses various types of chemicals to be used in alchemy.    
"""
class Labo_Dispensers(Furniture, Unmoveable):
    def __init__(self, emptyVial, testTube):
        super(Labo_Dispensers,self).__init__()

        self.VIAL_REF = emptyVial
        self.TUBE_REF = testTube
        
        self.searchDialog = ("Many foreign chemical can be dispensed from their containers on the wall.")
        self.description = ("The series of six opaque dispensers are " +
                           "lined up next to each other over a sink. At the bottom " +
                           "of each one is a rotating stopcock.")
        self.actDialog = ("You need a vial or test tube to dispense into!")

        self.addNameKeys("(?:opaque )?(?:dispensers?|containers?)", 
                "dispenser stopcock", "liquid|chemicals?(?: dispensers?)?")
        self.addUseKeys(EMPTY_VIAL, TEST_TUBE)
        self.addActKeys("use", Furniture.VALVEPATTERN, Furniture.GETPATTERN, "dispense|drain|empty|titrate")
    
    def interact(self, key):   
        if Player.hasItem(TEST_TUBE):
            if self.askToDispense():
                Player.getInv().remove(self.TUBE_REF)
                Player.getInv().add(self.dispense())
            return Furniture.NOTHING
        elif Player.hasItem(EMPTY_VIAL):
            if self.askToDispense():
                Player.getInv().remove(self.VIAL_REF)
                Player.getInv().add(self.dispense())
            return Furniture.NOTHING
        else:
            return self.actDialog
    
    def useEvent(self, item):
        return self.interact("use")
    
    def dispense(self):
        GUI.out("There are six dispensers on the wall. You cannot see inside them, " +
                "but each bears a label. From left to right, the labels read: \t\t1 - H2CO3   2 - Br " +
                "         3 - Ae      4 - HF          5 - NACL    6 - C20H14O4 \t\t\t\t\tDispense which one?")
        
        ans = GUI.askChoice(Menus.LABO_DISP, ONE_TO_SIX)
        
        GUI.out("Liquid will be dispensed in 5 mL increments. Press enter to start titrating, then again after a period to stop titrating.")
        GUI.menOut(Menus.ENTER)
        GUI.promptOut()
        
        volume = TitrationTask.titrate()
        i = int(ans)

        if i == 1:
            return Ingredient("H2CO3 " + volume + "mL", 0, "The vial holds a clear mundane liquid.")
        elif i == 2:
            return Ingredient("Br " + volume + "mL", volume, "The vial holds a odd rusty liquid. It's evaporating aggressively.")
        elif i == 3:
            return Ingredient("ae " + volume + "mL", volume, "The vial holds a pale blue, aromatic liquid.")
        elif i == 4:
            return Ingredient("HF " + volume + "mL", 0, "It's bubbling. Better be careful with self.")
        elif i == 5:
            return Ingredient("NaCl " + volume + "mL", 0, "The vial holds a clear mundane liquid.")
        else:
            return Ingredient("C20H14O4 " + volume + "mL", 0, "The vial holds a funny pink liquid.")
    
    def askToDispense(self):
        GUI.out("You have something to dispense into. Would you like to dispense liquid?")
        return Player.answeredYes(GUI.askChoice(NL + "Dispense a chemical?", YES_NO_P))



class Labo_Distiller(Furniture, Moveable):
    def __init__(self, ID, ID2, tstTube, vial):
        super(Labo_Distiller,self).__init__()

        self.PIPE_ID = ID
        self.TUBE_REF = tstTube
        self.VIAL_REF = vial
        self.FLORENCE_FLASK_REF = Labo_Flask(ID2, self.TUBE_REF, self.VIAL_REF)
        self.HOSE_REF = Labo_Hose()

        self.actDialog = ("There doesn't seem to be much to work on with your hands. You " +
                         "will need some tools to interact with self.")
        self.searchDialog = ("The contraption is comprised of many alchemical components. " +
                            "Though they're alien to you, you note nothing out of the ordinary.")
        self.description = ("It's one half of a larger alchemical contraption in the room. " +
                           "On the table is a metal flask rack and a bunsen burner " +
                           "under it. Above the setup is a curved glass tube connecting it " +
                           "to the condenser on the other side of the table.")

        self.addActKeys("use|distill|boil", "strike", "light")
        self.addNameKeys("distillery?", "(?:bunsen )?burner", "(?:flask )?rack", "distillation tube")
        self.addUseKeys(RUBBER_HOSE, FLORENCE_FLASK, STRIKER, HAND_TORCH, 
                        BEAKER, TEST_TUBE, EMPTY_VIAL, COPPER_POT, COPPER_PAN)
    
    def getDescription(self):
        if Player.getPos().hasFurniture(FLORENCE_FLASK):
            return "The flask now rests nicely on the rack in between the burner and the distillation tube."
        else:
            return self.description
    
    def interact(self, key):
        if key == "strike" or key == "light":
            if Player.hasItem(STRIKER):
                return self.useEvent(Item(STRIKER, 0, ""))
            else:
                return ("You have nothing in your possession to get that task done.")
        else:
            return self.actDialog
    
    def useEvent(self, item):
        name = str(item)

        if name == RUBBER_HOSE:
            Player.getInv().remove(item)
            Player.getPos().addFurniture(self.HOSE_REF)
            return ("You connect the hose to the bunsen burner nozzle and the other end to the gas pipe.")
        elif name == FLORENCE_FLASK:
            Player.getInv().remove(item)
            Player.getPos().addFurniture(self.FLORENCE_FLASK_REF)
            return ("You place the florence flask onto the rack.")
        elif name == HAND_TORCH:
            return ("An ingenious idea by our clever player, " +
                "but the torch's flame is unfortunately too weak for that.")
        elif re.match("beaker|test tube|empty vial|copper pot|copper pan", name):
            return ("That type of vessel was not designed for boiling chemicals! Put it down before you set the room on fire.")
        else:
            p = Player.getPos().getFurnRef(self.PIPE_ID)
                    
            if p.isOn() and Player.getPos().hasFurniture("hose"):
                if Player.getPos().hasFurniture(self.FLORENCE_FLASK_REF.getID()):
                    AudioPlayer.playEffect(45)
                    self.FLORENCE_FLASK_REF.distill()
                    return Furniture.NOTHING
                else:
                    AudioPlayer.playEffect(45)
                    return ("You strike the top of the burner. For a minute, it burns " +
                           "with an intense flame under open space before dying out.")
            elif p.isOn() and not Player.getPos().hasFurniture("hose"):
                AudioPlayer.playEffect(32)
                return ("As you squeeze the striker, a big poof of fire ignites and singes your face. " +
                       "The smell of gas fades momentarily and slowly comes back.")
            else:
                return ("You strike the burner with no effect.")
    
    def moveIt(self):
        return ("The contraption looks pretty fragile. You think it best to leave it where it is.")



class Labo_Flask(SearchableFurniture):
    def __init__(self, ID, tstTb, vial):
        super(Labo_Flask,self).__init__()
        
        self.CNDNSR_ID = ID
        self.TUBE_REF = tstTb
        self.VIAL_REF = vial
        self.description = ("It's an empty glass flask with a bulbous base. This is the choice flask for distillation.")
        self.actDialog = ("There's no reason to do that now.")
        self.searchDialog = ("Here's what you've added.")
        
        # Will accept any ingredient (item with 'mL')
        self.addUseKeys("(?:chilled )?[\\w\\d]+ \\d{1,2}mL")
        
        self.inv = Flsk_Inventory()

        self.addUseKeys(Furniture.ANYTHING) # Anything can be used on this, but it must be of type "ingredient".
        self.addNameKeys("(?:florence |bulbous )?flask")
        self.addActKeys(Furniture.GETPATTERN)
    
    def distill(self):
        c = Player.getPos().getFurnRef(self.CNDNSR_ID)
        
        if not self.inv.isEmpty() and c.condense(self.determineProduct()): 
            self.inv.emptyAndAddResidue()
        elif self.inv.isEmpty():
            GUI.out("You strike the burner, producing an aggressive flame. The " +
                   "flame heats the empty flask for about a minute, yielding " +
                    "no interesting results.")
    
    def determineProduct(self):
        if self.inv.size() == 6 and \
                self.containsItem("chilled Br 10mL") and \
                self.containsItem("vinegar 5mL") and \
                self.containsItem("ae 20mL") and \
                self.containsItem("wine 15mL") and \
                self.containsItem("chilled H2O 30mL") and \
                self.containsItem("H2CO3 35mL"):
            return 1
        else:
            return 0
    
    def getDescription(self):
        if self.inv.size() == 0:
            return self.description
        elif self.inv.size() == 1:
            return ("The glass flask contains " + self.inv.get(0) + ".")
        else:
            return ("The glass flask contains a solution of... stuff.")
    
    def useEvent(self, item):
        Player.getInv().give(item, self.inv)
        return Furniture.NOTHING
    

class Flsk_Inventory(Inventory):
    def __init__(self):
        super(Flsk_Inventory,self).__init__()
    
    def add(self, item):
        if item.getType() == Names.INGREDIENT:
            GUI.out("You pour it in.")
            super(Flsk_Inventory,self).add(item)
            Player.getInv().forceAdd(self.TUBE_REF)
            return True
        else:
            GUI.out("That's not an ingredient!")
            return False
    
    def give(self, item, giveToThis):
        if str(item) == "gray residue":
            self.remove(item)
            giveToThis.add(item) # Residue unneeded. No need to force in.
            GUI.out("You take the residue out.")
            return True
        elif self.size() == 1:
            if giveToThis.contains(str(self.TUBE_REF)):
                self.remove(item)
                giveToThis.remove(self.TUBE_REF)
                giveToThis.forceAdd(item)
                GUI.out("You pour it back out.")
                return True
            elif giveToThis.contains(str(self.VIAL_REF)):
                self.remove(item)
                giveToThis.remove(self.VIAL_REF)
                giveToThis.forceAdd(item)
                GUI.out("You pour it back out.")
                return True
            else:
                GUI.out("You have no vial or test tube to empty it out into. ")
                return False
        else:
            GUI.out("The ingredients are in solution. You can't take it back out.")
            return False
    
    def emptyAndAddResidue(self):
        self.CONTENTS.clear()
        self.CONTENTS.append(Item("gray residue", -50, "It's an awful smelling product of distillation."))



class Labo_GasPipe(Furniture, Unmoveable):
    def __init__(self):
        super(Labo_GasPipe,self).__init__()

        self.gasIsOn = False
        self.description = ("The metal pipe runs from the floor to ceiling in " +
                  "the room's corner. In the middle is a valve and an uncovered nozzle.")
        self.actDialog = ("You turn the valve.")
        self.useDialog = ("You fit the rubber tube over the nozzle tightly and connect the other end to the bunsen burner.")

        self.addNameKeys("(?:metal )?(?:gas )?(?:pipe|valve|nozzle)")
        self.addUseKeys(RUBBER_HOSE)
        self.addActKeys("turn", "rotate", "twist", "spin")
    
    def getDescription(self):
        if Player.getPos().hasFurniture("hose"):
            return ("The metal pipe runs from the floor to ceiling. In the middle is a valve and nozzle connected to a rubber tube.")
        else:
            return self.description
    
    def interact(self, key):
        hoseConnected = Player.getPos().hasFurniture("hose")

        if self.toggleGas(): 
            if self.hoseConnected:
                return (self.actDialog + " You start to hear a hissing noise.")
            else:
                return (self.actDialog + " You turn the valve and begin to smell gas.")
        else:
            if self.hoseConnected:
                return (self.actDialog + " The hissing noise stops.")
            else:
                return (self.actDialog + " Slowly, the gas odor fades away.")
    
    def useEvent(self, item):
        Player.getInv().remove(item)
        Player.getPos().addFurniture(Labo_Hose())
        return self.useDialog
    
    def isOn(self):
        return self.gasIsOn
    
    def toggleGas(self):
        AudioPlayer.playEffect(17)
        self.gasIsOn = not self.gasIsOn
        return self.isOn()



class Labo_Hose(Furniture):
    def __init__(self):
        super(Labo_Hose,self).__init__()

        self.description = ("The yellow rubber hose connects the gas pipe to the bunsen burner.")
        self.addNameKeys("(?:yellow )?(?:rubber )?hose")



"""
    This is furniture found in the laboratory.
    Used to cool down ingredients in the alchemy puzzle.
    Multi-threaded. Runs a thread call Chill_Thread.    
"""
class Labo_IceBarrel(SearchableFurniture, Openable, Unmoveable): 
    def __init__(self, flask):
        super(Labo_IceBarrel,self).__init__()

        DRY_ICE_REF = Item("dry ice", 0, "This stuff is cold! It hurts for you to hold.")
        self.inv = Ice_Inventory([DRY_ICE_REF, DRY_ICE_REF, flask, DRY_ICE_REF, DRY_ICE_REF])
        
        self.description = ("The wooden barrel is wrapped in some kind of foam " +
                  "functioning as insulation. There's some writing on the lid: \"25 seconds.\"")
        self.searchDialog = ("The barrel is filled with dry ice.")

        self.addNameKeys("(?:unusual )?(?:wooden |foam )?barrel")
    


"""
    Chills any chemical if left alone for 25 seconds.
    Uses a hash map to keep track of any active threads. A new thread is
    made whenever an ingredient is added, and threads are canceled when
    ingredients are removed.
"""
class Ice_Inventory(Inventory):
    # Don't want to try to serialize any threads.
    def __init__(self, itemList=[]):
        super(Ice_Inventory,self).__init__(itemList)
        self.THREAD_MAP = {}

    def __getstate__(self):
        self.THREAD_MAP = None
        return self.__dict__

    def add(self, item):
        super(Ice_Inventory,self).add(item)
        
        if not self.THREAD_MAP:
            self.THREAD_MAP = {}
        
        if item.getType() == INGREDIENT:
            # Chills the chemical for a bit, seals off barrel.
            GUI.out("Better give it some time to chill before taking it out.")
            t = Chill_Thread(item, self.CONTENTS)
            self.THREAD_MAP[item] = t
            t.start()

        return True

    def remove(self, removeThis):
        # If player removes ingredient while cooling, interrupts the thread.
        super(Ice_Inventory,self).remove(removeThis)

        if self.THREAD_MAP and (removeThis in self.THREAD_MAP.keys()):
            self.THREAD_MAP.pop(removeThis).interrupt()
            GUI.out("Your impatience has interrupted the cooling.")
    


"""
    Converts chemical into chilled chemicals in 25 seconds.
"""
class Chill_Thread(Thread):
    def __init__(self, item, inv):
        super(Chill_Thread,self).__init__()
        self.setDaemon(True)
        self.CHEMICAL = item
        self.BARREL_INV = inv
        self.cancelled = False

    def interrupt(self):
        self.cancelled = True

    def run(self):     
        time.sleep(25)
        if not self.cancelled:
            self.cancelled = True
            self.addChilledItem()

    def addChilledItem(self):
        if self.BARREL_INV.contains(str(self.CHEMICAL)):
            # If chilled ingredients are chilled, they become "Super chilled")
            # Super chilled ingredients become "Super super chilled".
            prefix = ("super " if re.matches("(?:super|chilled).+", str(self.CHEMICAL)) else "chilled ")
            self.BARREL_INV.remove(self.CHEMICAL)
            self.BARREL_INV.add(Ingredient(prefix + str(CHEMICAL), 0, "The chemical feels cold to the touch."))   



"""
    Player must successfully create a phase door potion to progress in the game.
    The puzzle involves measuring and distilling various ingredient Items.
    
    1. Use florence flask on distiller
    2. Connect hose to gas pipe and turn it on
    3. Open condensing tube
    3.5. Put bromine into barrel, let it chill for 30 seconds.
    4. Titrate and add exactly these 5 ingredients (Use dispensers and burette):
        chilled H2O, 30mL
        chilled bromine, 10mL
        vinegar, 5mL
        aether, 20mL
        wine, 15mL
        carbonic acid, 35mL
    5. Use beaker on condenser
    6. Use striker on the bunsen burner
    7. Take the beaker.
"""
class Labo(Room):
    def __init__(self, name, ID):
        super(Labo,self).__init__(name, ID)

    def triggeredEvent(self):
        if not Player.hasVisited(self.ID):
            GUI.out("As you enter this room, you feel overwhelmed at the sight " +
                     "of many unknown instruments of alchemy.")
            
        return self.NAME



class Labo_Shelf(SearchableFurniture, Openable, Moveable):
    def __init__(self, itemList=[]):
        super(Labo_Shelf,self).__init__(itemList)
        
        self.description = ("The metal shelf holds many different mysterious alchemical ingredients.")
        self.searchDialog = ("You look on the shelves.")
        self.addNameKeys("(?:metal )?shelf")



class Labo_Sink(Furniture):
    def __init__(self, ref1, ref2, ref3, ref4):
        super(Labo_Sink,self).__init__()

        self.isOn = False
        self.BUCKET_REF = ref3
        self.VIAL_REF = ref1
        self.BEAKER_REF = ref2 
        self.WATER_REF = ref4
        
        self.description = ("It's a square metal sink for dumping liquids and hand washing.")
        self.actDialog = ("What a smart idea! You quickly wash your hands before carrying on.")
        self.searchDialog = ("It's a dirty metal sink, and has lost most, if any shine it ever had.")
        self.useDialog = ("You pour it down the drain.")

        self.addNameKeys("(?:square )?(?:metal )?(?:sink|faucet)")
        self.addUseKeys(r"(?:super )*(?:chilled )?[\w\d]+ \d{1,2}mL", 
                        BUCKET_OF_WATER, SPRUCE_EXTRACT, HOLY_WATER,
                        POTION_OF_SCIENCE, PHASE_DOOR_POTION, BOTTLE_OF_WINE,
                        BOTTLE_OF_VINEGAR)
        self.addActKeys("use", "wash", "turn", "run", "activate")
    
    def useEvent(self, item):
        s = str(item)
        
        if s == BOTTLE_OF_VINEGAR or s == PHASE_DOOR_POTION or s == BOTTLE_OF_WINE:
            return ("That would be such a waste!")
        elif s == BUCKET_OF_WATER:
            Player.getInv().remove(item)
            Player.getInv().add(self.BUCKET_REF)
            return self.useDialog
        else:
            Player.getInv().remove(item)
            
            if s == POTION_OF_SCIENCE:
                Player.getInv().add(self.BEAKER_REF)
            else:
                Player.getInv().add(self.VIAL_REF)
            
            return self.useDialog

    def interact(self, key):
        if key == "use" or key == "wash":
            return (self.actDialog if self.isOn else "The sink is off though!")
        else:
            self.isOn = not self.isOn
            
            if self.isOn:
                Player.getPos().addFurniture(self.WATER_REF)
                return ("The sink is now running.")
            else:
                Player.getPos().removeFurniture(self.WATER_REF.getID())
                return ("The sink is now off.")



"""
    This is used to resolve ambiguity since there are multiple stopcocks in the 
    room for the player to turn.    
"""
class Labo_StopCock(Furniture):
    def __init__(self):
        super(Labo_StopCock,self).__init__()

        self.actDialog = ("Both the dispensers and the burette have a stopcock. " +
                         "State 'burette stopcock' or 'dispenser stopcock'.")
        self.description = ("They are small turnable switches for operating titrating instruments. " + 
                        self.actDialog)
        self.searchDialog = self.actDialog

        self.addNameKeys("stopcocks?")
        self.addActKeys("use", Furniture.VALVEPATTERN, "dispense", "drain")



class Labo_Table(Furniture, Moveable):
    def __init__(self):
        super(Labo_Table,self).__init__()

        self.description = ("The small black table in the center of the room supports the burette on top.")
        self.actDialog = ("There's fragile stuff on top. Better not do that!!")
        self.searchDialog = ("Nothing but a burette on top")
        
        self.addNameKeys("(?:small )?(?:black )?table")
        self.addActKeys("kick|nudge|jostle")



"""
    Allows player to select a specific number, representing volume of a titrated
    chemical, incremented by 5 every 2.5 seconds in a thread.
"""
class TitrationTask(Thread):
    def __init__(self):
        self.volume = 0
        self.cancelled = False

    def run(self):
        while not self.cancelled and volume <= 50:
            volume += 5
            GUI.out("Amount dispensed: " + str(volume) + "mL.")
            time.sleep(1)

    def interrupt(self):
        self.cancelled = True
        return self.volume
    
    @staticmethod
    def titrate():
        task = TitrationTask()
        task.start()
        GUI.promptOut()
        return task.interrupt()
