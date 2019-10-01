from Structure_gen import Floor, Staircase, Door
from Patterns import *
import re, sched, time
from Room import Room
from Inventory import Inventory
from GUI import GUI
from Names import PIECE_OF_PIPE, HAND_TORCH, PIECE_OF_PIPE, METAL_BUCKET
import Direction, Menus, Id, AudioPlayer
from Player import Player
from Furniture import *

"""
    Normal floor for dungeon rooms.
"""
class Dungeon_Floor(Floor):
    def __init__(self, itemList=[]):
        super(Dungeon_Floor,self).__init__("The ground is damp and made of large gray stone bricks. Here and there, moss grows in the cracks.", itemList=[])



"""
    Serves as a way to reference the tunnel monster.
    This furniture is important, as it helps the player in determining where
    the monster is.    
"""
class DungeonMonsterFurniture(Furniture):
    CANT_SEE_IT = ("You can't hear or see it from here. The " +
              "creature's attention is apparently drawn from your position.")
    
    def __init__(self):
        super(DungeonMonsterFurniture,self).__init__()

        self.description = ("A disfigured corpse-like creature is roaming the tunnels. " +
                           "It holds a dangling chain wrapped around itself several times " +
                           "and drags its bare feet as it walks crookedly. ")
        self.actDialog = ("It's probably best to stay as far from that thing as possible.")
        self.searchDialog = self.useDialog = self.actDialog

        self.addNameKeys("(?:disfigured )?(?:corpse-like )?(?:creature|monster|thing)", 
                "(?:unsettling )?(?:noise|sound)")
        self.addUseKeys(Furniture.ANYTHING)
        self.addActKeys(".{2,}")
    
    def interact(self, key):
        if key == "listen" or CHECK_P.match(key):
            return self.getDescription()
        else:
            return self.actDialog
    
    def getDescription(self):
        result = None 
        pos = Player.getPosId()
        
        if pos in (Id.CRY1, Id.CRY2, Id.DKCH, Id.INTR): 
            result = DungeonMonsterFurniture.CANT_SEE_IT
        elif Id.areaName(pos) == "ESC":
            result = ("It's lurking around somewhere above your head... You can't hear it though.")
        elif (Id.areaName(DungeonMonster.getPos()) == "CIS" and not NO_SEE_AREA_W.match(pos)) or \
             (Id.areaName(DungeonMonster.getPos()) == "SEW" and not NO_SEE_AREA_E.match(pos)): 
            result = CANT_SEE_IT
        else:
            pos = DungeonMonster.getPos()

            if pos in (SEW0, SEW1, SEW2):
                result = ("It's lurking at the east end of the tunnel.")
            elif pos == SEW3: 
                result = ("It's lurking halfway down the tunnel's center, at the junction.")
            elif pos == SEW4 or pos == SEW5:
                result = ("It's lurking at the west end of the tunnel.")
            elif pos == CIS1 or pos == CIS2:
                result = ("It's lurking in the north end of the cistern walkway.")
            else:
                result = ("It's lurking in the south end of the cistern walkway.")
            
            if pos == Id.PRIS or pos == Id.OUB1 or pos == Id.AARC:
                result += " You should be out of its line of sight from here."
        
        return self.description + "\t\t\t\t\t\t\t" + result



