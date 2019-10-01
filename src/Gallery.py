from Furniture import *
from GUI import GUI
import Id, Menus, Direction, MachineColor, AudioPlayer
from Inventory import Inventory
from Names import *
from Patterns import GAL_TOTEM_ONE_TO_FOUR, YES_NO_P
from Things import Carpet, Statue, Fireplace, WallArt
from Structure_gen import Door, Balcony, Staircase, Column
import re, random, time
from threading import Thread
from Mechanics import Lever, Button
from Cellar import Cel5_Lock
from Item import BreakableItem, Item, Weapon
from Room import Room
from Player import Player



"""
    A part of a puzzle in the gallery that emits colors of light depending on
    combinations of lenses that are put into it.
    
    Interacts with the statue in the central chamber.
"""
class Gal_LightMachine(SearchableFurniture):
    def __init__(self):
        super(Gal_LightMachine,self).__init__()
        self.on = False
        self.beam = MachineColor.COLOR_MAP[0b0000]
        self.addUseKeys(RED_FOCUS, BLUE_FOCUS, YELLOW_FOCUS, DARK_FOCUS)

    def determineColor(self):
        color = 0
        
        for i in self.inv:
            if str(i) == RED_FOCUS:
                color |= 0b0100
            elif str(i) ==  BLUE_FOCUS:
                color |= 0b0010
            elif str(i) ==  YELLOW_FOCUS:
                color |= 0b0001
            elif str(i) ==  DARK_FOCUS:
                color |= 0b1000

        self.beam = MachineColor.COLOR_MAP[color]

    def isOn(self):
        return self.on

    def getBeam(self):
        return self.beam

    def useEvent(self, item):
        Player.getInv().give(item, self.inv)
        return self.useDialog



class Gal1_Armor(Furniture):
    def __init__(self):
        super(Gal1_Armor,self).__init__()

        self.description = ("You know a set of samurai armor when you see one. " +
                           "This set is mostly black and brown with gold plating " +
                           "on the helmet. Not as colorful as what you've seen " +
                           "before, but this must be the functional kind.")
        self.searchDialog = ("You find many little intricate parts to this piece, " +
                            "but nothing removable.")
        self.actDialog = ("You will probably get hurt trying to do that.")
        self.addActKeys("wear", "equip")
        self.addNameKeys("samurai armor", "armor suit", "(?:suit )?armor") 



"""
    One of two object which turn on the GAL1 Dragon    
"""
class Gal1_Button(Button):
    def __init__(self, ID):
        super(Gal1_Button,self).__init__()
        self.actDialog = ("You press the button. ")
        self.DRAGON_ID = ID 

    def event(self, key):
        d = Player.getRoomObj(Id.GAL1).getFurnRef(self.DRAGON_ID)
        return self.actDialog + d.switchEye(0)



"""
    One of four elements of the light machine puzzle in the gallery.
    Foci must be added to this in the correct order while the statue is holding
    the funny orb in order to raise the statue to the next level.
"""
class Gal1_Dragon(Gal_LightMachine):
    def __init__(self, ID, yellowFocus):
        super(Gal1_Dragon,self).__init__()

        self.searchDialog = ("The only place to search is the dragon's mouth.")
        self.turnOffDialog = ("The light in the dragon's mouth shuts off.")
        self.description = ("The room's most prominent piece is this detailed " +
                           "dark green dragon statue. It looks original to east " +
                           "Asia. Its serpent-like body twists around and it stares menacingly ")
        self.EYES = [False, False]
        self.GAL2_STAT_ID = ID
        self.addNameKeys("snake-like dragon(?: statue)?", "(?:dragon|statue)", "(?:dragon's |statue's )?mouth")
        self.inv = Drgn_Inv(self, yellowFocus)    

    def getDescription(self):
        if self.isOn: 
            return (self.description + "with its two eyes lit. A light from within " +
                                 "the dragon shines brightly through its mouth.")
        elif self.EYES[0] and not self.EYES[1]:
            return (self.description + "at the statue in the central chamber. " +
                                  "Its left eye glows brightly from an unknown source.")
        elif not EYES[0] and EYES[1]:
            return (self.description + "at the statue in the central chamber. " +
                                  "Its right eye glows brightly from an unknown source.")
        else:
            return (self.description + "with cold eyes at the statue in the central chamber. " +
                      "Careful inspection reveals two wires coming out the back. One leads " +
                      "behind the screen, the other behind the scroll.")

    def switchEye(self, i):
        # 0 is left, 1 is right
        self.EYES[i] = not self.EYES[i]
        eye = ("left" if (i == 0) else "right")
        
        rep = ("The dragon's " + eye + " eye lights up. " if self.EYES[i] else \
                               "The glow in the dragon's " + eye + " eye fades. ")
        
        if self.EYES[0] and self.EYES[1]:
            return rep + self.turnOn()
        elif self.isOn:
            return rep + self.turnOff()
        else:
            return rep

    def turnOn(self):
        self.determineColor()
        self.isOn = True       
        s = Player.getRoomObj(Id.GAL2).getFurnRef(self.GAL2_STAT_ID)
        return self.beam + " emits from the dragon's mouth. " + s.activate(self.beam)

    def resetStatue(self):
        Player.getRoomObj(Id.GAL2).getFurnRef(self.GAL2_STAT_ID).reset()



class Drgn_Inv(Inventory):
    def __init__(self, ref, yellowFocus):
        super(Drgn_Inv,self).__init__([yellowFocus])
        self.DRAGON_REF = ref
    
    def add(self, item): 
        if item.getType() == Names.FOCUS:
            AudioPlayer.playEffect(43)
            super(Drgn_Inv,self).add(item)
            
            if self.DRAGON_REF.isOn():
                self.trigger()
            else:
                GUI.out("You place the " + str(item) + " into the dragon's mouth.")
            
            return True
        else:
            GUI.out("It doesn't seem like that belongs there.")
            return False
    
    def remove(self, removeThis):
        super(Drgn_Inv,self).remove(removeThis)
        
        if self.DRAGON_REF.isOn():
            self.trigger()
    
    def trigger(self):
        self.DRAGON_REF.determineColor()
        s = Player.getRoomObj(Id.GAL2).getFurnRef(self.DRAGON_REF.GAL2_STAT_ID)
        GUI.out(beam + " emits from the dragon's mouth. " + s.activate(beam))



class Gal1_Hearth(Fireplace):
    def __init__(self, ref):       
        super(Gal1_Hearth,self).__init__(ref)

        self.descLit = ("The small hearth is tiled green and purple like the rest of the room.")



"""
    A sword which can be taken off the wall.
    When this is taken, this removes itself from the room and adds itself to
    the player's inventory. Can be used to cut the rope in Gal3.    
"""
class Gal1_KatanaFurniture(Furniture):
    def __init__(self):
        super(Gal1_KatanaFurniture,self).__init__()

        self.description = ("The black katana looks exceptionally sharp.")
        self.actDialog = ("You take the katana off its display.")
        
        self.addActKeys(Furniture.GETPATTERN, "wield")
        self.addNameKeys("(?:black )?(?:katana|sword)")

    def interact(self, key): 
        if Player.getInv().add(Weapon("katana", 80)):
            Player.getPos().removeFurniture(self.getID())
            return self.actDialog
        else:
            return Furniture.NOTHING



class Gal1_Lights(Furniture):
    def __init__(self):
        super(Gal1_Lights,self).__init__()

        self.description = ("These lights are electric. Your assumption is that " +
                           "this is a newer wing of the castle.")
        self.actDialog = ("Ow! It's not fire, but it's still hot!")
        self.addActKeys(Furniture.HOLDPATTERN)
        self.addNameKeys("(?:electric )?lights?")



