from Structure_gen import Column, Balcony, Door, Ceiling
import Direction
from Room import Room
from Things import Statue

class Entr_Balcony(Balcony):
    def __init__(self):
        super(Entr_Balcony,self).__init__()
        
        self.description = ("The balcony(many feet ahead to the front " +
                           "door. Past the railings on either side give view to " +
                           "the brambles of vegetation about 13 feet below.")

        self.addNameKeys("long balcony")



class Entr_Columns(Column):
    def __init__(self):
        super(Entr_Columns,self).__init__()
        self.description = ("The four-foot wide columns extend a couple stories " +
                         "up. They look like more than enough to hold up that roof.")

        self.addNameKeys("(?:four-foot )?(?:wide )?(?:columns?|pillars?)")



class Entr_Door(Door):
    def __init__(self, direct):
        super(Entr_Door,self).__init__(direct)
        self.description = ("The castle's front doors are quite impressive. They " +
                           "are tall a couple stories, and look to be made of " +
                           "pine wood with large iron hinges. Their knobs amuse " +
                           "you however, as they look way too minuscule to be " +
                           "appropriate for doors of this magnitude.")
        self.addNameKeys("front doors?")



"""
    Superficial.
    Front entrance of the castle.    
"""
class Entr(Room):
    def __init__(self, name, ID):
        super(Entr,self).__init__(name, ID)

    def getBarrier(self, direct):
        if direct == Direction.EAST or direct == Direction.WEST:
            return ("There's just a railing that way.")
        else:
            return ("There's a wall in the way.")



class Entr_Roof(Ceiling):
    def __init__(self):
        super(Entr_Roof,self).__init__()
        self.description = "The portico is shaded by an elongated mansard roof extending from the castle's front wall."



class Entr_Statues(Statue):
    def __init__(self):
        super(Entr_Statues,self).__init__()
        self.description = ("The six statues are all of ominous cloaked figures. " +
                "These are in much better condition than the ones in the courtyard.")
