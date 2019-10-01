from Room import Room
from Structure_gen import Staircase, Door
from Things import Statue
from Names import HAND_TORCH
from Furniture import Furniture, Unmoveable

"""
    Access to catacombs, a maze complex leading to the caves.
    Connects to Cs35 and Cry2
"""
class Cas1(Room):
    def __init__(self, name, ID):
        super(Cas1, self).__init__(name, ID)

    def getBarrier(self, direct):
        if direct == Direction.WEST:
            return ("The balcony edge is that way.")
        else:
            return self.bumpIntoWall()



class Cas_Stairs(Staircase):
    def __init__(self, direct, dest):
        super(Cas_Stairs,self).__init__(direct, dest, 15)
        
        self.description = ("The two curved stone staircases both lead " + str(direct) + ".")
        self.addNameKeys("curved (?:staircases?|stairs|steps)")



class Cs35_Door(Door):
    def __init__(self, direction):
        super(Cs35_Door, self).__init__(direction)
        
        self.description = ("The door is rounded and iron, with many large rivets around the perimeter.")
        self.addNameKeys("(?:round )?(?:iron |metal )?door")



class Cs35_Statue(Statue):
    def __init__(self):
        super(Cs35_Statue, self).__init__()
        self.description = ("The three robed males tower over you. Each bears in " +
                           "his hand what looks like an archaic key. The first " +
                           "male is bearded and wears a crown made of grass. " +
                           "The second is clean-shaven and holds a scepter. He " +
                           "wears the hat of a scholar. The third looks old and " +
                           "has a demonic presence to him. He holds a candelabra " +
                           "and wears an ostensibly metal crown.")
        self.searchDialog = ("The keys are just part of the statue.")

        self.addNameKeys("males?", "male statues?")



class Cs35_Torches(Furniture, Unmoveable):
    def __init__(self):
        super(Cs35_Torches, self).__init__()

        self.searchDialog = ("There's nothing behind the obelisks.")
        self.description = ("The tall obelisks burn brightly with a blue flame.")
        self.actDialog = ("There's no way you are going to touch that fire.")
        self.useDialog = ("Your torch is still lit, despite the fact that you've been carrying it all this time.")
        
        self.addNameKeys("(?:standing )?torch(?:es)?", "(?:bright )?(?:blue )?flame", "(?:tall )?obelisks")
        self.addActKeys(Furniture.GETPATTERN, "touch")
        self.addUseKeys(HAND_TORCH)
    
    def interact(self, key):
        if key == "touch":
            return self.actDialog
        else:
            return ("It's a standing torch. Too large and heavy to pick up.")