class Gal1_Painting1(WallArt):
    def __init__(self):
        super(Gal1_Painting1,self).__init__()
        self.description = ("This painting is highly detailed and colorful. " +
                           "Painted on it are many different colored Hindu " +
                           "deities playing musical instruments. One of them " +
                           "riding in a chariot resembles an elephant.")
        self.addNameKeys("indian painting")



class Gal1_Painting2(WallArt):
    def __init__(self):
        super(Gal1_Painting2,self).__init__()
        self.description = ("This one is painted in all blue and outlined in white. " +
                           "A furious godly figure stands in the middle and appears " +
                           "to be burning. The rest of this painting illustrates the " +
                           "elements water and fire decoratively.")
        self.addNameKeys("tibetan painting")



class Gal1_Painting3(WallArt):
    def __init__(self):
        super(Gal1_Painting3,self).__init__()
        self.description = ("This one depicts a nocturnal landscape. It's painted " +
                           "in mostly a blue-green with trees accented in orange. " +
                           "The black outlining is prominent.")
        self.addNameKeys("korean painting")



class Gal1_Paintings(Furniture):
    def __init__(self):
        super(Gal1_Paintings,self).__init__()
        
        self.description = ("You quickly browse around the paintings in the room. " +
                           "You find:\t\t\t" +
                           "<> A Tibetan painting\t\t" +
                           "<> An Indian painting\t\t" +
                           "<> A Korean painting\t\t" +
                           "<> A Chinese scroll")
        self.searchDialog = ("You aren't sure which one to search first.")
        self.actDialog = ("You aren't sure which one to move.")
        self.addActKeys(Furniture.GETPATTERN)
        self.addActKeys("move", "lift", "slide")
        self.addNameKeys("painting", "paintings")



"""
    Contains the GAL1 dragon which is a light machine interacted with in the
    gallery light machine puzzle.
    Connects to Gal2 and Foyc    
"""
class Gal1(Room):
    def __init__(self, name, ID):
        super(Gal1,self).__init__(name, ID)

    def getDescription(self):
        if not self.hasFurniture("katana"):
            return super(Gal1, self).getDescription().replace("A katana is displayed " +
                                "over a hearth on the south wall and an armor suit " +
                                "against the north wall", 
                                    "A hearth rests against the south wall and an armor suit is north", 1)
        else:
            return super(Gal1, self).getDescription()



"""
    Hides a lever which must be pulled to turn on the GAL1 Dragon.    
"""       
class Gal1_Screen(Furniture):
    def __init__(self, ref):
        super(Gal1_Screen,self).__init__()

        self.REF = ref
        self.description = ("The four-paneled Japanese screen sits in the corner " +
                           "of the room. A panorama is hand-drawn on it. Its " +
                           "delicate black lines depict a mountain front landscape.")
        self.searchDialog = ("The light shining through this screen forms an odd " +
                            "silhouette on its surface.")
        self.actDialog = ("You slide the screen out of the way some, revealing a " +
                        "large black lever mounted to the floor.")
        self.addActKeys(Furniture.MOVEPATTERN, Furniture.GETPATTERN)
        self.addNameKeys("(?:japanese )?screen")

    def interact(self, key):     
        if not Player.getPos().hasFurniture(self.REF.getID()):
            AudioPlayer.playEffect(41)
            Player.getPos().addFurniture(self.REF)
            return self.actDialog
        else:
            return ("You have already moved the screen.")



"""
    Hides a button which is pushed to turn on the GAL1 dragon.
"""
class Gal1_Scroll(Furniture):
    def __init__(self, ref):
        super(Gal1_Scroll,self).__init__()

        self.BTTN_REF = ref
        self.description = ("The hanging scroll is ink drawn in black on an " +
                           "orange-stained parchment. It depicts a few scraggly " +
                           "trees in front of a mountain range. At the top, " +
                           "something is written in a foreign language. The " +
                           "light is hitting this piece strangely.")
        self.searchDialog = ("There is something odd about the light hitting this scroll.")
        self.actDialog = ("Upon lifting the scroll from the wall, you discover a " +
                      "hollow containing a dome-shaped button.")
        self.addActKeys(Furniture.MOVEPATTERN, Furniture.GETPATTERN)
        self.addNameKeys("(?:hanging )?(?:chinese )?scroll")

    def interact(self, key):     
        if not Player.getPos().hasFurniture(self.BTTN_REF.getID()):
            Player.getPos().addFurniture(self.BTTN_REF)
            return self.actDialog
        else:
            return ("You have already moved it!")



class Gal1_Sculptures(Furniture):
    def __init__(self):
        super(Gal1_Sculptures,self).__init__()
        
        self.description = ("You quickly browse around the sculptures in the room. You find: " +
                           "\t\t\t<> A dragon " +
                           "\t\t\t<> A screen " +
                           "\t\t\t<> Some armor ")
        self.searchDialog = ("You aren't sure which one to search first.")
        self.addNameKeys("sculptures?")



"""
    One of two object which turn on Gal1 Dragon    
"""        
class Gal1_Switch(Lever):
    def __init__(self, ID):
        super(Gal1_Switch,self).__init__()
        
        self.description = ("It's a large black lever on the floor")
        self.actDialog = ("You pull the lever. ")
        self.DRAGON_ID = ID 
        self.addNameKeys("(?:large )?(?:black )?lever")

    def event(self, key):
        d = Player.getRoomObj(Id.GAL1).getFurnRef(self.DRAGON_ID)
        return self.actDialog + d.switchEye(1)



class Gal2_Columns(Column):
    def __init__(self):
        super(Gal2_Columns,self).__init__()

        self.description = ("These columns are clean white stone. They're Greek Ionic.")
        self.addNameKeys("columns?")



class Gal2_Machine(SearchableFurniture, Openable):
    def __init__(self, itemList=[]):
        super(Gal2_Machine,self).__init__()

        self.inv = Machine_Inventory(self, itemList)
        self.pluggedIn = True
        self.moved = False
        
        self.NOT_MOVED = ("The machine rests flush against the wall and hides any existing outlet.")
        self.useDialog = ("Hitting the machine only sends a sharp current of electricity through your body.")
        self.searchDialog = ("As you touch the front handle, a strong electrical " +
                          "current propels up your arm. You yank your hand back.")
        self.description = ("The small machine rests % and appears to be a " +
                "short black metal box, waist-high, with a front door " +
                "and handle. The front and top are metal, but the sides are rubber. &")
        self.actDialog = ("With bear-like strength, you push against the heavy " +
                         "machine and succeed in moving it a small amount. " +
                         "A plugged-in outlet reveals itself behind the machine.")
        
        self.addUseKeys(Furniture.ANYTHING)
        self.addActKeys(Furniture.MOVEPATTERN, Furniture.HOLDPATTERN,"(?:un)?plug", "turn", "fix|repair")
        self.addNameKeys("(black )?(?:metal )?(?:box|machine|handle)")

    def getDescription(self):
        result = self.description
        
        result = result.replace("%", 
            ("to the side revealing an outlet on the wall." if self.moved else "flush against the wall."), 1)
        
        return result.replace("&", 
            ("Many lights blink on its surface and electrical arcs jump between two metal rods protruding from the top." \
                if self.pluggedIn else "The lights and electrical arcs have stopped."), 1)

    def interact(self, key):
        if key == "unplug":
            if self.moved:
                result = ("You pull the cord and cease the machine's shenanigans." \
                    if self.pluggedIn else "The machine is already unplugged!")
                self.pluggedIn = False
                return result
            else:
                return self.NOT_MOVED
        elif key == "plug":
            if self.moved:
                result = ("The machine is already plugged in!" if self.pluggedIn else "You plug back in the machine.")
                self.pluggedIn = True
                return result
            else:
                return self.NOT_MOVED
        elif key == "fix" or key == "repair":
            return ("You are by no means a mechanic.")
        elif key == "turn":
            return ("There is no visible off switch on this thing.")
        elif self.moved:
            return ("You have already moved the machine as far as you can.")
        else:
            self.moved = True
            AudioPlayer.playEffect(41)
            self.addNameKeys("outlet")
            return self.actDialog

    def getSearchDialog(self):
        self.searchable = Player.hasItem(WORK_BOOTS) or Player.hasItem(RUBBER_GLOVES) or not self.pluggedIn
        
        if not self.pluggedIn:
            return ("With the machine unplugged, you succeed in opening the machine door.")
        else:
            return ("With the provided insulation, you succeed in opening the machine door." \
                if self.searchable else self.searchDialog)

    def useEvent(self, item):
        name = str(item)
        
        if name == HAND_DRILL or name == SCREWDRIVER:
            return ("So you're a mechanic now?")
        elif item.getType() == WEAPON:
            if Player.hasItem(WORK_BOOTS) or Player.hasItem(RUBBER_GLOVES) or not self.pluggedIn:
                return ("Attempts to savagely smash the machine yield no progress forward.")
            else:
                return self.useDialog
        elif name == BUCKET_OF_WATER:
            return "Whoa there... do you have a death wish?" if self.pluggedIn else Furniture.DEFAULT_USE
        else:
            return Furniture.DEFAULT_USE


