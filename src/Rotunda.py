from Structure_gen import Door
from GUI import GUI
import Id, Direction, AudioPlayer
from Player import Player
from Room import Room
from Furniture import Furniture, Unmoveable
from Things import Statue, PottedPlant


class Rotu_Door(Door):
    def __init__(self, direct):
        super(Rotu_Door,self).__init__(dir)
        self.description = ("A heavy wooden door. It's surrounded at the edge by " +
                           "a seam, as if separate from the rest of the room. Very peculiar.")


"""
    Can be drained by a valve in Look which gives access to a wheel which
    rotates the Rotunda.    
"""
class Rotu_Fountain(Furniture, Unmoveable):
    def __init__(self):       
        super(Rotu_Fountain,self).__init__()
        
        self.ROTU_WHEEL = Rotu_Wheel()
        self.valvesTurned = 0
        self.drained = False
        self.description = ("It's rounded and carefully carved from a smooth rock. " +
                           "It looks quite beautiful, except that it's filled " +
                           "with opaque brown water.")
        self.actDialog = ("Are you really that desperate for a drink? There must be some cleaner water in here somewhere...")
        self.searchDialog = ("You can't see anything through the brown water.")
        self.addActKeys("drink", "swim", "drain", "empty")
        self.addNameKeys("(?:round )?(?:marble )?fountain", "water")

    def interact(self, key):
        if key == "drink":
            if self.drained: 
                return ("The disgusting water has already been drained.")
            else:
                return self.actDialog
        elif key == "swim":
            if self.drained: 
                return ("The disgusting water has already been drained.")
            else:    
                return ("An absolutely smashing idea. You'll be out of here in no time.")
        else:
            if self.drained:
                return ("The disgusting water has already been drained.")
            else:    
                return ("You have nothing useful with which to empty it.")

    def getSearchDialog(self):        
        if self.drained:
           return ("Looking inside the bowl, you find decaying plant matter " +
             "resting on the bottom. A curious stone wheel wraps around " +
             "the base of the fountain inside the bowl.")
        else:
            return self.searchDialog 

    def getDescription(self):
        if self.drained:
           return ("With the fountain drained, you find decaying plant matter " +
               "resting on the bottom. A curious stone wheel wraps around " +
               "the base of the fountain inside the bowl.")
        else:
            return self.description 

    def drain(self):
        self.drained = True   
        AudioPlayer.playEffect(20)
        Player.getRoomObj(Id.ROTU).addFurniture(self.ROTU_WHEEL)

    def loosen(self, amount):
        self.valvesTurned += amount

        if not self.drained and self.valvesTurned == 3:
            self.drain()
            return ("As you turn it, a gush of water can be heard flowing through the nearby pipe.")
        else:
            return Furniture.NOTHING

    def isDrained(self):
        return self.drained



class Rotu_Frames(Furniture, Unmoveable):
    def __init__(self):
        super(Rotu_Frames,self).__init__()

        self.description = ("They are arched, door-shaped, and seem as if they " +
                           "form the entry of some kind of hidden magical passage.")
        self.searchDialog = ("These frames seem as though they hide something, but " +
                            "after inspecting every inch, you can only confirm " +
                            "they are plain carvings.")
        self.actDialog = ("You feel as though if you do that, you will get a face-full of rock.")
        
        self.addActKeys("go|walk|run")
        self.addNameKeys("(?:arched )?frames?", "carvings?")



"""
    Player can escape through this from the Garden once trapped in the castle
    rear using a leather hose.    
"""
class Rotu_Hole(Furniture):
    def __init__(self):
        super(Rotu_Hole,self).__init__()

        self.description = ("It's a hole carved in the ceiling, about a meter " +
                           "wide. It looks to lead outside to the roof, although " +
                           "there's a glass encasing around the space above.")
        self.actDialog = ("The hole is high up in the ceiling. How would you go " +
                         "about that? Especially with your heft. Few ropes could " +
                         "support such weight.")
        self.searchDialog = ("The hole is but empty space. You have nothing to search.")
        
        self.addActKeys(Furniture.CLIMBPATTERN, "jump")
        self.addNameKeys("hole(?: ceiling)?")



class Rotu_Plants(PottedPlant):
    def __init__(self, soil, gift):
        super(Rotu_Plants,self).__init__(soil, gift)

        self.description = ("The plants don't seem to be in good shape. They droop and some are crowded with weeds.")



