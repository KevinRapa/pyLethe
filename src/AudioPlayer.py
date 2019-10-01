"""
    Maps every room to an audio file that will play whenever that room is moved
    into, and maps various events to sound effects.
"""
from Names import SEP, W_DIR
from Id import *
import Patterns
from pygame import mixer
import os, re, threading, time

mixer.init()

TPTH = W_DIR + SEP + "data" + SEP + "ambience" + SEP # Filepath for ambience.
EPTH = W_DIR + SEP + "data" + SEP + "effects" + SEP  # Filepath for effects.
EXT = ".mp3" 

trackMuted, effectsMuted = False, False
curTrack = None
TRACKS = {}

EFFECTS = [(EPTH + sound + EXT) for sound in (\
    "steps",       "inventory",   "pageTurn",    "keys",        
    "knobJiggle",  "doorLocking", "wallThump",   "gateSlam",   
    "doorSlam",    "doorClose",   "basicClick",  "buttonPush",
    "leverPull",   "doorUnlock",  "woodStairs",  "stoneSteps",  
    "ladderClimb", "dungValve",   "rotuRot",     "rotuRot2",    
    "valveTurn",   "keyClick",    "keyClick2",   "keyClick3",
    "dungeonDoor", "monster",     "windowOpen",  "keyDrop",     
    "gateSwitch",  "sparkles",    "rockCrumble", "ladderFall",  
    "enchantPop",  "handDrill",   "digging",     "metalPing",
    "hoseClimb",   "galStatue",   "galGears",    "fireDouse",   
    "woodBang",    "woodSliding", "waterScoop",  "medalClick",  
    "totemTurn",   "bunsBurner",  "zombieMoan",  "metalLadder",
    "grateMove",   "teleportZap", "concBlock",   "concShort",   
    "atticNoise",  "piano",       "harp",        "doorKnock")]

"""
    Stops the current track and starts a new one if the room
    if the player entered is mapped to a different track OR if
    the current track is null (i.e. the game has just started).
    @param ID A room ID.
"""
def playTrack(ID):
    global curTrack

    if Patterns.CAVES_CAT_P.match(ID): 
        # For caves and catacombs. Removes final 2 digits so 
        # they all map To the same track.
        ID = ID[:2]

    # Switches music only if new area has different associated soundtrack.
    if not curTrack == TRACKS[ID]:
        mixer.music.stop()
        curTrack = TRACKS[ID]
        mixer.music.load(curTrack)
        
        if trackMuted:
            mixer.Music.set_volume(0)
        
        mixer.music.play(-1)

"""
    Plays a sound effects.
    @param ID An integer corresponding to a sound effect.
"""
def playEffect(ID, volume=-1):
    return
    if not effectsMuted:
        if not volume == -1:
            mixer.Channel(1).set_volume(volume)
        mixer.find_channel().play(mixer.Sound(EFFECTS[ID]))

def toggleMute(b): 
    if not trackMuted and not effectsMuted: 
        trackMuted = True
        #b.setText("Mute II")
        GUI.out("Muted all ambience.")
    elif trackMuted and not effectsMuted:
        effectsMuted = True
        #b.setText("Mute III")
        GUI.out("Muted everything.")
    elif trackMuted and effectsMuted:
        trackMuted = False
        #b.setText("Unmute")
        GUI.out("Muted all sound effects.")
    else:
        effectsMuted = False
        #b.setText("Mute")
        GUI.out("Unmuted.")
    
    mixer.music.set_volume(0 if trackMuted else 1.0)

def releaseTracks():
    mixer.music.stop()
    mixer.quit()

def _putAllTracks(track, *ids):
    _track = TPTH + track + EXT

    for ID in ids: 
        TRACKS[ID] = _track

_putAllTracks("nightAmbience", COU1, COU2, COU3, COU4, COU5, COU6, ENDG, COU7, COU8, FOR1, FOR2, FOR3, FOR4, FOR5)
_putAllTracks("spookyWindInterior", FOY1, FOY2, FOY3, FOY4, VEST)
_putAllTracks("wavesCrashing",  FOYB, LOOK, FOYC)
_putAllTracks("ironHallCustom", IHA1, IHA2)
_putAllTracks("westWingCustom", WOW1, WOW2, WOW3, SHA1, SHA2, SQUA, EOW1, EOW2, EOW4, SHAR, CLOS)
_putAllTracks("galChoir",       GAL2, GAL4, GAL5)
_putAllTracks("creepyOrgan",    CHS1, CHS3, CHA1, CHA2)
_putAllTracks("parlorCustom",   PAR1, PAR2, JHA1, JHA2)
_putAllTracks("marbleHall",     MHA1, MHA2, MHA3)
_putAllTracks("loungeCustom",   DIN1, DIN2, DRAR)
_putAllTracks("libraryCustom",  LIB1, LIB2, LIB3, LIB4, LIB5)
_putAllTracks("backHall",       BHA1, BHA2, BHA3)
_putAllTracks("gardenCustom",   GAR1, GAR2, GAR3, GAR4)
_putAllTracks("atticCustom",    SST1, SST2, ATT1, ATT2)
_putAllTracks("obsCustom",      OBS1, OBS2, OBS3)
_putAllTracks("caveLoop",       "CT", "CV", MY18)
_putAllTracks("caveDistortion", MS65, MS66)
_putAllTracks("tombCustom",     TM16, TM66, TM32, AN65, AN55, VAUE)
_putAllTracks("sewerHallCustom", SEW0, SEW1, SEW2, SEW3, SEW4, SEW5)
_putAllTracks("cisternCustom",  CIS1, CIS2, CIS3, CIS4, CIS5, CEL6)
_putAllTracks("aeolianWindHarp", OUB1, OU62, AARC)
_putAllTracks("prisonCustom",   PRIS, TORC)
_putAllTracks("sewerCogwork",   INTR, ESC1, ESC2, ESC3, ESC4, ESC5, ESC6, DKCH)
_putAllTracks("torcCustom",     TORC, CRY1, CRY2, CAS1, CS35)
_putAllTracks("endTrack",       BLS1, BLS2, TOW1, TOW2, LQU1, LQU2, SOUL)
_putAllTracks("antechamberCustom", FOYW, VAUE, VAU1, VAU2) 
_putAllTracks("rotundaCustom",  ROTU, CEL1, CEL2, CEL3, CEL4, CEL5)
_putAllTracks("hell", HADS)    
_putAllTracks("gal1wCustom", GAL1)         
_putAllTracks("gal2wCustom", GAL3)   
_putAllTracks("gal3wCustom", GAL6)             
_putAllTracks("labCustom", LABO)     
_putAllTracks("kitchenCustom", KITC)          
_putAllTracks("dungeonStairs", DST1) 
_putAllTracks("fire", STUD)              
_putAllTracks("tbalCustom", TBAL)    
_putAllTracks("workShopCustom", WORK)     
_putAllTracks("westBalconyCustom", WBAL)   
_putAllTracks("deepSpace", COUS)    
_putAllTracks("sewpCustom", SEWP)    
_putAllTracks("titleTrack", TITL)