class Machine_Inventory(Inventory):
    def __init__(self, ref, itemList=[]):
        super(Machine_Inventory,self).__init__(itemList)
        self.MACH_REF = ref

    def add(self, item):
        self.MACH_REF.searchable = \
            Player.hasItem(WORK_BOOTS) or Player.hasItem(RUBBER_GLOVES) or not self.MACH_REF.pluggedIn
        
        if self.MACH_REF.searchable:
            return super(Machine_Inventory,self).add(item)
        else:
            GUI.out(self.MACH_REF.searchDialog)
            return False



class Gal2_Staircase(Staircase):
    def __init__(self, direction, dest):
        super(Gal2_Staircase,self).__init__(direction, dest, 14)
        self.description = ("The dark wooden stairs curve following the edge of " +
                           "the balcony until meeting it on the second floor.")



"""
    Part of the light puzzle.
    Player must use the crystal orb on self.    
"""
class Gal2_Statue(SearchableFurniture):
    def __init__(self, ref):
        super(Gal2_Statue,self).__init__()
        
        self.inv = Stat_Inv(self)
        self.REF3 = ref
        self.level = 0
        self.description = ("The grandiose statue stands in the exact center of " +
                           "the circular room. It portrays a male figure. He " +
                           "poises elegantly, with his right arm extended over " +
                           "his head and left hand held low as if bearing an " +
                           "object, though it's empty.")
        self.searchDialog = ("The statue's hand is empty.")
        self.useDialog = ("You set the orb in the statue's palm. ")
        self.addNameKeys("(?:grandiose )?statue", "(?:statue(?:'s)? )?(?:hand|palm)")
        self.addUseKeys(CRYSTAL_ORB)

    def getState(self):
        return self.level

    def activate(self, color):
        if self.containsItem(CRYSTAL_ORB) and level != 3:
            if (color == MachineColor.COLOR_MAP[0b0100] and self.level == 0) or \
                    (color == MachineColor.COLOR_MAP[0b0110] and self.level == 1) or \
                    (color == MachineColor.COLOR_MAP[0b1110] and self.level == 2):
                return self.rise() 
            elif self.level == 0:
                return ("The beam of light shines into the orb with no effect.")
            elif self.level == 1 or self.level == 2:
                self.level = 0
                return ("The orb's hum dies and its glow fades.")
        elif not self.containsItem(CRYSTAL_ORB):
            self.level = 0
            return ("The beam of light shines at the statue in the central chamber.")
        elif self.level == 3:
            return ("The beam shines at the statue's risen base.")
        
        return ("The orb sits comfortably in the statue's palm.")

    def rise(self):
        if self.level == 0:
            return ("The crystal orb in the statue's palm begins to glow red.")
        elif self.level == 1: 
            return ("The orb starts to hum louder and its glow turns purple.")
        else:
            self.searchable = False
            Player.getRoomObj(Id.GAL4).addFurniture(self.REF3)
            AudioPlayer.playEffect(37)
            return ("The orb's glow turns a dark purple before fading into " +
                  "ultraviolet. The statue raises on its platform to the second floor.")

        self.level += 1

    def getDescription(self):
        if self.containsItem(CRYSTAL_ORB):   
            if self.level == 0: 
                return ("The statue now stands holding the glinting crystal orb.")
            elif self.level == 1:
                return ("The statue stands holding the glowing orb. It hums softly.")
            elif self.level == 2:
                return ("The statue stands holding the glowing orb. It's humming quite loudly now.")
            else:
                return ("The statue has risen up to the next floor. Its tall base " +
                        "is all that's left on this level.")
        else:
            return self.description

    def getSearchDialog(self):
        if self.searchable and self.containsItem(CRYSTAL_ORB):
            return self.searchDialog + "The statue stands bearing the crystal orb."
        elif not self.searchable:
            return self.searchDialog + "The statue's palm is now out of reach."
        else:
            return self.searchDialog 

    def useEvent(self, item):
        Player.getInv().give(item, self.inv)
        return Furniture.NOTHING

    def addDragonRef(self, dragon):
        self.inv.DRGN_ID = dragon.getID()

    def reset(self):
        if self.level <= 2:
            self.level = 0
    

class Stat_Inv(Inventory):
    def __init__(self, ref, itemList=[]):
        super(Stat_Inv,self).__init__(itemList)
        self.DRGN_ID = None
        self.STAT_REF = ref
    
    def add(self, item):
        if str(item) == CRYSTAL_ORB:
            drgn = Player.getRoomObj(Id.GAL1).getFurnRef(DRGN_ID)
            super(Stat_Inv,self).add(item)
            
            if drgn.isOn():
                GUI.out(self.STAT_REF.useDialog + self.STAT_REF.activate(drgn.getBeam()))
            else:
                GUI.out(self.STAT_REF.useDialog)
            
            return True
        else:
            GUI.out("The statue isn't supposed to be holding that.")
            return False
    
    def remove(self, removeThis):  
        super(Stat_Inv, self).remove(removeThis)
        drgn = Player.getRoomObj(Id.GAL1).getFurnRef(DRGN_ID)
        
        if drgn.isOn():
            GUI.out(activate(drgn.getBeam()))



class Gal3_Artifact1(Statue):
    def __init__(self):
        super(Gal3_Artifact1,self).__init__()

        self.description = ("The small statuette stands on a pedestal in the room's " +
                           "center. It resembles a ravenous humanoid with lifeless " +
                           "eyes. Next to it, a small label reads: \"Yombe\".")
        self.addNameKeys("statuette", "zambian statuette")



class Gal3_Artifact2(Statue):
    def __init__(self):
        super(Gal3_Artifact2,self).__init__()

        self.description = ("In the corner of the room stands this odd statue. " +
                           "It resembles a human, but barely. All you can make " +
                           "out are two shoulders and a deformed face with no " +
                           "features apart from a couple ears.")
        self.addNameKeys("statue", "deformed statue")



