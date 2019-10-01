from Inventory import Inventory
from Names import *
from Player import Player
from Furniture import *
import Direction, Id, AudioPlayer
from Room import Room
from Things import Statue, LockedContainer
import re
from Structure_gen import Column
from Item import Item

class Gar13_Planter(SearchableFurniture, Unmoveable):
    def __init__(self, soil, itemList=[]):
        super(Gar13_Planter,self).__init__(itemList)
        
        self.SOIL_REF = soil
        self.description = ("The long planter(along the length of the " +
                           "garden's western edge. In it are a variety of plants " +
                           "which have seemingly flourished over the years.")
        self.actDialog = ("You're a lumberjack, not a gardener!")
        self.searchDialog = ("You fan around the plants in the planter.")
        self.useDialog = ("You uncover nothing, but you do store a bit of soil in your pockets.")

        self.addNameKeys("planter|bed|plants|dirt", "(?:bed of )?(?:soil|dirt)", SOIL)
        self.addUseKeys(HOE, TROWEL, SHOVEL, SEED, FERTILIZER)
        self.addActKeys(Furniture.GETPATTERN)
        self.addActKeys("garden", "plant", "dig", "shovel")
    
    def useEvent(self, item):
        if re.match("trowel|shovel", str(item)):
            AudioPlayer.playEffect(34)
            
            if Player.getInv().add(self.SOIL_REF):
                return self.useDialog
            else:
                return Furniture.NOTHING
        else:
            return self.actDialog
    
    def interact(self, key):
        if key == "garden" or key == "plant":
            return self.actDialog
        elif Player.hasItem(TROWEL) or Player.hasItem(SHOVEL):
            i = Player.getInv().get(SHOVEL)
            
            if i == Inventory.NULL_ITEM:
                i = Player.getInv().get(TROWEL)
            
            return self.useEvent(i)
        else:
            return ("You have nothing to dig with.")



class Gar1(Room):
    def __init__(self, name, ID):
        super(Gar1,self).__init__(name, ID)

    def getBarrier(self, direct):
        if direct == Direction.WEST:
            return ("There's about a 150 foot drop right there.")
        else:
            return self.bumpIntoWall()



class Gar1_Statue(Statue):
    def __init__(self):
        super(Gar1_Statue,self).__init__()
        self.description = ("The statue depicts half a female body mounted on " +
                           "a base. Her expressionless face gazes downwards " +
                           "and her arms are cut off at the shoulders.")



class Gar24_Sconce(Furniture, Gettable):
    def __init__(self):
        super(Gar24_Sconce,self).__init__()

        self.description = ("The fire burning inside the black iron sconce emits a cold yellow hue.")
        self.actDialog = ("That light looks pretty hot...")

        self.addNameKeys("(?:black )?(?:iron )?(?:sconce|light)", "fire")
        self.addActKeys(Furniture.GETPATTERN, Furniture.HOLDPATTERN)
    
    def interact(self, key):
        if re.match(Furniture.HOLDPATTERN, key):
            return self.actDialog
        else:
            return self.getIt()



class Gar2_BrokenHose(Furniture):
    def __init__(self):
        super(Gar2_BrokenHose,self).__init__()

        self.description = ("The old leather hose has broken in two... at just the right time.")
        self.actDialog = ("It has broken and offers no purpose now.")

        self.addNameKeys("(?:broken )?(?:leather )?hose")
        self.addActKeys("untie", Furniture.CLIMBPATTERN)



class Gar2_Columns(Column):
    def __init__(self):
        super(Gar2_Columns,self).__init__()

        self.description = ("The four Corinthian-style pillars hold up a circular " +
                           "stone rim, on which sits a paned glass dome.")

        self.addNameKeys("(?:stone |corinthian )?(?:column|pillar)s?")



class Gar2_Dome(Furniture, Unmoveable):
    def __init__(self):
        super(Gar2_Dome,self).__init__()

        self.description = ("The paneled dome must be there to prevent rain from " +
                           "dripping into the room below. Still, why have a hole " +
                           "there in the first place?")
        self.useDialog = self.actDialog = ("If you do that, the glass will probably " +
                         "rain down on you as a deadly shower of glass.")

        self.addUseKeys(STONE_BLOCK, RED_BALL, CUE_BALL, ROCK)
        self.addActKeys("shatter")
        self.addNameKeys("(?:paneled )?(?:glass )?dome")



