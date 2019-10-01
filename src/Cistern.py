from GUI import GUI
from Player import Player
from Names import METAL_BUCKET, WOODEN_OAR, HAND_TORCH
import Id, Menus, Direction, AudioPlayer
from NonPlayerCharacter import NonPlayerCharacter
from Room import Room
from Structure_gen import Column
from Furniture import Gettable, Furniture, SearchableFurniture, Resetable
from Tunnels import Dungeon_Tunnel
import re

"""
    Initially contains toxic gas preventing the player from entering this room.
    Player must solve a valve puzzle to disperse the gas.    
"""
class Cis1(Dungeon_Tunnel, Resetable):
    def __init__(self, name, ID):
        super(Cis1, self).__init__(name, ID)
        self.hasToxicGas = True

    def triggeredEvent(self):
        if self.hasToxicGas:
            Player.move(Direction.EAST)
            GUI.out("You walk into the room passed the door and are greeted by a thick " +
                    "green smog. It burns your eyes and nose. You cannot bear it and " +
                    "retreat back into the tunnel.")
        
        return str(Player.getPos())

    def getBarrier(direct):
        if direct == Direction.NORTH:
            return Dungeon_Tunnel.WATER_THERE
        else:
            return self.bumpIntoWall()

    def turnOffGas(self):
        self.hasToxicGas = False

    def reset(self):
        self.hasToxicGas = True



class Cis2_Boat(SearchableFurniture):
    def __init__(self, itemList=[]):
        super(Cis2_Boat,self).__init__(itemList)
        
        self.description = ("The slender wooden canoe floats in the disgusting " +
                  "water, docked right near the ledge.")
        self.actDialog = ("You are now inside the canoe.")
        self.searchDialog = ("You look inside the canoe.")
        self.useDialog = ("You paddle in silence for many minutes in the dark. " +
                  "Somehow, without any guidance, you see a stone platform emerge " +
                  "from the darkness ahead, and the canoe gently docks by it.")

        self.addNameKeys("(?:slender )?(?:wooden )?(?:canoe|boat)")
        self.addUseKeys(WOODEN_OAR)
        self.addActKeys("ride|paddle|launch|get", "climb|enter|go", "leave")
    
    def interact(self, key):              
        if key == "leave":
            return ("You aren't even in the canoe.")
        elif Player.hasItem(WOODEN_OAR):
            return self.transport()
        else:
            return ("You really have nothing proper to paddle with.")
    
    def useEvent(self, item):
        return self.transport()
    
    # Transports the player between areas of the cistern.
    def transport(self):
        if Player.getPosId() == Id.CIS2:
            Player.setOccupies(Id.CIS5)
        else:
            Player.setOccupies(Id.CIS2)
        
        AudioPlayer.playEffect(42)
        GUI.menOut(Menus.ENTER)
        GUI.descOut(self.useDialog)
        GUI.clearDialog()
        GUI.promptOut()
        Player.describeRoom()
        
        return Furniture.NOTHING


"""
    Superficial.    
"""
class Cis2(Dungeon_Tunnel):
    def __init__(self, name, ID):
        super(Cis2, self).__init__(name, ID)

    def getBarrier(direct):
        return Dungeon_Tunnel.WATER_THERE



"""
    Superficial.
"""
class Cis3(Dungeon_Tunnel):
    def __init__(self, name, ID):
        super(Cis3, self).__init__(name, ID)

    def getBarrier(self, direct):
        if direct == Direction.WEST:
            return Dungeon_Tunnel.WATER_THERE
        else:
            return self.bumpIntoWall()



"""
    Superficial
"""
class Cis4(Dungeon_Tunnel):
    def __init__(self, name, ID):
        super(Cis4, self).__init__(name, ID)

    def getBarrier(self, direct):
        if direct == Direction.WEST:
            return Dungeon_Tunnel.WATER_THERE
        else:
            return self.bumpIntoWall()



