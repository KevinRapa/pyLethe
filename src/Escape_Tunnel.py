import Id, Direction, AudioPlayer
from Names import METAL_BAR, HAND_TORCH
from Furniture import Furniture, Resetable, Climbable, Gettable
from GUI import GUI
from Player import Player
from Structure_gen import Ceiling, Wall
from Room import Room
from Tunnels import DungeonMonsterFurniture, Dungeon_Floor

class Esc_Mchnry(Furniture):
    def __init__(self):
        super(Esc_Mchnry,self).__init__()

        self.description = ("All sorts of dangerous exposed machinery operate " +
                           "around you. You better be careful moving. This " +
                           "machinery must power some areas of the castle?")
        self.actDialog = ("You wouldn't dream of going anywhere near it.")
        self.searchDialog = ("You best keep moving and get out of here.")

        self.addNameKeys("machinery", "gears?", "pistons?")
        self.addActKeys("touch", "operate")

    def getDescription(self):
        if Esc.playerHasTorch():
            return self.description
        else:
            return Esc.TOO_DARK



class Esc_F(Dungeon_Floor):
    def __init__(self):
        super(Esc_F,self).__init__()
        self.searchable = False
        self.searchDialog = ("There's nothing here, and you don't feel comfortable " +
                "putting anything down where it will drop into oblivion.")

    def getDescription(self):
        if Esc.playerHasTorch():
            return self.description
        else:
            return Esc.TOO_DARK



class Esc1_Ladder(Furniture, Climbable):
    def __init__(self):
        super(Esc1_Ladder, self).__init__()
        
        self.description = ("It's a metal ladder with rudimentary rungs attached " +
                           "directly to the stone wall.")
        self.actDialog = ("You climb back up the ladder.")

        self.addNameKeys("(?:metal )?ladder", "rungs?")
        self.addActKeys("use", Furniture.CLIMBPATTERN)
    
    def interact(self, key):      
        AudioPlayer.playEffect(47)
        Player.setOccupies(Id.INTR)
        return self.actDialog
    
    def getDir(self):
       return Direction.UP



"""
    Player must pry this with the metal bar before climbing up the ladder into
    SEWP.
"""
class Esc6_Grate(Furniture, Resetable, Gettable):
    def __init__(self):
        super(Esc6_Grate,self).__init__()

        self.opened = False
        self.MOVED_GRATE = ("You've already moved the grate!")
        self.description = ("The metal grate blocks access to the above room.")
        self.actDialog = ("It's too heavy. You can't open it.")
        self.useDialog = ("You jam the bar in the corner of the grate. The grate pops " +
                         "up a bit, and you force the bar in more. With the rest of " +
                         "your strength, you pop the grate out.")

        self.addNameKeys("(?:metal )?grate")
        self.addUseKeys(METAL_BAR)
        self.addActKeys("lift", "move", "pry")
        self.addActKeys(Furniture.GETPATTERN)
    
    def getDescription(self):
        return ("The grate has been moved." if self.opened else self.description)
    
    def getSearchDialog(self):
        return ("The ladder goes up about 30 feet." if self.opened else self.searchDialog)
    
    def interact(self, key):  
        if key == "lift" or key == "move":
            return self.MOVED_GRATE if self.opened else self.actDialog
        elif key == "pry" and Player.hasItem(METAL_BAR):
            return self.useEvent(None) # Safe. Arg unused here.
        elif key == "pry":
            return ("You have nothing to do that with.")
        else:
            return self.getIt()

    def useEvent(self, item):
        if not self.opened:
            AudioPlayer.playEffect(48)
            self.opened = True
            return self.useDialog
        else:
            return self.MOVED_GRATE
    
    def reset(self):
        self.opened = False
    
    def isMoved(self):
        return self.opened



class Esc6_Ladder(Furniture, Resetable, Climbable):
    def __init__(self, ID):
        super(Esc6_Ladder,self).__init__()

        self.searchable = False
        self.GRATE_ID = ID
        self.description = ("It's a metal ladder with rudimentary rungs attached " +
                           "directly to the stone wall.")
        self.actDialog = ("You climb up the ladder.")

        self.addNameKeys("(?:metal )?ladder", "rungs?")
        self.addActKeys("use", Furniture.CLIMBPATTERN)
    
    def getDescription(self):
        if Player.getRoomObj(Id.ESC6).getFurnRef(self.GRATE_ID).isMoved():
            return self.description
        else:
            return (self.description + " The way up is blocked by a grate.")
    
    def interact(self, key):    
        if Player.getRoomObj(Id.ESC6).getFurnRef(self.GRATE_ID).isMoved():
            Player.getRoomObj(Id.INTR).setLocked(True)
            Player.getRoomObj(Id.SEWP).setLocked(False)
            Player.setOccupies(Id.SEWP)
            AudioPlayer.playEffect(47)
            return self.actDialog
        else:
            return ("Your way up is blocked by a grate.")
    
    def reset(self):
        Player.getRoomObj(Id.INTR).setLocked(False)
        Player.getRoomObj(Id.SEWP).setLocked(True)
    
    def getDir(self):
       return Direction.UP



"""
    Represents the tunnels the player must walk through to escape INTR (cell).    
"""
class Esc(Room):
    MACHINERY_REF = Esc_Mchnry()
    FLOOR_REF = Esc_F()
    ESC_WALL = Wall("The walls are masked by a wall of machinery.")
    ESC_CLNG = Ceiling("The ceiling is pretty low here.")
    MONSTER = DungeonMonsterFurniture()
    MACHINERY_DESC = ("You're crammed in a small utility tunnel. Many " +
      "pistons, gears, and other complicated machinery operate around " +
      "you. The hallway offers a bit of space in which to move forward. ")
    REFUSE_TO_MOVE = ("It's too dark to see anything, and there is a lot " +
      "of dangerous sounding machinery. You don't feel comfortable moving forward.")
    TOO_DARK = ("It's too dark to see anything at all. " +
      "All you here is a bunch of dangerous sounding machinery.")

    @staticmethod
    def playerHasTorch():
        return Player.hasItem(HAND_TORCH)

    def __init__(self, name, ID):
        super(Esc,self).__init__(name, ID)
        self.addFurniture(Esc.MACHINERY_REF, Esc.FLOOR_REF, Esc.ESC_WALL, Esc.ESC_CLNG, Esc.MONSTER)

    def getBarrier(self, direct):
        if Esc.playerHasTorch():
            return ("There's a lot of dangerous looking machinery that way.")
        else:
            return Esc.TOO_DARK

    def getDescription(self):
        if Esc.playerHasTorch():
            return Esc.MACHINERY_DESC + super(Esc,self).getDescription()
        else:
            return Esc.TOO_DARK

    def triggeredEvent(self):
        if not Esc.playerHasTorch() and not Player.getPosId() == Id.ESC1:
            GUI.out(Esc.REFUSE_TO_MOVE)
            Player.setOccupies(Id.ESC1)
        return str(Player.getPos())