"""
    This class simulates a creature that roams the halls of the tunnels.
    The monster uses a queue to switch rooms at fixed intervals. Every time the
    player or monster moves, the monster checks for the player. 
    The monster does not move if the player is not in the dungeon area.
"""
class DungeonMonster(object):
    NONE = 0 # Not supposed to play.
    VERY_SOFT = 2
    SOFT = 4
    MEDIUM_SOFT = 7
    MEDIUM = 10
    MEDIUM_LOUD = 30
    LOUD = 50
    
    pos, ROOM_QUEUE, timer = None, None, None

    """
        Every fixed interval of time, moves the monster, plays a sound, and
        checks for player.
    """
    @staticmethod
    def creature_task():
        # Monster only moves if the player is in Z-coordinate 4, the dungeon/tunnel area.
        # Does not move if player is in the vault (Column 8 in map).
        if Player.getPos().getCoords()[0] == 4 and Player.getPos().getCoords()[2] < 7:
            DungeonMonster.move()
            DungeonMonster.checkForPlayer()

        DungeonMonster.timer.enter(5, 5, DungeonMonster.creature_task)

    @staticmethod
    def startMovement():
        DungeonMonster.pos = Id.SEW0
        DungeonMonster.ROOM_QUEUE = [Id.SEW0, Id.SEW1, Id.SEW2, Id.SEW3, Id.SEW4, Id.SEW5,
                                    Id.CIS1, Id.CIS2, Id.CIS3, Id.CIS4, Id.CIS3, Id.CIS2,
                                    Id.CIS1, Id.SEW5, Id.SEW4, Id.SEW3, Id.SEW2, Id.SEW1]
        DungeonMonster.timer = sched.scheduler(time.time, time.sleep)
        DungeonMonster.timer.enter(5, 5, DungeonMonster.creature_task, ())
        DungeonMonster.timer.run()
    
    @staticmethod
    def move():
        m_Area = Id.areaName(DungeonMonster.pos)
        p_Area = Id.areaName(Player.getPosId())
        pos = ROOM_QUEUE[0]
        ROOM_QUEUE.append(ROOM_QUEUE.pop(0))
        
        if not re.match(Id.areaName(DungeonMonster.pos), m_Area) and \
                not QUIET_AREA.match(p_Area):
            AudioPlayer.playEffect(24)

        vol = determineVolume()
        
        if vol != DungeonMonster.NONE:
            AudioPlayer.playEffect(25, vol)
    
    @staticmethod
    def determineVolume():
        """
            Every time the monster moves, it makes a sound depending on where it
            and the player are, this determines what it should be.
        """
        m_Id = Id.areaName(DungeonMonster.pos)# Where the monster is
        p_Id = Id.areaName(Player.getPosId()) # Where the player is

        if (m_Id == "CIS" and not CISTERN_AREA.match(p_Id)) or \
                (m_Id == "SEW" and not TUNNEL_AREA.match(p_Id)) or \
                (QUIET_AREA.match(p_Id)): 
            return DungeonMonster.NONE # They are in different halves of the dungeon.
        elif Player.getPos().isAdjacent(DungeonMonster.pos):
            # They are right next to each other.
            if m_Id == p_Id:
                return DungeonMonster.LOUD # Open space separates them.
            else :
                return DungeonMonster.MEDIUM_LOUD # A door separates them.
        else:
            # Bases volume off of distance.
            d = DungeonMonster.determineProximity()

            # Checks again if they are in the same area.
            if m_Id == p_Id:
                if d <= 1.9:
                    return DungeonMonster.MEDIUM_LOUD
                elif d > 1.9 and d <= 2.2:
                    return DungeonMonster.MEDIUM
                elif d > 2.2 and d <= 3.5:
                    return DungeonMonster.MEDIUM_SOFT
                else:
                    return DungeonMonster.SOFT
            elif d <= 2.0:
                return DungeonMonster.MEDIUM_SOFT
            elif d > 2.0 and d <= 3.0:
                return DungeonMonster.SOFT
            else:
                return DungeonMonster.VERY_SOFT
    
    @staticmethod
    def determineProximity():
        # Uses pythagorean theorem to determine distance.
        plyrCrd = Player.getPos().getCoords()
        thisCrd = Player.getRoomObj(pos).getCoords()

        return math.sqrt((abs(thisCrd[2] - plyrCrd[2]) ** 2) + (abs(thisCrd[1] - plyrCrd[1]) ** 2))
    
    @staticmethod
    def checkForPlayer():
        """
            Whenever the player or monster moves, it checks if it's right next
            to or in the same cell as the other.
            Synchronized because two separate threads can call self.
        """
        if re.match(Id.areaName(Player.getPosId()), Id.areaName(DungeonMonster.pos)) \
                and DungeonMonster.determineProximity() == 1.0:
            DungeonMonster.warnPlayer()
        
        if DungeonMonster.pos == Player.getPosId():
            DungeonMonster.capturePlayer()
    
    @staticmethod
    def warnPlayer():
        result = ("That creature is very close! It's directly ")
        intplyrCrd = Player.getPos().getCoords()
        thisCrd = Player.getRoomObj(DungeonMonster.pos).getCoords()
        
        if plyrCrd[1] < thisCrd[1]:
            GUI.out(result + str(Direction.SOUTH) + "!")
        elif plyrCrd[1] > thisCrd[1]:          
            GUI.out(result + str(Direction.NORTH) + "!")
        elif plyrCrd[2] < thisCrd[2]:
            GUI.out(result + str(Direction.EAST) + "!")
        else:
            GUI.out(result + str(Direction.WEST) + "!")
        
    
    @staticmethod
    def capturePlayer():
        timer.cancel()
        Player.setOccupies(Id.INTR)
        DungeonMonster.captureDialog()
        Player.getRoomObj(Id.SEWP).resetAllObjects()
        DungeonMonster.startMovement()
    
    @staticmethod
    def isInactive():
        return DungeonMonster.timer == None
    
    """
        Turns the monster around when player climbs the stairs in SEW0.
        Allows player to escape the creature if cornered in SEW0.
    """
    @staticmethod
    def turnMonsterAround():
        while not ROOM_QUEUE[0] == DungeonMonster.pos:
            ROOM_QUEUE.append(ROOM_QUEUE.pop(0))
        
        ROOM_QUEUE.append(ROOM_QUEUE.pop(0))
    
    @staticmethod
    def captureDialog():
        GUI.out("The hideous creature lassos you with its chain and drags " +
                "you back to the tiny untility room. Your items are taken. " +
                "The creature seems too mindless to take your keys though.")
        AudioPlayer.playEffect(24)
    
    @staticmethod
    def getPos():
        return DungeonMonster.pos



