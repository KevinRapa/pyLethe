from Player import Player
from Furniture import SearchableFurniture, Moveable, Furniture, Unmoveable
from NonPlayerCharacter import NonPlayerCharacter
from GUI import GUI
import Id, Menus, AudioPlayer
from Names import GLOWING_EMERALD, WEAPON
from Room import Room
import re

class Drar_Bar(SearchableFurniture):
    def __init__(self, itemList=[]):
        super(Drar_Bar,self).__init__(itemList)
        
        self.description = ("Behind its solid oak table and chairs, you see a " +
                           "shelf populated with many kinds of alcohol.")
        self.searchDialog = ("You peruse the bar's shelves.")
        self.actDialog = ("A drink sounds like a good idea right about now. All the alcohol " +
                         "here must be stale and bitter by now though.")
        
        self.addActKeys(Furniture.SITPATTERN, "drink")
        self.addNameKeys("bar|shelf|alcohol|wine|beer|liquor")



class Drar_Billiards(SearchableFurniture, Moveable):
    def __init__(self, ID, itemList=[]):
        super(Drar_Billiards,self).__init__()
        self.GHOST_ID = ID
        self.description = ("The billiard table is clothed in the typical green, " +
                           "though the pockets are missing...")
        self.searchDialog = ("You look on the table's surface.")
        self.actDialog = ("What in the... this is a rich people's billiard table " +
                         "with no pockets. You can't play self.")
        self.addNameKeys("billiard table", "pool(?: table)?", "billiards")
        self.addActKeys("play", "use")
    
    def getSearchDialog(self):
        g = Player.getPos().getFurnRef(self.GHOST_ID)
        
        if g and g.firstTime():
            return ("Ignoring the ghost completely, you look on the billiard table's surface.")
        else:
            return self.searchDialog
    
    def interact(self, key):
        g = Player.getPos().getFurnRef(self.GHOST_ID)
         
        if g and g.firstTime():
            return ("Now is not the time for that. There's a ghost in here!")
        else:
            return self.actDialog



class Drar_Chess(SearchableFurniture, Moveable):
    def __init__(self, ID, itemList=[]):
        super(Drar_Chess,self).__init__(itemList)
        
        self.GHOST_ID = ID
        self.description = ("The fancy chess table bears a polished ceramic " +
                           "surface and many detailed pieces. You wish you " +
                           "knew how to play.")
        self.searchDialog = ("You look on the table's surface.")
        self.actDialog = ("'I aren't smart enough to play this' you speak softly in soliloquy.")
        self.addActKeys("play")
        self.addNameKeys("(?:fancy )?chess table", "chess")

    def getSearchDialog(self):
        g = Player.getPos().getFurnRef(self.GHOST_ID)
        
        if g and g.firstTime():
            return ("Ignoring the ghost completely, you search the chess table's surface.")
        else:
            return self.searchDialog

    def interact(self, key):
        g = Player.getPos().getFurnRef(self.GHOST_ID)
        
        if g and g.firstTime():
            return ("Now is not the time for that. There's a ghost in here!")
        else:
            return self.actDialog



class Drar_Couch(Furniture, Moveable):
    def __init__(self, ID):
        super(Drar_Couch,self).__init__()
        self.GHOST_ID = ID

        self.description = ("The Victorian-era couch is a bold green color. This " +
                           "one looks quite comfortable actually.")
        self.searchDialog = ("There's nothing hidden on this couch.")
        self.actDialog = ("This is the most comfortable couch you've sat in yet. " +
                              "Why haven't you grabbed a drink?")
        self.addActKeys(Furniture.SITPATTERN)
        self.addNameKeys("(?:(?:bold )?green )?(?:victorian-era )?couch")

    def getSearchDialog(self):
        g = Player.getPos().getFurnRef(self.GHOST_ID)
        
        if g and g.firstTime():
            return ("You do realize that there's a ghost in here, right?")
        else:
            return self.searchDialog
    
    def interact(self, key):
        g = Player.getPos().getFurnRef(self.GHOST_ID)
        
        if g and g.firstTime():
            return ("You do realize that there's a ghost in here, right?")
        else:
            return self.actDialog