class Gar2_Hole(Furniture):    
    def __init__(self, ref):
        super(Gar2_Hole,self).__init__()

        self.HOSE_REF = ref
        self.searchDialog = self.description = \
                ("You peer over the thick granite railing into the " +
                "hole. To your surprise, it's the rotunda you were " +
                "in earlier! It's about a 25 foot drop down.")
        self.actDialog = ("The drop is too great. It's about 25 feet down. You'd surely break something.")
        self.useDialog = ("You tie the end of the hose to the railing and throw " +
                         "it over the edge. Hopefully it will support your weight.")

        self.addNameKeys("(?:thick )?(?:granite )?railing", "hole")
        self.addUseKeys(LEATHER_HOSE)
        self.addActKeys("jump", Furniture.CLIMBPATTERN, "vault")
    
    def getDescription(self):
        if Player.getPos().hasFurniture(LEATHER_HOSE):
            return (self.description + " A leather hose, tied around the railing, hangs " +
                                      "downward and almost touches the floor.")
        elif Player.getPos().hasFurniture("broken hose"):
            return (self.description + " The broken leather hose is still tied around the railing.")
        else:
            return self.description
    
    def getSearchDialog(self):
        return self.getDescription()
    
    def useEvent(self, item):
        Player.getPos().addFurniture(self.HOSE_REF) # Player must be in GAR2
        Player.getInv().remove(item)
        
        return self.useDialog



class Gar2_Hose(Furniture, Climbable):
    def __init__(self, brokenHoseItem):
        super(Gar2_Hose,self).__init__()

        self.BRKNHOSE_REF = brokenHoseItem
        self.BRKNHOSE_REF2 = Gar2_BrokenHose()
        
        self.description = ("The cracked leather hose dangles down into the room " +
                          "below. It's only a short drop from the bottom. " +
                          "Hopefully it will take your weight.")
        self.actDialog = ("Slowly, you climb down the hose. The hose maintains itself, " +
                        "however only feet from the bottom, the hose splits in half " +
                        "and falls to the floor. Only minimally hurt, you stand " +
                        "back up and peer at the other half, still tied to the railing.")

        self.addNameKeys("(?:leather )?hose")
        self.addActKeys(Furniture.CLIMBPATTERN)
    
    def interact(self, key):              
        Player.setOccupies(Id.ROTU)
        AudioPlayer.playEffect(36)
        Player.getRoomObj(Id.GAR2).removeFurniture(self.getID())
        Player.getRoomObj(Id.GAR2).addFurniture(self.BRKNHOSE_REF2)
        Player.getRoomObj(Id.FOY3).setLocked(False)
        Player.getInv().add(self.BRKNHOSE_REF)
        Player.printInv()
        
        return self.actDialog
    
    def getDir(self):
       return Direction.DOWN



class Gar3_Chest(LockedContainer):
    def __init__(self, itemList=[]):
        super(Gar3_Chest,self).__init__(Id.GCHS, itemList=[])
        
        self.actDialog = ("It takes a small bit of force, but the rusty key manages to open the chest.")
        self.description = ("It's a wooden chest for the holding of gardening, and " +
                 "other nonsense. This one has a rather large keyhole.")
        self.searchDialog = ("To your dismay, the chest has been locked previously.")
        self.useDialog = ("An ingenious idea. The player manages to break the lock using the drill " +
                         "with a swift jab into the keyhole.")

        self.addUseKeys(HAND_DRILL, CROWBAR)
        self.addNameKeys("(?:wooden )?(?:utility )?chest", "lock")
    
    def useEvent(self, item):
        if self.searchable:
            return ("The chest has already been unlocked.")
        
        self.searchable = True
        
        if str(item) == HAND_DRILL:
            return self.useDialog
        else:
            return ("The crowbar offers enough leverage to pry the lid open, yielding glorious access.")



