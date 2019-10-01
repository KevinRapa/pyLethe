from Foyer import Foy2_Button
import Direction, Id, AudioPlayer
from Structure_gen import Door, Column
from Player import Player
from Things import Statue
from Furniture import Furniture
from Room import Room
from Mechanics import Lever, Button
from Rotunda import Rotu

class Want_Button(Button):
    def __init__(self, ID):
        super(Want_Button,self).__init__()
        
        self.FOY2_LVR_ID = ID
        self.description = ("There's a small black button on the wall next to the gate.")
        self.addNameKeys("(?:small )?(?:black )?button")
    
    def event(self, key):
        return Player.getRoomObj(Id.FOY2).getFurnRef(self.FOY2_LVR_ID).event("")



class Want_Door(Door):
    def __init__(self, direct):
        super(Want_Door,self).__init__(direct)
        self.description = ("The door at the bottom of the ramp catches your eye. " +
                           "It's carved very artfully. At its center, a cobra's  " +
                           "head is carved into the wood.")



class Want_Gate(Door):
    def __init__(self, direct):
        super(Want_Gate,self).__init__(direct)
        self.actDialog = ("You wouldn't be able to lift it with your hands.")
        self.description = ("The open gateway leads back into the foyer.")
        self.addNameKeys(str(direct) + " gate", "gate")

    def interact(self, key):
        op = Player.getPos().isAdjacent(Id.FOY1) or Player.getPos().isAdjacent(Id.FOY2)
        
        if key == "close":
            if op:
                return ("That would only impede your progress.")
            else:
                return ("The gate is closed already!")
        elif self.open:
            return ("It's just empty space. Maybe you should go through it?")
        elif key == "open" or key == "lift":
            return self.actDialog
        else:
            return super(Want_Gate,self).interact(key)

    def getDescription(self):
        if Player.getPos().isAdjacent(Id.FOY1) or Player.getPos().isAdjacent(Id.FOY2):
            return self.description
        else:
            return "The closed gate bars your way into the foyer."



class Want_Lever(Lever):
    def __init__(self):
        super(Want_Lever,self).__init__()

        self.description = ("It's a black iron lever resting on the plinth of the statue.")
        self.searchDialog = ("There's a pile of gold! No, not really, just a lever.")
        self.actDialog = ("You pull the lever. The room vibrates and you " +
                         "here a prolonged rumble past the wall to your west.")
        self.addNameKeys("lever", "(?:black )?(?:iron )?lever")

    def event(self, key):
        ref = Player.getRoomObj(Id.ROTU)
        
        if ref.getState() == Rotu.EAST_WEST:
            return ("You pull the lever, but nothing happens except a faint " +
                   "-click- sounding past the wall to your west.")
        else:
            AudioPlayer.playEffect(19, 30)
            ref.rotate()
            return self.actDialog



class Want_Pillars(Column):
    def __init__(self):
        super(Want_Pillars,self).__init__()

        self.description = ("They're grooved, sandstone pillars holding up the " +
                           "ceiling two stories above. They're grand- about 5 " +
                           "feet in diameter and stand on square plinths.")
        self.addNameKeys("pillars?", "columns?")



"""
    Contains a hidden lever that can be pulled to rotate the rotunda.
    Room description doesn't refer to lever. Player can assume one is there
    because there are one's in Stud, Look, and Iha1.    
"""
class Want(Room):
    def __init__(self, name, ID):
        super(Want,self).__init__(name, ID)

    def getBarrier(self, direct):
        if direct == Direction.WEST:
            AudioPlayer.playEffect(6)  # If the rotunda has rotated.
            return ("The door is missing!")
        elif direct == Direction.EAST:
            AudioPlayer.playEffect(4)  # If the foyer gate is closed.
            return ("The gate that way is closed.")
        else:
            return self.bumpIntoWall()



class Want_Ramp(Furniture):
    def __init__(self):
        super(Want_Ramp,self).__init__()

        self.description = ("At the far end of the antechamber, a ramp slopes " +
                           "downward about six feet before terminating at a door.")
        self.searchDialog = ("There's nothing there except dust and a few cobwebs.")
        self.addNameKeys("ramp")



class Want_Statue(Statue):
    def __init__(self):
        super(Want_Statue,self).__init__()

        self.description = ("Inspecting each statue, you discover each to be " +
                           "depicting an Egyptian god. There's Anubis, god " +
                           "of the dead, Isis, goddess of magic, Thoth, god of " +
                           "wisdom, and Wadjet, goddess of protection. You " +
                           "notice what appears to be a lever attached to " +
                           "the base of one of them.")
        self.searchDialog = ("They are plain statues. Upon closer inspection " +
                            "of one though, you find a lever hidden.")
        self.actDialog = ("You feel a statue, but you are discomforted in thinking " +
                         "that somehow, the other statues may be watching you.")
        self.addNameKeys("statues")



class Want_Torches(Furniture):
    def __init__(self):
        super(Want_Torches,self).__init__()

        self.description = ("Tall tan obelisks standing in the corners of the room " +
                           "support metal baskets of burning wood chunks. They " +
                           "are burning quite audibly and furiously.")
        self.actDialog = ("These are large standing torches, and much too heavy " +
                         "for you to just take and carry around. Find one on a " +
                         "wall somewhere.")
        
        self.addActKeys(Furniture.GETPATTERN)
        self.addNameKeys("(?:standing )?torch(?:es)?", "(?:metal )?baskets", 
                "(?:burning )?(?:wood(?:en)? )?chunks")