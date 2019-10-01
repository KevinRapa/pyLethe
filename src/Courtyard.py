from Player import Player
from Room import Room
from Furniture import *
from Structure_gen import Staircase, Floor
import Id, Direction, AudioPlayer
from Names import *
from GUI import GUI
from NonPlayerCharacter import NonPlayerCharacter
from Patterns import YES_NO_P
from Things import Statue
from Inventory import Inventory
from Item import Note, Item
import re, random

MAP = {
    "ac" : 1, "tw" : 2, "th" : 3, "fo" : 4, "fi" : 5, "si" : 6, "se" : 7, 
    "ei" : 8, "ni" : 9, "te" : 10, "ja" : 10, "qu" : 10, "ki" : 10
}

class Card(Item):    
    """
        The card's type is used in removing them all from your inventory between games.
        @param name The name of the card.
    """
    def __init__(self, name):
        super(Card,self).__init__(name, 0)
        self.type = CARD
        self.description = ("A ghostly and eerily solid playing card. It feels cool to the touch.")
        self.VALUE = self.determineValue(name[0,2])
    
    """
        Determines the value of each card using the hash map.
        For aces, the value is one, however if the value 11,is advantageous
        during a game, that value is used instead. Face cards are worth 10,
        all numbered ranks use their own value.
        @param name The first two letters of a card's name.
        @return The card's value.
    """
    @staticmethod
    def determineValue():
        return MAP[name]
    
    def getVal(self):
        return self.VALUE



class Courtyard_Growth(Furniture):
    def __init__(self):
        super(Courtyard_Growth,self).__init__()

        self.addUseKeys("\\w* (?:ax|sword)", SCYTHE, HAND_TORCH, HOE)
        self.addActKeys("grab|touch|hold", "cut|chop|prune|remove")
    
    def interact(self, key):              
        if re.match("grab|touch|hold", key):
            return self.actDialog
        else:
            return ("With your hands???")
    
    def useEvent(self, item):
        i = str(item)
        
        if i == HAND_TORCH:
            return self.useDialog
        elif i == HOE:
            return ("You aren't a gardener!")
        else:
            return self.cutDialog



class Cou_Floor(Floor, Gettable):
    def __init__(self, ref1, ref2, ref3, itemList=[]):
        super(Cou_Floor,self).__init__("The ground is a mixture of grass, weeds, and clover.", itemList=[])

        self.SOIL_REF = ref1
        self.GRASS_REF = ref2
        self.CLOVER_REF = ref3
        
        self.actDialog = ("You dig a small hole in the ground, but find nothing of interest " +
                         "and kick the dirt back in the hole.")
        self.useDialog = ("You have nothing with which to dig.")

        self.addNameKeys("dirt|earth", SOIL, GRASS, "weeds?|clovers?")
        self.addUseKeys(SHOVEL, TROWEL, HOE)
        self.addActKeys(Furniture.GETPATTERN, "dig", SHOVEL)
    
    def interact(self, key):
        if key == "dig" or key == SHOVEL:
            if Player.hasItem(SHOVEL) or Player.hasItem(TROWEL):
                i = Player.getInv().get(SHOVEL)
                
                if i == Inventory.NULL_ITEM:
                    i = Player.getInv().get(TROWEL)
                
                return self.useEvent(i)
            else:
                return self.useDialog
        else:
            return self.getIt()
    
    def getIt(self):
        i = Player.getInv()
        
        if i.add(self.SOIL_REF) and i.add(self.GRASS_REF) and i.add(self.CLOVER_REF): 
            return ("You jam your fingers into the ground and grab a fistful of Earth.")
        else:
            return ("You have full pockets.")
    
    def useEvent(self, item):
        if str(item) == HOE:
            return ("You aren't a gardener!")
        else:
            AudioPlayer.playEffect(34)
            return self.actDialog




class Courtyard_Fountain(SearchableFurniture, Unmoveable):
    def __init__(self, itemList=[]):
        super(Courtyard_Fountain,self).__init__(itemList)
        
        self.actDialog = ("There's not even any water in here!")
        self.searchDialog = ("You search through its basin.")
        self.useDialog = ("You better not just waste that water you brought all the way here..")

        self.addNameKeys("(?:ancient )?(?:empty)?(?:stone )?(?:fountain|basin)")
        self.addUseKeys("bucket of water", "\\w* coins?")
        self.addActKeys("swim", "drink")
    
    def useEvent(self, item):
        if re.match("\\w* coins?", str(item)):
            Player.getInv().give(item, self.inv)
            return ("You flick the coin in and wish yourself out. Alas, you are still here.")
        else:
            return self.useDialog
            