class Gal3_Artifact3(Statue):
    def __init__(self):
        super(Gal3_Artifact3,self).__init__()

        self.description = ("It's a small terracotta statue. It depicts a sitting " +
                           "female with large lips, wide open eyes, and detailed " +
                           "hair. Next to it, a small label reads: \"Nok\".")
        self.addNameKeys("trinket", "nigerian trinket")



class Gal3_Artifacts(Furniture):
    def __init__(self):
        super(Gal3_Artifacts,self).__init__()

        self.description = ("You quickly browse around the artifacts in the room. " +
                           "You find:\t\t\t" +
                           "<> A Zambian statuette\t\t" +
                           "<> A deformed statue\t\t" +
                           "<> A Nigerian trinket")
        self.searchDialog = ("You aren't sure which one to search first.")
        self.addNameKeys("artifacts?", "statues?")



class Gal3_Hatch(Furniture):
    def __init__(self):
        super(Gal3_Hatch,self).__init__()

        self.description = ("The hatch leads upwards into another room.")
        self.actDialog = ("The hatch is open already.")
        
        self.addNameKeys("hatch")
        self.addActKeys("open", "close", "jump")

    def interact(self, key):
        if key == "open":
            return self.actDialog
        elif key == "jump":
            return ("The hatch is going upward you fool...")
        else:
            return ("The hatch is too high up. Why do that anyway???")



class Gal3_Hearth(Fireplace):
    def __init__(self, ref):       
        super(Gal3_Hearth,self).__init__(ref)

        self.descLit = ("The small hearth is made of a yellow plaster.")



class Gal3_Hole(Furniture):
    def __init__(self):
        super(Gal3_Hole,self).__init__()

        self.description = ("The rope feeds into the small hole. Around the hole " +
                           "is a metal lip. This was likely installed recently.")
        self.searchDialog = ("You peek into the hole, and see only the rope fade into the dark.")
        self.addNameKeys("hole")



class Gal3_KoraFurniture(Furniture): 
    def __init__(self):
        super(Gal3_KoraFurniture,self).__init__()

        self.description = ("You've never seen anything like this before. You'd " +
                           "call it a guitar, but then again, it looks like a " +
                           "harp too. Beneath it you see a small label: \"Kora\".")
        self.actDialog = ("You carefully remove the instrument from its display.")
        self.addNameKeys("(?:stringed )?instrument", "kora")
        self.addActKeys(Furniture.GETPATTERN, "hold", "play", "strum")

    def interact(self, key): 
        if re.match("strum|play", key):
            return ("You would try, but it's up on the wall right now.")
        else:
            if Player.getInv().add(Gal3_Inst("kora")):
                Player.getRoomObj(Id.GAL3).removeFurniture(self.getID())
                return self.actDialog
            else:
                return Furniture.NOTHING



class Gal3_Inst(Item):
    def __init__(self, name):
        super(Gal3_Inst,self).__init__(name, 30)
        self.useID = 1
        self.description = ("The exotic instrument consists of a half-sphere for " +
                           "a body and a long neck. But it resembles a harp more " +
                           "than a guitar or cello.")
        self.useDialog = ("You give it a strum. 'Sounds terrible!' you think, " +
                         "although you've never played a kora before. The sound " +
                         "itself is actually quite nice, like that of a " +
                         "classical guitar.")



class Gal3_Ladder(Staircase):
    def __init__(self):
        super(Gal3_Ladder,self).__init__(Direction.UP, Id.GAL6, 16)

        self.description = ("The ladder is suspended above the ground in the hatch, too high to grab hold of.")
        self.lowered = False
        self.NAMEKEYS = []
        self.addNameKeys("ladder")

    def getDescription(self):
        return (self.description if not self.lowered else \
            "With the rope cut, the ladder now gives way to the gallery loft.")

    def lower(self):
        self.lowered = True

    def interact(self, key):     
        if self.lowered:
            return super(Gal3_Ladder, self).interact(key)
        else:
            return ("The ladder is too high up to climb.")



class Gal3_Mask1(WallArt):
    def __init__(self):
        super(Gal3_Mask1,self).__init__()
        self.description = ("This mask freaks you out. It is uncannily long with " +
                           "a slender nose almost reaching its chin. It has no " +
                           "mouth and only two tiny eye holes.")
        self.addNameKeys("gabonese mask")



class Gal3_Mask2(WallArt):
    def __init__(self):
        super(Gal3_Mask2,self).__init__()
        self.description = ("This mask has an interesting comb structure on top. " +
                           "It has no mouth, but a long slender nose. Below, you " +
                           "see a small label: \"Bambara\".")
        self.addNameKeys("malian mask")



class Gal3_Mask3(WallArt):
    def __init__(self):
        super(Gal3_Mask3,self).__init__()
        self.description = ("This mask has an avian appearance. It has a long beak, " +
                           "but it bears two horns as well. Below, there is a " +
                           "small label: \"Mossi\".")
        self.addNameKeys("burkinabe mask")



class Gal3_Masks(Furniture):
    def __init__(self):
        super(Gal3_Masks,self).__init__()
        self.description = ("You quickly browse around the masks in the room. " +
                           "You find:\t\t\t\t" +
                           "<> A Malian mask\t\t" +
                           "<> A Burkinabe mask\t\t" +
                           "<> A Gabonese mask")
        self.searchDialog = ("You aren't sure which one to search first.")
        self.actDialog = ("You aren't sure which one to move.")
        self.addActKeys(Furniture.GETPATTERN)
        self.addActKeys("move", "lift", "slide", "wear")
        self.addNameKeys("masks?")

    def interact(self, key):
        if key == "wear":
            return ("What point would wearing them serve?")
        else:
            return self.actDialog



class Gal3_Peg(Furniture):
    def __init__(self, ID):
        super(Gal3_Peg,self).__init__()
        self.GAL3_TTM_ID = ID
        self.description = ("The pegs stick out the sides of each segment. " +
                           "Interesting- there is a seam between each segment.")
        self.addActKeys("turn", Furniture.MOVEPATTERN)
        self.addNameKeys("pegs?")

    def interact(self, key):
        return Player.getRoomObj(Id.GAL3).getFurnRef(GAL3_TTM_ID).interact(key)



class Gal3(Room):
    def __init__(self, name, ID, ref):
        super(Gal3,self).__init__(name, ID)
        self.ROPE = ref

    def getDescription(self):
        if self.ROPE.isCut(): 
            return super(Gal3, self).getDescription().replace(" and is suspended above the floor by a rope holding it up", "", 1)
        else:
            return super(Gal3, self).getDescription()



class Gal3_Rope(Furniture):
    def __init__(self, ID):
            super(Gal3_Rope,self).__init__()
            self.cut = False
            self.LDDR_ID = ID
            
            self.actDialog = ("You cut the rope. The ladder drops down into the room, giving access to the loft.")
            self.description = ("The rope is tied to the ladder and hoists it up " +
                               "with a pulley. It feeds into a hole in the wall " +
                               "next to you. Above the hole, you see a switch.")
            self.searchDialog = ("It's just an ordinary rope.")
            
            self.addActKeys("cut", "pull", "untie")
            self.addUseKeys("katana", "(?:silver|rusty|broken) sword", "(?:war|battle) ax")
            self.addNameKeys("rope")

    def getDescription(self):
        return ("The rope is now cut." if self.cut else self.description)

    def interact(self, key): 
        if not self.cut:
            if key == "cut":
                if self.detectItem():
                    Player.getPos().getFurnRef(self.LDDR_ID).lower()
                    self.cut = True
                    Player.describeRoom()
                    return self.actDialog
                else:
                    return ("You have nothing to cut the rope with.")
            elif key == "pull":
                return ("The rope doesn't budge.")
            else:
                return ("The knot in the rope is too high up to untie.")
        else:
            return ("The rope is cut already.")

    def useEvent(self, item):
        Player.getPos().getFurnRef(self.LDDR_ID).lower()
        self.cut = True
        
        return ("You cut the rope with the " + item + ". " +
               "The ladder drops down into the room, " +
               "giving access to the loft.")

    def detectItem(self):
        # Detects if you have a blade to cut the rope with.
        item = Player.getInv().get("katana|.+(?:sword|ax)")
        return item != Inventory.NULL_ITEM

    def isCut(self):
        return self.cut



