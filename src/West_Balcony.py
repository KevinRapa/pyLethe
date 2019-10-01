from Names import FIXED_LADDER
from Furniture import Furniture, Unmoveable
import Direction
from Room import Room

class Wbal_Beacon(Furniture, Unmoveable):
    def __init__(self):
        super(Wbal_Beacon,self).__init__()

        self.description = ("It's a ten foot high stone obelisk. At the top is " +
                           "a large bowl of flame. It's so bright, I'm sure one " +
                           "could see this from a long distance.")
        self.searchDialog = ("The beacon is too tall. Plus, it's on fire.")
        self.actDialog = ("Your body isn't optimized for that sort of activity.")
        self.useDialog = ("You think it better is stay as far from the roaring " +
                         "flame as possible. You wore your flammable overalls today.")
        
        self.addUseKeys(FIXED_LADDER)
        self.addActKeys(Furniture.GETPATTERN, "extinguish")
        self.addNameKeys("(?:ten foot (?:high )?)?(?:tall )?(?:stone )?(?:obelisk|beacon)")

    def interact(self, key):
        if key == "extinguish":
            return ("The beacon is too tall for that.")
        else:
            return self.actDialog



class Wbal_Forest(Furniture):
    def __init__(self):
        super(Wbal_Forest,self).__init__()

        self.description = ("The large expanse of trees(to the south until " +
                           "terminating at the foothills of a distant mountain. " +
                           "To the east, it wraps around and leads back to your village.")
        self.searchDialog = ("It's pretty dark and spooky. You can't even get to " +
                            "it from here anyway.")
        self.addNameKeys("(?:dark )?(?:forest|woods)")



"""
    The wooden rod for the fixed ladder can be found on the floor here.
    Connects to Wow1.    
"""
class Wbal(Room):
    def __init__(self, name, ID):
        super(Wbal,self).__init__(name, ID)

    def getBarrier(self, direct):
        if direct == Direction.WEST or direct == Direction.SOUTH:
            return ("There's a couple hundred foot drop right there.")
        else:
            return self.bumpIntoWall()