"""
    This is a text-based adventure game called Lethe
    written as a personal project.

    All super classes are in package A_Super. Packages are organized by room.
    A room class is named by its ID and is four characters long (i.e. Cou4, Torc).

    You control an unnamed character who is exploring a castle after having 
    wandered through the woods to it without any apparent reason. As the game
    progresses, puzzles get steadily more complex and a story develops. As a
    secondary objective, the player may collect loot and add it to a loot sack
    found in the foyer.

    To play, just run this project. Unless testing, make sure 
    START_LOCATION under the main method is set to Id.COU4.
"""

from Names import SEP, W_DIR
from RoomGraph import RoomGraph
from Player import Player, SAVE_PATH, NEW_GAME_DATA_PATH, ROOMS_DATA_PATH
import Map, Map_Display, AudioPlayer, Id, Menus
from GUI import GUI
import random, pickle, os, sys
from shutil import copytree, rmtree

START_LOCATION = Id.COU4  # Default COU4
TITLE_PATH = W_DIR + SEP + "data" + SEP + "img" + SEP

# DECLARE FRAMES
# DECLARE TITLE AND PANEL LABLES
# SET LOOK AND FEEL
# SET TITLE PANEL SIZE AND BACKGROUND COLOR
# GET GIF IMAGE
# SET TITLE PANEL WITH GIF IMAGE, OR HANDLE IF ISNT THERE.
# ADD LISTENER TO TITLE PANEL AND LISTEN FOR KEY STROKE
# ADD LABEL TO PANEL

"""
    Loads a game if there is one or starts a new game.
    @param args Optional room id. Will start player in that area.
"""
# INSTANTIATE GUI
# SET DEFAULT CLOSE OPERATION
# SET LOCATION AND DIMENSIONS OF GAME FRAME
# SET OTHER FRAME PARAMS

def startGame():
    try:
        with open(SAVE_PATH, "rb") as gameData:
            print("Data found. Loading game.")
            RoomGraph.assignCoordinates()
            Player.loadAttributes(pickle.load(gameData))
    except:
        # Creates a new game if one isn't found.
        print("Creating new game.")
        RoomGraph.constructRoomGraph() # Sets up game map.
        startCoords = RoomGraph.getCoords(START_LOCATION)

        if len(sys.argv) > 1:
            if sys.argv[1] == Id.NULL:
                print("Not a valid starting location.")
                exit(1)
            else:
                try:
                    startCoords = RoomGraph.getCoords(argv[1])
                except:
                    print("Not a valid starting location.")
                    exit(1)

        rmtree(ROOMS_DATA_PATH, True)
        copytree(NEW_GAME_DATA_PATH, ROOMS_DATA_PATH);
        Player.setNewAttributes(startCoords) # Sets up character.
        startDialog()

    # SET TITLE FRAME TO VISIBLE
    Player.mainPrompt() # START GAME
    endGameProcedure()  # ENDS GAME

# END GAME ##########################################################

def startDialog():
    # Short dialog that starts at the beginning of the game.
    AudioPlayer.playTrack(Id.TITL)

    GUI.menOut(Menus.ENTER)
    GUI.descOut(("Beneath the starry welkin, you stand, having trekked on " +
            "foot to your destination through the forest. The looming " +
            "stone colossus appears curiously vacant, yet inviting."))
    GUI.promptOut()    
    GUI.descOut(("You slowly approach, fighting the humid summer gales, " +
            "until inside the front gateway. A transient thought " +
            "drifts through your mind - what was your business " +
            "here, again? You ponder a moment, but can't quite remember."))
    GUI.promptOut()
    GUI.descOut(Menus.VERSION)     
    GUI.promptOut()
    GUI.clearDialog()

def endGameProcedure():
    AudioPlayer.releaseTracks()            # Stops what's playing
    # DISPOSE FRAME
    Map_Display.disposeMap()           # Frees the game map