class Gal3_Segment(Furniture):
    def __init__(self, ID):
        super(Gal3_Segment,self).__init__()
        self.GAL3_TTM_ID = ID
        self.searchDialog = ("The segments aren't hiding any items. You notice a seam between each.")
        self.description = ("The faces on each segment are surreal and spooky. Seams separate the four of them slightly.")
        self.addActKeys(Furniture.VALVEPATTERN, "pull", "move")
        self.addNameKeys("segments?")

    def interact(self, key):
        return Player.getRoomObj(Id.GAL3).getFurnRef(self.GAL3_TTM_ID).interact(key)


        
class Gal3_Switch(Lever):
    def __init__(self):
        super(Gal3_Switch,self).__init__()
        
        self.description = ("It's a small metal switch.")
        self.actDialog = ("To your displeasure, flicking the switch does nothing. " +
                      "'Maybe this pulley mechanism is broken,' you wonder. " +
                      "'It wouldn't be the only broken thing in this castle...'")

        self.addNameKeys("(?:metal )?switch")

    def event(self, key):
        return self.actDialog



"""
    One of four components of the light machine puzzle in the gallery.
    Uses bit operations to spin heads just for the heck of it. Used to be
    an array of booleans.    
"""
class Gal3_Totem(Gal_LightMachine):
    def __init__(self, ID):
        super(Gal3_Totem,self).__init__()

        self.searchable = False
        self.GAL4_STAT_ID = ID
        self.heads = 0
        self.searchDialog = ("The only place to search is the totem's open third mouth. ")
        self.turnOffDialog = ("The lights in the totem's eyes and mouth fade.")
        
        self.addActKeys("turn", "spin", "twist")
        self.addUseKeys(RED_FOCUS, BLUE_FOCUS, YELLOW_FOCUS, DARK_FOCUS)
        self.addNameKeys("totem", "wood totem", "wooden totem")
        self.inv = Ttm_Inv(self)       

    def getDescription(self):
        return ("The tall wooden totem stands back against the west " +
               "wall facing the central chamber. Its four stacked " +
               "segments are carved to resemble obscure faces. " + self.numBackwards() +
               " On each side of the segments is a peg sticking out.")

    def numBackwards(self):
        temp = self.heads
        numBackward = 4
        
        while not temp == 0:
            # Counts the number of 1 bits in HEADS.
            if temp & 1 == 0b0001:
                numBackward -= 1

            temp >>= 1 
        
        if self.numBackward == 0:
            return ("All of them face forward. From the third shines a light.")
        elif self.numBackward == 1:
            return ("One of them faces back towards the wall.")
        elif self.numBackward == 2:
            return ("Two of them face back towards the wall.")
        elif self.numBackward == 3:
            return ("Three of them face back towards the wall.")
        else:
            return ("All of them face back towards the wall.")

    def getSearchDialog(self):
        if not self.searchable:
            return self.searchDialog + "That head is now facing towards the wall."
        else:
            return self.searchDialog

    def interact(self, key):  
        result = Furniture.NOTHING
        h1 = h2 = h3 = h4 = None
        
        while True:
            h1 =      ("~[-_-]~  4"   if (self.heads & 1) == 1 else      "~[   ]~  4")
            h2 = ("\t   ~[\"o\"]~  3" if (self.heads & 2) == 2 else "\t   ~[   ]~  3")
            h3 = ("\t   ~[=_=]~  2"   if (self.heads & 4) == 4 else "\t   ~[   ]~  2")
            h4 = ("\t   ~[-_-]~  1"   if (self.heads & 8) == 8 else "\t   ~[   ]~  1")
        
            GUI.out("           " + h1 + "       \t" + h2 + "\t\t" + 
                       h3 + "\t\t" + h4 + "\t\t\t\t\t\t" + result)
        
            action = GUI.askChoice(Menus.GAL_TOTEM, GAL_TOTEM_ONE_TO_FOUR)
        
            if action:
                self.turnHead(int(action))
                result = self.check()
            else:
                break
        
        return Furniture.NOTHING

    def check(self):
       if self.heads == 0b1111: 
           return self.turnOn()
       elif self.isOn():
           return self.turnOff()
       else:
           return Furniture.NOTHING

    def turnHead(self, head):
        AudioPlayer.playEffect(44)

        if head == 1:
            self.heads ^= 0b1010 # Switch 1 and 3
        elif head == 2:
            self.heads ^= 0b0111 # Switch 2, 3, and 4
        elif head == 3:
            self.heads ^= 0b1011 # Switch 1, 3, and 4
        else:
            self.heads ^= 0b0011 # Switch 3 and 4
        
        self.searchable = (self.heads & 0b0010) == 0b0010

    def turnOn():
        self.determineColor()
        self.isOn = True       
        s = Player.getRoomObj(Id.GAL4).getFurnRef(GAL4_STAT_ID)
        r = ("The totem's eyes begin to glow. " + beam +
               " emits from the totem's third mouth. ")
        
        return ((r + s.activate(beam)) if s else r)

    def resetStatue(self):
        s = Player.getRoomObj(Id.GAL4).getFurnRef(GAL4_STAT_ID)
        
        if s:
            s.reset()
    

class Ttm_Inv(Inventory):   
    def __init__(self, ref):
        super(Ttm_Inv,self).__init__()
        self.TOTEM_REF = ref
    
    def add(self, item): 
        if item.getType() == Names.FOCUS:
            AudioPlayer.playEffect(43)
            super(Ttm_Inv,self).add(item)
            
            if self.TOTEM_REF.isOn():
                self.trigger()
            else:
                GUI.out("You stick the " + str(item) + " into the totem's mouth.")
            
            return True

        GUI.out("That doesn't look like it fits there.")
        return False
    
    def remove(self, removeThis):
        super(Ttm_Inv,self).remove(removeThis)
        
        if self.TOTEM_REF.isOn(): 
            self.trigger()
    
    def trigger(self):   
        self.TOTEM_REF.determineColor()
        s = Player.getRoomObj(Id.GAL4).getFurnRef(GAL4_STAT_ID)
        r = beam + " emits from the totem's mouth. "
        GUI.out((r + s.activate(beam)) if s else r)



class Gal4_Carpet(Carpet):
    def __init__(self):
        super(Gal4_Carpet,self).__init__()
        
        self.searchDialog = ("You walk along the balcony, scanning the carpet for " +
                            "irregularities and lifting it every now and then. " +
                            "You can't seem to find anything of interest.")
        self.description = ("An luxurious looking rug, as are the rest in this " +
                           "castle. Woven into the rug along the edges " +
                           "are fine golden meandering designs.")

        self.addNameKeys("(?:royal )?(?:blue )?carpet(?: runner)")