class Cou1_Bench(Furniture, Unmoveable):
    def __init__(self):
        super(Cou1_Bench,self).__init__()

        self.description = ("The bench is blanketed in multiflora. Its backrest " +
                           "lies on the ground behind it.")
        self.searchDialog = ("You aren't risking getting pricked by those thorns.")
        self.actDialog = self.searchDialog
        self.addActKeys(Furniture.SITPATTERN, Furniture.JOSTLEPATTERN, Furniture.MOVEPATTERN)
        self.addNameKeys("(?:ruined )?(?:stone )?bench")

    def interact(self, key):
        if re.match(Furniture.SITPATTERN, key):
            return self.actDialog
        elif re.match(Furniture.JOSTLEPATTERN, key):
            return ("You give it a nudge. 'Sure is sturdy!' You think to yourself.")
        else:
            return ("It's solid stone and heavy. You can't move it.")



"""
    The player digs a hole here to find a brass plate needed for Observatory puzzle    
"""
class Cou1_Floor(Cou_Floor):
    def __init__(self, ref1, ref2, ref3, ref4, itemList=[]):
            super(Cou1_Floor,self).__init__(ref1, ref2, ref3, itemList=[])
            
            self.HOLE_REF = ref4
            self.description = ("The ground is a mixture of grass, weeds, and clover. " +
                               "It is roughened, as if someone had dug it up recently.")
            self.actDialog = ("You have nothing to dig the ground with.")
            self.useDialog = ("You dig about a foot-deep hole in the ground. In the hole, " +
                             "you uncover something.")

    def getDescription(self):
        if Player.getPos().hasFurniture("hole"):
            return ("The ground is a mixture of grass, weeds, and clover, interrupted " +
                   "by the small hole you dug.")
        else:
            return self.description

    def useEvent(self, item):
        if str(item) == HOE:
            return super(Cou1_Floor, self).useEvent(item)
        elif Player.getPos().hasFurniture("hole"):
            return ("You have already dug up the ground here.")
        else:
            Player.getPos().addFurniture(self.HOLE_REF)
            AudioPlayer.playEffect(34)
            return self.useDialog

    def interact(self, key):        
        if key == "dig" or key == SHOVEL:
            if Player.hasItem(SHOVEL) or Player.hasItem(TROWEL):
                i = Player.getInv().get(SHOVEL)
                
                if i == Inventory.NULL_ITEM:
                    i = Player.getInv().get(TROWEL)

                return self.useEvent(i)
            else:
                return super(Cou1_Floor, self).useDialog
        else:
            return super(Cou1_Floor, self).getIt()



"""
    Contains one of the plates needed for the observatory puzzle.    
"""
class Cou1_Hole(SearchableFurniture):
    def __init__(self, itemList=[]):
        super(Cou1_Hole,self).__init__(itemList)

        self.description = ("It's a foot-deep hole you dug in the ground.")
        self.searchDialog = ("You crouch down and reach into the hole.")
        self.actDialog = ("There's no need to dig the hole any deeper.")
        self.useDialog = self.actDialog
        self.addNameKeys("hole", "(?:foot-deep )?hole")
        self.addUseKeys(SHOVEL, TROWEL)
        self.addActKeys("dig")



"""
    One the plates for observatory statue puzzle can be found here in a hole.    
"""
class Cou1(Room):
    def __init__(self, name, ID):
        super(Cou1,self).__init__(name, ID)

    def getBarrier(self, direct):
        if direct == Direction.EAST:
            AudioPlayer.playEffect(6)
            return ("You'll need to climb the steps to get up there.")
        if direct == Direction.NORTH or direct == Direction.WEST:
            return ("There's too much thorny growth to go anywhere else.")
        else:
            return self.bumpIntoWall()



class Cou1_Thorns(Courtyard_Growth):
    def __init__(self):
        super(Cou1_Thorns,self).__init__()

        self.description = ("It's matted up multiflora rose, an invasive. This " +
                           "stuff is the bane of your career as a lumberjack.")
        self.searchDialog = ("You aren't getting pricked by those thorns.")
        self.cutDialog = ("You start wacking at the thorns. You start getting pelted in the face with thorns and decide to stop.")
        self.actDialog = ("That would probably hurt!")
        self.addNameKeys("thorns?", "(?:matted (?:up )?)?(?:multiflora rose|thorns)")