class Cis5_FigureNPC(NonPlayerCharacter):
    def __init__(self):
        super(Cis5_FigureNPC, self).__init__()
        
        self.description = ("The tall figure stands at least 7 feet and is fully " +
                  "dressed in a black robe. It holds a tall straight staff " +
                  "topped with a red jewel, and its face is hidden. It stands, " +
                  "silent with its attention to you, but stays passive.")
        self.actDialog = ("\"Death beckons you with its grim implement. " + 
                         "Embrace its cold grasp and speak 'It is I, friend, " +
                         "welcome me' before its front door, and you will be " +
                         "invited into its kingdom.\"")
        self.searchDialog = ("How very rude that would be.")
        self.useDialog = ("\"I need not possessions!\" the figure screeches.")

        self.addNameKeys("(?:black )?(?:cloaked )?(?:figure|person)", "him|it|her")
        self.addUseKeys(Furniture.ANYTHING)
    
    def interact(self, key):   
        if re.match(NonPlayerCharacter.ATTACK_PATTERN, key):
            return NonPlayerCharacter.ATTACK_DIALOG
        elif self.firstTime:
            return self.converse1()
        else:
            return self.converse2()
    
    def converse1(self):
        GUI.menOut(Menus.ENTER)
        GUI.out("You feel out of breath and can't muster any words. For " +
                  "a moment, you and the figure stand in silence. Suddenly, " +
                  "the figure brings its other hand to its staff and leans " +
                  "toward to slightly.")
        GUI.promptOut()
        GUI.out("The black cloaked figure speaks a verse to you in a hideous voice:")
        GUI.promptOut()
        GUI.out(self.actDialog)
        GUI.promptOut()
        return ("You have not much a taste for riddles, but you have no intent of asking its meaning.")
    
    def converse2(self):
        GUI.menOut(Menus.ENTER)
        GUI.out("The black cloaked figure speaks a verse to you in a hideous voice:")
        GUI.promptOut()
        return actDialog



class Cis5(Room):
    def __init__(self, name, ID):
        super(Cis5, self).__init__(name, ID)

    def getBarrier(self, direct):
        return ("There is water in all directions from here, extending into the black void.")



class Cis_Columns(Column):
    def __init__(self):
        super(Cis_Columns, self).__init__()

        self.description = ("The fat tiled pillars are each about 10 to 12 feet " +
                           "wide and extend upwards. Towards the bottom they are " +
                           "covered in algae. You cannot see the ceiling, " +
                           "for the room is too large and dark.")
        self.searchDialog = ("You aren't wading through the disgusting water to search those.")

        self.addNameKeys("(?:fat )?(?:tiled )?(?:protruding )?(?:stone )?(?:columns?|pillars?)", "ceiling")



class Cis_Darkness(Furniture, Gettable):
    def __init__(self):
        super(Cis_Darkness, self).__init__()

        self.description = ("The darkness hides the True size of the room, though " +
                           "you suppose it could be as big as 100 feet across and " +
                           "50 feet high, perhaps more. Claustrophobia sets in as " +
                           "the darkness and turgid air envelop you.")
        self.useDialog = ("The darkness swallows up the torch light, keeping visibility low.")
        
        self.addActKeys(Furniture.GETPATTERN)
        self.addUseKeys(HAND_TORCH)
        self.addNameKeys("darkness|dark void|void|blackness|ceiling")
    
    def interact(self, key):
        return self.getIt()



class Cis_Water(Furniture, Gettable):
    def __init__(self, ref):
        super(Cis_Water, self).__init__()
        
        self.WTR_BCKT = ref
        
        self.description = ("The water is stagnant and fills the room with a putrid smell. " +
                           "A skin of algae coats nearly all of it.")
        self.actDialog = ("This water looks and smells terrible. You aren't doing that.")
        self.searchDialog = ("You aren't keen to search that.")
        self.useDialog = ("You pick some of the water up in the bucket.")

        self.addNameKeys("(?:stagnant )?(?:(?:large )?body of )?(?:putrid |disgusting |smelly |awful )?(?:stagnant )?water")
        self.addActKeys(Furniture.GETPATTERN)
        self.addActKeys("swim", "jump", "drink", "hide")
        self.addUseKeys(METAL_BUCKET)
    
    def useEvent(self, item):
        AudioPlayer.playEffect(42)
        Player.getInv().remove(item)
        Player.getInv().add(self.WTR_BCKT)
        return self.useDialog
    
    def interact(self, key):
        if key == "swim" or key == "jump" or key == "dive":
            return self.actDialog
        elif key == "hide" or key == "drink":
            return ("The water is much too disgusting and treacherous.")
        else:
            return self.getIt()
    
    def getIt(self):
        if Player.hasItem(METAL_BUCKET):
            return self.useEvent(Player.getInv().get(METAL_BUCKET))
        else:
            return ("You'll need an empty bucket...")