class Gal4_Case(SearchableFurniture, Openable, Unmoveable):    
    def __init__(self, itemList=[]):
        super(Gal4_Case,self).__init__(itemList)
        
        self.searchable = False
        
        self.description = ("The mounted metal case is padlocked shut and currently protecting a " +
                "large painting of a woman posing to the left in a chair. She has long " +
                "brown hair and pale, perfect skin, as well as a slight grin. " +
                "Interesting, as you note that she also lacks eyebrows.")
        
        self.actDialog = ("You jam every key you can into the padlock, but nothing fits.")
        self.searchDialog = ("The case is locked shut, and you cannot pry it open.")
        self.useDialog = ("The glass front is clearly designed to keep dimwits like you out.")

        self.addNameKeys("(?:mounted )?(?:protected )?(?:metal )?case", "painting")
        self.addUseKeys(Furniture.ANYTHING)
        self.addActKeys("break|destroy", "unlock", "loot", "unscrew")
    
    def getDescription(self):
        return (self.description if self.containsItem(MONA_LISA) else "The mounted case is empty.")
    
    def getSearchDialog(self):
        return ("You open the case." if self.searchable else self.searchDialog)
    
    def interact(self, key):              
        if key == "break" or key == "destroy":
            return ("This case is strong.")
        elif key == "unlock":
            return ("The lock is broken already!" if self.searchable else self.actDialog)
        elif key == "unscrew":
            return ("There aren't even any screws on self.")
        else:
            return ("You would like to do that, wouldn't you.")
    
    def useEvent(self, item):
        if item.getType() == WEAPON:
            AudioPlayer.playEffect(35)
            return self.useDialog
        elif str(item) == BOTTLE_OF_VINEGAR:
            return ("Dissolving the case with vinegar is an amusing idea at most.")
        elif str(item) == SCREWDRIVER:
            return ("There are no screws to turn on the protected case.")
        else:
            return Furniture.DEFAULT_USE
    
    def unlock(self):
        self.searchable = True



class Gal4_Door(Door):
    def __init__(self, direct):
        super(Gal4_Door,self).__init__(direct)
        self.description = ("The double doors here are made of brass. These must " +
                           "lead somewhere important! They appear composed of " +
                           "many mechanical parts.")



class Gal4_Glass(Furniture, Gettable, Moveable):
    def __init__(self):
        super(Gal4_Glass,self).__init__()
        
        self.description = ("It's plain glass. Looks strong though...")
        self.actDialog = ("Attempts to shatter the glass are in vain. This glass is built to last.")
        self.useDialog = self.actDialog

        self.addNameKeys("glass")
        self.addUseKeys(Furniture.ANYTHING)
        self.addActKeys("shatter", "break|destroy", 
            Furniture.JOSTLEPATTERN, Furniture.GETPATTERN)
    
    def interact(self, key):
        if re.match(Furniture.GETPATTERN, key):
            return self.getIt()
        else:
            AudioPlayer.playEffect(35)
            return self.actDialog

    def useEvent(self, item):
        if item.getType() == WEAPON:
            return self.interact("break")
        else:
            return Furniture.DEFAULT_USE



class Gal4_Lever(Lever):
    def __init__(self):
        super(Gal4_Lever,self).__init__()
        
        self.description = ("The small lever protrudes from the side of the tall radio. It appears to be an on switch.")
        self.actDialog = ("Pulling the lever on the side appears to do nothing. The radio is evidently broken and is for show only.")
        self.addNameKeys("(?:small )?lever")

    def event(self, key):
        return self.actDialog



class Gal4_Loft(Furniture):
    def __init__(self):
        super(Gal4_Loft,self).__init__()

        self.description = ("At the third floor level on the west side of the " +
                           "central chamber, you see an adjoining room " +
                           "overlooking the whole gallery.")
        self.searchDialog = ("The loft is way up there!")
        self.addNameKeys("loft")



class Gal4_Padlock(Cel5_Lock):
    def __init__(self, ID):
        super(Gal4_Padlock, self).__init__()
        
        self.CASE_ID = ID
        self.description = ("The padlock is sealing the door of the mounted case.")
        self.useDialog = ("A nice hard smack, combined with your insatiable thirst for " +
                  "good art, is enough to defeat the lock.")
    
    def useEvent(self, item):
        if item.getType() == WEAPON:
            AudioPlayer.playEffect(35)
            Player.getPos().removeFurniture(self.getID())
            Player.getPos().getFurnRef(CASE_ID).unlock()
            return self.useDialog
        else:
            return super(Gal4_Padlock, self).useEvent(item)



"""
    The 1mm screws for fixing the red focus are found here. The player must a use
    a screwdriver found in the workshop to obtain the screws from here.    
"""
class Gal4_Radio(Furniture, Gettable, Moveable):
    def __init__(self, ref):
        super(Gal4_Radio,self).__init__()
        
        self.screwsLeft = 4
        self.SCREW_REF = ref
        
        self.description = ("Its glassed-in surface protects many gauges, copper coils, " +
                "and bulbs of which you know little. Holding the panel in are " +
                "several metal brackets around the edge as well as four small " +
                "screws on the corners of the box. A small lever " +
                "sticks out from the right side of the box.")
        
        self.DESC_2 = ("Its glassed-in surface protects many gauges, copper coils, " +
                "and bulbs of which you know little. Holding the front glass " +
                "panel in are several metal brackets around the edge. A " +
                "small lever sticks out from the right side of the box.")

        self.actDialog = ("Nothing useful has ever been accomplished through senseless " +
                         "violence. Lets keep our wits and figure out a more rational " +
                         "course of action.")
        
        self.searchDialog = ("There is nothing interesting hidden on the box, nor " +
                            "are any of the odd mechanical parts inside of interest.")
        
        self.useDialog = ("The screwdriver fits into one of the screws on the " +
                         "tall radio. You twist and with little-effort, the " +
                         "miniature screw falls out into your palm.")

        self.addNameKeys("(?:tall )?(?:blue )?(?:modern )?(?:metal )?(?:machine|radio)", 
                "(?:tiny )?screws?", "(?:front )?(?:glass )?panel")
        self.addUseKeys(Furniture.ANYTHING)
        self.addActKeys(Furniture.GETPATTERN, "break", "unscrew", "listen")
    
    def getDescription(self):
        return (self.description if (screwsLeft > 0) else self.DESC_2)
    
    def interact(self, key):
        if key == "break":
            return self.actDialog
        elif key == "listen":
            return ("The radio isn't on for you to do that.")
        else:
            return ("The only obtainable thing on this box seems to be the front " +
                   "screws, but digging them out by hand seems infeasible.")
    
    def useEvent(self, item):
        if item.getType() == WEAPON:
            return actDialog
        elif str(item) == SCREWDRIVER:
            if screwsLeft > 0:
                if Player.getInv().add(self.SCREW_REF):
                    screwsLeft -= 1
                    return self.useDialog
                else:
                    return Furniture.NOTHING
            else:
                return ("You have already unscrewed everything you can. Perhaps " +
                       "you should be more aware of where you leave things.")
        else:
            return ("You can't imagine what useful thing you could get done with that.")