"""
    NPC which assigns a task to the player in exchange for a couple items.
    Requests that player find an emerald from the trophy room.
    Gives key to kitchen as a reward and also a dark focus for the Gallery puzzle.
"""
class Drar_Ghost(NonPlayerCharacter):
    def __init__(self, ref1, ref2, ref3, ID):
        super(Drar_Ghost,self).__init__()
        self.DRKFCS_REF = ref1
        self.KITCKEY_REF = ref2
        self.EMRLD_REF = ref3
        self.BAR_ID = ID
        self.searchDialog = ("The ghost probably wouldn't appreciate that.")
        self.useDialog = ("It's a ghost- translucent and gaseous, sooo...")
        self.actDialog = ("The apparition returns to sipping from the ghostly cup.")
        self.description = ("The white apparition resembles a male dressed in " +
                           "robes wearing the hat of a scholar. His face is " +
                           "disfigured and horribly wrinkly.")
        
        self.addUseKeys(Furniture.ANYTHING)
        self.addNameKeys("ghost", "(?:white )?(?:apparition|ghost)", "him")

    def interact(self, key):
        if re.match(NonPlayerCharacter.ATTACK_PATTERN, key):
            return NonPlayerCharacter.ATTACK_DIALOG
        elif self.firstTime:
            self.converse1()
        elif not Player.hasItem(GLOWING_EMERALD):
            self.converse2()
        else:
            self.converse3()       
            return ("The apparition fades away into nothing.")
        
        return self.actDialog
    
    def useEvent(self, item):
        if str(item) == GLOWING_EMERALD:
            if self.firstTime:
                self.converse1()
            else:
                self.converse3()
            
            return Furniture.NOTHING
        else:
            return "\"No no, that's not it. It's green and should be glowing, as souls do.\""
    
    def converse1(self):
        self.firstTime = False
        
        GUI.out("Just as you do, the apparition interrupts " +
                "and begins to talk to you....")
        GUI.menOut(Menus.ENTER)
        GUI.promptOut()
        
        GUI.out("\"You are the first living soul I have seen in 6 centuries. " +
                "Well, excluding my brother Eurynomos, though he is not really " +
                "alive anymore. Do you know of whom I speak of? What is " +
                "your name even?...\"")
        GUI.promptOut()
        
        GUI.out("\"Is that so? Not a name I have heard before. " +
                "Certainly never during my time.\"")
        GUI.promptOut()
        
        GUI.out("I am Asterion. My family provided great services to this " +
                "kingdom, ever since my parents' overthrow of the corrupt " +
                "king Cronus. We offered freedom and knowledge to the " +
                "people of this land. But enough of me. Tell me, why by " +
                "the Gods are you here?")
        GUI.promptOut()
        
        GUI.out("You were invited here? Do you remember recieving an " +
                "invitation? Because if you did, you would never have " +
                "accepted it. Besides, this residence has not had " +
                "outgoing mail in centuries. No, this is not sensible...")
        GUI.promptOut()
        
        GUI.out("\"But then again, that does bring some questions to light. " +
                "The magic of Eurynomos is foreign to me. He is " +
                "impulsive willing to delve into any uncharted realm " +
                "of magic. Though I know little of the dark arts, I can " +
                "only imagine this is the result of it. Eurynomos is a " +
                "lich, and his mind should have melted to a pulp by now.\"")
        GUI.promptOut()
        
        GUI.out("\"Lichery, my friend, is taboo one of the most refrained " +
                "upon divisions of magic. A lich walks as the living do, " +
                "yet approaches death asymptotically, its mind and body " +
                "rotting slowly, and its soul never leaving. Lichdom is " +
                "a grand curse, and carries with it grim consequences.\"")
        GUI.promptOut()
        
        GUI.out("\"After our parents' death, we discovered a powerful, " +
                "infernal fountain of magic in the castle depths. It " +
                "birthed an artifact, named the Factum. We toyed with " +
                "its ability to distort the fabric of the universe. We " +
                "traveled many places. Many times. I soon identified it " +
                "as a danger, but Eurynomos was much too stubborn to agree.\"")
        GUI.promptOut()
        
        GUI.out("\"The magic, the Source, was a toxin. It corroded all our " +
                "minds here, and we began to forget. Before I knew it, " +
                "I was dead by Eurynomos' hands, and many others in the " +
                "castle followed. Eurynomos wished to live with the " +
                "artifact, and thus he lived on under the wretched Curse.\"")
        GUI.promptOut()
        
        GUI.out("\"But you are concerned with escape, not history. I would " +
                "like to help you, but I would also like you to do something " +
                "for me. As it turns out, Eurynomos bound me to a jewel. " +
                  "Though this castle houses my grave, it shall not be my " +
                  "resting place. I would like you to bring my the emerald " +
                  "so that I may destroy it.\"")
        GUI.promptOut()
        
        GUI.out("\"I know enough to say that the trophy room is off the " +
                "second floor gallery. I have something that is connected " +
                "to the unlocking mechanism. Please have it....\"")
        GUI.promptOut()
        
        GUI.out("\"... No I can't just walk in there because I'm a ghost. " +
                "Death has rules! We don't live in anarchy here...\"")
        GUI.promptOut()
        
        if Player.getInv().add(self.DRKFCS_REF):
            Player.printInv()
            GUI.out("The apparition hands you a dark tinted lens...")
        else:
            Player.getPos().getFurnRef(BAR_ID).getInv().add(self.DRKFCS_REF)
            GUI.out("... \"Huh, you sure like to carry around lots. " +
                      "I'll leave it here on the bar.\"")
        
        GUI.promptOut()
        GUI.toMainMenu()
        GUI.out("\"Please come back when you have the gem.\" ")

        return Furniture.NOTHING
    
    def converse2(self):
        GUI.out("\"Do you have the emerald yet? It's so " +
                "important to me. I will to repay you.\"")
        
        GUI.menOut(Menus.ENTER)
        GUI.promptOut()
        GUI.toMainMenu()
        
        return Furniture.NOTHING

    def converse3(self):       
        GUI.menOut(Menus.ENTER)
        GUI.out("\"Oh, you have found it! You have no idea what " +
                "this means to me. Oh, well I suppose you do. " +
                "As promised, I will help you find a way out " +
                "of here....\"")
        Player.getInv().remove(self.EMRLD_REF)
        GUI.promptOut()
        
        GUI.out("\"There is a rack of keys in the kitchen. I'm not sure " +
                "there's one that will get you out of here, but it will " +
                "open up more doors for you, quite literally. The kitchen " +
                "is locked, and I have the key.\"")
        GUI.promptOut()
        
        GUI.out("\"Eurynomos keeps a phylactery of his in the kitchen a fruit. He split " +
                "\"his soul among 5 objects, you know. One other is a scepter he " +
                "took from Rhadamanthus. The other three, well I don't rightfully know.\"")
        GUI.promptOut()
        
        GUI.out("The apparition drops a key into your palm...")
        Player.addKey(self.KITCKEY_REF)
        AudioPlayer.playEffect(3)
        Player.printInv()
        GUI.promptOut()
        
        GUI.out("\"Goodbye, my friend...\"")
        GUI.promptOut()
        GUI.toMainMenu()
        Player.getRoomObj(Id.DRAR).removeFurniture(self.getID())  
        Player.describeRoom()



