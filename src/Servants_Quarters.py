from Furniture import SearchableFurniture, Moveable, Gettable, Furniture, Openable
from Structure_gen import StaticWindow
import AudioPlayer
from Item import Item
import re

class Squa_Bed(SearchableFurniture, Moveable):
    def __init__(self, itemList=[]):
        super(Squa_Bed,self).__init__(itemList)
        self.description = ("A plain single bed with a metal frame. The sheets are gone.")
        self.searchDialog = ("You crouch down and look under the bed.")
        self.actDialog = ("It's really not the time for sleeping now.")
        self.addNameKeys("bed", "plain bed", "single bed")
        self.addActKeys(Furniture.SITPATTERN)


        
class Squa_Candle(Furniture, Gettable):
    def __init__(self):
        super(Squa_Candle,self).__init__()

        self.description = ("A lit candle. The wax has hardly melted!")
        self.actDialog = ("Ouch! That's really hot!")
        self.addNameKeys("(?:lit )?(?:wax )?candle")
        self.addActKeys(Furniture.GETPATTERN, Furniture.HOLDPATTERN)

    def interact(self, key):
        if re.match(Furniture.HOLDPATTERN, key):
            AudioPlayer.playEffect(39, 30)
            return self.actDialog
        else:
            return self.getIt("You attempt to blow out the flame before taking it. As though " +
              "part of some elaborate prank, the flame refuses to die and thwarts your intention.")



class Squa_Desk(SearchableFurniture, Openable, Moveable):
    def __init__(self, itemList=[]):
        super(Squa_Desk,self).__init__(itemList)
        self.description = ("A plain wooden desk, resting flush against the " + 
                           "wall. On top is a small lit candle.")
        self.searchDialog = ("You slide open the drawer and peer inside.")
        self.actDialog = ("You give the desk a small kick. 'It's a good desk...' " +
                      "you think to yourself. It's definitely not as " +
                      "impressive as that desk in the vestibule, though.")
        self.addNameKeys("(?:plain )?(?:wooden )?desk")
        self.addActKeys(Furniture.JOSTLEPATTERN)



class Squa_Ladder(Item):
    def __init__(self, name, forms, thresh):
        super(Squa_Ladder, self).__init__(name, 0, forms=forms, thresh=thresh)
        self.useID = 1
        self.useDialog = ("This ladder has a couple rungs missing, and your " +
                         "short legs can't handle the gap.")



class Squa_Wardrobe(SearchableFurniture, Openable, Moveable):
    def __init__(self, itemList=[]):
        super(Squa_Wardrobe,self).__init__(itemList)
        self.description = ("A plain wooden wardrobe. It's built so modestly " +
                           "that it nearly brings a tear to your eye. Likely, " +
                           "it was once used by a servant or serf.")
        self.searchDialog = ("You open the wardrobe.")
        self.addNameKeys("(?:plain )?(?:wooden )?wardrobe")



class Squa_Window(StaticWindow):
    def __init__(self):
        super(Squa_Window,self).__init__()
        self.description = ("The barred window gives a view of the sea crashing " +
                           "against a cliff to the south of the castle. In the " +
                           "distance, you can see a lighthouse.")