class Gal4_Statue(Furniture):
    def __init__(self, ref):
        super(Gal4_Statue,self).__init__()
        
        self.GAL7_STAT_REF = ref
        self.level = 0
        
        self.actDialog = ("What glorious rippling muscles the statue has!")
        self.description = ("The statue now stands surrounded by the second floor " +
                           "balcony. The orb has stopped glowing, but one of " +
                           "the statue's eyes has started to.")
        self.searchDialog = ("The statue's hand is out of reach")
        
        self.addNameKeys("(?:grandiose )?statue")
        self.addActKeys("admire")

    def getState(self):
        return self.level

    """
        Hits the orb in the statue's hand with light.
        @param color the color of the beam.
        @return returns a string of what happens.
    """
    def activate(self, color):
        if Player.getRoomObj(Id.GAL4).hasFurniture(self.getID()):
            if (color == MachineColor.COLOR_MAP[0b0010] and self.level == 0) or \
                (color == MachineColor.COLOR_MAP[0b0011] and self.level == 1) or \
                (color == MachineColor.COLOR_MAP[0b0111] and self.level == 2):
                return self.rise() 
            elif self.level == 0:
                return ("The beam of light shines into the orb with no effect.")
            elif self.level <= 2:
                self.level = 0
                return ("The orb's hum dies and its glow fades.")
            else:
                return ("The beam of light shines at the statue's base.")
        else:
            return ("The beam of light shines into the central chamber.")

    def rise(self):
        if self.level == 0: 
            return ("The crystal orb in the statue's palm glows blue.")
        elif self.level == 1: 
            return ("The orb's glow turns green and it begins to hum.")
        else: 
            Player.getRoomObj(Id.GAL7).addFurniture(self.GAL7_STAT_REF)
            AudioPlayer.playEffect(37)
            return ("The crystal orb's glow brightens to a blinding white " +
                  "light. It hums loudly and rises once again to the " +
                  "third floor level.")
        level += 1

    def getDescription(self):
            if self.level == 1:
                return ("The statue stands holding the glowing orb. It hums softly.")
            elif self.level == 2:
                return ("The statue stands holding the glowing orb. It's humming quite loudly now.")
            elif self.level == 3:
                return ("The statue has risen yet again to the highest area of " +
                      "the central chamber across from the third floor loft. " +
                      "The statue's plinth is now exceedingly long and unusual.")
            else:
                return self.description

    def reset(self):
        if self.level <= 2:
            self.level = 0



"""
   Charges the battery for 25 seconds.
"""
class Apparatus_Inventory(Inventory):
    def __init__(self):
        super(Apparatus_Inventory, self).__init__()
        self.chargeThread = None

    def add(self, item):
        super(Apparatus_Inventory,self).add(item)
        
        if str(item) == DEAD_BATTERY:
            # Charges the battery.
            self.chargeThread = Charge_Thread(item, self)
            self.chargeThread.start()
        
        return True
 
    def __getstate__(self):
        self.chargeThread = None         
        return self.__dict__

    def remove(self, removeThis):
        super(Apparatus_Inventory,self).remove(removeThis)
        
        if str(removeThis) == DEAD_BATTERY and self.chargeThread:
            self.chargeThread.interrupt()
            self.chargeThread = None
            


"""
    Player must use this to charge the dead battery before using it on the cannon    
""" 
class Gal6_Apparatus(SearchableFurniture, Gettable):
    def __init__(self):
        super(Gal6_Apparatus,self).__init__()
        
        self.inv = Apparatus_Inventory()
        
        self.searchDialog = ("You look on the platform.")
        self.actDialog = ("The device appears to be powered by some invisible source and lacks an off switch.")
        self.description = ("The weird apparatus looks like a metal platform " +
                           "with three curved arms projecting out and over the top " +
                           "of itself. Wires run all over the thing, and lights " +
                           "on it go *bleep bleep bleep*. The machine emits " +
                           "some sort of blue light. Next to the apparatus is a label " +
                           "that reads: \"Plasma induction charger\".")
        
        self.addActKeys(Furniture.GETPATTERN, "turn", "repair|fix")
        self.addNameKeys("(?:unknown )?apparatus", "(?:plasma induction )?charger")

    def interact(self, key):
        if key == "turn":
            return self.actDialog
        elif key == "repair" or key == "fix":
            return ("I don't think that device is broken.")
        else:
            return self.getIt("This device is too big and heavy to put in your pockets.")


"""
    Converts chemical into chilled chemicals in 25 seconds.
"""
class Charge_Thread(Thread):
    def __init__(self, battery, inv):
        super(Charge_Thread, self).__init__()
        self.setDaemon(True)
        self.DEAD_BATTERY = battery
        self.APPARATUS_INV = inv
        self.cancelled = False

    def run(self):     
        GUI.out("The battery appears to be charging. Better give it some time.")
        time.sleep(25)

        if not self.cancelled:
            if self.APPARATUS_INV.contains(str(self.DEAD_BATTERY)):
                GUI.out("The battery has likely charged enough at this point.")
                self.APPARATUS_INV.remove(self.DEAD_BATTERY)
                self.APPARATUS_INV.add(BreakableItem(CHARGED_BATTERY, 160))

            self.cancelled = True
    
    def interrupt(self):
        if not self.cancelled:
            GUI.out("Your impatience has interrupted the charging cycle.")
            self.cancelled = True



"""
    Teleports the player to a previously visited room when pressed.
    Superficial, not important to game progression.    
"""
class Gal6_Button(Button):
    def __init__(self):
        super(Gal6_Button,self).__init__()
        self.description = ("It's a bright red button! Very tempting...")
        self.actDialog = ("That was a smart decision.")

    def interact(self, key):
        return self.event(key)

    def event(self, key):
        GUI.out("Are you really sure you want to press the button?")
        choice = GUI.askChoice(Menus.GAL6_BTTN, YES_NO_P)

        if Player.answeredYes(choice):
            AudioPlayer.playEffect(11)
            Player.teleport()

            return ("'... Huh? What just happened? You scratch your head and look around the room.")
        
        return self.actDialog



"""
    One of four components of the light machine puzzle in the gallery    
"""
class Gal6_Canon(Gal_LightMachine):
    def __init__(self, ID):
        super(Gal6_Canon,self).__init__()
        self.searchDialog = ("You search around the futuristic cannon.")
        self.actDialog = ("You have no idea how this thing works.")
        self.turnOffDialog = ("The lights on the cannon stop blinking.")
        self.description = ("This thing looks complicated. It's black, and... it " +
                           "has some kind of big ball for a body. And it's metal. " +
                           "Yeah, you're sure that's metal. It has a long barrel " +
                           "coming out the front with slots in it and the whole " +
                           "thing is covered in lights and wires. Wait... there's " +
                           "an empty square compartment on top. What is that for?")
        self.GAL7_STAT_ID = ID
        self.addActKeys("fire", "shoot")
        self.addNameKeys("(?:electr(?:on)?ic )?cann?on")
        self.addUseKeys(CHARGED_BATTERY, DEAD_BATTERY)
        self.inv = Cnn_Inv(self)       
    
    def getDescription(self):   
        if self.containsItem(CHARGED_BATTERY):
            return ("The cannon is blinking and making bleeping noises. " +
                   "A ray of light shoots out the barrel too. It must be on!")
        else:
            return self.description 
    
    def turnOn(self):
        self.determineColor()
        s = Player.getRoomObj(Id.GAL7).getFurnRef(self.GAL7_STAT_ID)
        r = ("The lights on the cannon light up and start bleeping. " + beam + " emits from the barrel. ")
        self.isOn = True     
        
        return (r + s.activate(beam)) if s else r
    
    # Reset statue does nothing
    