class Cou2_Bushes(Courtyard_Growth, Gettable):
    def __init__(self, ref):
        super(Cou2_Bushes,self).__init__()

        self.BERRY_REF = ref
        
        self.description = ("They're unkept thorny bushes growing red berries, and probably the only " +
                           "pretty things in this yard.")
        self.searchDialog = ("You pick through the bushes and get stuck by a thorn.")
        self.actDialog = ("That would probably hurt!")
        self.cutDialog = ("Is the bush not tidy enough for you?")
        self.addActKeys(Furniture.GETPATTERN)
        self.addNameKeys("(?:unkept )?(?:thorny )?bush(?:es)?", "(?:bright )?(?:red )?berr(?:ies|y)")

    def interact(self, key):
        if re.match(Furniture.GETPATTERN, key):
            return self.getIt()
        else:
            return super(Cou2_Bushes, self).interact(key)

    def getIt(self):
        if Player.getInv().add(self.BERRY_REF):
            return ("You pick a bright red berry off the bush.")
        else:
            return Furniture.NOTHING



class Cou2_Fountain(Courtyard_Fountain):
    def __init__(self, itemList=[]):
        super(Cou2_Fountain,self).__init__(itemList)
        self.description = ("What remains of the ancient fountain is just a stone " +
                           "basin and its toppled over centerpiece. It looks like " +
                           "a statue of a male figure used to stand in the center")
        self.addNameKeys("(?:toppled over )?centerpiece", "(?:male )?statue")



"""
    Superficial.    
"""
class Cou2(Room):
    def __init__(self, name, ID):
        super(Cou2,self).__init__(name, ID)

    def getBarrier(direct):
        if direct == Direction.SOUTH:
            return (self.bumpIntoWall() + 
                "About 15 feet up though, you can see a fissure in the wall of the castle.")
        else:
            return self.bumpIntoWall()



class Cou3_Fork(Furniture):
    def __init__(self, ref):
        super(Cou3_Fork,self).__init__()

        self.FORK = ref
        self.actDialog = ("A clever decision by the player is rewarded with a " +
                  "breathtaking treasure of artisanal mastery.")
        self.description = ("The fork in the path leads to both the left " +
                  "and right halves of the courtyard.")

        self.addNameKeys("fork")
        self.addActKeys(Furniture.GETPATTERN, "pick")
    
    def interact(self, key):  
        if Player.getInv().add(self.FORK):
            Player.getPos().removeFurniture(self.getID())
            return self.actDialog
        else:
            return Furniture.NOTHING



"""
    The castle's front gate.    
"""
class Cou3_Gate(Furniture, Unmoveable):
    def __init__(self):
        super(Cou3_Gate,self).__init__()

        self.useDialog = ("Not even with your exceptional stamina could you drill a hole through this gate with that.")
        self.description = ("The monstrous two-story solid oak gate traps you inside.")
        self.actDialog = ("It's huge. Even if it were unlocked, you wouldn't be able to budge it alone.")
        
        self.addUseKeys(HAND_DRILL)
        self.addActKeys("open", "use", "knock", "close", "shut")
        self.addNameKeys("(?:monstrous )?(?:two-story )?(?:solid )?(?:oak )?(?:main |front )?gate")

    def interact(self, key):
        if key == "open" or key == "use":
            return self.actDialog
        elif key == "knock":
            AudioPlayer.playEffect(55)
            return ("You give the gate a knock. To your astonishment, your knock is left unanswered.")
        else:
            return ("Why would you do that? The PROBLEM is that it's closed!")



class Cou3_Ivy(Courtyard_Growth):
    def __init__(self):
        super(Cou3_Ivy,self).__init__()

        self.description = ("European ivy grows rampantly over everything.")
        self.searchDialog = ("It's just plain old Hedera helix.")
        self.cutDialog = ("It's no use cutting it. It will just grow back.")
        self.actDialog = ("It's no use ripping this off it will just grow back.")
        self.addActKeys(Furniture.CLIMBPATTERN)
        self.addNameKeys("(?:european )?ivy", "hedera helix")
    
    def interact(self, key):              
        if re.match(Furniture.CLIMBPATTERN, key):
            return ("You are too heavy. This will never support you!")
        else:
            return super(Cou3_Ivy, self).interact(key)



