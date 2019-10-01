from Names import SEP, W_DIR
import Menus
import random, re

ENDC = "\033[1;37;40m"
BRWN = "\033[1;33;40m"
PRPL = "\033[1;35;40m"
CY = "\033[1;36;40m"

"""
    This class is responsible for the game interface.
    All graphical components are set up here.
    Any text useful to the player is collected here and displayed.
    Any input from the player is processed here. 
"""
class GUI(object):
    # Faux click noises when player types. Optional feature.
    NONE = -1
    SOFT = 0 
    CLICK = 1
    VINTAGE = 2
    
    keySound = NONE
    
    # LABELS
        
    # BUTTONS
    
    # TEXT FIELD
    
    # Holds previous input. Linked list
    UNDO = []
    
    # Queue treated as circular to rotate between key sounds.
    KEYSOUND = [NONE, SOFT, CLICK, VINTAGE] # linked list
    
    # Queue treated as curcular to rotate font colors.
    COLORS_DIAL = None # List of colors
    COLORS_LABEL = None # List of colors

    """lightBrown = Color(122, 84, 13)
    darkRed = Color(196, 11, 15)
    forestGreen = Color(51, 141, 29)
    teal = Color(52, 182, 156)"""

    def __init__(self):
        pass
     
    def addComponents(self):
        pass

    # These methods collect all text output in the game for the player.
    # Each method sets the text of a different GUI component.    

    """
        Collects all text not collected by the other collectors.
        Complicated events may send an empty string which won't display.
        @param txt dialog text.
    """
    @staticmethod
    def out(txt):
        print(PRPL + txt + "\n" + ENDC) 
    
    """
        Collects all room descriptions.
        @param txt a room description.
    """
    @staticmethod
    def descOut(txt):
        print(txt + '\n')
    
    """
        Collects <code>triggeredEvent</code> return text.
        For triggered events that move the player, empty string is sent.
        @param txt <code>triggeredEvent</code> room text
    """
    @staticmethod
    def roomOut(txt):
        print("Location: " + txt + '\n') 
    
    """
        Collects all menu text text which prompts player for input.
        @param txt menu text
    """
    @staticmethod
    def menOut(txt):
        print(CY + txt + '\n' + ENDC)
    
    """
        Displays all <code>toString</code> calls on inventories.
        @param txt inventory toString method return text. 
    """
    @staticmethod
    def invOut(txt):
        print(CY + txt + '\n' + ENDC)

    """
        Used for any request of player input.
        Main thread is here most of the time.
        @return Commands input by the player.
    """
    @staticmethod
    def promptOut():
        return raw_input(">>> ")

    @staticmethod
    def askChoice(menu, pattern):
        GUI.menOut(menu)
        answer = GUI.promptOut()
        
        while not pattern.match(answer):
            GUI.menOut("That's not valid" + menu)
            answer = GUI.promptOut()

        return answer

    @staticmethod
    def toMainMenu():
        pass # Print main menu controls

    @staticmethod
    def clearDesc():
        pass

    @staticmethod
    def clearDialog():
        pass

    @staticmethod
    def updateMovesAndScore(moves, score):
        pass # update moves and score label

    @staticmethod
    def resetScroll():
        pass

    @staticmethod
    def giveFocus():
        pass # Give input to text field
    
    @staticmethod
    def mute():
        pass # click mute button
    
    @staticmethod
    def setClick():
        pass # click click button
    
    @staticmethod
    def swap():
        pass # Swap two panes

    """
        For the easter egg command 'XYZZY'.
    """
    @staticmethod
    def randomizeColors():
        pass

    @staticmethod
    def displayCredits():
        GUI.invOut(("AMBIENT TRACK SOURCES (All from freesound.org): " +
             "AniCator, Bluehand, BrainClaim, cormi, EKVelika, ERH, dobroide, " +
             "E1ectr0n1cF4n, felix.blume, German1990, heatfuse, holger.schwetter, " +
             "iankath, InSintesi, JarredGibb, jobro, juskiddink, karma-ron, " +
             "klankbeeld, MattJ99, mensageirocs, NoiseCollector, omnisounddesign, " +
             "plagasul, richardemoore, RogerBoyX69, Setuniman, ShadyDave, silencyo, " +
             "spoonbender, tc630, Timbre, veedgo, waveplay"))
        
        GUI.out(("SOUND EFFECT SOURCES (All from freesound.org): Erdie, " +
             "everythingsounds, Evil-Dog, fons, FreqMan, GreekIrish, " +
             "hanneswannerberger, Hybrid_V, ignotus, jc144940, KorgMS2000B, " +
             "LittleRobotSoundFactory, MalMan35, martian, mhtaylor67, " +
             "missozzy, MWLANDI, OtisJames, qubodup, Reitanna, " +
             "Robinhood76, RutgerMuller, rwm28, SmartWentCody, " +
             "Suprasummun, Taira Komori, tec studios, thefilmbakery, " +
             "tiagusilva37, timgormly, thearxx08, viaaico2013, VSokorelos"))
        
        GUI.menOut(Menus.CREDITS)
        GUI.promptOut()
        clearDialog()
        Player.printInv()

# LISTENER FOR WHEN KEYS ARE PRESSED

# LISTENER FOR TEXT FIELD

# BUTTON LISTENER HERE
