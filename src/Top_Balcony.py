from Structure_gen import Column, Staircase
from Room import Room
import Direction, Id, AudioPlayer

class Tbal_Pillar(Column):
    def __init__(self):
        super(Tbal_Pillar,self).__init__()

        self.description = ("The wide column is about 20 feet wide and supports " +
                           "the enormous weight of the chamber to the north.")
        self.searchDialog = ("You can't reach it from here.")
        self.addNameKeys("(?:magnificent )?(?:wide )?(?:pillar|column)")



"""
    Superficial room, serves as access to the soul chamber.
    Connects to Soul and Tow2    
"""
class Tbal(Room):
    def __init__(self, name, ID):
        super(Tbal,self).__init__(name, ID)

    def getBarrier(self, direct):
        return ("The balcony railing is that way. It's a long drop to the sea.")



class Tbal_Stairs(Staircase):
    def __init__(self):
        super(Tbal_Stairs,self).__init__(Direction.UP, Id.TBAL, 15)

        self.description = ("The straight set of steps leads to a door giving " +
                  "entrance to the solemn building to the north.")
    
    def interact(self, key): 
        AudioPlayer.playEffect(15)
        return ("You slowly climb the set of steps.")