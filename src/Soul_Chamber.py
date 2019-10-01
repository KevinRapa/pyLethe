from GUI import GUI
import Id, Menus
from Names import PHYLACTERY
from Player import Player
from Furniture import Furniture
from Room import Room
from Lichs_Quarters import Lich_Room
from Things import Statue 
from Structure_gen import StaticWindow

class Soul_Pool(Furniture):
    def __init__(self, ID, lichRms):
        super(Soul_Pool,self).__init__()
        
        self.LICH_RMS = lichRms
        self.SPHERE_ID = ID
        self.numPhylacteries = 0
        
        self.description = ("The pool of aether swirls with white... stuff, and " +
                           "gently bubbles. The blue liquid inside " +
                           "is opaque, but can't be more than a couple feet deep.")
        self.actDialog = ("You leap into the pool and die. The end. Oh, the tragedy, " +
                         "having made it this far only to make such a stupid decision. " +
                         "That's how it would have been if you'd have actually jumped.")
        self.searchDialog = ("You just find a bunch of aether.")

        self.addNameKeys("pool", "pool of aether", "aether pool")
        self.addUseKeys(Furniture.ANYTHING)
        self.addActKeys("swim")
    
    def useEvent(self, item):
        Player.getInv().remove(item)
        
        if item.getType() == PHYLACTERY:
            self.numPhylacteries += 1
            
            if self.numPhylacteries == 5:
                self.killLich()
                return Furniture.NOTHING
        
        return ("You toss the " + str(item) + " into the glowing pool. The water bubbles " +
               "and a luminenscent gas escapes from the pool's surface.")
    
    def killLich(self):    
        GUI.menOut(Menus.ENTER)
        GUI.out("You stand before a pool of glowing aether, the very substance " +
                "which frees the dead of their earthly bodies.")
        GUI.promptOut()

        GUI.out("A short moment passes, and you cast the final phylactery " +
                "the pool. At that moment, the feeling of burden and dread " +
                "leaves you, and you feel comfortably alone. A burst of light " +
                "emerges from the pool and then disperses. The throbbing in your head ceases.")
        GUI.promptOut()
        GUI.toMainMenu()

        for r in self.LICH_RMS:
            r.killLich()

        Player.getRoomObj(Id.LQU1).addAdjacent(Id.LQU2)
        Player.getRoomObj(Id.TOW1).removeFurniture(self.SPHERE_ID)
        Player.getRoomObj(Id.TOW2).removeFurniture(self.SPHERE_ID)

        # Closes off areas to direct player out and avoid conflictions with night and day.
        Player.getRoomObj(Id.FOYC).removeAdjacent(Id.GAL1)
        Player.getRoomObj(Id.FOY3).removeAdjacent(Id.PAR2)
        Player.getRoomObj(Id.IHA2).removeAdjacent(Id.WOW2)
        Player.getRoomObj(Id.FOY1).removeAdjacent(Id.VEST)



class Soul_Statues(Statue):    
    def __init__(self):
        super(Soul_Statues,self).__init__()

        self.description = ("Each tall statue is dressed in mage's garb, but looks " +
                           "awfully morbid wrinkled, old, and close-to-death.")
        self.addNameKeys("(?:tall )?statues?")



class Soul_Window(StaticWindow):    
    def __init__(self):
        super(Soul_Window, self).__init__()
        
        self.description = ("The stained glass window depicts a grim image. An old " +
                           "wizard, it seems, looms over an ostensibly dying person. " +
                           "The persons mouth is open, and a bluish stream leaves the " +
                           "mouth and enters the wizard's mouth.")
        self.addNameKeys("stained-?glass window")