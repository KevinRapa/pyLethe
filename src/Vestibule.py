from Player import Player
from Mechanics import Button
from Furniture import SearchableFurniture, Furniture, Moveable, Openable
import Direction, Id, Menus, AudioPlayer
from Structure_gen import Door, Window
from Things import Fireplace, WallArt
from NonPlayerCharacter import NonPlayerCharacter
import re
from GUI import GUI
from Room import Room

class Vest_Button(Button):
    def __init__(self, ID):
        super(Vest_Button,self).__init__()
        self.description = ("You look closely at the small rock protrusion scorched from the heat of the fire. It's definitely a button.")
        self.FRPLC_ID = ID
        self.addNameKeys("(?:small )?(?:rock )?(?:protrusion|button)")

    def interact(self, key):
        return self.event(key)

    def event(self, key):
        frplc = Player.getPos().getFurnRef(self.FRPLC_ID)
        
        if frplc.isLit():
            AudioPlayer.playEffect(39, 30)
            return ("Ouch! There is fire in the way!")
        else:
            AudioPlayer.playEffect(11)
            AudioPlayer.playEffect(5)
            Player.getRoomObj(Id.FOY1).setLocked(False)
            return ("You push the button and hear a click behind you.")



class Vest_Case(SearchableFurniture, Openable, Moveable):
    def __init__(self, itemList=[]):
        super(Vest_Case,self).__init__(itemList)
        self.description = ("A white and blue ceramic case of Asian origin. The gold latch on its front looks unlocked.")
        self.searchDialog = ("You open the case and look inside.")
        self.addNameKeys("(?:white and blue |white |blue )?(?:ceramic )?case")



class Vest_Chair(Furniture, Moveable):
    def __init__(self):
        super(Vest_Chair,self).__init__()

        self.description = ("An ornate red velvet chair. Although a woodworker by trade, you have never been keen on upholstery.")
        self.searchDialog = ("You look underneath, but find nothing.")
        self.actDialog = ("You sit down in the chair, but not for long, for the chair is hard and uncomfortable.")
        self.addNameKeys("chairs?")
        self.addActKeys(Furniture.SITPATTERN)



class Vest_Desk(SearchableFurniture, Openable, Moveable):
    def __init__(self, itemList=[]):
        super(Vest_Desk,self).__init__(itemList)
        self.description = ("A tenuous wooden desk, resting flush against " +
                           "a dark corner. It collects dust from a lack of use. " +
                           "On it rests a strange, neglected glass orb. " +
                           "A single drawer is visible under its surface.")
        self.searchDialog = ("You slide open the drawer and peer inside.")
        self.actDialog = ("You give the desk a small kick. Though creaky and " +
                         "old, it's a good desk. Perhaps if you weren't trapped " +
                         "here, you'd take it home with you.")
        self.addNameKeys("(?:tenuous |dusty )?(?:wood(?:en)? )?desk")
        self.addActKeys(Furniture.JOSTLEPATTERN)



class Vest_Dr(Door):
    def __init__(self, direct):
        super(Vest_Dr,self).__init__(direct)
        self.description = ("A heavy wooden door. There seems to be a lot " +
                           "more mechanical works to this door than is typical.")



class Vest_EndTable(Furniture, Moveable):
    def __init__(self):
        super(Vest_EndTable,self).__init__()

        self.description = ("An round, ornate, wooden end table. A ceramic " +
                           "case rests on top.")
        self.searchDialog = ("The table does not seem to be hiding anything. " +
                            "The case on top looks tempting, however.")
        self.actDialog = ("Jostling the table a little, you find its " +
                         "craftsmanship impressive. The carvings on it are " + 
                         "equally such.")
        self.addNameKeys("(?:wood(?:en)? )?(?:end )?table")
        self.addActKeys(Furniture.JOSTLEPATTERN)



class Vest_Fireplace(Fireplace):
    def __init__(self, bckt):       
        super(Vest_Fireplace,self).__init__(bckt)

        self.descLit = ("A roaring fireplace. It engulfs the room with a " +
                       "warm, flickering glow. Looking more closely, you " +
                       "notice an odd protrusion in the back.")
        
        self.descUnlit = self.descUnlit + " It looks like there's a small button in the back."
        
        self.searchDialogUnlit = ("You can't see much but ash. There looks to be a " +
                                "small button in the back though.")



