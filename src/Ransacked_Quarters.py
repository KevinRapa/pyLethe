from NonPlayerCharacter import NonPlayerCharacter
from Player import Player
import AudioPlayer
from Names import CROWBAR
from Item import Key, Item
from Furniture import SearchableFurniture, Moveable, Furniture, Openable
        
class Rqua_Bed(Furniture):
    def __init__(self):
        super(Rqua_Bed,self).__init__()

        self.moved = False
        self.description = ("It's a plain, wooden bedframe. The mattress has been thrown off. A tile beneath " +
                            "the bed looks suspicious.")
        self.searchDialog = ("Nothing here. It's a bad place to hide something, " +
                            "as someone has already searched it. A tile beneath " +
                            "the bed looks suspicious, though.")
        self.actDialog = ("You move the bed out of the way, exposing a loose tile. " +
                         "The woman in the room keeps grinning wildly at you.")
        self.addNameKeys("(?:flimsy )?(?:metal )?(?:bedframe|bed)")
        self.addActKeys(Furniture.MOVEPATTERN, Furniture.SITPATTERN)

    def interact(self, key):  
        if re.match(Furniture.MOVEPATTERN, key):
            if not self.moved:
                self.moved = True
                AudioPlayer.playEffect(41)
                return self.actDialog
            return ("You have already moved the bed.")
        else:
            return ("This bed looks most uncomfortable.")

    def isMoved(self):
        return self.moved



class Rqua_Clothes(Furniture):
    def __init__(self):
        super(Rqua_Clothes,self).__init__()
        
        self.LINENS = Item("wrinkled sheet", 0, "A carelessly thrown about bed linen that you found in the servant's wing.")
        self.description = ("Wrinkled sheets and clothes lie on the floor, tossed from the now emptied dresser.")
        self.actDialog = ("It is not an appropriate time for dress-up.")
        self.searchDialog = ("There isn't anything hidden inside the clothes.")

        self.addNameKeys("(?:scattered )?(?:clothes|linens?)")
        self.addActKeys(Furniture.GETPATTERN)
        self.addActKeys("wear")
    
    def interact(self, key):              
        if key == "wear":
            return self.actDialog
        elif Player.getInv().add(LINENS):
            return ("You pick up one of the large scattered linens")
        else:
            return ("You already carry enough useless sundries.")



class Rqua_Dresser(Furniture, Openable, Moveable):
    def __init__(self):
        super(Rqua_Dresser,self).__init__()

        self.description = ("It's a low dresser with a couple opened drawers in it.")
        self.actDialog = ("There's no reason to do that...")
        self.searchDialog = ("Seems like a bad place to hide something, as someone has already searched it.")
        self.addActKeys("close")
        self.addNameKeys("(?:low )?dresser")  



class Rqua_Mattress(Furniture, Moveable):
    def __init__(self):
        super(Rqua_Mattress,self).__init__()

        self.description = ("It's a debris-covered mattress thrown carelessly on the floor.")
        self.searchDialog = ("Nothing here. It's a bad place to hide something, " +
                            "as someone has already searched it.")
        self.actDialog = ("It's really not the time for sleeping now.")
        self.addNameKeys("mattress", "debris-covered mattress")
        self.addActKeys(Furniture.SITPATTERN, "lift")

    def interact(self, key):
        return (self.moveIt() if key == "lift" else self.actDialog) 

    def moveIt(self):
        return ("Lifting the mattress reveals nothing useful.")



"""
    Pried using a crowbar to give the player a key.    
"""
class Rqua_Panel(Furniture):
    def __init__(self, studKey, ID):
            super(Rqua_Panel,self).__init__()
            
            self.lifted = False
            self.STUDKEY_REF = studKey
            self.BED_ID = ID
            self.description = ("The tile underneath the bed looks loose.")
            self.searchDialog = ("You'll have to lift this up first.")
            self.actDialog = ("It's too heavy and awkward to remove with your hands. " +
                                  "You'll need to find something to pry this up.")
            self.useDialog = ("The crowbar fits! You successfully remove the tile, " +
                             "revealing a small molded key which you take. The " +
                             "woman speaks: \"Now you will know his secret!!\"")
            self.addNameKeys("tile", "panel")
            self.addActKeys("pry", "move", "lift", "remove")
            self.addUseKeys(CROWBAR)

    def useEvent(self, item):
        b = Player.getPos().getFurnRef(self.BED_ID)
        
        if not self.lifted and b.isMoved():
            self.lifted = True
            Player.addKey(self.STUDKEY_REF)
            AudioPlayer.playEffect(3)
            return self.useDialog
        elif not b.isMoved():
            return "You fully intend to do that, but there is a bed in the way."
        else:
            return "You have already removed the tile."

    def interact(self, key):     
        if Player.getPos().getFurnRef(self.BED_ID).isMoved():
            return ("You have already lifted the tile." if self.lifted else self.actDialog)
        else:
            return ("You will try that, but there is a bed in the way.")



class Rqua_Table(SearchableFurniture, Moveable):
    def __init__(self):
        super(Rqua_Table,self).__init__()

        self.description = ("The plain wood end table lies on its side.")
        self.actDialog = ("The table has been fooled around with enough. Best leave it alone...")
        self.searchDialog = ("Nothing here. It's a bad place to hide something, " +
                            "as someone has already searched it.")
        self.addActKeys(Furniture.JOSTLEPATTERN)
        self.addNameKeys("(?:plain )?(?:wood(?:en)? )?(?:end )?table")



class Rqua_WomanNPC(NonPlayerCharacter):
    def __init__(self):
        super(Rqua_WomanNPC,self).__init__()

        self.description = ("The elderly woman sits on the floor in a corner " +
                           "garbed in black robes which cover all her body save " +
                           "her face. She keeps her unsettling glare on you and " +
                           "laughs quietly to herself.")
        self.actDialog = ("*A deranged laugh* \"We all forget, so why measure oneself " +
                         "with impalpable knowledge when we have our wealth???? Eury " +
                         "does not know my secret!!! All his riches can be mine at my " +
                         "pleasure!!!! Hell treats the wealthy comfortably and the wise " +
                         "with contempt!!!!\"")
        self.searchDialog = ("Approaching her seems like a dangerous thing to do.")

        self.addNameKeys("(?:elderly )?(?:laughing )?(?:robed )?(?:woman|lady)", "her")
    
    def interact(self, key):              
        if self.firstTime:
            self.firstTime = False
            return self.converse1()
        else:
            return self.converse2()
    
    def converse1(self):
        return self.actDialog
    
    def converse2(self):
        return ("Hell treats the wealthy comfortably and the wise with contempt!!!\"")