"""
    First room entered by the player. 
    Only room from which the inside of the castle may be accessed.    
"""
class Cou3(Room):
    def __init__(self, name, ID):
        super(Cou3,self).__init__(name, ID)

    def triggeredEvent(self):
        if not Player.hasVisited(self.ID):
            AudioPlayer.playEffect(7)
            GUI.out("As you walk into the front courtyard, the huge gates slowly swing shut behind you.")
    
        return self.NAME



class Cou3_Steps(Staircase):
    def __init__(self, direction, dest):
        super(Cou3_Steps,self).__init__(direction, dest, 15)
        self.description = ("The long set of crumbling steps climb to a front " +
                           "balcony before the castle's great front doors.")
        self.addNameKeys("front (?:steps|stairs)")



class Cou4_Forest(Furniture):
    def __init__(self):
        super(Cou4_Forest,self).__init__()

        self.description = ("All you can see is an endless dark expanse of trees.")
        self.searchDialog = ("You have no intention of turning back now.")
        self.actDialog = ("That's your trade, you know. But it's too late for logging now.")
        self.addActKeys("chop", "cut", "log")
        self.addNameKeys("forest", "trees?")



"""
    The front gate of the castle, before it shuts behind the player.    
"""
class Cou4_Gate(Furniture, Unmoveable):
    def __init__(self):
        super(Cou4_Gate,self).__init__()

        self.description = ("It's a monstrous two-story solid oak gate.")
        self.actDialog = ("It's open already.")
        self.addActKeys("open", "use", "knock", "close", "shut")
        self.addNameKeys("(?:monstrous )?(?:two-story )?(?:solid )?(?:oak )?(?:main |front )?gate")

    def interact(self, key):
        if re.match("close|shut", key):
            return ("It's way too big to close by hand!")
        else:
            return self.actDialog



class Cou4_Mailbox(SearchableFurniture, Openable, Gettable, Unmoveable):
    def __init__(self, itemList=[]):
        super(Cou4_Mailbox,self).__init__(itemList)
        
        self.description = ("It's a plain white mailbox. It feels quite out of place here.")
        self.actDialog = ("Mailboxes don't work that way!")
        self.searchDialog = ("You open up the mailbox.")

        self.addNameKeys("(?:small )?(?:mail)?box")
        self.addActKeys(Furniture.GETPATTERN, "lock", "unlock")
    
    def interact(self, key):  
        return (self.actDialog if key == "lock" or key == "unlock" else self.getIt())



class Cou4(Room):
    def __init__(self, name, ID):
        super(Cou4,self).__init__(name, ID)

    def getDescription(self):
        if Player.getLastVisited() == Id.FOR1:
            return ("Okay, we're back. Now, as we were. " +
                   super(Cou4,self).getDescription().upper() + "LET'S GO INSIDE.")
        else:
            return super(Cou4, self).getDescription()



class Cou4_Trail(Furniture):
    def __init__(self):
        super(Cou4_Trail,self).__init__()

        self.description = ("The winding trail(back into the dark forest.")
        self.actDialog = ("If you want this game to start, you better go through the front gate!")
        self.addActKeys("walk", "travel", "run", "use")
        self.addNameKeys("(?:long )?(?:dark )?(?:winding )?(?:path|trail)")



"""
    Contains the stone disk, needed for the door in the marble hall    
"""
class Cou5_Fountain(Courtyard_Fountain, Gettable):
    def __init__(self, itemList=[]):
        super(Cou5_Fountain,self).__init__(itemList)

        self.description = ("This fountain is in better shape than the one at the " +
                           "west. A slender statue of a helmed female figure " +
                           "holding a staff and shield stands in the center. " +
                           "She resembles a soldier.")
        self.addActKeys(Furniture.GETPATTERN)
        self.addNameKeys("(?:slender |helmed )?(?:female )?statue", "staff|shield|soldier")

    def interact(self, key):
        if key == "drink" or key == "swim":
            return self.actDialog
        else:
            return self.getIt("Well... It's made of stone and attached to the fountain, so " +
               "you're going to have to live without that.")



