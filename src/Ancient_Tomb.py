from GUI import GUI
from Player import Player
import AudioPlayer
from Names import KEY_OF_ANCESTRY, KEY_OF_INTELLECT, KEY_OF_CONTINUITY, BRAIN, COMPASS
from Furniture import SearchableFurniture, Openable, Furniture
from Item import Item, Note
from NonPlayerCharacter import NonPlayerCharacter
from Structure_gen import Ceiling
from Room import Room

"""
    The two important objects in this room are Ant_NPC and Ant_Cskt.
    The NPC gives the player a tool to find the iridescent jewel in the catacombs.
    The casket contains the location of the iridescent jewel. To open the casket,
    the player must find three keys hidden in parts of the catacombs.
    Connects to An65 and Catacombs.
"""
class An55(Room):    
    def __init__(self, name, ID):
        super(An55, self).__init__(name, ID)

    def triggeredEvent(self):
        if not Player.hasVisited(self.ID):
            GUI.out("As you enter the room, you become immediately aware of " +
                    "a horrible figure standing on the room's opposite end. " +
                    "You freeze and stare. The figure stands perfectly still, " +
                    "his mouth gaping and eyeless face pointed right at you.")
            
        return self.NAME


"""
    The two important objects in this room are Ant_NPC and Ant_Cskt.
    The NPC gives the player a tool to find the iridescent jewel in the catacombs.
    The casket contains the location of the iridescent jewel. To open the casket,
    the player must find three keys hidden in parts of the catacombs.
"""
class An65(Room):    
    def __init__(self, name, ID):
        super(An65, self).__init__(name, ID)

    def triggeredEvent(self):
        if not Player.hasVisited(self.ID):
            GUI.out("You step closer to the zombie-like figure. It remains still, " +
                    "swaying slightly with its attention drawn to you.")
            
        return self.NAME



class Ant_Casket(SearchableFurniture, Openable):
    def __init__(self, itemList=[]):
        super(Ant_Casket,self).__init__(itemList)
        self.searchable = False
        self.searchDialog = ("You can't seem to push the lid off. It's sealed with an archaic lock system.")
        self.actDialog = ("It's very impolite to hit coffins!")
        self.description = ("The casket lies horizontal in the center of the room. " +
                           "It's unlike the rest of the caskets made of stone, and " +
                           "covered by a thick lid. There are three keyholes lined " +
                           "up vertically in the center of the lid.")
        self.numKeys = 0
        
        self.addActKeys(Furniture.JOSTLEPATTERN)
        self.addNameKeys("(?:stone )?(?:casket|coffin)", "keyholes?", "holes?", "lid")
        self.addUseKeys(KEY_OF_ANCESTRY, KEY_OF_INTELLECT, KEY_OF_CONTINUITY)

    def useEvent(self, item):
        result = ("You insert the key into one of its holes and turn it.")
        AudioPlayer.playEffect(51)
        Player.getInv().remove(item)
        self.numKeys += 1
        
        if self.numKeys == 3:
            self.searchable = True
            AudioPlayer.playEffect(50)
            return (result + " With the last key inserted, you feel the lid jolt a bit. " +
                            "You push the lid with all your might, and it slides off to the side. " +
                            "To your surprise, there is nothing inside except for a leaf of parchment.")
        else:
            return result

    def getDescription(self):    
        if self.numKeys == 1: 
            return ("The lid is locked. Two of the keyholes remain empty.")
        elif self.numKeys == 2:
            return ("The lid remains locked tightly. One keyhole remains empty.")
        elif self.numKeys == 3:
            return ("All of the keys have been inserted into the coffin keyholes.")
        else:
            return self.description

    def getSearchDialog(self):
        return ("You look inside the coffin." if self.searchable else self.searchDialog)



class Ant_Caskets(Furniture, Openable):
    def __init__(self):
        super(Ant_Caskets, self).__init__()
        
        self.actDialog = ("It's very impolite to hit coffins!")
        self.description = ("The various ramshackle coffins are pieced together " +
                           "with many nailed-together wooden planks.")
        self.searchDialog = ("You are being watched... best not to do that.")

        self.addActKeys(Furniture.JOSTLEPATTERN)
        self.addNameKeys("caskets", "wooden caskets")

class Ant_Ceiling(Ceiling):
    def __init__(self):
        super(Ant_Ceiling, self).__init__()
        self.description = ("The sandstone brick ceiling arches gently over your head.")
        self.searchDialog = ("It's a ceiling...")
        self.addNameKeys("(?:low )?(?:arched )?ceiling")