"""
    Defines general methods for the river in the tunnels.    
"""
class Sewer_River(SearchableFurniture, Gettable):
    def __init__(self, ref, itemList=[]):
        super(Sewer_River,self).__init__(itemList)
        self.WTR_BCKT = ref
        
        self.description = ("The river runs rapidly through a square channel on " +
                           "one side of the tunnel. The water looks cool and clear. " +
                           "This is possibly being used as a power source before " +
                           "reaching the ocean.")
        self.actDialog = ("The water is treacherous and not worth the risk.")
        self.searchDialog = ("You crouch down and scan the bottom of the river.")
        self.useDialog = ("You scoop up some of the water into the bucket.")

        self.addNameKeys("(?:raging )?river(?: of water)?", "(?:flowing )?water", 
                "(?:square )?channel")
        self.addActKeys("swim", "jump", "drink", Furniture.GETPATTERN, "hide")
        self.addUseKeys(METAL_BUCKET)
    
    def useEvent(self, item):
        AudioPlayer.playEffect(42)
        Player.getInv().remove(item)
        Player.getInv().add(self.WTR_BCKT)
        return self.useDialog
    
    def getDescription(self):
        if not self.inv.isEmpty(): 
            return self.description + " You can see something lying at the bottom."
        else:
            return self.description
    
    def interact(self, key):       
        if key == "drink":
            return ("The water looks and smells clean enough. You crouch down and take a swig, feeling refreshed.")
        elif key == "swim" or key == "hide" or key == "jump":
            return self.actDialog
        else:
            return self.getIt()
    
    def getIt(self):
        if Player.hasItem(METAL_BUCKET):
            return self.useEvent(Player.getInv().get(METAL_BUCKET))
        else:
            return ("You'll need an empty bucket...")