"""
    This furniture provides spruce extract, a needed item.
"""
class Cou5_Spruce(SearchableFurniture, Climbable, Gettable, Unmoveable):
    def __init__(self, ref1, ref2, itemList=[]):
        super(Cou5_Spruce,self).__init__(itemList)

        self.searchDialog = ("There doesn't seem to be much...")
        self.useDialog = ("Drilling a small hole into the trunk allows a small " +
                         "sample of sap to ooze out.")
        self.actDialog = ("The closely-spaced branches of the spruce make the climb " +
                  "easier than in most trees, however the stiff spruce needles " +
                  "scrape and jab your skin through your flannel shirt.")
        self.description = ("The ancient tree looms over you and creaks slowly in " +
                   "the breeze. It stands out as the most life-like thing " +
                   "in the courtyard, even more than the birds. The spruce " +
                   "is an evergreen, genus Picea, with stiff sharp needles. " +
                   "The closely-spaced branches make climbing a possibility.")
        
        self.dir = Direction.UP
        self.EXTRCT_REF = ref2
        self.VIAL_REF = ref1
        self.drilled = False
        
        self.addActKeys("drill", Furniture.CLIMBPATTERN, Furniture.GETPATTERN, "swing")
        self.addNameKeys("(?:spruce |hole )?tree", "spruce", "(?:hole )?trunk", "branch(?:es)?")
        self.addUseKeys(HAND_DRILL, EMPTY_VIAL)

    def useEvent(self, item):
        if str(item) == HAND_DRILL:
            if self.drilled:
                return ("You have already drilled a small hole.")
            else:
                self.addNameKeys("(?:tree ?)?sap", "hole")
                self.drilled = True
                AudioPlayer.playEffect(33)
                rep = self.useDialog
                
                if Player.getInv().contains(str(self.VIAL_REF)):
                    Player.getInv().remove(self.VIAL_REF)
                    Player.getInv().add(self.EXTRCT_REF)
                    return (rep + " You collect some of the sap in the small vial you are carrying.")
                else:
                    return (rep + " You have nothing to collect the sap in, though.")
        elif self.drilled:
            Player.getInv().remove(self.VIAL_REF)
            Player.getInv().add(self.EXTRCT_REF)
            return (" You collect some of the sap in the small vial you are carrying.")
        else:
            return ("You have nothing to put in the vial.")

    def interact(self, action):
        if action == "drill":
            if Player.hasItem(HAND_DRILL):
                self.addNameKeys("(?:spruce )?sap")
                return self.useEvent(Player.getInv().get(HAND_DRILL))
            else:
                return ("You have nothing to drill into it with.")
        elif re.match(Furniture.CLIMBPATTERN, action):
            if self.dir == Direction.UP:
                Player.setOccupies(Id.COU8)
            else:
                Player.setOccupies(Id.COU5)
            
            AudioPlayer.playEffect(16)
            return self.actDialog
        elif action == "swing":
            return ("You're much too old for that.")
        else:
            return self.getIt()

    def getIt(self):
        if self.drilled:
            if Player.getInv().contains(str(self.VIAL_REF)):
                Player.getInv().remove(self.VIAL_REF)
                Player.getInv().add(self.EXTRCT_REF)
                return ("You collect some of the sap in the small vial you are carrying.")
            else:
                return ("You have nothing to collect the sap in.")
        else:
            return ("What exactly do you mean by that?")

    def getDir(self):
        return self.dir



def evalHit(val, score):
    if val == 1:
        return (11 if (score + 11 <= 21) else 1)
    else:
        return val

def bust(score):
    return score > 21

def blackJack(score):
    return score == 21