class Cnn_Inv(Inventory):
    def __init__(self, ref):
        super(Cnn_Inv,self).__init__()
        self.CANON_REF = ref
    
    def add(self, item):   
        if item.getType() == Names.FOCUS:
            AudioPlayer.playEffect(43)
            super(Cnn_Inv,self).add(item)
            
            if self.CANON_REF.isOn():
                self.trigger()
            else:
                GUI.out("You slide the " + str(item) + " inside a slot on the cannon barrel.")
            
            return True
        elif str(item) == CHARGED_BATTERY:
            AudioPlayer.playEffect(43)
            super(Cnn_Inv,self).add(item)
            GUI.out("You slide the box inside the square compartment in the cannon. " + Gal6_Canon.self.turnOn())
            return True
        elif str(item) == DEAD_BATTERY:
            AudioPlayer.playEffect(43)
            super(Cnn_Inv,self).add(item)
            GUI.out("The box fits snugly inside the cannon, however nothing interesting happens.")
            return True
        else:
            GUI.out("That doesn't look like it fits there.")
            return False

    def remove(self, item):
        self.CONTENTS.remove(item)
        
        if str(item) == CHARGED_BATTERY:
            GUI.out(self.CANON_REF.turnOff())
        elif self.CANON_REF.isOn():
            self.trigger()
    
    def trigger(self): 
        self.CANON_REF.determineColor()
        s = Player.getRoomObj(Id.GAL7).getFurnRef(self.GAL7_STAT_ID)
        r = beam + " shoots out the front of the cannon. "
        GUI.out((r + s.activate(beam)) if s else r)

class Gal6_Hatch(Furniture):
    def __init__(self):
        super(Gal6_Hatch,self).__init__()

        self.description = ("The hatch leads down into the room below.")
        self.actDialog = ("The hatch is open already.")
        
        self.addActKeys("open", "close", "jump")
        self.addNameKeys("hatch")

    def interact(self, key):
        if key == "open":
            return self.actDialog
        elif key == "jump":
            return ("That sounds dangerous.")
        else:
            return ("If you do that, you won't be able to leave!")



"""
    Prints a weird dialog when worn.
    Superficial, not important to game progression.    
"""
class Gal6_Helmet(Furniture):
    def __init__(self):
        super(Gal6_Helmet,self).__init__()

        self.searchDialog = ("Everything on the helmet looks concretely attached " +
                            "to the helmet and not removable.")
        self.description = ("The metal helmet is covered in wires and metal rods. " +
                           "On the inside are three metal contact plates. It would " +
                           "not be a good idea to wear self.")
        self.actDialog = ("AAAAAAAAAAAAAAAAAAAAAAHHHHHHHHHHHHHHHHHHHHHHH " +
                      "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! " +
                      "With all your strength, you rip the helmet off your head. " +
                      "It takes you a few moments to catch your breath and recover " +
                      "your sense of direction. You cannot comprehend what just happened.")
        
        self.addActKeys(Furniture.GETPATTERN)
        self.addActKeys("wear", "put")
        self.addNameKeys("(?:bizarre|cool )?helmet")

    def interact(self, key):
        GUI.out("Are you really sure you want to wear the helmet?")

        choice = GUI.askChoice(Menus.GAL6_HELM, YES_NO_P)

        if Player.answeredYes(choice):
            for i in range(18000):
                r = str(random.randint(0,1))
                for j in range(60):
                    r += str(random.randint(0,1))    
                GUI.out(r)
        else:
            return ("That was a smart decision.")

        return self.actDialog



class Gal6_Ladder(Staircase):
    def __init__(self):
        super(Gal6_Ladder,self).__init__(Direction.DOWN, Id.GAL3, 16)
        self.searchDialog = ("The ladder hides nothing.")
        self.description = ("The ladder leads down the hatch into the room below.")
        self.NAMEKEYS = []
        self.addNameKeys("(?:wood(?:en)? )?ladder")

class Gal6_Machine(Furniture):
    def __init__(self):
        super(Gal6_Machine,self).__init__()

        self.searchDialog = ("Everything on the machine looks attached and not removable.")
        self.description = ("The machine is a tall metal box with a bunch of dials, " +
                           "wires, and lights. Some wires feed out the back directly " +
                           "into the wall. Above, an extension resembling a shower " +
                           "head comes out the top of the machine. Oh, what's this? " +
                           "There's a single button on the front. Better not press " +
                           "that...")
        self.actDialog = ("Turning the dials does... nothing at all it seems.")
        
        self.addActKeys("turn")
        self.addNameKeys("(?:metal )?machine", "shower head", "dials?|wires?|lights?")



class Gal6(Room):
    def __init__(self, name, ID):
        super(Gal6,self).__init__(name, ID)

    def getBarrier(self, direct):
        if direct == Direction.EAST:
            return ("There's just open space that way. Wouldn't want to fall.")
        else:
            return self.bumpIntoWall()



class Gal6_Table(Furniture):
    def __init__(self):
        super(Gal6_Table,self).__init__()

        self.description = ("Why are you so focused on an ordinary table when " +
                           "there's all this other stuff to look at?")
        self.searchDialog = ("Nothing here but the cool helmet on top.")
        self.actDialog = ("Be careful! You don't want to break anything in here.")
        
        self.addActKeys(Furniture.JOSTLEPATTERN)
        self.addNameKeys("(?:ordinary )?table")



class Gal6_Technology(Furniture):
    def __init__(self):
        super(Gal6_Technology,self).__init__()

        self.description = ("Wow! So much cool technology! This sure beats coal and steam.")
        self.searchDialog = ("You can't decide which thing to search first.")
        self.useDialog = ("You would have no idea what to do. This stuff is foreign to you.")
        
        self.addUseKeys(Furniture.ANYTHING)
        self.addNameKeys("(?:cool )?technology")



class Gal7_Statue(Furniture):
    def __init__(self):
        super(Gal7_Statue,self).__init__()
        self.level = 0
        self.actDialog = ("The statue is out of reach")
        self.description = ("The statue now stands high in the central chamber " +
                           "at the thrid floor level. Its orb is cold yet again, " +
                           "but both of its eyes now glow brightly.")
        self.searchDialog = ("The statue's hand is out of reach")

    def getLevel(self):
        return self.level

    """
        Hits the orb in the statue's hand with light.
        @param color the color of the beam.
        @return returns a string of what happens.
    """
    def activate(self, color):
        if Player.getRoomObj(Id.GAL7).hasFurniture(self.getID()): 
            if level == 0:
                if color == MachineColor.COLOR_MAP[0b1111]:
                    return self.rise() 
                else:
                    return ("The beam of light shines into the orb with no effect.")
            else:
                return ("The beam of light shines at the orb, but the orb continues to glow hellishly.")
        else:
            return ("The beam of light shines into the central chamber.")

    def rise(self):
        self.level += 1
        Player.getRoomObj(Id.GAL5).setLocked(False)
        AudioPlayer.playEffect(38, 30)
        return ("The crystal orb in the statue's palm glows with a dark " +
               "hellish glow. Cogwork can be heard behind the walls and " +
               "before long, you hear a clicking sound down below.")

    def getDescription(self):
        if self.level == 1:
                return ("The statue stands in the central chamber holding the orb. " +
                       "Its eyes are brightly lit and the orb glows in a surreal " +
                       "dark light while humming loudly.")
        else:
            return self.description

class Gal_Balcony(Balcony):
    def __init__(self):
        super(Gal_Balcony,self).__init__()
        self.description = ("The balcony wraps around the perimeter of the central chamber.")



class Gal_Dome(Furniture):
    def __init__(self):
        super(Gal_Dome,self).__init__()

        self.description = ("The glass dome offers a nice view of the stars.")
        self.searchDialog = ("The dome is way too high up.")
        self.useDialog = self.actDialog = ("If you do that, the shards will probably " +
                         "rain down on you as a deadly glass shower.")
        
        self.addUseKeys(STONE_BLOCK, RED_BALL, CUE_BALL, ROCK)
        self.addActKeys("shatter")
        self.addNameKeys("(?:glass )?dome")