"""
    Hallway in which the monster walks. 
    Whenever the player enters this room, the monster checks if it is in the
    same room as the player. If so, the player is captured.    
"""
class Dungeon_Tunnel(Room):
    WATER_THERE = ("Do you feel like going for a swim?")
    MONSTER = DungeonMonsterFurniture()

    def __init__(self, name, ID):
        super(Dungeon_Tunnel,self).__init__(name, ID)
        self.addFurniture(Dungeon_Tunnel.MONSTER)

    def triggeredEvent(self):
        if DungeonMonster.isInactive():
            DungeonMonster.startMovement()
            
        DungeonMonster.checkForPlayer()
        return str(Player.getPos())



class Sew0_Stairs(Staircase):
    def __init__(self):
        super(Sew0_Stairs,self).__init__(Direction.UP, Id.DST1, 15)
        self.description = ("It's a mossy, spiraling brick staircase with no railings. " +
                          "The stairs sit right at the tunnel's end and lead upwards.")



class Sew15_Gate(Furniture):
    def __init__(self):
        super(Sew15_Gate,self).__init__()

        self.description = ("Passed the iron gate, you can see the tunnel leading " +
                           "further down into darkness. The iron bars extend down " +
                           "into the water where they form a grate of sorts, you " +
                           "suppose to prevent things from... escaping unwantedly.")
        self.actDialog = ("You can't get the gate open. It's locked.")
        self.searchDialog = ("They're just iron bars.")
        self.addNameKeys("(?:iron )?(?:barred )?(?:gate|grate)")
        self.addActKeys("open", "close")
    
    def interact(self, key):              
        if key == "open":
            return self.actDialog
        else:
            return ("The gate is already closed...")



"""
    River here contains pipe piece.
    Connects to Sew0 and Sew2    
"""
class Sew1(Dungeon_Tunnel):
    def __init__(self, name, ID):
        super(Sew1,self).__init__(name, ID)

    def getBarrier(self, direct):
        if direct == Direction.NORTH:
            return Dungeon_Tunnel.WATER_THERE
        elif direct == Direction.EAST:
            return ("You can't get the gate open. It's locked.")
        else:
            return self.bumpIntoWall()



"""
    Items added to any part of the river will be added to this object's inventory
    instead.
    The metal piece of pipe, a needed item, can be found here.    
"""
class Sew1_River(Sewer_River):
    def __init__(self, pipe, wtr):
        super(Sew1_River,self).__init__(wtr)

        self.inv = Sew1_River_Inventory(pipe)
        self.description = ("The river is about 11 feet across and 5 feet deep. " +
                           "It flows through an artificial square trench " +
                           "constructed into the floor. The water looks clear " +
                           "and smells quite clean. You imagine that it was " +
                           "a natural spring at some point before being built " +
                           "around. It flows briskly and terminates here at " +
                           "a metal grate.")
    


class Sew1_River_Inventory(Inventory):
    def __init__(self, pipe):
        super(Sew1_River_Inventory,self).__init__(pipe)
    
    def add(self, item):
        GUI.out("You reluctantly drop it in the river.")
        return super(Sew1_River_Inventory,self).add(item)
    
    def remove(self, item):
        super(Sew1_River_Inventory,self).remove(item)
        GUI.out("Though your aren't fond of the idea of jumping in, you figure " +
                "that your weight should be enough to keep you on your feet. " + 
                "you jump in, holding on to the edge, and retrieve the item.")