"""
    This room rotates, only allowing access to two of its adjacent rooms at a time.
    Room is rotated by four levers in the adjacent rooms or by a wheel in the
    fountain, that must first be drained.
    Connects to Foyw, Look, Stud, and Iha1 
"""
class Rotu(Room):
    EAST_WEST = 0
    NORTH_SOUTH = 1

    def __init__(self, name, ID):
        super(Rotu,self).__init__(name, ID)
        
        self.NDOOR = Rotu_Door(Direction.NORTH)
        self.SDOOR = Rotu_Door(Direction.SOUTH)
        self.EDOOR = Rotu_Door(Direction.EAST)
        self.WDOOR = Rotu_Door(Direction.WEST)
        
        self.addFurniture(self.WDOOR, self.EDOOR)
        
        self.state = Rotu.EAST_WEST

    def rotate(self):
        AudioPlayer.playEffect(18)
        
        if self.state == Rotu.EAST_WEST:
            self.addAdjacent(Id.STUD)
            Player.getRoomObj(Id.STUD).addAdjacent(self.ID)
            self.addAdjacent(Id.IHA1) 
            Player.getRoomObj(Id.IHA1).addAdjacent(self.ID)
            self.removeAdjacent(Id.FOYW)
            Player.getRoomObj(Id.FOYW).removeAdjacent(self.ID)
            self.removeAdjacent(Id.LOOK)
            Player.getRoomObj(Id.LOOK).removeAdjacent(self.ID)
            
            self.removeFurniture(self.EDOOR.getID())
            self.removeFurniture(self.WDOOR.getID())
            self.addFurniture(self.NDOOR)
            self.addFurniture(self.SDOOR)
        else:
            self.addAdjacent(Id.FOYW)
            Player.getRoomObj(Id.FOYW).addAdjacent(self.ID)
            self.addAdjacent(Id.LOOK) 
            Player.getRoomObj(Id.LOOK).addAdjacent(self.ID)
            self.removeAdjacent(Id.STUD)
            Player.getRoomObj(Id.STUD).removeAdjacent(self.ID)
            self.removeAdjacent(Id.IHA1)
            Player.getRoomObj(Id.IHA1).removeAdjacent(self.ID)
            
            self.removeFurniture(self.NDOOR.getID())
            self.removeFurniture(self.SDOOR.getID())
            self.addFurniture(self.EDOOR)
            self.addFurniture(self.WDOOR)

        self.state ^= 1

    def getState(self):
        return self.state

    def triggeredEvent(self):
        if not Player.hasVisited(self.ID):
            GUI.out("\"What a foul stench of decay!\" You think to yourself as you enter this domed chamber.")
            
        return self.NAME



class Rotu_Rock(Furniture):
    def __init__(self):
        super(Rotu_Rock,self).__init__()

        self.description = ("It looks like marble. But where could one possibly accumulate all this marble from?")
        self.searchDialog = ("You are a lumberjack, not a miner.")
        self.addNameKeys("(?:polished )?(?:rock|marble)")



class Rotu_Sconce(Furniture):
    def __init__(self):
        super(Rotu_Sconce,self).__init__()

        self.description = ("It's a spherical light. It's so bright! And there " +
                           "looks not to be a bulb inside.")
        self.searchDialog = ("You're no wizard, but it's glass filled with " +
                            "some sort of magical gas or aether.")
        self.actDialog = ("Hmm... You really expected that to hurt, but it is quite cool " +
                         "to the touch. The gas is encapsulated, and you cannot obtain any.")
        self.addNameKeys("(?:spherical )?(?:sconces?|lights?)", "(?:magical )?(?:gas|aether)")
        self.addActKeys(Furniture.GETPATTERN, Furniture.HOLDPATTERN)



class Rotu_Sky(Furniture, Unmoveable):
    def __init__(self):
        super(Rotu_Sky,self).__init__()

        self.description = ("You gaze at the dark sky. The stars are bright and a bit of moonlight shines in.")
        self.searchDialog = ("Don't be silly.")
        self.addNameKeys("(?:dark )?sky")



class Rotu_Statue(Statue):
    def __init__(self):
        super(Rotu_Statue,self).__init__()
        self.description = ("The cloaked statues gloom over you with angry " +
                           "stares. Perhaps they were happier at one point when " +
                           "this room was cleaner? Surely any normal person would " +
                           "be opposed to keeping such sinister objects in their home.")
        self.actDialog = ("You feel the statue, but you feel discomforted in thinking " +
                         "that somehow, the other statues may be watching you.")
        self.addNameKeys("(?:cloaked )?(?:glaring )?statues?")



"""
    Rotates the rotunda when turned.
    Found in the fountain    
"""
class Rotu_Wheel(Furniture):
    def __init__(self):
        super(Rotu_Wheel,self).__init__()

        self.searchDialog = ("Nope, nothing. But there are interesting seams " +
                            "above and below the wheel.")
        self.description = ("Looking closely at the wheel, you spot a seam " +
                           "separating it from the main structure of the fountain.")
        self.actDialog = ("As you turn the wheel, your balance shifts and you hear a loud " +
                         "rumble. The room appears to have shifted.")
        self.addNameKeys("(?:stone )?wheel")
        self.addActKeys("turn", "rotate", "spin", "twist")

    def interact(self, key):
        Player.getRoomObj(Id.ROTU).rotate()
        return self.actDialog