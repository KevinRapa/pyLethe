from Names import PHYLACTERY
from Things import Carpet, Fireplace, WallArt, Safe
from Furniture import SearchableFurniture, Openable, Moveable, Furniture
from Item import Note, Book
import Id, Direction, AudioPlayer
from Player import Player
from Room import Room

class Stud_BookCase(SearchableFurniture, Moveable):
    def __init__(self, itemList=[]):
        super(Stud_BookCase,self).__init__(itemList)
        self.description = ("It's a small square bookcase with a stone head sculpture on top.")
        self.searchDialog = ("You peruse its shelves.")
        self.addNameKeys("(?:small )?(?:square )?(?:bookcase|bookshelf|shelf)", 
                "books", "(?:stone )?(?:head )?sculpture")



class Stud_BookPhylactery(Book):
    def __init__(self, name, score, filename):
        super(Stud_BookPhylactery,self).__init__(name, filename)
        self.type = PHYLACTERY
        self.score = score



class Stud_Carpet(Carpet):
    def __init__(self):
        super(Stud_Carpet,self).__init__()

        self.description = ("A thick red carpet. On top sits the writing desk and chair.")
        self.searchDialog = ("To your great curiosity, lifting up the carpet " +
                            "reveals a second identical carpet underneath.")
        
        self.addNameKeys("(?:thick )?(?:red )?(?:carpet|rug)")



class Stud_Couch(SearchableFurniture, Moveable):
    def __init__(self):
        super(Stud_Couch,self).__init__()

        self.description = ("A purple gothic-era couch. It looks way more fancy than comfortable.")
        self.searchDialog = ("You look underneath.")
        self.actDialog = ("You relax on the couch for a moment, staring at the " +
                         "portrait resembling Bob Gunton. It looks a bit crooked.")
        self.addActKeys(Furniture.SITPATTERN)
        self.addNameKeys("couch", "sofa")



class Stud_Desk(SearchableFurniture, Openable, Moveable):
    def __init__(self, itemList=[]):
        super(Stud_Desk,self).__init__(itemList)
        self.description = ("A fancy desk with curved legs. Its glossy surface reflects the glow of the fireplace. ")
        self.searchDialog = ("You slide open the drawer and peer inside.")
        self.actDialog = ("You give the desk a small kick. Though creaky and " +
                      "old, it's a good desk. Perhaps if you weren't trapped " +
                      "here, you'd take it home with you.")
        
        self.addActKeys(Furniture.JOSTLEPATTERN)
        self.addNameKeys("desk", "fancy desk")



class Stud_Fireplace(Fireplace):
    def __init__(self, bckt):       
        super(Stud_Fireplace,self).__init__(bckt)
        self.useDialog = ("That's probably not a good idea. It's the only thing lighting this room.")
        self.descLit = ("It's a small, fancy marble fireplace. The edges are an " +
                       "ornate wood. 'Magnificent!' you think to yourself. Its " +
                       "glow tones the room in a warm sepia.")

    def useEvent(self, item):
        return self.useDialog



class Stud_Portrait(WallArt):
    def __init__(self, safe):
        super(Stud_Portrait,self).__init__()
        self.SAFE_REF = safe
        self.description = ("The portrait depicts a bald male with round glasses, " +
                           "maybe fifty years old. He looks a bit like an angry " +
                           "Bob Gunton. 'Could this be a picture of Eurynomos?' you say " +
                           "to yourself. 'Wait, who's Bob Gunton?' you ask, but " +
                           "you hear no answer. With the light cast from the " +
                           "fireplace, it seems like this picture is not resting " +
                           "flush on the wall.")
        self.searchDialog = ("There's nothing on this picture. Interestingly, the " +
                            "portrait does not rest flush on the wall.")
        self.actDialog = ("You lift up the portrait resembling Bob Gunton, " +
                         "appropriately revealing a safe.")
        self.addNameKeys("portrait", "picture", "painting")

    def interact(self, key):  
        if key == "admire":
            return ("Yes, what a beautiful piece of artwork. You take a moment " +
                   "to soak in the creative essence. Yes...")
        elif not Player.getRoomObj(Id.STUD).hasFurniture("safe"):
            Player.getRoomObj(Id.STUD).addFurniture(self.SAFE_REF)
            return self.actDialog
        else:
            return ("You have already discovered the safe.")



"""
    Contains the first phylactery behind the painting, inside a safe.
    Safe password in the Pi book.
    Connects to Rotu.    
"""
class Stud(Room):
    def __init__(self, name, ID):
        super(Stud,self).__init__(name, ID)

    def getBarrier(self, direct):
        if direct == Direction.SOUTH:
            AudioPlayer.playEffect(6)
            return ("The door is missing!")
        else:
            return self.bumpIntoWall() 



"""
    Holds the first phylactery, a book.    
"""
class Stud_Safe(Safe):
    def __init__(self, combo, itemList=[]):
        super(Stud_Safe,self).__init__(combo, itemList)
        self.description = ("It's a black metal safe hidden in the wall!")