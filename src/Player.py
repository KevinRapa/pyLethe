from Names import *
from Patterns import *
from Inventory import Inventory
from Item import *
import Direction, Furniture, Map_Display, Menus, Id
from RoomGraph import RoomGraph
import pickle, re, random, collections
from shutil import rmtree

"""
    Represents the player and processes user input (Game's 'operating system').
    All player actions originate from this class. The player has access
    to its own location, and thereby each furniture and item in the location
    too.

    The text parser and player attributes class are nested inside this class
    because of their close relationship with Player.

    The game is spent entirely in the mainPrompt() loop.
"""

class Player(object):
    ROOM_CACHE = collections.deque() # Stores room visited in the current game.
    notEnd = True   # Game ends when this is False.

    lastItem, lastFurn, lstVisit, shoes = "", "", "", ""
    inv, keys, visited, pos = None, None, None, None
    moves, score = 0, 0
    moveScheme = WSDA
    defAct = "examine"
 
    MAIN_CMD = {}  # Maps commands from main prompt
    ODD_CMD = {}   # Maps random commands
    
    ERROR_MSGS = (
        "I might have misunderstood you on something...", "I beg your pardon?",
        "Is that how kids are saying it nowadays?" , "Bless you!",
        "Might want to look that over again.", "Is that slang for something?")    
    DENIAL_MSGS = (
        "That is quite an ambitious proposition.", "A valiant attempt.", 
        "Did you have much to drink before you came?", "A novel concept!",
        "An ingenious idea from one of your education.",
        "The player is thwarted in the ridiculous attempt.")
    
    # Maps various simple commands in the game to their actions.
    goUp =     lambda: GUI.out(Player._findStaircase(Direction.UP))
    goDown =   lambda: GUI.out(Player._findStaircase(Direction.DOWN))
    goNrth =   lambda: Player.move(Direction.NORTH)
    goSth =    lambda: Player.move(Direction.SOUTH)
    goEast =   lambda: Player.move(Direction.EAST)
    goWest =   lambda: Player.move(Direction.WEST)
    goNw =     lambda: Player.move(Direction.NW)
    goNe =     lambda: Player.move(Direction.NE)
    goSw =     lambda: Player.move(Direction.SW)
    goSe =     lambda: Player.move(Direction.SE)
    showInv =  lambda: Player.printInv()
    moveSelf = lambda: Player._evaluateAction("move", "self")
    quit =     lambda: Player._endGame()
    viewKeys = lambda: Player.viewKeyRing()
    denialMsg = lambda: Player.randomDenialMsg()
    note =     lambda: Player._writePrompt()
    yell =     lambda: GUI.out("AHHHHHGGGHHH!!!!!")
    options =  lambda: Player._options()
    showMap =  lambda: Map_Display.displayMap()
    openLoot = lambda: Player._openLootSack()
    showHelp = lambda: Help.helpSub()
    stand =    lambda: GUI.out("You stand and do nothing.")
    rest =     lambda: GUI.out("You sit and rest a moment.")
    combine =  lambda: Player._combineSub()
    sortInv =  lambda: Player.inv.sortInventory()
    indefLook = lambda: Player._evaluateAction("look", "it")
    win =      lambda: GUI.out("Oh wait, that's itnot You winnot Congratulationsnot You may go home now.")
    civilMsg = lambda: GUI.out("Let us act like civilized guests whilst we're here.")
    balloon =  lambda: GUI.out("Does this look like some kind of balloon to you?")
    inappr =   lambda: GUI.out("You are sure the owner wouldn't wanting you doing that.")
    zork =     lambda: GUI.out("What do you think this is? Zork?")
    story =    lambda: GUI.out(("Well I was born in Norwich England in a rather poor household. " +
                                  "I have fond memories of mother and I weaving baskets to sell " +
                                  "at the local market, and my sister and I would always collect " +
                                  "pebbles on the ground that resembled Welshmen. Oh, I think I'm " +
                                  "beginning to drone..."))

    def xyzzy():
        GUI.out("A hollow clown says surprise.") 
        GUI.randomizeColors()

    def hide():
        ID = areaName(Player.getPosId()) 
        if ID == "SEW" or ID == "CIS":
            GUI.out("There is nowhere to hide.")
        else:
            GUI.out("There is no apparent reason to do that...")

    for command, action in \
            (("h", showHelp),
             ("k", viewKeys),
             ("m", showMap),
             ("n", note),
             ("l", openLoot),
             ("o", options),         
             ("q", quit),
             ("w", goNrth),
             ("s", goSth),    
             ("a", goWest), 
             ("d", goEast), 
             ("north", goNrth),
             ("south", goSth),
             ("west", goWest),
             ("east", goEast),
             ("forward", goNrth),
             ("backward", goSth),
             ("backwards", goSth),    
             ("back", goSth),
             ("left", goWest),
             ("right", goEast),
             ("up", goUp),
             ("down", goDown), 
             ("upward", goUp),
             ("downward", goDown),
             ("upwards", goUp),
             ("downwards", goDown), 
             ("upstairs", goUp),
             ("downstairs", goDown),
             ("nw", goNw),
             ("ne", goNe),
             ("sw", goSw), 
             ("se", goSe),
             ("northwest", goNw),
             ("northeast", goNe),
             ("southwest", goSw), 
             ("southeast", goSe),
             ("i", showInv),
             ("inv", showInv),
             ("inventory", showInv),
             ("move", moveSelf),
             ("walk", moveSelf),
             ("go", moveSelf), 
             ("run", moveSelf),
             ("travel", moveSelf),
             ("keys", viewKeys),
             ("keyring", viewKeys), 
             ("loot", openLoot),
             ("help", showHelp),
             ("sort", sortInv), 
             ("map", showMap),
             ("note", note),
             ("write", note),
             ("write note", note),
             ("wait", stand), 
             ("stand", stand),
             ("sit down", rest),
             ("sit", rest),
             ("chat", story),
             ("talk", story), 
             ("converse", story),
             ("it", indefLook),
             ("them", indefLook),
             ("scream", yell),
             ("yell", yell),
             ("win", win),
             ("win the game", win),
             ("combine", combine),
             ("hi", zork),
             ("brief", zork),
             ("diagnose", zork),
             ("hello", zork),
             ("hey", zork),
             ("sup", zork),
             ("verbose", zork),         
             ("superbrief", zork),
    #
            ("mute",   lambda: GUI.mute()),
            ("click", lambda: GUI.setClick()),
            ("swap",   lambda: GUI.swap()),
            ("options", options),
            ("save", lambda: Player.saveGame()),
            ("close",  lambda: Map.hideMap()),
            ("quit", quit),
            ("exit", quit),
            ("credits",lambda: GUI.displayCredits()), 
            ("version", lambda: GUI.out(Menus.VERSION)),
            ("lethe",  lambda: GUI.out("Hello, dear.")),
            ("zork",   lambda: GUI.out("You must be mistaking me for someone else.")),
            ("smell",  lambda: GUI.out("Smells like a brisk autumn night in 1932.")),
            ("jump",   lambda: GUI.out("You jump a short height into the air. Well,  that was fun.")),
            ("die",    lambda: GUI.out("You can't just die at will. Try \"commit suicide\" or something else. Should I have mentioned that?")),
            ("look",   lambda: _TextParser.getCommand("look at").perform()),
            ("listen", lambda: GUI.out("Sounds like an old castle.")),
            ("fly",    lambda: GUI.out("You do not possess the skills to fly.")),
            ("kneel",  lambda: GUI.out("You kneel down.")),
            ("garden", lambda: GUI.out("That isn't really a hobby of yours.")),
            ("pray",   lambda: GUI.out("The gods will help those who help themselves.")),
            ("swim",   lambda: GUI.out("You are not the greatest swimmer.")),
            ("relax",  lambda: GUI.out("You can hardly relax standing up.")),
            ("sleep",  lambda: GUI.out("You decide to rest your eyes standing for a brief period. An unknown amount of time passes.")),
            ("xyzzy",  lambda: xyzzy), 
            ("hide",  lambda: hide)):
        MAIN_CMD[command] = action 

    
    ODD_CMD["climb"] = civilMsg    
    ODD_CMD["jump"] = civilMsg
    ODD_CMD["write"] = inappr
    ODD_CMD["draw"] = inappr
    ODD_CMD["inflate"] = balloon
    ODD_CMD["deflate"] = balloon
    
    ODD_CMD["smell"] = lambda: GUI.out("You press your nose up against it and inhale deeply.")
    ODD_CMD["find"] =  lambda: GUI.out("You have already found it detective.")
    ODD_CMD["count"] = lambda: GUI.out("You didn't climb all the way up to this precipice to do math.")
    ODD_CMD["burn"] =  lambda: GUI.out("Yes... burn it... burn it all down to the ground.")
    
    for cmd in ("take", "get", "eat", "fight", "speak", "talk", "lift", "pick"):
        ODD_CMD[cmd] = denialMsg

    """
        Converts a string of a piece of furniture to its object equivalent.
        Furniture is checked for existence before calling this method.
        @param name The name of a piece of furniture in your location.
        @return The furniture object with the name.
    """
    @staticmethod
    def getFurnRef(name):
        for furn in Player.getPos().getFurnishings():
            if furn.nameKeyMatches(name):
                return furn           

        return None
    
    @staticmethod
    def randomDenialMsg():
        GUI.out(random.choice(Player.DENIAL_MSGS))
    
    @staticmethod
    def randomErrorMessage():
        GUI.out(random.choice(Player.ERROR_MSGS))
    
    @staticmethod
    def getLastVisited(): 
        return Player.lstVisit 
    
    @staticmethod
    def getInv():
        return Player.inv 

    @staticmethod
    def addKey(key): 
        keys.add(key) 

    @staticmethod
    def getPos(): 
        return Player.getRoomObj(RoomGraph.getRoomID(Player.pos))

    @staticmethod
    def getPosId():
        return RoomGraph.getRoomID(Player.pos)

    """
        Returns a room object with the ID.
        Constants from the ID class should be used with self.
        @param ID a four-character room ID
        @return A room object with the ID.
    """
    @staticmethod
    def getRoomObj(ID):
        # Searches for a room in ROOM_CACHE with the ID.
        for room in Player.ROOM_CACHE:
            if room.getID() == ID:
                Player.ROOM_CACHE.remove(room)
                Player.ROOM_CACHE.appendleft(room)
                return room

        # Not found. Load it into the front of the room cache.
        c = RoomGraph.getCoords(ID)
        result = Player._readInRoom(ID, c[0], c[1])
        Player.ROOM_CACHE.append(result) 
        return result

    """
        Reads in a room from a file based on the room's ID, floor number, and
        row number (Assuming the room wasn't found in <code>ROOM_CACHE</code>.
        @param id The ID of the room
        @param lvl The floor the room is on.
        @param row The row number the room is on.
        @return A reference to the room.
    """
    @staticmethod
    def _readInRoom(ID, lvl, row):
        # Rooms are organized by floor and then row number in the filesystem.
        path = (ROOMS_DATA_PATH + SEP + "lvl_" + str(lvl) + 
            SEP + "row_" + str(row) + SEP + ID + ".data")

        with open(path, "rb") as roomObj:
            return pickle.load(roomObj)
    
    @staticmethod
    def getShoes():
        return Player.shoes 

    @staticmethod
    def getCurrentFloor(): 
        return Player.pos[0] # Used to update the picture in the map.

    @staticmethod
    def getScore(): 
        return Player.score 

    @staticmethod
    def _tryIndefRef_Furn(s):
        # If the argument equals "it/them" returns last referenced furniture.
        return (Player.lastFurn if (s == "it" or s == "them") else s)

    @staticmethod
    def _tryIndefRef_Item(s):
        # If the argument equals "it/them" returns the last referenced item.
        return (Player.lastItem if (s == "it" or s == "them") else s)

    
    """
        Checks if an item in the player's inventory has the exact name of itemName.
        For use with strings in Names
        
        @param itemName The name of an item.
        @return If the player's inventory contains an item with the exact name.
    """
    @staticmethod
    def hasItem(itemName):
        return Player.inv.contains(itemName)

    """
        Sends the player to Hades and removes all non-loot sack items from the 
        player's inventory.
        A Zork references.
        @param message The reason for the death.
    """
    @staticmethod
    def _commitSuicide(message):
        if not Player.getPosId() == Id.HADS:
            Player._incrementMoves()
            GUI.descOut(message) 
            GUI.menOut(Menus.ENTER)
            GUI.promptOut()
            i = Player.inv.get(LOOT_SACK)
            Player.inv.clear()
            
            # Saves the loot sack.
            if not i is Inventory.NULL_ITEM:
                Player.inv.add(i)
            
            Player.printInv()
            Player.setOccupies(Id.HADS)
        else:
            GUI.out("You can't do even that.")
    
    """
        'Teleports' the player to another room from a choice.
        @param id destination area.
    """
    @staticmethod
    def setOccupies(ID):
        Player.lstVisit = Player.getPosId()
        Player.pos = RoomGraph.getCoords(ID)
        Map_Display.updateMap()
        Player.describeRoom()
        GUI.roomOut(Player.getPos().triggeredEvent())
        
        if not Player.hasVisited(Player.getPosId()):
            Player.visited.append(Player.getPosId()) 
    
    """
        Teleports the player to a room at random.
        Avoids illegal rooms (Rooms that could potentially trap the player).
        Used by the teleporter in the Gallery and the Factum
    """
    @staticmethod
    def teleport():
        i = random.randint(0, Player.visited.size() - 1)
        ID = visited.get(i)

        while NO_TELEPORT_P.match(id) or ID == Player.getPosId():
            i = random.randint(0, Player.visited.size() - 1)
            ID = Player.visited.get(i)
        
        Player.setOccupies(id)

    @staticmethod
    def _setLastInteract_Furn(furnName):
        Player.lastFurn = furnName

    @staticmethod
    def _setLastInteract_Item(itemName):
        Player.lastItem = itemName

    @staticmethod
    def setShoes(shoes):
        Player.shoes = shoes

    @staticmethod
    def _incrementMoves():
        Player.moves += 1
        GUI.updateMovesAndScore(Player.moves, Player.score)

    @staticmethod
    def updateScore(score):
        Player.score = score
        GUI.updateMovesAndScore(Player.moves, Player.score)
    
    @staticmethod
    def eraseGame():
        if os.path.exists(SAVE_PATH):
            os.remove(SAVE_PATH)
            rmtree(ROOMS_DATA_PATH)
            print("Data erased.")
        else:
            print("Data to erase not found.")
        

    # Writes fields to a .data file to be read next time a game starts.
    @staticmethod
    def savePlayerAttributes(file): 
        pickle.dump(_PlayerAttributes(), file)
    
    """
        Serializes each room in <code>ROOM_CACHE</code> when a save is made.
    """
    @staticmethod
    def saveRoomChanges():
        base = ROOMS_DATA_PATH + SEP + "lvl_"
        
        for room in Player.ROOM_CACHE:
            c = room.getCoords()
            path = base + str(c[0]) + SEP + "row_" + str(c[1]) + SEP + room.getID() + ".data"
            
            with open(path, "wb") as file: 
                pickle.dump(room, file)

        Player.ROOM_CACHE.clear()

    @staticmethod
    def saveGame():
        with open(SAVE_PATH, "wb") as gameData:
            # Successfully saves the game.
            Player.savePlayerAttributes(gameData) 
            Player.saveRoomChanges()
            GUI.out("Game saved")

    """
        Sets <code>Player</code> fields to the saved player attributes.
        Used when a game is loaded from a file.
        @param attr _PlayerAttributes object
    """
    @staticmethod
    def loadAttributes(attributes):
        Player.inv = attributes.INV
        Player.keys = attributes.KEYS
        Player.pos = attributes.POS
        Player.visited = attributes.VISITED
        Player.lstVisit = attributes.LSTVISITED
        Player.shoes = attributes.SHOES
        Player.score = attributes.SCORE
        Player.moves = attributes.MOVES
        Player.defAct = attributes.DEF_ACT
        Player.moveScheme = attributes.MOVE_SCHEME
        GUI.updateMovesAndScore(Player.moves, Player.score)

    """
        Creates new attributes that the player starts a new game with.
        @param coords Coordinates the player begins the game at.
    """
    @staticmethod
    def setNewAttributes(coords):
        Player.inv = PlayerInventory()
        Player.keys = Inventory([])
        Player.visited = []
        Player.pos = coords
        GUI.updateMovesAndScore(0, 0)
    
    @staticmethod
    def _endGame():
        Player.notEnd = False

    """
        The main prompt for controlling the player's moves.
    """
    @staticmethod
    def mainPrompt():
        AudioPlayer.playTrack(Player.getPosId())
        Player.printInv()
        GUI.roomOut(Player.getPos().triggeredEvent())
        Player.describeRoom()

        while Player.notEnd:
            # Asks player over and over again for commands.
            GUI.toMainMenu()
            ans = GUI.promptOut()

            if len(ans) > 2000:
                GUI.out("Wow, that was long. I really don't feel like figuring that one out.")
            elif ans in Player.MAIN_CMD.keys(): 
                Player.MAIN_CMD[ans]() # Simple command
            elif ans: 
                _TextParser.getCommand(ans).perform() # Complicated command.
            
            if not Player.notEnd:
                # Player entered 'quit' or 'q'.
                # Asks to save a game, erase one, go back, or just quit.
                ans = GUI.askChoice(Menus.SAVE_QUIT, SAVE_QUIT_RESET_P)
        
                if ans == "s": 
                    Player.saveGame()
                elif ans == "r": 
                    Player.eraseGame()
                elif ans == "b":
                    Player.notEnd = True

    @staticmethod
    def answeredYes(playerChoice):
        return playerChoice == "yes" or playerChoice == "y"

    """
        For some events that trigger the first time the player enters a room, etc.
        @param roomID The ID of a particular room.
        @return If you have visited the given room before.
    """
    @staticmethod
    def hasVisited(roomID):
        return roomID in Player.visited

    """
        Moves the player in the specified direction.
        Two rooms are considered not to have a door between them if the first
        three characters of their IDs are identical. An exception is made for 
        caves and catacombs, which have no doors. Stairs and climables move the
        player up and down. Nothing else should.
        @param d A cardinal direction.
    """
    @staticmethod
    def move(d): 
        dstId = RoomGraph.getRoomID((Player.pos[0] + d.Z, Player.pos[1] + d.Y, Player.pos[2] + d.X))
        dest = Player.getRoomObj(dstId)
        Player._incrementMoves()
        
        if not (d.X or d.Y or d.Z):
            # Player typed an ordinal dection.
            GUI.out("Your humble life as a tradesman knows not how to move " + str(d) + ".")
        elif not Player.getPos().isAdjacent(dstId):
            GUI.out(Player.getPos().getBarrier(d)) # Non-door barrier in the way.
        elif dest.isLocked() and not Player.hasKey(dstId):
            AudioPlayer.playEffect(4) # Locked and you don't have a key.
            GUI.out("The door here is locked.") 
        else:
            # Moves the player, determines the noise to play.
            GUI.clearDialog()
            Player.lstVisit = Player.getPosId()
            Player.pos = dest.getCoords()
            Map_Display.updateMap()

            if dest.isLocked() and not Player.hasVisited(dstId):
                AudioPlayer.playEffect(13) # Plays unlock sound.
            elif Player.pos[0] < 5 and not dstId.startswith(Id.areaName(Player.lstVisit)):   
                # Not in catacombs or caves.
                if (Player.pos[0] == 4 and dstId == Id.CS35) or dstId == Id.CT34:
                    AudioPlayer.playEffect(24) # Metal door. In dungeon area. 
                else:
                    AudioPlayer.playEffect(9)  # Wooden door sound. 
            elif Player.pos[0] >= 5  and not dstId.startswith(Player.lstVisit[0:2]):
                AudioPlayer.playEffect(9) # Wood door sound in catacombs.
            else:
                AudioPlayer.playEffect(0) # Footsteps. No door there.
            
            Player.describeRoom()
            GUI.roomOut(dest.triggeredEvent())
            
            if not Player.hasVisited(dstId):
                Player.visited.append(dstId)  
    
    """
        Searches for a climbable object in the room going in the specified
        direction.
        Used when the player types something like "up" or "down".
        @param d The direction the object should lead, 'up' or 'down'.
    """
    @staticmethod
    def _findStaircase(direct):
        for furn in Player.getPos().getFurnishings():
            if isinstance(furn, Furniture.Climbable):
                if furn.getDir() == Direction.BOTH:
                    return furn.interact(str(direct))                    
                if furn.getDir() == direct:
                    return furn.interact("climb")
        
        return "There's nothing here to take you " + str(direct) + "."

    """
        In the player's position, plays its music and displays its description.
    """
    @staticmethod
    def describeRoom():
        AudioPlayer.playTrack(Player.getPosId())
        desc = Player.getPos().getDescription()
        
        GUI.descOut(desc if desc else ("Immediately, a pair of rather large flies dart into " +
                        "your eyes, blinding you momentarily. You cannot see a thing."))

    @staticmethod
    def viewKeyRing():
        AudioPlayer.playEffect(3)
        GUI.out("Keys:" + NL + str(Player.keys)) 
    
    """
        Used to check if the player may enter a particular locked room.
        @param keyID The ID of a key, corresponding to a room ID.
        @return If you have the key.
    """
    @staticmethod
    def hasKey(keyID):
        for key in Player.keys.CONTENTS:              
            if key.getType() == keyID:
                return True

        return False

    """
        Prints the furniture search dialog and initiates search if searchable.
        @param furn The furniture being searched.
    """
    @staticmethod
    def trySearch(furn):
        GUI.out(furn.getSearchDialog())
        
        if furn.isSearchable():
            Player.search(furn.getInv()) 
    
    """
        Subroutine for exchanging itemList between player and furniture inventories.
        @param furnInv The furniture being searched.
    """
    @staticmethod
    def search(furnInv):
        while True:
            Player.printInv(furnInv)
            GUI.menOut(Menus.TRADE_SUB)
            cmd = GUI.promptOut()
            
            if LOOT_ACTION_P.match(cmd):
                # Takes as many items as possible from the furniture.
                Player._incrementMoves()

                while not furnInv.isEmpty() and not Player.inv.isFull():
                    Player._evalTake(furnInv, furnInv.get(0)) 

                GUI.out("You ravenously stuff your pockets.")
            elif cmd:
                scan = cmd.split(' ')
                action = scan.pop(0)

                if not scan:
                    # If player enters just a digit, means "examine <slot>"
                    if ANY_DIGIT_P.match(action):
                        item = furnInv.get(action)
                        
                        if item is Inventory.NULL_ITEM:
                            GUI.out("There's nothing there.")
                        elif isinstance(item, Key):
                            GUI.out("It's a small key.")
                        else:
                            GUI.out(item.getDesc())
                    else: 
                        # Notifies that a list wasn't entered.
                        GUI.out("Did you... forget to enter something there?")
                #
                elif CHECK_P.match(action):
                    # Player wants to examine something from the search routine.
                    i = Player._getItemList(' '.join(scan), furnInv)
                    Player._incrementMoves()
                    
                    if len(i) > 1:
                        GUI.out("Whoa now, one thing at a time please.")
                    elif not len(i):
                        GUI.out("You're going to need to enter something in...")
                    elif i[0] is Inventory.NULL_ITEM:
                        GUI.out("I couldn't find that in there...")
                    else:
                        if isinstance(i[0], Readable):
                            AudioPlayer.playEffect(2) # Plays the page turning sound.
                        
                        GUI.out(i[0].getDesc())
                #
                elif STORE_P.match(action):
                    # Player wants to take items.
                    Player._incrementMoves()

                    for i in Player._getItemList(' '.join(scan), Player.inv):
                        if Player.inv.contains(str(i)):
                            Player._evalStore(furnInv, i)
                        else:
                            Player.randomErrorMessage()
                #
                elif TAKE_P.match(action):
                    # Player wants to store items.
                    Player._incrementMoves()

                    for i in Player._getItemList(' '.join(scan), furnInv):
                        if furnInv.contains(str(i)):
                            Player._evalTake(furnInv, i) 
                        else:
                            Player.randomErrorMessage()
                #
                else:
                    GUI.out("A thousand pardons... what was that first thing you typed??")
                
                Player.describeRoom()
            else:
                break
            
        Player.printInv()
    
    """
        Takes a list of names, returns a list of items found in the inventory.
        Items that weren't found are replaced by a NULL_ITEM.
        Example 1: "take the book, the parchment, and the pen"
        Example 2: "take 1, 2, and 3"
    """
    @staticmethod
    def _getItemList(itemList, inv):
        if not itemList: 
            return []
            
        # Trims articles off.
        trimmed = ARTICLE_P.sub("", itemList)

        if (trimmed == "it" or trimmed == "them") and Player.inv.size() == 1:
            # If "it/them" used, and has one item, only option is first item.
            return [inv.get(0)]
        elif trimmed == "all" or trimmed == "everything":
            return inv.CONTENTS[:]

        itemArray = LIST_P.split(trimmed)
        resultArray = []

        for itemName in itemArray:
            # Populate the list with items
            itemName = Player._tryIndefRef_Item(itemName) # Resolves 'it'
            item = inv.get(itemName) # Gets NULL_ITEM if not found.
            
            if not item in resultArray: # Prevents adding duplicates
                resultArray.append(item)

        #DEBUG print("ITEMS PARSED -> " + str(resultArray))
        return resultArray

    
    """
        Evaluates the player's take action.
        @param furniture The furniture from which to take an item.
        @param take The item being taken.
    """
    @staticmethod
    def _evalTake(furnInv, take):
        if KEY_P.match(take.getType()):
            # Matches a non-cave/catacomb room ID, which keys use as types.
            furnInv.give(take, Player.keys)
            AudioPlayer.playEffect(3)
        else:
            Player._setLastInteract_Item(str(take))
            furnInv.give(take, Player.inv)         
    
    """
        Evaluates the player's store action.
        @param furnInv The inventory in which the item is being stored.
        @param store The item being stored.
    """
    @staticmethod
    def _evalStore(furnInv, store):
        Player.inv.give(store, furnInv) 

        if str(store) == Player.shoes:
            Player.shoes = "" # If player stores the shoes currently wearing.

    """
        Processes a player's action on furniture.
        For processing actions on items, see execute() in Command class below.
        @param furnName the name of the furniture being acted upon.
        @param verb the action the player is performing on the furniture.
    """
    @staticmethod
    def _evaluateAction(verb, furnName):
        obj = Player._tryIndefRef_Furn(furnName)
        item = Player.inv.get(Player._tryIndefRef_Item(furnName))
        furnExists = Player.getPos().hasFurniture(obj)

        if furnExists:
            # Furniture exists to be interacted with.
            furn = Player.getFurnRef(obj)
            Player._setLastInteract_Furn(obj)

            if furn.actKeyMatches(verb):
                # Player typed an action specific to a furniture type.
                Player._incrementMoves()
                GUI.out(furn.interact(verb)) 
                Player.describeRoom()
                Player.printInv()
            elif CHECK_P.match(verb):
                # Player typed something resembling "examine <furniture>"
                Player._incrementMoves()
                GUI.out(furn.getDescription()) 
            elif SEARCH_P.match(verb) or \
                    (verb == "open" or verb == "empty" and isinstance(furn, Openable)):      
                Player.trySearch(furn) # Player implied a search
            else:
                Player._incrementMoves()
                
                if MOVE_P.match(verb) and isinstance(furn, Furniture.Moveable): 
                    # Player typed something resembling "move <furniture>"
                    GUI.out(furn.moveIt())
                elif DESTROY_P.match(verb):
                    # Player typed something like "get <furniture>" but isn't gettable.
                    GUI.out("Yes, you're frustrated and hungry, but abstain from the wrathful thoughts.")
                elif verb in Player.ODD_CMD.keys():
                    # Standard output strings for wierd input.
                    (Player.ODD_CMD[verb])()
                else:
                    GUI.out("Doing that to the " + obj + " seems unnecessary right now.")
        #
        elif CHECK_P.match(verb) and not item is Inventory.NULL_ITEM: 
            # The furniture isn't here, but maybe the player meant an item in the inventory.
            Player._setLastInteract_Item(furnName)
            GUI.out(item.getDesc())
        #
        elif verb == "pick" or verb == "take":
            # Player wants to take something off the floor.
            if not item is Inventory.NULL_ITEM:
                GUI.out("You are already carrying the " + str(item) + 'not')
            elif Player.getPos().hasFurniture("floor"):
                inven = Player.getFurnRef("floor").getInv()
                item = inven.get(furnName)
                
                if not item is Inventory.NULL_ITEM:
                    Player._evalTake(inven, it)
                    Player.printInv()
                    GUI.out("You pick the " + str(it) + " off the ground.")
                else:
                    GUI.out("There is no " + furnName + " on the floor here.")
            else:
                GUI.out("There is not much of a floor here to take something off of.")
        #
        elif obj == "self" or obj == "yourself":
            # Player performing action on itself. Mostly superficial.
            if CHECK_P.match(verb):
                Player._incrementMoves()
                GUI.out("Yes, all your parts are still there, thank goodness.") 
            elif MOVE_P.match(verb):
                # Moves player in a random direction
                direct = random.choice((Direction.SOUTH, Direction.EAST, Direction.WEST, Direction.NORTH))
                Player.move(direct)
                GUI.out("Alright, how does " + str(direct) + " sound?")
            elif TAKE_P.match(verb):
                Player._incrementMoves()
                GUI.out("Indeed, how romantic!")
            elif DESTROY_P.match(verb):
                Player._commitSuicide("In a spectacular fashion, you spontaneously explode all over the room.")
            else:
                GUI.out("Your binary isn't designed to do that.")
        #
        elif SEARCH_P.match(verb) or re.match("open|empty", verb):
            # Player wants to open an item.
            if str(item) == LOOT_SACK:
                # Loot sack is found in the foyer.
                Player._openLootSack() 
                Player._setLastInteract_Item(LOOT_SACK)
            elif str(item) == SHOE_BOX:
                # Loot sack is found in Kampe's quarters.
                item.useEvent() 
                Player._setLastInteract_Item(SHOE_BOX)
            elif not item is Inventory.NULL_ITEM:
                GUI.out("You fumble with the " + obj + ", but nothing useful is accomplished.")
            else:
                GUI.out("I don't think there's any " + obj + " here.")
        #
        elif verb == "speak" or verb == "say":
            # Player typed something like "<speak> <words>".
            GUI.out("\"" + furnName + "not\" You speak the words, but they only echo and fade.")
        #
        elif GEN_FURNITURE_P.match(obj):
            # Player used a very vague term to interact with.
            GUI.out("Don't be lazy now. Specify please.")
        #
        else: 
            # Something invalid was entered innot
            GUI.out(("There is no " + obj + " here that you can see. Or are " +
                     "we perhaps being lazy and attempting to pick up items that " +
                     "aren't mentioned in the room description?")) 

    """
        Opens the loot sack if the player is carrying it.
        Prints score, a message, and the number of phylacteries collected.
        Inventories check for phylacteries and treasures based on value
    """
    @staticmethod
    def _openLootSack():
        pi = Player.inv.countPhylacteries()
        
        if Player.hasItem(LOOT_SACK):
            sack = Player.inv.get(LOOT_SACK)
            t = sack.countTreasures()
            ps = sack.countPhylacteries()
            p = pi + ps
            message = None
            
            # Displays player score
            if Player.score >= 19000:
                message = "Your wealth transcends all understanding that exists."
            elif Player.score >= 15000:
                message = ("You possess the wealth, cunning, and power to overcome " +
                          "any holy or unholy force that dare challenge you.")
            elif Player.score >= 13000:
                message = ("Your wealth is beyond the dreams of avarice and " +
                          "will earn you a divine seat in the afterlife.")
            elif Player.score >= 11000:
                message = "Your wealth is legendary and would bring a tear to Plutus' eye."
            elif Player.score >= 9000:
                message = ("Your wealth is nearly insurmountable and would " +
                           "stun all men, women, and Gods alike.")
            elif Player.score >= 7750:
                message = ("Your wealth is nearly insurmountable and would " +
                          "stun all men and women alike.")
            elif Player.score >= 6500:
                message = ("You have amassed a grand fortune which will certainly, should you " +
                          "return, grant you any Earthly desire.")
            elif Player.score >= 5250:
                message = ("You have amassed a grand fortune which instills fear in " +
                          "all kings and queens.")
            elif Player.score >= 4000:
                message = "Your riches would earn you the respect of many kings."
            elif Player.score >= 2750:
                message = "You are a top contender in the hunt for treasure."
            elif Player.score >= 1500:
                message = ("You're skilled in the hunt for treasure, though " +
                          "you have such a long way to go.")
            elif Player.score >= 750:
                message = ("Your eye for wealth is strong. You will likely have much " +
                          "to pawn off, should you return.")
            elif Player.score >= 500:
                message = ("You abide by your manly ethics to work hard and provide " +
                          "for your family. Although, the thought of wealth visits you frequently.")
            elif Player.score >= 250:
                message = ("You are rich in character, a true fortune to be respected. " +
                          "Material possessions are secondary, of course.")
            elif Player.score >= 0:
                message = ("You have a humble spirit, and long not for possessions. " +
                          "Your only wish, of course, is only to return home.")
            else:
                message = ("You have eccentric, perplexing tastes. So long as " +
                          "hope of returning home lingers, you spirit remains strong.")
            
            # If the player has looted phylacteries.
            if ps > 0:
                message += (" However, you have lost the desire to escape, " +
                           "and wish only to bask eternally in your riches.")
            
            GUI.out("Your score is " + str(Player.score) + ". You have discovered " + str(t) + 
                    " out of 15 legendary treasures and " + str(p) + " out of 5 phylacteries. " + message)
            
            GUI.out(sack.useEvent()) # Enters the loot sack sub prompt.
        else:
            GUI.out(("You have collected " + str(pi) + " out of 5 phylacteries, and " +
                     "you unfortunately do not have a giant sack of loot right now.")) 
    
    """
        The options menu subroutine.
    """
    @staticmethod
    def _options():
        while True:
            GUI.menOut(Menus.OPTIONS.replace("%", Player.moveScheme,
                1).replace("&", Player.defAct, 1))
            choice = GUI.promptOut()

            if choice == "1":
                # Switches which keys are used to move: w,s,a,d | n,s,e,w
                if Player.moveScheme == WSDA:
                    Player.moveScheme = NSEW
                    Player.MAIN_CMD.pop("w")
                    Player.MAIN_CMD.pop("a")
                    Player.MAIN_CMD.pop("d")
                    Player.MAIN_CMD["s"] = lambda: Player.move(Direction.SOUTH)
                    Player.MAIN_CMD["n"] = lambda: Player.move(Direction.NORTH)
                    Player.MAIN_CMD["e"] = lambda: Player.move(Direction.EAST)
                    Player.MAIN_CMD["w"] = lambda: Player.move(Direction.WEST)
                else:
                    Player.moveScheme = WSDA
                    Player.MAIN_CMD.pop("n")
                    Player.MAIN_CMD.pop("e")
                    Player.MAIN_CMD.pop("w")
                    Player.MAIN_CMD["s"] = lambda: Player.move(Direction.SOUTH)
                    Player.MAIN_CMD["w"] = lambda: Player.move(Direction.NORTH)
                    Player.MAIN_CMD["d"] = lambda: Player.move(Direction.EAST)
                    Player.MAIN_CMD["a"] = lambda: Player.move(Direction.WEST)
            elif choice == "2":
                # Switches what happens when only the name of furniture is entered.
                Player.defAct = SEARCH if Player.defAct == EXAMINE else EXAMINE
            elif not choice:
                break

    @staticmethod
    def printInv(furnInv=None):
        GUI.invOut("You are carrying:" + NL + str(Player.inv) + 
            ((NL + "You find:" + NL + str(furnInv)) if furnInv else ""))

    """
        Subroutine entered into when an item is used from the player's inventory.
        It is generally quicker to use items on objects from the main prompt.
        @param furniture Furniture the item is being used on.
        @param item The item being used
    """
    @staticmethod
    def _evalUse(item, furniture):
        furniture = Player._tryIndefRef_Furn(furniture)
        
        if Player.getPos().hasFurniture(furniture):
            Player._setLastInteract_Furn(furniture)
            target = Player.getFurnRef(furniture)
            Player._incrementMoves()

            if target.useKeyMatches(str(item)):
                # Item is name is in the furniture's list of item names.
                GUI.out(target.useEvent(item))
                Player.describeRoom()
                Player.printInv()
            else:
                GUI.out("You jam the " + str(item) + " into the " + 
                    furniture + " as hard as you can with no exciting results.")
        elif furniture:
            GUI.out("A sharp squint around the room reveals no " + 
                furniture + " at all.") 

        Player.printInv()

    """
        Allow the player to write a note to itself. This can only be done if the
        player has the notepad and a pen.
    """
    @staticmethod
    def _writePrompt():
        if not (Player.hasItem(PEN) and Player.hasItem(NOTEPAD)):
            GUI.out("You will need a pen and notepad in order to write a note to yourself.")
            return
        
        GUI.menOut(Menus.NOTE_SUB)
        title = GUI.promptOut()
        newNote = None

        if title:
            if ANY_DIGIT_P.match(title):
                # Player is appending to existing note.
                n = Player.inv.get(title)

                if n is Inventory.NULL_ITEM:
                    Player.randomErrorMessage()
                elif isinstance(n, Note) and not isinstance(n, Book):
                    # Player may write on notes but not books.
                    
                    if str(n) == RIPPED_SHREDS:
                        GUI.out("You can't write on the torn paper.")
                    else:
                        newNote = NotepadNote(str(n), n.getDesc() + ' ' + Player._getNoteBody())
                        Player.inv.remove(n)
                elif str(n) == NOTEPAD:
                    Player._writePrompt()
                elif str(n) == PEN:
                    GUI.out("That would be quite impressive...")
                else:
                    GUI.out("That isn't a note if I've ever seen one.")       
            #
            elif not Player.inv.isFull():
                newNote = NotepadNote("note - " + title + ': ', Player._getNoteBody())
            else:
                GUI.out("You're carrying too much stuff to write a new note!")

            if newNote:
                Player.inv.add(newNote)
                Player._setLastInteract_Item(str(newNote))
                Player._incrementMoves()
                Player.printInv()
    
    """
        Gets string input from player to write to a note.
        Since promptOut() makes everything lowercase, this has to undo that.
        @return A capitalized string.
    """
    @staticmethod
    def _getNoteBody():
        GUI.menOut("Ok. Write down your momento now...")
        body = list(GUI.promptOut())
        capitalize = True
        
        if not body:
            return ""
        
        for i in range(len(body)):
            c = body[i]
            
            if c == '.': 
                capitalize = True # Capitalize the next lowercase letter.
            elif capitalize and c.isalpha():
                capitalize = False # It's a lowercase letter.
                body[i] = c.upper()    
        
        GUI.out("Note has been written.")
        return "".join(body)
    
    """
        Prompts the player for an item list, verifies it, moves to _evalCombine().
        Uses parameter if defined instead.
        A list is valid if it contains exactly 2 or 3 existing items in the
        player's inventory.
        @param combineThese A list of items
    """
    @staticmethod
    def _combineSub(combineThese=None):
        if combineThese:
            Player._evalCombine(itemList)
        else:
            GUI.menOut(Menus.INV_COMBINE)
            
            while True:
                combineThese = GUI.promptOut() # Prompts for list of items.

                if combineThese:
                    Player._incrementMoves()
                    Player._evalCombine(combineThese) # Tries to combine them if list is valid.
                else:
                    break
    
    """
        Validates the correctness of a list of items to combine generated by the
        player, prints an error message if False.
        @param list a variable-length list of items.
        @return if an attempt at combining can be performed on the list.
    """
    @staticmethod
    def _validateList(lst):
        # Checks for None items
        if Inventory.NULL_ITEM in lst:
            Player.randomErrorMessage()
            return False
        
        # Checks if correct length
        l = len(lst)

        if l >= 2:
            return True
        elif l == 0:
            Player.randomErrorMessage()
        elif l == 1:
            GUI.out("You don't know how to combine an item with itself.")
        else:
            GUI.out("You possess only the dexterity to combine 2 or 3 items.")
            
        return False
    
    """
        Tries to combine a list of 2 or 3 items into a new item.
        @param list a list of 2 or 3 items.
    """
    @staticmethod
    def _evalCombine(lst):
        itemList = Player._getItemList(lst, Player.inv)

        if Player._validateList(itemList):
            if Player._allCombineToSame(itemList):
                if lst[0].getThreshold() == len(itemList):
                    # All items combine to the same, but one is missing.
                    GUI.out(Player.inv.combine(itemList, itemList[0].forms())) 
                    Player._setLastInteract_Item(str(itemList[0].forms()))
                    Player.printInv()
                else:
                    # 2 objects are correct, but 1 is missing or incorrect.
                    GUI.out("You need something else for this to work.") 
            elif len(lst) == 2:
                GUI.out("You push them together as hard as you can, but it does nothing.") 
            else:
                GUI.out("You are pretty sure all these don't go together.") 
    
    """
        Checks that all the items in the list combine into the same object.
        @param itemList A list of items
        @return If the items combine into the same object.
    """
    @staticmethod
    def _allCombineToSame(itemList):
        formsInto = itemList[0].forms()

        if not formsInto: 
            return False # The first does not combine to anything.

        combinesTo = str(formsInto)

        for item in itemList:
            # Checks that they all combine to same as first item.
            result = str(item.forms())
            
            if not result or not result == combinesTo:
                return False

        return True # The group is valid, a new item will be formed.