class Drar_Piano(Furniture, Unmoveable):    
    def __init__(self):
        super(Drar_Piano,self).__init__()
        
        self.description = ("The wooden upright piano sits against the wall. The " +
                           "paint has begun to chip, but the piano still appears " +
                           "functional. A couple keys on the piano have gone missing.")
        self.actDialog = ("Egh... sounds terrible. You're no musician.")
        self.useDialog = ("You aren't sure what useful task would get done from that.")

        self.addNameKeys("(?:upright )?(?:brown )?piano", "(?:piano )?keys?")
        self.addUseKeys(Furniture.ANYTHING)
        self.addActKeys("play", "press", Furniture.SITPATTERN)
    
    def interact(self, key):              
        AudioPlayer.playEffect(53)
        return self.actDialog
    
    def useEvent(self, item):
        if item.getType() == WEAPON:
            return ("Now why would you want to destroy such a beautiful instrument?")
        else:
            return self.useDialog



"""
    Ghost NPC which the player interacts with is here.
    All other furniture is superficial.
"""
class Drar(Room):
    def __init__(self, name, ID):
        super(Drar,self).__init__(name, ID)
    
    def triggeredEvent(self):   
        if not Player.hasVisited(self.ID): 
            GUI.out("From across the room, an apparition stares at you with " +
                    "open eyes. You freeze and meet its stare with your own.")
        else:
            return self.NAME

    def getDescription(self):
        if self.hasFurniture("ghost"):
            return super(Drar, self).getDescription()
        else:
            return re.sub("A ghostly white.+recognize on it.",  
                    "You are in a relaxing lounge. A drinking bar furnishes the south of the room.", 
                    super(Drar, self).getDescription(), 1)



class Drar_Table(SearchableFurniture, Moveable):
    def __init__(self, ID, itemList=[]):
        super(Drar_Table,self).__init__(itemList)
        self.GHOST_ID = ID
        self.description = ("The low coffee table is glossy and clean.")
        self.searchDialog = ("You look on the table's surface.")
        self.actDialog = "How shameful it would be to dirty the table. Let's not touch it."
        
        self.addUseKeys(Furniture.JOSTLEPATTERN)
        self.addNameKeys("(?:low )?(?:coffee )?table")

    def getSearchDialog(self):
        g = Player.getPos().getFurnRef(self.GHOST_ID)
        
        if g and g.firstTime():
            return ("You comb the table's surface. You do realize there's a ghost " +
                     "in here, correct? Probably integral to the game's progression...")
        else:
            return self.searchDialog