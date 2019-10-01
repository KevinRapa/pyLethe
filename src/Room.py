from Names import W_DIR, SEP
import AudioPlayer
from GUI import GUI
from RoomGraph import RoomGraph
import re

""" 
  Represents a room in the castle. 
  The player always has a defined attribute of integer coordinates which
  give access to furniture in the room when the player is at those coordinates.
   
  Each room has a unique ID string, roughly corresponding to the room name.
  The IDs uniquely identify the room for the purposes of getting coordinates
  and adjacent rooms. The ID is used by Keys as well.
   
  Rooms are adjacent to other rooms, which means that movement between them
  is possible. Two adjacent rooms are separated by empty space if the first 3 letters
  of their IDs match, excluding the caves and catacombs. Otherwise, they are
  separated by a door, unless they are on two different floors, e.g. connected
  by stairs.
   
  Rooms may be locked, which means that movement into them is not allowed unless
  the player carries a key with the matching ID number.
   
  Rooms have a triggeredEvent method, called whenever the player 
  enters. Generally, the method outputs the room name at least.
"""
class Room(object): 
    PATH = W_DIR + SEP + "data" + SEP + "desc" + SEP # Path to desc folder
    WALL_BARRIER = "There is a wall that way."
    EXT = ".txt"

    def __init__(self, name, ID):   
        self.ID = ID  # Unique 4-character ID
        self.NAME = name
        self.locked = False
        self.COORDS = RoomGraph.getCoords(self.ID) # Coordinates of this room
        self.ADJ = RoomGraph.getAdj(self.ID) # Rooms accessable from this one
        self.FURN = [] # Holds furniture
        self.desc = None

    def __str__(self): 
        return self.NAME 
    
    def __getstate__(self):
        odict = self.__dict__ 
        odict['desc'] = None
        return odict

    """
        Notifies player of incorrect direction and plays a sound.
        @return Standard dialog that player has moved towards a solid wall.
    """
    @staticmethod
    def bumpIntoWall():
        AudioPlayer.playEffect(6)
        return Room.WALL_BARRIER

    """
        Reads the room's description from a file. 
        Descriptions are not serialized.
        @param filename Name of the file containing this room's description.
        @return The room's description.
    """
    @staticmethod
    def _readDescription(filename):
        desc = "" 

        try:   
            with open(Room.PATH + filename, "r") as lines:
                descLine = lines.readline()

                while descLine:
                    desc += "  " + descLine
                    descLine = lines.readline()
        except:
            print("Could not find room description.")

        return desc

    def getID(self): 
        return self.ID 
     
    def getCoords(self): 
        return self.COORDS
    
    def getFurnRef(self, ID): 
        # Name must be a pattern name.
        for furniture in self.FURN: 
            if furniture.getID() == ID:
                return furniture
        
        return None
    
    def getDescription(self): 
        if not self.desc: 
            if re.match(self.ID, r"CT\d\d"): 
                self.desc = Room._readDescription("CT" + Room.EXT)
            else:
                self.desc = Room._readDescription(self.ID + Room.EXT)
        
        return self.desc
    
    """
        If the player fails a movement attempt, this returns the reason.
        Overridden if the room contains other barrier types (e.g. railing)
        @param dir A direction.
        @return Why the move failed.
    """
    def getBarrier(self, direct): 
        return Room.bumpIntoWall() 
    
    def getFurnishings(self): 
        return self.FURN
    
    def setLocked(self, locked): 
        self.locked = locked
    
    """
        Adds a room adjacent to this one.
        @param roomID A room to be added to adjacent.
    """
    def addAdjacent(self, roomID): 
        if not roomID in self.ADJ:
            self.ADJ.append(roomID)
    
    """
        Removes a room from self.adjacent.
        @param roomID A room to remove from adjacent.
    """
    def removeAdjacent(self, roomID): 
        try:
            self.ADJ.remove(roomID)
        except:
            print(roomID + " not found.")
    
    def removeFurniture(self, removeId): 
        for i in range(len(self.FURN)): 
            if self.FURN[i].getID() == removeId: 
                self.FURN.pop(i)
                return

        GUI.out("Suspicious: furniture to remove was not found.")
    
    def addFurniture(self, *furnishings): 
        self.FURN += furnishings
 
    """
        The event that occur whenever the player enters this room.
        @return A string default that says which room you are in.
    """
    def triggeredEvent(self): 
        return self.NAME
    
    def isLocked(self): 
        return self.locked 
    
    """
        Checks if a room is accessible from this one, used in movement.
        By 'accessible', is the destination separated by this room by either
        a door or empty space?
        @param destination A room ID.
        @return If room is adjacent to this one.
    """
    def isAdjacent(self, destination): 
        return destination in self.ADJ

    """
        Checks this room for a piece of furniture with the name.
        @param name the name of the furniture.
        @return If your location contains furniture with that name.
    """
    def hasFurniture(self, name):
        if type(name) is int:
            return self._hasFurnitureWithId(name)

        for furn in self.FURN:
            if furn.nameKeyMatches(name):
                return True
        return False
    
    def _hasFurnitureWithId(self, id): 
        for furn in self.FURN:
            if furn.getID() == id:
                return True
        return False
