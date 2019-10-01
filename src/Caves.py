from Names import HAND_TORCH, SEP, W_DIR 
import Id, AudioPlayer
from Player import Player
from Structure_gen import Floor, Door
from Room import Room
from Furniture import Gettable, SearchableFurniture, Furniture
from Item import Item
import math, random

"""
    The caves comprise a maze of similar tunnels.
    The caves will generate their own descriptions and will distort their own
    descriptions to a degree determined by its distance from room MS66. The
    reason for this is story-based.    
"""
class Cave(Room):    
    DISTORTION = open(W_DIR + SEP + "data" + SEP + "ambience" + SEP + "caveDistortion.wav", "r")

    def __init__(self, ID, wall, ceiling):
        super(Cave,self).__init__("Cave network", ID)
        X, Y = self.COORDS[2], self.COORDS[1] # X and Y coordinates of this room.

        self.DISTANCE = round(math.sqrt(abs(5 - X) ** 2) + (abs(6 - Y) ** 2))
        descB = ""
        descL = ""
        
        if self.DISTANCE in (7, 6, 5):
            descL += "You feel inexplicably dizzy."
        elif self.DISTANCE == 4:
            descL += "You can feel the dizzyness intensifying."
        elif self.DISTANCE == 3:
            descL += "Your head begins to hurt, and the dizzyness intensifies."
        elif self.DISTANCE == 2:
            descL += "You feel delirious, and your senses begin to numb."
        else:
            descL += "You start slipping into an acute dementia, and you can barely orient yourself."
        
        descB += descL
        
        descB += (" This area is pitch black just like the level above. " +
                 "It's uncomfortably cold, and you hear nothing but " +
                 "drops of water and an awful racket deep within the tunnels.")
        
        descL += (" The torch lights a short way ahead. This area is much " +
                 "like above, though the walls and floor are plain rock. " +
                 "You can hear an awful noise deep within the tunnels. " +
                 "                                         To the ")
        
        """
            Builds the lit description of the room. Here, the constructor figures
            out what is in each direction of the caves. The description will
            reflect if there if empty space or a door in any direction.
        """
        
        # List of X and Y coordinates of the adjacent cave rooms.
        adjCaveCoords = []
        
        # Holds directions to append to descLit.
        dirs = []
        
        for i in self.ADJ:
            coords = int(i[2]), int(i[3])
            adjCaveCoords.append(coords)
        
        # Figures out the directions in which there are more catacombs.
        for j in adjCaveCoords:
            if j[0] == Y - 1:
                dirs.append("NORTH")
            elif j[0] == Y + 1:
                dirs.append("SOUTH")
            elif j[1] == X - 1:
                dirs.append("WEST")
            elif j[1] == X + 1:
                dirs.append("EAST")

        # Appends the correct directions to descLit.
        length = len(dirs)
        
        if length == 1:
            descL += dirs[0]
        elif length == 2:
             descL += dirs[0] + " and " + dirs[1]
        else:
            i = 0 
            while i < length - 1:
                descL += (dirs[i] + ", ")
                i += 1

            descL += "and " + dirs[i]
        
        descL += ", the tunnel veers into darkness. "

        self.descLit = descL
        self.descUnlit = descB
        self.addFurniture(Floor("The floor is cold hard rock and uninteresting."), wall, ceiling)

    def getDescription(self):
        if Player.hasItem(HAND_TORCH):
            return distortDescription(self.DISTANCE, self.descLit)
        else:
            return distortDescription(self.DISTANCE, self.descUnlit)

    """
        Plays hellish music at volume respective to player's distance from MS65.
        @return distorted room name.
    """
    def triggeredEvent(self):
        """
        if clip:
            Cave.stopClip()
        
        clip = AudioSystem.getClip()
        clip.open(AudioSystem.getAudioInputStream(DISTORTION))
        
        ((FloatControl)clip.getControl(FloatControl.Type.MASTER_GAIN))
                .setValue(-(self.DISTANCE ** 2))
        
        clip.loop(Clip.LOOP_CONTINUOUSLY)
        clip.start()

        if Player.hasItem(HAND_TORCH): 
            return Cave.distortDescription(self.DISTANCE, NAME)
        else:
            "???")
        """

    """
           Scrambles the string to a degree based on DISTANCE.
           @param degree the degree to which distort the description.
           @param desc A string to distort.
        @return a scrambled string.
    """
    @staticmethod
    def distortDescription(degree, desc):
        desc = desc
        length =len(desc)
        
        if degree == 7: 
            return desc # Degree 7 will not distort at all.
        
        for d in range(42, degree*7, -2):
            i = random.randint(0, length-1)
            j = random.randint(0, length-1)
            Cave.swapChars(desc, i, j) 
            desc[GENERATOR.nextInt(length)] += 20 # Shifts character up the unicode set.

        return desc

    @staticmethod
    def swapChars(array, i, j):
        temp = array[i]
        array[i] = array[j]
        array[j] = temp

    @staticmethod
    def stopClip():
        if clip:
            clip.stop()