class Vest_Orb(NonPlayerCharacter):    
    def __init__(self):
        super(Vest_Orb,self).__init__()
        
        self.description = ("It's a dusty glass orb on the desk in the corner. " +
               "There's some sort of light coming from within. Did " +
               "this thing speak to you? Suddenly, a voice speaks- " +
               "\"Is staring at things a hobby of yours? Aren't you " +
               "going to say anything to me?\"")
        self.actDialog = (
                "You extend your hand out to grab the auspicious orb. A voice " +
                "then speaks before you reach it. \"Hey you! Do not taint my " +
                "window from this prison with your dirty hands. Say something " +
                "to me damn you!\"")
        self.searchDialog = ("You can't seem to find anything out of the " +
                  "ordinary. Suddenly, a voice speaks- " +
                  "\"Is staring at things a hobby of yours? " +
                  "Aren't you going to say anything to me?\"")

        self.addActKeys(Furniture.GETPATTERN)
        self.addNameKeys("(?:dusty )?(?:glass )?orb")
    
    def interact(self, key):       
        if re.match(NonPlayerCharacter.ATTACK_PATTERN, key):
            return NonPlayerCharacter.ATTACK_DIALOG
        elif re.match(Furniture.GETPATTERN, key):
            return self.actDialog
        elif self.firstTime:
            return self.converse1()
        else:
            return self.converse2()
    
    def converse1(self):
        GUI.menOut(Menus.ENTER)
        GUI.out("You open your mouth and utter a \"hullo\".")
        GUI.promptOut()

        GUI.out("\"Yes, hello. Thank you for coming over and talking to me. Others " +
                "seem to startle so easily, and I must guide them over here like " +
                "a small child...\"")
        GUI.promptOut()
        
        GUI.out("\"I... really don't think I could help you with that. It was " +
                "your choice to enter this room. Frankly, I don't quite know " +
                "where I am, or how long I've been in here.\"")
        GUI.promptOut()
        
        GUI.out("\"I'm afraid that doesn't help my good man there are many tall " +  
                "rooms with fireplaces here. Everybody who wanders here tells "  +
                "me something very similar. Seems so many get lost in the forest " +  
                "and expect some assistance here. Someone should be down "  +
                "sometime to assist, as someone always does, and I assume they " + 
                "just find their way home safely.\"")
        GUI.promptOut()
        
        GUI.out("\"... You're telling me you were invited here? Do you remember " + 
                "an invitation? How unusual. Most visit here vacuous and "  +
                "confused. I was hoping you'd be different.\"")
        GUI.promptOut()
        
        GUI.out("\"Well, I suppose I'm not too different. I feel fine, though " +
                "I must say that I'm quite ignorant of my situation. All I " +
                "remember is that my name is Rhadamanthus and that I studied " +
                "here. I have two brothers... Eurynomos and Asterion, but I " +
                "do not know their state. One or the other should be coming " +
                "to assist at some point, but you picked an inconvenient " +
                "time to visit.\"")
        GUI.promptOut()
        
        GUI.out("\"Ah, well... I lived with my two parents here- Tyre and "  +
                "Europa. But after they were gone, supported by their "  +
                "wealth and success, we turned our attention to magical " + 
                "study in order to help this kingdom and achieve their "  +
                "success. Hmph... I forgot I knew that.\"")
        GUI.promptOut()
        
        return ("\"Beyond that... I have only nebulous fragments of "  +
                "memory. I remember a discovery. I remember journey. " + 
                "But beyond that is a haze. Perhaps you could look "  +
                "around if you can figure out that door... I feel "  +
                "tired though. I'm sure you can find something to help you out.")
    
    def converse2(self):
        return ("I'm sure you can find something to help you out.")
    
    def moveIt(self):
        return "\"I am not a mere household decoration!\" The orb speaks. \"Be respectful and talk to me!\""



"""
    The first puzzle in the game, the player is locked in here upon entry and
    must find a way out.
    The room is escaped by opening the window and then pushing the button in
    the back of fireplace.
    Connects to Foy1.    
"""
class Vest(Room):
    def __init__(self, name, ID):
        super(Vest,self).__init__(name, ID)
        self.windowOpen = False

    def getDescription(self):
        if not self.windowOpen:
            return super(Vest,self).getDescription()
        else:
            return super(Vest,self).getDescription().replace("a closed", "an open", 1)

    def triggeredEvent(self):  
        # The check is in case player teleported here.
        if Player.getLastVisited() == Id.FOY1:
            # Locks the door to the foyer.
            AudioPlayer.playEffect(5)
            Player.getRoomObj(Id.FOY1).setLocked(True)

            if not Player.hasVisited(self.ID):
                GUI.out("You hear a click behind you. As you enter, you hear a " +
                        "whispering voice coming from the corner of the room. " +
                        "\'Hey! Over here, on the desk.\'")
            else:
                GUI.out("You hear a click behind you.")

        return self.NAME

    def switchWindow(self):
        self.windowOpen = not self.windowOpen



class Vest_Tpstr(WallArt):
    def __init__(self):
        super(Vest_Tpstr,self).__init__()
        self.description = ("A large, medieval-era tapestry. It appears to " +
                           "depict an impoverished man offering a glowing " +
                           "object to a king in a throne. The king appears " +
                           "curiously frail and famished.")
        self.addNameKeys("(?:large )?(?:medieval-era )?tapestry")



class Vest_Window(Window):
    def __init__(self, ID):
        super(Vest_Window,self).__init__()
        
        self.isOpen = False
        self.FIREPLACE_ID = ID
        self.escapeDialog = ("You would never be able to fit through those bars, and they're too thick to cut...")
        self.searchDialog = ("The only place to look is on the sill, but there's nothing there.")
        self.descOpen = ("It's an open, barred arched window of stone. A strong " +
                        "draft rolls in. From it, you can see the front " +
                        "courtyard surrounded by the rest of the castle " +
                        "and a tall front gate. ")
        self.descClosed = ("It's a closed, barred stone arched window with a " +
                          "small hole in the glass. A small gust of " +
                          "air forces its way through.")

    def interact(self, key):
        vest = Player.getPos() # Player must be in vesibule.
        frplc = vest.getFurnRef(self.FIREPLACE_ID)

        if key == "open" or key == "close":
            if self.isOpen and key == "close":
                self.close() 
                vest.switchWindow()
                AudioPlayer.playEffect(26)
                return ("You close the window.")
            elif not self.isOpen and key == "open":
                self.open()
                vest.switchWindow()
                AudioPlayer.playEffect(26)

                if frplc.isLit():
                    frplc.extinguish()
                    return ("You open the window. A strong gust comes through and extinguishes the fireplace.")
                else:
                    return ("You open the window.")
            else:
                return ("The window is already " + ("open" if key == "open" else "closed") + "!")
        else:
            return self.escapeDialog