class Gar3_Fountain(SearchableFurniture):
    def __init__(self, itemList=[]):
        super(Gar3_Fountain,self).__init__(itemList)
        
        self.description = ("The low fountain works, surprisingly, and is spouting " +
                           "clear water. It collects and drains the water from a semi-circular " +
                           "pool at the bottom.")
        self.actDialog = ("You take a sip. Delicious! Some of the water seeps " +
                  "into your beard, which you have always found irritating.")
        self.searchDialog = ("You look into the pool at the base of the fountain.")

        self.addNameKeys("(?:low )?fountain")
        self.addActKeys("drink", "swim", "jump")
    
    def interact(self, key):
        if key == "drink":
            return self.actDialog
        else:
            return "You wouldn't be able to fit in there."
    
    def getDescription(self):
        if self.inv.isEmpty():
            return self.description
        else:
            self.description + " There's an object resting in it."



class Gar3(Room):
    def __init__(self, name, ID):
        super(Gar3,self).__init__(name, ID)

    def getBarrier(self, direct):
        if direct == Direction.WEST:
            return ("There's about a 150 foot drop right there.")
        else:
            return self.bumpIntoWall()



class Gar4_Planter(SearchableFurniture, Unmoveable):
    def __init__(self, ID, plate, itemList=[]):
        super(Gar4_Planter,self).__init__(itemList)
        self.PLQ_ID = ID
        self.PLT_REF = plate
        self.description = ("This planter contains no plants, just a bed of soil.")
        self.actDialog = ("You dig around the plaque, but find nothing in the soil.")
        self.searchDialog = ("The soil's surface is bare and hides nothing.")
        self.useDialog = self.actDialog

        self.addNameKeys("planter", "(?:bed of )?(?:soil|dirt)", "bed|dirt", SOIL)
        self.addUseKeys(SHOVEL, TROWEL)
        self.addActKeys(Furniture.GETPATTERN)
        self.addActKeys("dig", "plant", "garden", "shovel")
    
    def interact(self, key):
        if key == "garden" or key == "plant":
           return ("You aren't a gardener!")
        elif Player.hasItem(SHOVEL) or Player.hasItem(TROWEL):
            p = Player.getRoomObj(Id.GAR4).getFurnRef(self.PLQ_ID)
            
            if p.isMoved():
                if inv.contains(str(self.PLT_REF)):
                    if inv.give(self.PLT_REF, Player.getInv()):
                        AudioPlayer.playEffect(34)
                        return ("You dig under where the plaque was to find a shiny plate!")
                    else:
                        return ("You find a shiny plate under the dirt, but you are carrying too much stuff!")
                else:
                    return ("You have already dug under the plaque")
            else:
                AudioPlayer.playEffect(34)
                return self.actDialog
        else:
            return ("You have nothing to dig with, and your stocky hands are terrible for digging.")

    def useEvent(self, item):
        return self.interact("dig")
    
    def getSearchDialog(self):
        self.searchable = Player.getRoomObj(Id.GAR4).getFurnRef(PLQ_ID).isMoved()
        return ("You look in the planter" if self.searchable else self.searchDialog)



class Gar4_Plaque(Furniture):
    def __init__(self):
        super(Gar4_Plaque,self).__init__()
        self.isMoved = False
        
        self.description = "The small plaque reads, \"In memory of Daedalus, who lived to create.\""
        self.actDialog = ("You move the plaque off to the side.")
        self.searchDialog = ("You lift the plaque and find only soil. You put it back down to the side.")

        self.addNameKeys("(?:small )?plaque")
        self.addActKeys(Furniture.MOVEPATTERN, "lift", "read")
    
    def getSearchDialog():
        result = ("You have already moved the plaque." if self.isMoved else self.searchDialog)
        self.isMoved = True
        return result
    
    def interact(self, key):              
        if key == "read":
            return self.description
        elif not self.isMoved:
            AudioPlayer.playEffect(51)
            self.isMoved = True
            return self.actDialog
        else:
            return ("You have already moved the plaque.")
    
    def isMoved(self):
        return self.isMoved



class Gar4(Room):
    def __init__(self, name, ID):
        super(Gar4,self).__init__(name, ID)

    def getBarrier(self, direct):
        if direct == Direction.SOUTH:
            AudioPlayer.playEffect(6)
            return ("The door here budges only a little. Something is blocking it from the other side.")
        else:
            return self.bumpIntoWall()