"""
    Contains a well which is related to story.
    Connects to catacombs.
"""
class CV34(Cave):
    def __init__(self, name, ID, wall, ceiling):
        super(CV34, self).__init__(ID, wall, ceiling)
        self.descUnlit = ("You've found your way to an open area... There's something " +
                         "in the center. It feels stone, round and empty in the center.")
        self.descLit += ("This area is more open and circular than " +
                        "the rest of the cave. A round well stands in the center.")


"""
    The 'Source'
"""
class Cv_Well(Furniture):
    def __init__(self):
        super(Cv_Well, self).__init__()

        self.actDialog = ("That is definitely not a good idea!")
        self.description = ("You peer down the well. It seems to go on for a couple " +
                           "hundred feet. A bright green glow emanates from far below. ")
        self.searchDialog = self.description

        self.addNameKeys("(?:ancient )?well")
        self.addActKeys("jump", Furniture.CLIMBPATTERN)
    
    def getDescription(self):
        return Cave.distortDescription(4, description)
    
    def getSearchDialog(self):
        return self.getDescription()
    
    def interact(self, key):
        return Cave.distortDescription(4, actDialog)



"""
    This room distorts all descriptive output.
    The player must take the magic factum from this room, having prior knowledge
    that the factum is in here.    
"""
class Deep_Chamber(Room):

    def __init__(self, name, ID):
        super(Deep_Chamber, self).__init__(name, ID)

    def getBarrier(direct):
        return Cave.distortDescription(2, bumpIntoWall())

    def getDescription(self):
        return Cave.distortDescription(1, super(Deep_Chamber, self).getDescription())

    def triggeredEvent(self):
        Cave.stopClip()
        return Cave.distortDescription(1, self.NAME)



"""
    Responds to all strings the player types and is used to prevent undistorted
    descriptions from displaying in MS65 and MS66.
"""
class Dummy_Furniture(Furniture):
    def __init__(self):
        super(Dummy_Furniture, self).__init__()
        
        self.description = ("a5 ojkvjkljelzx sf093knf k4kgjg094ng nvkjrhniog9 9ug " +
                           "fe 0e08 fjkSEJKO f0ej HEWBK9 jfe90 kfjnks FLeosj selg " +
                           "wnmf 9f pg e9kf smn kfejp0fuesi3 ,n kk34p uofej9 yhfhbe.")
        
        self.addNameKeys(Furniture.ANYTHING) # Any non-empty string matches self.
        self.addUseKeys(Furniture.ANYTHING)
        self.addActKeys(Furniture.ANYTHING)
     
    def getDescription(self):
        return Cave.distortDescription(1, self.description)
    
    def getSearchDialog(self):
        return self.getDescription()
    
    def interact(self, key):              
        return self.getDescription()
    
    def useEvent(self, item):
        return self.getDescription()


"""
    The player must take this in the Deep Chamber to obtain the factum.
    This removes itself from this room once interacted with.    
"""
class FactumDummy(SearchableFurniture, Gettable):
    def __init__(self, ref):
        super(FactumDummy, self).__init__(ref)
        
        self.FACTUM_REF = ref
        self.description = ("You can't concentrate, your headache is too overwhelming.")
        self.actDialog = ("You fumble around and grab the artifact.")
        self.searchDialog = self.description

        self.addNameKeys(Furniture.ANYTHING)
        self.addActKeys(Furniture.ANYTHING)
    
    def getDescription(self):
        return Cave.distortDescription(5, self.description)
    
    def getSearchDialog(self):
        return Cave.distortDescription(1, self.searchDialog)
    
    def interact(self, key):
        Player.getInv().forceAdd(self.FACTUM_REF) # Forces itself in.
        Player.printInv()
        Player.getPos().removeFurniture(self.getID())
        Player.getRoomObj(Id.EOW1).setLocked(False)
        return Cave.distortDescription(3, self.actDialog)



"""
    This item teleports the player to a room in the castle that the player has
    visited.
    Used to access the Vault.
"""
class Factum(Item):
    def __init__(self, name, score):
        super(Factum, self).__init__(name, score)
        self.useID = 1
        self.type = ("phylactery")
        self.description = ("You find that you can't describe it very well. It's " +
                           "quite light and keeps folding in on itself- changing " +
                           "shape. You can't recognize the color either. Almost ultraviolet.")
        self.useDialog = ("You've just moved. You aren't quite sure how you did that.")
    
    """
       Displays the player's coordinates in the GUI output window.
       The coordinates are Cartesian, with the 1st floor being z = 0 and
       the top row of rooms in the map array being y = 6.
       @return coordinates of the player.
    """
    def useEvent(self):
        Cave.stopClip()
        AudioPlayer.playEffect(49)
        pos = Player.getPosId()

        if pos == Id.CHA2:
            Player.setOccupies(Id.VAUE)     
        elif pos == Id.VAUE:
            Player.setOccupies(Id.CHA2) 
        else:
            Player.teleport() 

        if Player.getPosId() == Id.HADS: 
            return ("The player is dissatisfied with their fate and makes a daring " +
                  "escape, foiling the devil itself in an instant.")
        else:
            return self.useDialog


class OminousDoor(Door):
    def __init__(self, direction):
        super(OminousDoor, self).__init__(direction)
        
        self.description = ("This door is carved decoratively all over, but is " +
                           "heavily dilapidated. Much of the rock has crumbled " +
                           "off.")