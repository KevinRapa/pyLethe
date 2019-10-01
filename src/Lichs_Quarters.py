from Room import Room
import Direction, Id, AudioPlayer
from Furniture import SearchableFurniture, Moveable, Openable, Furniture
from Names import HAND_DRILL
from Player import Player
from Mechanics import Lever
from Things import Carpet

"""
    Whether or not the lich is alive affects the dialog in these rooms.    
"""
class Lich_Room(Room):
    def __init__(self, name, ID):
        super(Lich_Room,self).__init__(name, ID)
        self.lichDead = False

    def killLich(self):
        self.lichDead = True

    def lichIsDead(self):
        return self.lichDead



class Lqu1_Bed(Furniture):
    def __init__(self):
        super(Lqu1_Bed,self).__init__()

        self.description = ("On the far side of the room, a sinister body lays on a bed. Perhaps not much longer.")
        self.actDialog = ("Really? That's a terrible idea.")
        self.searchDialog = ("It's too far away to do that.")
        self.addNameKeys("body", "bed", "lich")
        self.addActKeys(Furniture.SITPATTERN)



"""
    Holds the dampening staff.    
"""
class Lqu1_Cabinet(SearchableFurniture, Openable, Moveable):
    def __init__(self, itemList=[]):
        super(Lqu1_Cabinet,self).__init__(itemList)
        
        self.description = ("It's a standing glass cabinet for displaying " +
                           "weaponry, staffs, brooms, bedposts, and other long objects.")
        self.searchDialog = ("You open the cabinet and look inside.")
        self.addNameKeys("(?:tall )?(?:standing )?(?:glass )?(?:display )?(?:cabinet|case)", 
                "(?:tall )?(?:standing )?(?:glass )?display")



"""
    Player's items are sent here after being captured in the Attic.
    Currently this isn't used. Items sent to prison cabinet instead.    
"""
class Lqu1_Chest(SearchableFurniture, Openable, Moveable): 
    def __init__(self):
        super(Lqu1_Chest,self).__init__()
        
        self.description = ("It's a dark hickory chest.")
        self.searchDialog = ("You open the chest.")
        self.addNameKeys("(?:dark )?(?:hickory |wooden )?chest")



class Lqu1_Mirror(Furniture):
    def __init__(self):
        super(Lqu1_Mirror,self).__init__()
        
        self.description = ("You look in the mirror, nearly not recognizing " +
                           "yourself. You look and feel exhausted and hungry. " +
                           "Perhaps it's only a bit further that you must tread.")
        self.searchDialog = ("It's simply a plain mirror.")
        self.addNameKeys("(?:standing )?mirror")



"""
    Contains a display case holding the dampening staff, needed to obtain the 
    fifth phylactery, and a chest holding the player's items after being captured.
"""
class Lqu1(Lich_Room):
    def __init__(self, name, ID):
        super(Lqu1,self).__init__(name, ID)

    def getBarrier(self, direct):
        if direct == Direction.EAST:
            return ("You shouldn't get to close to that thing over there...")
        else:
            return self.bumpIntoWall()

    def getDescription(self):
        modifier = ("lifeless" if self.lichDead else "breathing")
        return super(Lqu1,self).getDescription().replace("%", modifier, 1)



class Lqu1_Wardrobe(SearchableFurniture, Openable, Moveable):
    def __init__(self, itemList=[]):
        super(Lqu1_Wardrobe,self).__init__(itemList)
        
        self.description = ("It's a tall blue wooden wardrobe accented in yellow.")
        self.searchDialog = ("You open up the wardrobe.")
        self.addNameKeys("(?:tall )?(?:blue )?(?:wooden )?wardrobe")



class Lqu2_Bed(SearchableFurniture, Moveable):    
    def __init__(self, itemList=[]):
        super(Lqu2_Bed,self).__init__(itemList)

        self.description = ("It seems he will not have to roam eternally in madness after all... " +
                  "You suppose someone will find him eventually. " +
                  "Not great to just leave a dead body alone. Oh well.")
        self.searchDialog = ("Well, he's dead, might as well rob him!")
        self.addNameKeys("(?:lifeless )?(?:innocent )?(?:body|lich)", "bed")



"""
    Unlocks the front gate.    
"""
class Lqu2_Lever(Lever):
    def __init__(self, ID):
        super(Lqu2_Lever,self).__init__()
        
        self.GATE_ID = ID
        self.OPEN_GATE = Cou3_OpenedGate()
        
        self.description = ("A plain lever on the wall.")
        self.actDialog = ("With the last of your energy, you pull the lever. You hear a gate open.")
        self.addNameKeys("lever")
    
    def interact(self, key):
        if not self.isOn:
            self.swtch()
            AudioPlayer.playEffect(12)
            return self.event(key)
        else:
            return ("You best leave now...")
    
    def event(self, key):
        Player.getRoomObj(Id.COU4).setLocked(False)
        Player.getRoomObj(Id.COU3).removeFurniture(self.GATE_ID)
        Player.getRoomObj(Id.COU3).addFurniture(self.OPEN_GATE)
        AudioPlayer.playEffect(7, 25)
        return self.actDialog


    
class Cou3_OpenedGate(Furniture):
    def __init__(self):
        super(Cou3_OpenedGate,self).__init__()

        self.searchable = False
        self.description = ("The gate is open!")
        self.searchDialog = ("Did you find yourself at home here? Are wishing to stay busy?")
        self.useDialog = self.actDialog = self.description
        
        self.addUseKeys(HAND_DRILL)
        self.addActKeys("open", "use")
        self.addNameKeys("(?:monstrous )?(?:two-story )?(?:solid )?(?:oak )?(?:main |front )?gate")



class Lqu_Carpet(Carpet):
    def __init__(self):
        super(Lqu_Carpet,self).__init__()

        self.description = ("The lavender carpet covers much of the cold floor.")
        self.addNameKeys("(?:lavender )?carpet")