"""
    Adds combine methods and sorting abilities which aren't used by furniture.
    The PlayerInventory may not contain duplicates.
    Adds get(String itemName) method for use by the TextParser.
"""
class PlayerInventory(Inventory):
    MAX_SIZE = 10
    
    def __init__(self, itemList=[]): 
        super(PlayerInventory, self).__init__(itemList)
    
    def isFull(self): 
        return len(self.CONTENTS) >= PlayerInventory.MAX_SIZE
    
    """
        Adds an item to the inventory, unless the inventory is full.
        @param item An item to add to this inventory's contents.
        @return If the add was successful. 
    """
    def add(self, item):
        if not self.isFull(): 
            if item.getType() == LOOT_SACK: 
                Player.updateScore(item.getWorth())
                
            return super(PlayerInventory,self).add(item)
        else:
            GUI.out("You are already carrying too much!")
            return False
        
    def remove(self, removeThis): 
        super(PlayerInventory, self).remove(removeThis)
        
        if removeThis.getType() == LOOT_SACK: 
            Player.updateScore(0)
        
    """
        Removes all items from this inventory of the given type.
        @param typ The type of item to remove.
    """
    def removeType(self, typ):
        newContents = []

        for item in self.CONTENTS:
            if re.match(typ, item.getType()):
                newContents.append(item)

        self.CONTENTS = []
        self.CONTENTS += newContents
    
    """
        Removes combined items from this inventory and adds the object formed to self.
        @param itemList A list of combinable items to be removed.
        @param gift The item which the combinable items combined into.
        @return Notifies the player what he or she received.
    """
    def combine(self, itemList, gift): 
        for i in itemList: 
            self.CONTENTS.remove(i) 
        
        self.CONTENTS.append(gift)
        AudioPlayer.playEffect(29)
        Player.setLastInteract_Item(str(gift))
        
        return "You created: " + str(gift) + "."

    def sortInventory(self):
        Player._incrementMoves()
        self.CONTENTS.sort(key=str)
        Player.printInv()
    
    
    # Returns the number of phylacteries the player is carrying.
    def countPhylacteries(self):
        result = 0
        
        for i in self.CONTENTS: 
            if i.getScore() == 2000 or i.getScore() == 3000:
                result += 1
        
        return result