"""
    This is an in-game non-player character that plays blackjack with the player.
    The player may play as many times as her/she wants each encounter, and the
    player keeps the cards in his/her inventory after no more games are to be played.
    This NPC is a ghost. The ghost acts as the dealer.
"""
class Cou6_BlackJackGhost(NonPlayerCharacter):
    # Maps outcomes to dialogs.
    
    RES = { 
        122 : "How lucky. You got a blackjack already! ... Want to play again?",
        112 : "Hah! I have blackjack already. I win... Want to play again?",
        132 : "We both got blackjack... So a tie, how boring... Want to play again?",
        211 : "Agh... % too far over. I lose... Want to play again?",
        233 : "Hm... a tie. How boring... Want to play again?",
        223 :"You won. Good luck, mate, you need it tonight... Want to play again?",
        213 : "Looks like I won, mate, fair and square... Want to play again?",
        221 : "Looks like you busted! % too many! ... Want to play again?"
    }

    def __init__(self):
        super(Cou6_BlackJackGhost,self).__init__()

        self.searchDialog = ("The ghost won't appreciate that.")
        self.actDialog = ("\"Come back if you want to play again!")
        self.description = ("Leaning nonchalantly against the castle wall is a " +
                           "ghostly figure shuffling what seem to be cards. The apparition " +
                           "is garbed in distinctive clothing- a vest and a full-brimmed hat.")
        self.addActKeys("play")
        self.addNameKeys("ghost", "apparition", "spirit", "ghostly apparition")

    """
        Initiates dialog with the ghost player. 
        The ghost talks to you, then asks you if you would like to play blackjack.
        @param key The action the player typed to interact with self.
        @return End dialog with the ghost.
    """
    def interact(self, key):
        rep = self.actDialog
        
        if re.match(NonPlayerCharacter.ATTACK_PATTERN, key):
            return NonPlayerCharacter.ATTACK_DIALOG
        elif Player.getInv().size() >= 8:
            return ("You are carrying too much stuff mate. " +
                      "Come back after you've emptied your pockets some.")
        elif self.firstTime:
            GUI.out(self.converse1())
            if self.askToPlay():
                rep += " Hey why don't you keep those cards? I can make more!"
            self.firstTime = False
        else:
            GUI.out(self.converse2())
            if self.askToPlay():
                rep += " Hey why don't you keep those cards? I can make more! Hah!"

        return rep

    def converse1(self):
        GUI.menOut(NL + NL + "<enter> Continue...")
        GUI.out("You approach the apparition loitering in the courtyard. Before " +
                "you can accost it, its mouth opens to speak...")
        GUI.promptOut()
        
        GUI.out("The ghost speaks in a heavy Australian accent. \"Finally! " +
                "Another soul to play. It has been a while since I've " +
                "seen anyone to play cards with. Would you like to play? It's " +
                "called blackjack...\"")
        GUI.promptOut()
        
        GUI.menOut("<'yes'>" + NL + "<'no'>")
        
        return ("\"... well not at all! ... Does it look like I need money in " +
               "my state? Come on stranger, yes or no....\"")

    def converse2(self):
        return "Back to play?"

    """
        Asks the player if he/she would like to play a game of blackjack.
        After each game, if the player wants to play again, the cards are
        cleared from the player's inventory. If not, the player keeps the cards.
    """
    def askToPlay(self):
        ans = ("yes")
        played = False # If the player has played at least once.
        
        while not (ans == "no" or ans == "n" or not ans):
            ans = GUI.askChoice(NL + "Play him in blackjack?", YES_NO_P)
            
            if Player.answeredYes(ans):
                played = True
                Player.getInv().removeType(Names.CARD) # Removes all cards from player inventory.
                GUI.clearDialog()
                self.playCards() # Starts the game. 

            Player.printInv()
        
        GUI.clearDialog()
        
        return played

    """
        The main algorithm for the blackjack game.
        Game outcomes are mapped to by integers which display after each game.
        The first integer is 1 if the outcome happens immediately or 2 otherwise.
        The second represents the ghost (1), player (2), or both (3).
        The third represents the reason- bust (1), blackjack (2), or score (3).
        
        A new deck is made for each game. The NPC is a ghost, and thus uses ghost
        cards, so more are made by the ghost. The benefit of this is that the
        player may keep the cards and use them for something later, perhaps.
        
        If a player busts, the game also prints how many points that player is over.
        Whatever the ghost draws is printed in the console (For testing).
    """
    def playCards(self):
        ghostVal = 0 
        yourVal = 0 # The scores.
        deck = Deck()
        deck.shuffle()

        # Deals the initial two cards to the dealer.
        card1 = deck.draw()
        GUI.out("The ghost reveals:\t\t" + str(card1))
        ghostVal += evalHit(card1.getVal(), ghostVal) 
        ghostVal += evalHit(deck.draw().getVal(), ghostVal)
        
        # Deals the initial two cards to the player.
        plyrCard1 = deck.draw()
        plyrCard2 = deck.draw()
        Player.getInv().add(plyrCard1)
        Player.getInv().add(plyrCard2)
        yourVal += evalHit(plyrCard1.getVal(), yourVal) 
        yourVal += evalHit(plyrCard2.getVal(), yourVal)
        Player.printInv()
        
        print("\nGhost's starting score: " + str(ghostVal))
        
        # Checks for immediate blackjacks.
        if blackJack(ghostVal) or blackJack(yourVal):
            v = None

            if blackJack(yourVal) and blackJack(ghostVal):
                v = 132
            elif blackJack(yourVal):
                v = 122
            else:
                v = 112
            
            GUI.out(Cou6_BlackJackGhost.RES[v])
            return

        yourVal = self.playerTurn(yourVal, deck) # You take your turn.
        
        # Evaluates if you have busted.
        if bust(yourVal):
            GUI.out(Cou6_BlackJackGhost.RES[221].replace("%", str(yourVal - 21), 1))
            return
        
        ghostVal = self.ghostTurn(ghostVal, deck) # Ghost takes turn.
        
        # Evaluates if the dealer has busted.
        if bust(ghostVal):
            GUI.out(Cou6_BlackJackGhost.RES[211].replace("%", str(ghostVal - 21), 1))
            return
        
        # Compares the players' scores of nothing special happened.
        val = None

        if yourVal == ghostVal: 
            val = 233
        elif ghostVal > yourVal:
            val = 213
        else:
            val = 223
        
        GUI.out(Cou6_BlackJackGhost.RES[val])

    """
        This method lets you hit as many times as you want, or stand.
        If you bust, your turn is over and the loop ends.
        @param score The player's current score.
        @param deck A reference to the Deck object.
        @return The player's new current score.
    """
    def playerTurn(self, score, deck):
        ans = "" 
        
        while not re.match("s(tand|tay)", ans):
            GUI.menOut("Your total is " + str(score) + "." + NL +
                       "Would you like to hit or stand?" + NL +
                       "<'hit'>" + NL + "<'stand'>")
            ans = GUI.promptOut()
            
            if ans == "hit":
                current = deck.draw()
                Player.getInv().add(current)
                Player.printInv()
                score += evalHit(current.getVal(), score)
                
                if bust(score):
                    ans = ("stand")

        return score

    """
        The ghost hits as many times as possible until busting or over 17.
        @param ghostScore The ghost's current score.
        @param deck A reference to the Deck object.
        @return The ghost's new score.
    """
    def ghostTurn(self, ghostScore, deck):
        while ghostScore < 17:
            card = deck.draw()
            ghostScore += evalHit(card.getVal(), ghostScore)
            print("Ghost draws a " + str(card) + "\nGhost new score: " + str(ghostScore)) #FOR TESTING

        return ghostScore



