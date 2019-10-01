from Things import Skeleton
from Furniture import Furniture, Unmoveable
from Names import FIXED_LADDER, METAL_LADDER

class Ou62_Skeleton(Skeleton):
    def __init__(self, itemList=[]):
        super(Ou62_Skeleton,self).__init__(itemList)
        
        self.description = ("The clean skeleton is well preserved and not missing " +
                           "a single bone. Whoever sent it down here must have " + 
                           "forgotten about it.")
    
    def getDescription(self):
        if self.inv.isEmpty():
            return self.description
        else:
            return (self.description + " It appears to be holding something.")



class Ou62_Spike(Furniture, Unmoveable):
    def __init__(self):
        super(Ou62_Spike,self).__init__()

        self.description = ("The spike is made of iron and is quite sharp. Much " +
                           "more interesting, of course, is the clean skeleton " +
                           "adorning the spike.")

        self.addNameKeys("(?:sharp )?(?:iron )?spike")



class Ou62_Straw(Furniture):
    def __init__(self):
        super(Ou62_Straw,self).__init__()

        self.description = ("It's just plain straw.")
        self.addNameKeys("straw", "hay")



"""
    Superficial. 
    Links to Ou62 in the catacombs.    
"""
class Oub1_Pit(Furniture):
    def __init__(self):
        super(Oub1_Pit,self).__init__()

        self.description = ("You peer over the 8-foot wide pit. The pit empties " +
                           "into blackness. You cannot see the bottom. For " +
                           "a transient moment, a small glint catches your eye " +
                           "from an unknown distance down.")
        self.actDialog = ("Probably nothing good will come of that.")
        self.useDialog = ("The ladder is just too short for that...")

        self.addNameKeys("(?:8-foot wide )?(?:pit|hole)")
        self.addActKeys("jump", Furniture.CLIMBPATTERN)
        self.addUseKeys(METAL_LADDER, FIXED_LADDER)