"""
    An NPC that the player can talk to. Gives the player a tool to find the 
    iridescent jewel.
"""
class Ant_Zombie(NonPlayerCharacter):
    """
        drawerNum is passed is from the Cry_Drawers, which randomly puts the
        jarred brain in one of them. This parameter is which drawer that is
        so that it can be written on the note. This class must be instantiated
        AFTER Cry_Drawers is as a result.
    """
    def __init__(self, ref, drawerNum):
        super(Ant_Zombie, self).__init__()
        
        self.QUARTZ_DEVICE = Compass() # Zombie gives this to player.
        self.ZOMBIE_NOTE = Zombie_Note("message", drawerNum) # Zombie gives this to player.
        self.FLR_INV_ID = ref.getID() # Zombie drops note if player inv is full.
        self.pleased = False # pleased once player gives brain to zombie.
        
        self.description = ("The hideous dessicated figure is eyeless and frail. It just " +
                           "stands there in the corner of the room, pointing " +
                           "its face at you with its mouth hanging open. It " +
                           "is clothed in simple farming vestments and keeps " +
                           "one of its hands in its pocket. 'Is it alive?' " +
                           "You wonder to yourself.")
        self.actDialog = ("The figure makes a loud moan. You jump, and every " +
                        "hair on your body stands. The zombie takes the " +
                        "brain in a jar from you and manages to stuff it " +
                        "in its small pocket. The figure pulls its hand " +
                        "out and offers you a small boxy object. The " +
                        "figure makes another load moan and holds its hand " +
                        "out. You take the item. The figure " +
                        "makes a final loud moan and remains quiet.")
        
        self.useDialog = ("The zombie-like body, though horrific, appears passive. " +
                         "You aren't very inclined to attack it.")
        
        self.searchDialog = ("You aren't nearly sly enough for that.")
        
        self.CONVERSE_REP2 = ("The figure just stands there, staring at you with " +
                             "its mouth hanging open.")

        self.addUseKeys(BRAIN)
        self.addNameKeys("(?:frail )?(?:eyeless )?(?:dessicated )?(?:corpse|figure|zombie)", 
                "zombie-like (?:figure|body)", "him")

    def useEvent(self, item):
        if str(item) == BRAIN:
            Player.getInv().remove(item)
            self.pleased = True
            self.firstTime = False
            return self.converse1()
        else:
            return super(Ant_Zombie, self).useEvent(item)

    def interact(self, key): 
        if re.match(NonPlayerCharacter.ATTACK_PATTERN, key):
            return NonPlayerCharacter.ATTACK_DIALOG
        elif self.pleased or not self.firstTime:
            # Once zombie is pleased, first time is immediately False. No
            # need to handle firstTime = True here.
            return self.converse2()
        else:
            AudioPlayer.playEffect(46)
            self.firstTime = False
            return self.converse3()

    def converse1():
        # Player inv can't be full because the zombie just took the brain from the player.
        AudioPlayer.playEffect(46)
        Player.getInv().add(self.QUARTZ_DEVICE)
        return self.actDialog

    def converse2(self):
        return self.CONVERSE_REP2

    def converse3(self):
        result = ("The figure looks at you with a hollow stare. " +
                 "It slowly lifts its arm up and hands out a piece of paper.")
        
        if Player.getInv().add(self.ZOMBIE_NOTE):
            return (result + "You take the message. The figure then lifts " +
                     "its hand higher and points vaguely upwards.")
        else:
            Player.getPos().getFurnRef(self.FLR_INV_ID).getInv().add(self.ZOMBIE_NOTE)
            return (result + "The paper slowly drifts to the floor " +
                      "from the zombie's weak grasp. The figure then lifts " +
                      "its hand higher and points vaguely upwards.")


class Zombie_Note(Note):
    def __init__(self, name, drawerNum):
        super(Zombie_Note, self).__init__(name)
        self.DRAWER_NUM = str(drawerNum)

    def getDesc(self):
        return super(Zombie_Note,self).getDesc() + self.DRAWER_NUM + "."


class TombNote(Note):
    def __init__(self, name, coords):
        super(TombNote, self).__init__(name)
        self.COORDS = coords

    def getDesc(self):
        return super(TombNote,self).getDesc() + self.COORDS + "\"."



class Compass(Item):
    def __init__(self):
        super(Compass, self).__init__(COMPASS, score=100)
        self.useID = 1
        self.description = ("You can't quite figure out what it is. It's a small " +
                           "metal box with a bit of heft. A polished rock of " +
                           "quartz has been fit into its center indentation, acting " +
                           "as a window of sorts. On the top and bottom of the box " +
                           "are copper plates. The item appears meant to be squeezed.")
        self.useDialog = ("You grasp the box firmly with your fingers and palm " +
                         "covering the plates. In a short while, 3 digits:\t\t[")

    """
        Displays the player's coordinates in the GUI output window.
        The coordinates are Cartesian, with the 1st floor being z = 0 and
        the top row of rooms in the map array being y = 6.
        @return coordinates of the player.
    """
    def useEvent(self):
        c = Player.getPos().getCoords()
        z = abs(c[0] - 6) - 3
        y = abs(c[1] - 7)

        return self.useDialog + (str(c[2]) + ", " + str(y) + ", " + str(z) + 
                                     "]\t\tmaterializes in the quartz window.")