"""
    Contains the ghost that plays blackjack.    
"""
class Cou6(Room):
    def __init__(self, name, ID):
        super(Cou6,self).__init__(name, ID)

    def getBarrier(self, direct):
        if direct == Direction.WEST:
            AudioPlayer.playEffect(6)
            return ("You'll need to climb the steps to get up there.")
        if direct == Direction.NORTH or direct == Direction.EAST:
            return ("There's too much thorny growth to go anywhere else.")
        else:
            return self.bumpIntoWall()



class Cou6_Statue(Statue):
    def __init__(self, ID):
        super(Cou6_Statue,self).__init__()
        
        self.COU_FLOOR_ID = ID
        self.useDialog = ("You balance the % the best you can on the pair of legs, " +
                         "but can only watch helplessly as it falls back off onto " +
                         "the ground.")
        self.description = ("The statue is just a waist with legs. Part of it " +
                           "lies on the ground. It once depicted a male figure.")
        self.actDialog = ("The statue is rough and weathered- cracked all over " +
                         "from the variable weather it has endured for likely a while.")
        
        self.addUseKeys(STATUE_HEAD, STATUE_TORSO)
        self.addNameKeys("crumbling statue", "(?:pair of )?legs", "waist")

    def useEvent(self, item):
        i = Player.getPos().getFurnRef(self.COU_FLOOR_ID).getInv()
        Player.getInv().give(item, i)
        return self.useDialog.replace("%", str(item), 1)



class Cou8_Nest(SearchableFurniture, Gettable):
    def __init__(self, itemList=[]):
        super(Cou8_Nest,self).__init__(itemList)
        
        self.description = ("It's a small empty raven's nest perched precariously on " +
                           "a nearby branch. The nest is composed of many misshapen " +
                           "twigs and brambles sticking out every which way. The nest " +
                           "contains a few pieces of debris, but no eggs.")
        self.searchDialog = ("You look inside the nest.")
        self.actDialog = ("What a humorous thing to think to type in.")

        self.addNameKeys("(?:raven's )?nest", "(?:raven|bird's) nest")
        self.addActKeys(Furniture.SITPATTERN, Furniture.GETPATTERN)
    
    def interact(self, key):
        if re.match(Furniture.GETPATTERN, key): 
            return self.getIt("That belongs to a raven. You don't have it in your conscience to take that.") 
        else:
            return self.actDialog



class Cou8(Room):
    def __init__(self, name, ID):
        super(Cou8,self).__init__(name, ID)

    def getBarrier(direct):
        return ("Be careful! You don't want to fall out!")