"""
    This class holds all the attributes of the player to be serialized out to a file.
    When a game starts, if save game data exists, the serialized instance of this
    is read in and used as a template to form the player.
"""
class _PlayerAttributes(object):
    def __init__(self):
        self.POS = Player.pos
        self.INV = Player.inv
        self.KEYS = Player.keys
        self.LSTVISITED = Player.lstVisit
        self.SHOES = Player.shoes
        self.VISITED = Player.visited
        self.SCORE = Player.score
        self.MOVES = Player.moves
        self.DEF_ACT = Player.defAct
        self.MOVE_SCHEME = Player.moveScheme



"""
    Keywords from player commands are packaged into Command objects. Different
    orders and parameters construct different commands which are
    associated with different methods.
"""
class _Command(object): 
    def __init__(self, verb=None, obj=None, inst=None, msg=None, job=None):
        if verb and inst and obj:
            self.VALUE = "VERB: " + verb + "\tITEM: " + inst + "\tOBJECT: " + obj
            self.ACTION = lambda: _Command.execStore(verb, inst, obj)
        elif verb and obj:
            self.VALUE = "VERB: " + verb + "\tOBJECT: " + obj
            self.ACTION = lambda: Player._evaluateAction(str(verb), str(obj))
        elif inst and obj:
            self.VALUE = "ITEM: " + inst + "\tOBJECT: " + obj
            self.ACTION = lambda: _Command.execUse(obj, inst)
        elif verb and inst:
            self.VALUE = "VERB: " + verb + "\tITEM: " + inst
            self.ACTION = lambda: _Command.execUseLikeThis(verb, inst)
        elif job:
            self.VALUE = "Player method command -> " + str(job)
            self.ACTION = job
        elif msg:
            self.VALUE = "Print command -> \"" + msg + "\"."
            self.ACTION = lambda: GUI.out(msg)
        else:
            self.VALUE = "Command misunderstood"
            self.ACTION = Player.randomErrorMessage

    """
        Uses the item i on the furniture o.
    """
    @staticmethod
    def execUse(o, i):
        itemName = Player._tryIndefRef_Item(i)
        
        for item in Player._getItemList(i, Player.inv):
            if not item is Inventory.NULL_ITEM:
                Player._setLastInteract_Item(itemName)
                Player._evalUse(item, o)
            else:
                _TextParser.DONT_HAVE_CMD.perform()
            
    """
        Uses the item i in the specified way (v).
        Long chain of if statements in order to accept a variety of inputnot
        If player isn't carrying the item, checks if it's actually furniture
        the player typed. If it is, acts on it instead (Mainly for inspect/
        examine commands.
    """
    @staticmethod
    def execUseLikeThis(verb, i):
        instrument = Player._tryIndefRef_Item(i)
        item = Player.inv.get(instrument)
        
        if not item is Inventory.NULL_ITEM:
            # Player has the item.
            Player._setLastInteract_Item(instrument)
            Player._incrementMoves()

            name = str(item)
            itemType = item.getType()

            if verb == "use":
                GUI.out(item.useEvent())
            #
            elif verb == "read":
                if itemType == READABLE or name == BOOK_PHYL: 
                    GUI.out(item.useEvent()) # Phylactery type. Not readable
                else:
                    GUI.out("That isn't something you can read...")
            #
            elif verb == "fill":
                if name == METAL_BUCKET:
                    Player._evaluateAction("get", "water")
                elif name == BUCKET_OF_WATER:
                    GUI.out("That particular bucket is already full of water!")
                elif name == TEST_TUBE or name == EMPTY_VIAL:
                    GUI.out("Whoa now, that's scientific equipment. The only way to properly fill that is with a burette.")
                else:
                    GUI.out("That isn't something you should be filling with water.")
            #
            elif verb == "wear":
                if itemType == SHOES or itemType == CLOTHING:
                    GUI.out(item.useEvent())
                else:
                    GUI.out("That isn't something you can wear...")
            #
            elif verb == "throw":
                Player.inv.remove(item)
                floor = Player.getFurnRef("floor")

                if not floor:
                    GUI.out("A quick, ingenious decision is made to " +
                            "throw the " + str(item) + ". The item lands in " +
                            "an unknown location, lost to the aether.")
                #
                elif itemType == BREAKABLE:
                    floor.getInv().add(Item("destroyed " + str(item), -50,
                            "The " + str(item) + " is now broken and certainly useless."))

                    GUI.out("After some quick thinking, you passionately " +
                            "launch the " + str(item) + " as an olympic discus " +
                            "thrower would. The item lands on the floor.")
                #
                elif itemType == LIQUID or itemType == INGREDIENT or itemType == FOCUS: 
                    if not name == BUCKET_OF_WATER:
                        floor.getInv().add(BROKEN_GLASS)
                        GUI.out("A cunning decision is made. The player " +
                               "throws the " + str(item) + ", landing it " +
                               "on the floor. A glassy shatter swarms your " +
                               "ear and fills you with rue.")
                    #
                    else:
                        floor.getInv().add(item)
                        GUI.out("Be careful with that. You wouldn't want " +
                               "to get the floor all soaked and risk " +
                               "dying of a clumsy step.")
                #
                elif itemType == PHYLACTERY:
                    floor.getInv().add(item)
                    GUI.out("You naively launch the " + str(item) + " across the " +
                            "room in hopes of destroying the cursed item. The " +
                            str(item) + " lands unscathed on the floor.")
                #
                else:
                    floor.getInv().add(item)
                    GUI.out("After some quick thinking, you passionately " +
                            "launch the " + item + " as an olympic discus " +
                            "thrower would. The item lands on the floor.")
            #
            elif verb == "destroy" or verb == "break":
                if itemType == BREAKABLE:
                    Player.inv.remove(item)
                    Player.inv.add(Item("destroyed " + str(item), -50, 
                            "The " + str(item) + " is now broken and certainly useless."))
                    GUI.out("An acute sense of frustration causes you to crush it in your hand.")
                #
                elif (itemType == LIQUID and not name == BUCKET_OF_WATER) \
                        or itemType == FOCUS or itemType == INGREDIENT: 
                    Player.inv.remove(item)
                    Player.inv.add(BROKEN_GLASS)
                    GUI.out("An acute sense of frustration causes you to " +
                            "crush the feeble glass in your hand.")
                #
                elif itemType == READABLE:
                    Player.inv.remove(item)
                    Player.inv.add(RIPPED_SHREDS)
                    GUI.out("A cunning idea forms. You rip up the paper " +
                            "to shreds and stuff it back into your pocket.")
                #
                elif itemType == PHYLACTERY:
                    GUI.out("You try with all your might to destroy the " +
                          item + ", but fail to leave even a fingerprint.")
                #
                else: 
                    GUI.out("You lack the strength to do that.")
            #
            elif verb == "rip" or verb == "tear":
                if itemType == READABLE:
                    Player.inv.remove(item)
                    Player.inv.add(RIPPED_SHREDS)
                    GUI.out("A cunning idea forms. You violently rip up the paper " +
                             "and stuff it back into your pocket.")
                else:
                    GUI.out("That is not something you could rip up.")
            #
            elif verb == "drink":
                if itemType == INGREDIENT or itemType == LIQUID:
                    if name == PHASE_DOOR_POTION:
                        GUI.out(item.useEvent())
                    elif name == BUCKET_OF_WATER:
                        Player.inv.remove(item)
                        Player.inv.add(Item(METAL_BUCKET, 25, "It's an empty metal bucket."))
                        GUI.out("Ah, refreshing!!")
                        Player.printInv()
                    elif name == ACETONE or re.match("molten.*", name):
                        GUI.out("No possible way you're doing something that stupid!")
                    else:
                        GUI.out("You reluctantly take a small sip. 'Yughnot Bitter and disgustingnot'")
                else:
                    GUI.out("That is not something you can drink...")
            #
            elif verb == "eat" or verb == "consume":
                if name == GLOWING_FRUIT:
                    GUI.out("The fruit's glow and tasteful aroma entice you irresistibly. " +
                            "You bite down and find the fruit as hard as a rock. " +
                            "A sharp pain comes and you pull the fruit away.")
                elif name == COOKED_HAM:
                    Player.inv.remove(item)
                    GUI.out("Delicious!")
                else:
                    GUI.out("The " + str(item) + " seems most inedible...")
            #
            elif verb == "burn":
                if itemType == READABLE or name == NOTEPAD:
                    if Player.hasItem(HAND_TORCH):
                        Player.inv.remove(item)
                        Player.inv.add(BURNED_REMNANTS)
                        GUI.out("The disturbed player decides a promising " +
                                "course of action and burns it to a crisp.")
                    else:
                        GUI.out("Thank heavens you don't have a hand torch " +
                                "to commit such an anarchic act.")
                else:
                    GUI.out("That isn't something you can burn so easily.")
            #
            elif verb == "swing" or verb == "wave":
                if itemType == WEAPON:
                    GUI.out("You be careful with that. Wouldn't want to poke your eye out.")
                elif name == HAND_TORCH:
                    GUI.out("What a spectacular display of pyro acrobatics. " +
                            "If only someone were here to witness.")
                else:
                    GUI.out("Waving that around won't accomplish anything useful.")
            #
            elif verb == "hold" or verb == "squeeze":
                if name == COMPASS:
                    GUI.out(item.useEvent())
                elif verb == "squeeze" and ((itemType == LIQUID and not name == BUCKET_OF_WATER) \
                        or itemType == FOCUS or itemType == INGREDIENT): 
                    Player.inv.remove(item)
                    Player.inv.add(BROKEN_GLASS)
                    GUI.out("The player loses control of emotion and crushes " +
                            "the delicate glass.")
                else:
                    GUI.out("Holding the " + name + " accomplishes nothing interesting.")
            else:
                GUI.out("Sorry, that really wasn't specific enough for me.")
        else:
            # Player doesn't have the item, but perhaps the player meant furniture.
            Player._evaluateAction(verb, i)
        
        Player.printInv()
    
    """
        Stores the item list i into the furniture o.
        Can be of the form "putitem* down" or "dropitem*" to drop an item.
        Drop commands are actually first processed as a use item command.
        Verb is either 'put' or 'pour' depending on if player wants to store
        and item or pour liquid from a vessel out.
    """
    @staticmethod
    def execStore(v, i, o):
        furniture = Player._tryIndefRef_Furn(o)

        if Player.getPos().hasFurniture(furniture):
            # Checks that the furniture exists
            lst = Player._getItemList(i, Player.inv)
            furn = Player.getFurnRef(furniture)
            Player._setLastInteract_Furn(furniture)
            Player._incrementMoves()
            j = 0

            while j < len(lst):
                # Loops through the list and stores each
                if _Command.isNullItem(lst, j): 
                    break
                elif v == _TextParser.POUR_VERB:
                    Player._evalUse(lst[j], furniture)
                else:
                    Player._setLastInteract_Item(str(lst[j]))

                    if furn.isSearchable():
                        # Stores the current item in the item list.
                        Player._evalStore(furn.getInv(), lst[j])
                        Player.printInv()
                    elif furn.useKeyMatches(str(lst[j])):
                        # Not searchable, but perhaps it's meant to be used by the item still.
                        # e.g. the Labo distiller used by the florence flask.
                        GUI.out(furn.useEvent(lst[j]))
                        Player.printInv()
                        break
                    else:
                        GUI.out("You can't store anything in there.") 
                        break
                j += 1

            if furn.isSearchable() and len(lst) > 1 and j == len(lst):
                GUI.out("You store them all.") # Only prints if no error was entered.
        #
        elif furniture in (LOOT_SACK, "sack") and Player.hasItem(LOOT_SACK):
            # If the player wants to put something in the loot sack.
            # This case is essentially the same as above.
            if v == _TextParser.POUR_VERB:
                GUI.out("Pour it in?? Are you crazy?")
                return
            
            lst = Player._getItemList(i, Player.inv)
            sack = Player.inv.get(LOOT_SACK)
            Player._incrementMoves()
            j = 0

            while j < len(lst):
                if _Command.isNullItem(lst, j): 
                    break

                if str(lst[j]) == LOOT_SACK and not sack.isFull():
                    # Player can put the sack inside the sack, because why not.
                    GUI.out("Whoa there, be careful not to stuff the sack " +
                            "inside itself. I won't make it that easy.")
                    break
                
                Player._evalStore(sack.getInv(), lst[j])
                Player._setLastInteract_Item(LOOT_SACK)
                Player.printInv()
                j += 1

            if len(lst) > 1 and j == len(lst):
                GUI.out("You store them all in the sack.")
        #
        else:
            GUI.out("There is no " + furniture + " here that you can see.")
    
    """
        Determines if list[j] is a NULL_ITEM, prints and appropriate message.
        This means the player-entered item was not found in the inventory.
        @param list A list of items
        @param j An index into the list.
        @return If the item is None.
    """
    @staticmethod
    def isNullItem(list, j):
        if list[j] is Inventory.NULL_ITEM:
            if not j:
                GUI.out("I don't think you're carrying that.")
            else:
                GUI.out("Well, I understood " + str(list[j-1]) + 
                        " but that next thing I didn't get.")
            return True
        
        return False
    
    def perform(self):
        #DEBUG print(self.VALUE)
        self.ACTION()    