"""
    Items may be added to this, but because of the current, all items added
    to this will be diverted to Sew1_Rvr.    
"""
class Sew2345_River(Sewer_River):
    def __init__(self, ID, wtr):
        super(Sew2345_River,self).__init__(wtr)
        
        self.inv = River_Inventory(ID)
        
        self.description = ("The river is about 11 feet across and 5 feet deep. " +
                           "It flows through an artificial square channel " +
                           "constructed into the floor. The water looks clear " +
                           "and smells quite clean. You imagine that it was " +
                           "a natural stream at some point before being built " +
                           "around. The river flows down the tunnel " +
                           "eastwards with quite a strong current. ")
    
class River_Inventory(Inventory):
    def __init__(self, ID):
        super(River_Inventory,self).__init__()
        self.SEW1_RVR_ID = ID

    def add(self, item):
        GUI.out("You drop the item in. It immediately is whisked away down the river.")
        Player.getRoomObj(Id.SEW1).getFurnRef(self.SEW1_RVR_ID).getInv().forceAdd(item)
        return True



class Sew235_Pipe(Furniture):
    def __init__(self, room):
        super(Sew235_Pipe,self).__init__()

        if room == 2:
            self.description = ("The rusty metal pipe runs out the top of the console " +
                          "on the south wall, along the ceiling to the " +
                          "north side of the room, and along the length of " +
                          "the tunnel westward.")
        elif room == 3:
            self.description = ("The metal pipe is bracketed to the ceiling " +
                          "over the river below. It's very rusty from the " +
                          "apparent years of neglect.")
        elif room == 5:
            self.description = ("The rusty metal pipe runs around the bend along " +
                          "the ceiling and into the wall above the door to the west.")

        self.searchDialog = ("It doesn't seem to be hiding anything.")
        self.useDialog = ("There's nothing missing from the pipe in this area!")

        self.addNameKeys("(?:large )?(?:rusty )?(?:metal )?pip(?:e|ing)")
        self.addUseKeys(PIECE_OF_PIPE)



"""
    Contains the valves used to give access to the ancient cistern.
    Connects to Sew1 and Sew3    
"""
class Sew2(Dungeon_Tunnel):
    def __init__(self, name, ID):
        super(Sew2,self).__init__(name, ID)

    def getBarrier(self, direct):
        if direct == Direction.NORTH:
            return Dungeon_Tunnel.WATER_THERE
        else:
            return self.bumpIntoWall()



"""
    This is a valve puzzle. 
    The player must turn the correct combination of valves to on and then pull
    the lever in SEW5 to empty the poisonous gas from the cistern.
    
    SOLUTION: 001
              110
              011    
"""
class Sew2_Valves(Furniture, Resetable):
    class State:
        # Represents an on and off state and
        # an appropriate character image of
        # the dial.
        def __init__(self, dial, state):
            self.DIAL = dial
            self.STATE = state

        def __str__(self):
            return self.DIAL

        def state(self):
            return self.STATE
    
    ON = State("( /)  ", 1)
    OFF = State("(\\ )  ", 0)
    
    VLVS = (OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF)
    MAP = {"i": 0, "ii" : 1, "iii" : 2,  "iv" : 3, "v" : 4, "vi" : 5, "vii" : 6, "viii" : 7, "ix": 8}
    SOLUTION = (0, 0, 1, 1, 1, 0, 0, 1, 1)
    
    def __init__(self):
        super(Sew2_Valves,self).__init__()

        self.description = ("It's a grid of 9 valves protruding from a console " +
                           "on the wall. Above each is a roman numeral and a small " +
                           "gauge. The rusty metal pipe originates from and leads out of the console's top.")
        self.searchDialog = ("There's nothing here that you can take.")

        self.addNameKeys("(?:metal )?valves?", "console", "grid of valves", "(?:roman )?(?:numerals|numbers)")
        self.addActKeys(Furniture.VALVEPATTERN)
    
    def interact(self, key):    
        ans = (" ")

        while ans:
            GUI.out("There are dials above each.\t\t\t\t\t" +
                self.printValves() + "\t\t\t\tTurn which one?")
            ans = GUI.askChoice(Menus.SEW_VALVE, ROMAN_NUMERAL_P)

            if ONE_TO_NINE.match(ans): 
                self.turnValve(int(ans) - 1)
            elif ans: 
                self.turnValve(int(Sew2_Valves.MAP[ans]))
        
        return Furniture.NOTHING
    
    def printValves(self):        
        return ("       I     II   III\t\t" +
                "      " + str(Sew2_Valves.VLVS[0]) + str(Sew2_Valves.VLVS[1]) + str(Sew2_Valves.VLVS[2]) + "\t" +
                "       IV    V     VI\t\t" +
                "      " + str(Sew2_Valves.VLVS[3]) + str(Sew2_Valves.VLVS[4]) + str(Sew2_Valves.VLVS[5]) + "\t" +
                "      VII   VIII   IX\t\t" +
                "      " + str(Sew2_Valves.VLVS[6]) + str(Sew2_Valves.VLVS[7]) + str(Sew2_Valves.VLVS[8]) + "\t")
    
    def turnValve(self, v):
        AudioPlayer.playEffect(17)
        
        if Sew2_Valves.VLVS[valveNum] == Sew2_Valves.ON:
            Sew2_Valves.VLVS[valveNum] = Sew2_Valves.OFF
        else:
            Sew2_Valves.VLVS[valveNum] = Sew2_Valves.ON
    
    def solved(self):
        for v in range(9):
            if Sew2_Valves.SOLUTION[v] != Sew2_Valves.VLVS[v].state():
                return False

        return True
    
    def reset(self):
        for i in range(len(Sew2_Valves.VLVS)):
            Sew2_Valves.VLVS[i] = Sew2_Valves.OFF



