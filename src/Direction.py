"""
    Represents a simple direction in the game.
    Used with movement and doors.    
"""
class Direction(object):
    def __init__(self, ID, x, y, z):
        self.ID = ID                     # String representation of the direction. 
        self.X, self.Y, self.Z = x, y, z # Positive or negative direction to move in the array.
       
    def __str__(self):
        return self.ID

    def __eq__(self, other):
        return str(self) == str(other)

NORTH = Direction("north", 0, -1, 0) 
SOUTH = Direction("south", 0, 1, 0) 
EAST  = Direction("east", 1, 0, 0) 
WEST  = Direction("west", -1, 0, 0) 
UP    = Direction("up", 0, 0, -1) 
DOWN  = Direction("down", 0, 0, 1)
BOTH  = Direction("both", 0, 0, 0)
NE    = Direction("northeast", 0, 0, 0) 
NW    = Direction("northwest", 0, 0, 0) 
SE    = Direction("southeast", 0, 0, 0) 
SW    = Direction("southwest", 0, 0, 0)