class Cou8_Spruce(Cou5_Spruce):
    def __init__(self, ref1, ref2, itemList=[]):
        super(Cou8_Spruce,self).__init__(ref1, ref2, itemList=[])
        
        self.dir = Direction.DOWN
        self.actDialog = ("You climb back down.")
        self.description = ("You are sheltered inside the spruce canopy, about " +
                  "15 feet above the ground. The only thing of interest " +
                  "is a medium-sized raven's nest out on a nearby branch.")
        
        self.addNameKeys("(?:spruce )?needles?")



class Cou_Castle(Furniture, Unmoveable):
    def __init__(self):
        super(Cou_Castle,self).__init__()

        self.description = ("The monstrous castle appears ghastly standing in the " +
                           "night. Scanning it thoroughly, you figure it to be " +
                           "about four or five stories tall. The castle looks to " +
                           "be composed of a central area and a wing on each side.")
        self.searchDialog = ("Maybe you should go inside to do that.")
        self.actDialog = ("Perhaps you should find the front door and go through that.")
        
        self.addActKeys("go", "climb", "escape")
        self.addNameKeys("(?:monstrous )?castle", "portico")

    def interact(self, key):
        if key == "go":
            return self.actDialog
        elif key == "climb":
            return ("This is not a skill you possess.")
        else:
            return ("Ah! That's it, you win! You now rest comfortably at your " +
                      "home, sipping fine Islay scotch, reflecting on your " +
                      "triumphant victory. And then, your focus returns to reality.")



class Cou_Ravens(Furniture, Gettable):
    def __init__(self):
        super(Cou_Ravens,self).__init__()
        
        self.description = ("A few black ravens can be seen flying around inside " +
                           "the courtyard. Occasionally, one is seen flying into " +
                           "the nearby tree before exiting again not too long after.")
        self.actDialog = ("You don't speak raven.")

        self.addNameKeys("ravens?")
        self.addActKeys("catch", "speak|talk|converse|chat|greet|listen")
    
    def interact(self, key):
        if key == "catch":
            return ("You lack the reflexes to do so.")
        elif re.match(Furniture.GETPATTERN, key):
            return self.getIt()
        else:
            return self.actDialog



class Cou_Steps(Furniture):
    def __init__(self):
        super(Cou_Steps,self).__init__()

        self.description = ("The long set of crumbling steps climb to a front " +
                           "balcony before the castle's great front doors.")
        self.actDialog = ("You can't while at the side of the stairs.")
        self.addActKeys(Furniture.CLIMBPATTERN, "use")
        self.addNameKeys("(?:crumbling )?(?:staircase|steps|stairs)")



class Cou_Tiles(Furniture, Gettable):
    def __init__(self):
        super(Cou_Tiles, self).__init__()

        self.description = ("The array of square rock tiles wraps around the " +
                           "perimeter of the fountain. Many of them are " +
                           "weathered, uneven, and cracked")
        self.searchDialog = ("The tiles are much too heavy to lift with your hands.")
        self.actDialog = self.searchDialog
        self.useDialog = ("You pry one of the tiles up, but all revealed is only " +
                         "a square dirt indentation in the ground. Tired, you " +
                         "drop the tile back into the hole to avoid tripping.")

        self.addNameKeys("(?:tiled )?walkway", "(?:square )?(?:rock )?tiles")
        self.addUseKeys(SHOVEL, CROWBAR, HOE)
        self.addActKeys("lift", Furniture.MOVEPATTERN, Furniture.GETPATTERN)
    
    def interact(self, key):
        if re.match(Furniture.GETPATTERN, key):
            return self.getIt()
        else:
            return self.actDialog



"""
    Represents a deck of cards.    
"""
class Deck(object):
    def __init__(self):
        self.DECK = []
        ranks = ("ace", "two", "three", "four", "five", "six", "seven", 
                          "eight", "nine", "ten", "jack", "queen", "king")
        suits = ("hearts", "spades", "clubs", "diamonds")
        
        for suit in suits: # Creates all the cards.
            for rank in ranks:
                self.DECK.append(Card(rank + " of " + suit))
    
    """
        Shuffles the deck of cards.
        Removes all the cards off the stack randomly into the array, then 
        iterates through the array linearly, pushing each card back in.
    """
    def shuffle(self):
        random.shuffle(self.DECK)
    
    """
        Removes a card from the top of this deck.
        @return A card object.
    """
    def draw(self):
        return self.DECK.pop(0)