from Things import WallArt, Statue
import Id, Direction, AudioPlayer
from Room import Room
from Structure_gen import Door
from Furniture import Furniture, Moveable
from Names import AQUAMARINE, RUBY
from Player import Player

class Jha1_Painting(WallArt):
    def __init__(self):
        super(Jha1_Painting,self).__init__()
        self.description = ("The painting depicts two elder males hunched over a desk, " +
                           "curiously observing a flask filled with an amber " +
                           "liquid. The table bears other alchemical instruments " +
                           "as well. The background is dark.")

        self.addNameKeys("painting", "picture")



class Jha2(Room):
    def __init__(self, name, ID):
        super(Jha2,self).__init__(name, ID)

        self.DOOR = Jha_HiddenDoor(Direction.WEST)
        self.desc2 = ("You stand at the south end of the hall near a " +
                     "southern door leading outside. The jade lion at the east " +
                     "stares at the newly formed door on the west wall. A lantern " +
                     "hangs in the center of the ceiling.")
        self.eyes = 0

    def lionCheck(self):
        self.eyes += 1
        if self.eyes == 2:
            self.addFurniture(self.DOOR)
            self.addAdjacent(Id.SST1)
            return (" At this moment, you hear a strange noise coming from close " +
                   "behind you. You turn and discover that mysterious door has " +
                   "materialized at the south end of the hallway.")
        else:
            return ""

    def getDescription(self):
        return (self.desc2 if self.hasFurniture("mysterious door") \
            else super(Jha2,self).getDescription())



class Jha_HiddenDoor(Door):
    def __init__(self, direct):
        super(Jha_HiddenDoor,self).__init__(direct)

        self.description = ("The newly formed arched door has a blue-tint to it " +
                           "and bears many curved etchings. Carved in the center " +
                           "is a sphere with a smoke or mist rising from the top.")
        self.addNameKeys("(?:mysterious |secret |hidden )door")



class Jha_Jade(Furniture):
    def __init__(self):
        super(Jha_Jade,self).__init__()

        self.description = ("The stone on the walls is smooth and polished. It's " +
                           "dark green with tenuous white veins seeping through it.")
        self.searchDialog = ("It's just solid rock.")
        self.addNameKeys("jade", "stone", "marble")



class Jha_Lantern(Furniture):
    def __init__(self):
        super(Jha_Lantern,self).__init__()

        self.description = ("The paper lantern hanging from the ceiling flickers and lights the room dimly.")
        self.searchDialog = ("You can't reach it. Probably for the best. It is no doubt flammable to a deadly degree.")
        self.addNameKeys("(?:hanging )?lanterns?")



class Jha_Lion(Statue, Moveable):
    DESC2 = ("It's a menacing jade statue of a lion. Sparkling " +
             "rubies sit in both its eye sockets. Strange that " +
             "someone decided to display them way back here where " +
             "no one can see them.")
    
    def __init__(self):
        super(Jha_Lion,self).__init__()

        self.hasRuby = False
        self.description = ("It's a menacing jade statue of a lion. A sparkling " +
                           "ruby sits in one of its eye sockets. The other socket " +
                           "is empty. Strange that someone decided to display " +
                           "them way back here where no one can see them. ")
        self.searchDialog = ("There don't seem to be any secret compartments " +
                            "on this statue. Although, one of the rubies sitting " +
                            "in its eye sockets has gone missing.")
        self.useDialog = ("You place the ruby into the lion's eye socket. The ruby glints and stays in place.")

        self.addNameKeys("(?:jade )?(?:lion )?statue", "(?:jade )?lion", "(?:lion'?s? )?eye")
        self.addUseKeys(RUBY, AQUAMARINE)
    
    def getDescription(self):
        return (Jha_Lion.DESC2 if self.hasRuby else self.description)
    
    def getSearchDialog(self):
        if self.hasRuby:
            return "There doesn't seem to be any secret compartments on this statue."
        else:
            return self.searchDialog
    
    def useEvent(self, item):
        if not self.hasRuby:
            if str(item) == AQUAMARINE:
                return ("You insert the blue gem into the socket, but it sits " +
                       "there only momentarily before falling out.")
            else:
                self.hasRuby = True
                AudioPlayer.playEffect(43)
                Player.getInv().remove(item)
                return self.useDialog + Player.getRoomObj(Id.JHA2).lionCheck()
        else:
            return ("There's no place to fit the " + str(item) + ".")