"""
    This processes more complex sentences into statements containing verbs,
    items, and furniture.

    The text parser needs access to Player methods, so their relationship is
    close. This class is only used by player, which is why this is a private
    nested class.

    Sentences are broken down into key words. The key words are used to create 
    command objects which are then executed.
"""
class _TextParser(object):
    # Items to create when other items are thrown or broken.
    BROKEN_GLASS = Item("broken shards", -50)
    RIPPED_SHREDS = Note(RIPPED_SHREDS)
    BURNED_REMNANTS = Item("burned remnants")
    
    PUT_VERB = "put" 
    SEARCH_VERB = "search"
    POUR_VERB = "pour"
    FLOOR_OBJECT = "floor" # For drop commands

    # Holds every recognized preposition so that they can be removed.
    PREPOSITIONS = set(("up", "down", "inside", "in", "on", "into", "onto", "out", "off", 
        "of", "over", "through", "against", "from", "around", "to", "at", "under", "underneath"))

    # List of default commands.
    DEFAULT_CMD =   _Command(job=Player.randomErrorMessage)
    EXPLETIVE_CMD = _Command(msg="Mind yourself not You're a guest here!")
    SUICIDE_CMD =   _Command(job=lambda: Player._commitSuicide("You succumb to the ultimate decision."))
    NOTHING_CMD =   _Command(msg="")
    NO_SLOT_CMD =   _Command(msg="You don't have anything in your inventory there.")
    DONT_HAVE_CMD = _Command(msg="It doesn't look like you're carrying anything resembling that.")
    
    """
        Processes user input into a command to perform.
        @param cmd a sentence with the articles removed.
        @return a command to execute.
    """
    @staticmethod
    def getCommand(cmd):
        # Trims articles which never affect meaning.
        cmd = ARTICLE_P.sub("", cmd)
        
        # If the command is only a verb, prompts the user for an object.
        if cmd in Furniture.Furniture.ALL_ACTION_KEYS:
            GUI.out(cmd.title() + " what?")
            GUI.menOut(NL + "<Object> " + cmd + "...")
            obj = GUI.promptOut()

            if not obj:
                return _TextParser.NOTHING_CMD

            cmd += ' ' + ARTICLE_P.sub("", obj)
        

        # First six conditions handle simpler commands.
        if EXPLETIVE_P.search(cmd): # Zork-inspired
            return EXPLETIVE_CMD  
        #
        elif ANY_DIGIT_P.match(cmd):
            # Player typed a digit. Interpreted as "examine <item slot>"
            item = Player.inv.get(cmd)

            if item is Inventory.NULL_ITEM:
                return _TextParser.NO_SLOT_CMD 
            else:
                return _Command(job=lambda: GUI.out(item.getDesc()))
        #
        elif DIRECTION_P.match(cmd):
            # Sentence resembles a movement command.
            return _TextParser.getDirCmd(cmd)
        #
        elif SUICIDE_P.match(cmd):
            return _TextParser.SUICIDE_CMD
        #
        elif COMBINE_P.match(cmd):
            # Sentence resembles 'combine' <list of items>
            return _Command(job=lambda: Player._combineSub(COMBINE_P.sub("combine ", "", 1)))
        #
        # These handle more complicated input strings.
        elif USE_ITEM_CMD_P.match(cmd):
            return _TextParser.getItemCmd(USE_MANNER_P.split(cmd))
        
        elif STORE_CMD_P.match(cmd):
            # Command resembles "drop <item>" or "put <item> in <object>
            return _TextParser.getStoreCmd(SPACE_THEN_ALL_P.sub("", cmd), \
                                            STORE_AREA_P.split(STORE_SPACE_P.sub("", cmd)))
        #
        else: 
            if SEARCH_MANNER_P.search(cmd):
                # Replaces "look (in|on|around|under) with just 'search'"
                cmd = SEARCH_MANNER_P.sub(_TextParser.SEARCH_VERB, cmd)
                
            return _TextParser.getCmdActionFirst(INSTRUCTIVE_P.split(_TextParser.stripPrepositions(cmd)))
    
    """
        Removes prepositions, which won't effect the meaning in most contexts.
        @param input A string of input with articles stripped.
        @return The sentence stripped of prepositions.
    """
    @staticmethod
    def stripPrepositions(inp):
        words = SPC.split(inp)
        i = 0

        while i < len(words):
            if words[i] in _TextParser.PREPOSITIONS:
                words.pop(i)
            else:
                i += 1

        return " ".join(words)

    """
        Assembles a command where the player interacts with furniture with
        possibly an item.
        If s is size 2, then second string is presumably an item.
    """
    @staticmethod
    def getCmdActionFirst(s):
        firstWord = SPACE_THEN_ALL_P.sub("", s[0])
        everythingElse = FIRST_WORD_P.sub("", s[0])

        if len(s) == 2:
            return _Command(inst=s[1], obj=everythingElse)
        elif len(s) == 1:
            if firstWord == everythingElse:
                # Player entered a single word. Interpreted to mean whatever Player.defAct is.
                firstWord = _TextParser.SEARCH_VERB if Player.defAct == "search" else "examine"
            
            return _Command(verb=firstWord, obj=everythingElse)
        else:
            return _TextParser.DEFAULT_CMD
    
    """
        Assembles a command where the player stores an item.
        If the furniture turns out to not be searchable, the item is used
        on it instead in order to resolve ambiguity. If s is size 2, then
        the second string is presumably the name of furniture.
    """
    @staticmethod
    def getStoreCmd(verb, s):
        obj = s[0]
        dirObj = None
        v = _TextParser.POUR_VERB if verb == "dump" or verb == "pour" else _TextParser.PUT_VERB
        
        if obj.find("down") != -1:
            # Player typed "put <item> down"
            dirObj = _TextParser.FLOOR_OBJECT
            obj = re.compile(" ?down ?").sub("", obj)

        if len(s) == 2:
            return _Command(verb=v, inst=obj, obj=s[1])
        elif len(s) == 1:
            # If dirObj is null, player typed "store <item>", but not where.
            if not dirObj:
                i = Player.inv.get(obj)
                
                if LIST_P.match(obj):
                    GUI.out("Store them where?")
                elif i is Inventory.NULL_ITEM:
                    return _TextParser.DONT_HAVE_CMD
                else:
                    GUI.out("Store the " + i + " where?")
                
                # Prompts the player to specify where to store the item.
                place = GUI.promptOut()

                if not place:
                    return _TextParser.NOTHING_CMD
                
                dirObj = ARTICLE_P.sub("", _TextParser.stripPrepositions(place))
                
            return _Command(verb=v, inst=obj, obj=dirObj)
        else:
            return _TextParser.DEFAULT_CMD
    
    """
        Assembles a command where the player uses an item, possibly on a
        piece of furniture.
        If the verb is 'drop', then the store command takes care of the rest.
        If s is size 2, then the second string is presumably a furniture name.
    """
    @staticmethod
    def getItemCmd(s):
        verbObject = _TextParser.stripPrepositions(s[0])

        firstWord = SPACE_THEN_ALL_P.sub("", verbObject, 1)
        everythingElse = WORD_SPACE_P.sub("", verbObject, 1) 

        if firstWord == "drop" or firstWord == "remove":
            # If player types "drop <items>" then it's a store command instead
            # Sentence appeared to be <use> <item>. 
            return _Command(verb=_TextParser.PUT_VERB, inst=everythingElse, obj=_TextParser.FLOOR_OBJECT)
        #
        elif INSTRUCTIVE_P.search(everythingElse):
            # Player typed a phrase including "<furniture> with/using <item>
            furnItem = INSTRUCTIVE_P.split(everythingElse)
            return _Command(inst=furnItem[1], obj=furnItem[0])
        #
        elif len(s) == 1:
            return _Command(obj=firstWord, inst=everythingElse)
        elif len(s) == 2:
            if DESTROY_P.match(firstWord):
                return _Command(verb=firstWord, inst=everythingElse) 
            else: 
                return _Command(inst=everythingElse, obj=s[1])
        else:
            return _TextParser.DEFAULT_CMD
    
    """
        Gets a command which moves the player in a certain direction.
        The player may type something like 'go [direction]', in which case
        the command is obvious. A command like 'go [inside]' is more vague and
        depends on the room the player is in.
        @param s A string resembling a command to move.
        @return A command to run.
    """
    @staticmethod
    def getDirCmd(s):
        direct = FIRST_WORD_P.sub("", s, 1)

        if direct in Player.MAIN_CMD.keys():
            # Player wants to move in a specified direction.
            return _Command(job=Player.MAIN_CMD[direct])
        #
        elif direct == "inside" or direct == "in":
            # Player typed either "go inside" or "go in".
            pos = Player.getPosId()

            if pos in (Id.COU7, Id.GAR2, Id.TBAL):
                return _Command(job=Player.MAIN_CMD["north"])
            elif pos in (Id.FOYB, Id.FOYC, Id.GAR4):
                return _Command(job=Player.MAIN_CMD["south"])
            elif pos in (Id.WBAL, Id.LOOK):
                return _Command(job=Player.MAIN_CMD["east"])
        else:
            # Player typed either "go outside" or "go out".
            pos = Player.getPosId()

            if pos in (Id.FOY2, Id.GAL1, Id.TOW2):
                return _Command(job=Player.MAIN_CMD["north"])
            if pos in (Id.FOY1, Id.JHA2, Id.SOUL):
                return _Command(job=Player.MAIN_CMD["south"])
            if pos in (Id.WOW1, Id.ROTU):
                return _Command(job=Player.MAIN_CMD["west"])

        return _Command(msg="You can't go " + direct + " from here.")