"""
    The player must find a piece of pipe and use on this in order to properly
    operate the valves.
"""
class Sew4_Pipe(Furniture, Resetable, Unmoveable):
    def __init__(self, ID, pipe):
        super(Sew4_Pipe,self).__init__()
        
        self.SEW1_RVR = ID
        self.PIPE_REF = pipe
        self.hasPipe = False
        
        self.description = ("The rusty pipe runs along the ceiling around the " +
                           "bend right above the river. ")
        self.searchDialog = ("The pipe has a gap where a piece has fallen.")
        self.useDialog = ("The pipe is too high up for you to reach!")

        self.addNameKeys("(?:large )?(?:rusty )?(?:metal )?pip(?:e|ing)", "gap")
        self.addUseKeys(PIECE_OF_PIPE)
    
    def getDescription(self):
        if self.hasPipe:
            return self.description
        else:
            return self.description + "The piping here has a short 2-foot section missing."
    
    def getSearchDialog(self):
        return ("The pipe isn't hiding anything unusual." if self.hasPipe else self.searchDialog)
    
    def useEvent(self, item):
        if Player.getPos().hasFurniture(Names.METAL_LADDER):
            Player.getInv().remove(item)
            AudioPlayer.playEffect(51)
            self.hasPipe = True
            Player.describeRoom()
            return ("With all your strength, you shove the piping between the " +
                   "break in the piping. It's a good fit, but may not hold long...")
        else:
            return self.useDialog
    
    def isMissingPipe(self):
        return not self.hasPipe
    
    """
        Puts pipe back in Sew1 river and sets hasPipe to False.
    """
    def reset(self):
        if self.hasPipe:
            self.hasPipe = False
            Player.getRoomObj(Id.SEW1).getFurnRef(SEW1_RVR).getInv().forceAdd(self.PIPE_REF) # Prevents dialog.



"""
    Contains a pipe with a missing piece which player must replace.
    Connects to Sew3 and Sew5
"""
class Sew4(Dungeon_Tunnel):
    def __init__(self, name, ID, ID2):
        super(Sew4,self).__init__(name, ID)
        self.SEW4_PP = ID2

    def getDescription(self):
        p = Player.getRoomObj(Id.SEW4).getFurnRef(self.SEW4_PP)
        
        if p.isMissingPipe():
            return super(Sew4,self).getDescription() + " The pipe has a gap where a piece is missing..."
        else:
            return super(Sew4,self).getDescription()



