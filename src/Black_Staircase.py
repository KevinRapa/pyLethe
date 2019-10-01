from GUI import GUI
from Player import Player
from Things import PottedPlant, Statue
from Room import Room
from Structure_gen import StaticWindow, Staircase, Balcony

class Bls1_Plants(PottedPlant):
    def __init__(self, soil, gift):
        super(Bls1_Plants, self).__init__(soil, gift)

        self.description = ("Many small potted plants, trees, and bushes decorate the " +
                           "atrium. They appear okay, but could afford a bit more care.")

        self.addNameKeys("plants?", "trees?", "bush(?:es)?")



class Bls1_Statue(Statue):
    def __init__(self):
        super(Bls1_Statue, self).__init__()
        
        self.description = ("The black statue depicts a malevolent-looking male " +
                           "holding a scepter and a chalice.")

        self.addNameKeys("(?:black )?statue")



# Superficial
class Bls2(Room):    
    def __init__(self, name, ID):
        super(Bls2, self).__init__(name, ID)

    def getBarrier(self, direct):
        return ("The iron railing on the balcony is that way.")

    def triggeredEvent(self):
        if not Player.hasVisited(self.ID):
            GUI.out("The throbbing in your head intensifies.")
            
        return self.NAME


class Bls_Balcony(Balcony):
    def __init__(self):
        super(Bls_Balcony, self).__init__()

        self.description = ("The iron upper-floor balcony is small and suspended from " +
                           "the ceiling against the east wall via several cables.")
        
        self.addNameKeys("(?:iron )?(?:balcony|railing)")


class Bls_Staircase(Staircase):
    def __init__(self, direct, dest):
        super(Bls_Staircase, self).__init__(direct, dest, 15)
        
        self.description = ("The long curved staircase wraps around in a half circle " +
                           "and connects the atrium floor to its second story balcony. " +
                           "It is suspended from the ceiling by many black metal cables.")

        self.addNameKeys("(?:long )?(?:curved )?(?:suspended )?(?:black )?(?:iron )?(?:stair(?:s|case)|steps)")

class Bls_Windows(StaticWindow):
    def __init__(self):
        super(Bls_Windows, self).__init__()

        self.description = ("The atrium is glassed in from floor to ceiling. To " +
                           "the west, you can see the rooftop garden from which " +
                           "you escaped the parlor. To the north, you see a terminal " +
                           "room higher up in the castle supported by a large pillar. " +
                           "The moon begins to fade and a small amount of light brightens " +
                           "the sky.")

        self.addNameKeys("ceiling|walls?|windows?|glass|moon|day")