"""
    The end of the tunnel, contains valve to drain toxic gas from Cis1.
    Connects to Cis1, Pris, and Sew4    
"""
class Sew5(Dungeon_Tunnel):
    def __init__(self, name, ID):
        super(Sew5,self).__init__(name, ID)

    def getBarrier(self, direct):
        if direct == Direction.NORTH:
            return ("You can't get the gate open. It's locked.")
        else:
            return self.bumpIntoWall()


"""
    Disperses the gas in CIS1 if the valve puzzle in SEW2 has been solved.    
"""
class Sew5_Valve(Furniture):
    def __init__(self, ID, ID2):
        super(Sew5_Valve,self).__init__()
        
        self.SEW2VLVS = ID
        self.SEW4PP = ID2
        
        self.description = ("The metal valve is connected to a console mounted " +
                           "on the wall next to the door. A smaller pipe coming " +
                           "out the top of the console connects to the larger " +
                           "pipe running through the wall above the door.")
        self.actDialog = ("With all your strength, you manage to turn the valve.")

        self.addNameKeys("(?:metal )?valve", "console", "smaller pipe")
        self.addActKeys(Furniture.VALVEPATTERN)
    
    def interact(self, key):       
        AudioPlayer.playEffect(17)
        v = Player.getRoomObj(Id.SEW2).getFurnRef(self.SEW2VLVS)
        p = Player.getRoomObj(Id.SEW4).getFurnRef(self.SEW4PP)
        
        if not p.isMissingPipe() and v.solved():
            Player.getRoomObj(Id.CIS1).turnOffGas()
        
        return self.actDialog



class Sew_Bridge(Furniture, Unmoveable):
    def __init__(self, direct):
        super(Sew_Bridge,self).__init__()

        self.DIR = direct        
        self.description = ("The small, 11-foot stone bridge crosses over the river to another area.")
        self.searchDialog = ("There's nothing on or under the bridge.")
        self.actDialog = Furniture.NOTHING

        self.addNameKeys("(?:under (?:the )?)?(?:small )?(?:stone )?bridge", 
                  str(direct) + " (?:under (?:the )?)?(?:small )?(?:stone )?bridge")
        self.addActKeys("cross", "go|walk|run")
    
    def interact(self, key):
        Player.move(DIR)
        return self.actDialog



"""
    A metal door, as opposed to wooden doors found in the rest of the castle.    
"""
class Sew_Door(Door):
    def __init__(self, direct):
        super(Sew_Door,self).__init__(direct)
        self.description = ("It's an arched metal door with rivets around the edge.")
        self.NAMEKEYS.pop(1)
        self.addNameKeys("(?:arched )?(?:metal )?door")

    def useEvent(self, item):
        if str(item) == HAND_TORCH: 
            return ("Could you possibly burn down a metal door?")
        else:
            return super(Sew_Door, self).useEvent(item)



class Sew_Moss(Furniture):    
    def __init__(self):
        super(Sew_Moss,self).__init__()

        self.description = ("It looks like Sphagnum- a peaty moss genus.")
        self.addNameKeys("moss")



"""
    Provides a description of the tunnel for the player.    
"""
class Sew_Tunnel(Furniture, Unmoveable):
    def __init__(self):
        super(Sew_Tunnel,self).__init__()

        self.description = ("This underground tunnel is warm and humid. The tunnel " +
                           "is about 20 feet wide and has an arched ceiling about " +
                           "20 feet above. A river flows down its length along one " +
                           "wall. The tunnel is lit with many torches nailed to the walls.")
        self.searchDialog = ("The tunnel is too large to do that.")

        self.addNameKeys("(?:warm )?(?:humid )?(?:underground )?tunnel", "(?:tunnel )?ceiling")