import re
"""
    Stores pattern constants for use by Player and TextParser.
    
"""    

# If the player is vague in a command, using words like these, game lets the player know        
GEN_FURNITURE_P = re.compile("furniture|furnishings|stuff|things?")
     
# USED IN SEARCHES
SEARCH_P = re.compile("search|e|s")    
LOOT_ACTION_P = re.compile("loot|l|take (?:all|everything)")  # Player wants everything  
TAKE_P = re.compile("t|take|get")     # Player wants to take an item
STORE_P = re.compile("s|store|put")   # Player wants to store an item
        
# Matches a key so that they can be put in keyring when picked up
# Exception is made for OU62 key, since it's in catacombs breaks the rule
# That the first 3 letters are used to identify the area it's in.
KEY_P = re.compile("[A-Z]{3}[A-Z1-9]|OU62") 


# USED TO MATCH DIFFERENT KINDS OF COMMON ACTIONS
DESTROY_P = re.compile("destroy|break|shatter|obliterate|throw")        
MOVE_P = re.compile("move|slide|displace|push|pull|spin|rotate")
CHECK_P = re.compile("c|check|examine|look|view|inspect|watch")

SAVE_QUIT_RESET_P = re.compile("^[srb]|$")   # Used when player quits game
        
# Protects from numberFormatException by restricting to 4 digits at most.
# Matches empty strings also. Used in a menu that prompts for a digit.        
DIGIT_OR_BLANK_P = re.compile(r"\d{1,4}|") 

# A list delimited by a comma or 'and', or possibly a comma followed by 'and'.
LIST_P = re.compile(" ?,(?: ?and ?)? ?| and ")
        
      
# These five are the most specific cases and are checked first.        
EXPLETIVE_P = re.compile("fuck|shit|cunt|damn|bitch")
DIRECTION_P = re.compile("^(?:(?:in|out)(?:side)?|(?:go|walk|move|run) (?:north|forwards?|south|east|right|west|left|(?:down|back|up)(?:wards?|stairs)?|(?:in|out)(?:side)?))$")
SUICIDE_P = re.compile("(?:commit )?suicide|(?:kill|hangS) (?:your)?self(?: with| using)?")
COMBINE_P = re.compile("combine ") # Anything beginning with 'combine' is a combine command
       
# Matching to this likely means the player is trying to store something.        
STORE_CMD_P = re.compile("(?:put|store|pour|dump|give) [a-z0-9: ,'-]+") 
        
# Looking normally implies examining, unless followed by these prepositions.
SEARCH_MANNER_P = re.compile("look (?:on|in(?:side)?|under|around)")
 
# Likely means player is inspecting an item.
INSPECT_P = re.compile("look (?:at)?|inspect|examine|check")
        
        
# SPECIFIC TO ITEM USE COMMANDS
# List of all the things a player can do to an item.
USE_ITEM_CMD_P = re.compile("(?:use|read|drop|wear|remove|fill|burn|eat|swing|wave|drink|throw|destroy|break|lean|tie|rip|tear|hold|squeeze) [a-z0-9: ,'-]+")
USE_MANNER_P = re.compile(" (?:on|against|to|at) ") # Separates item from furniture.
         
# Once a store command is matched, these words are fine to remove.
STORE_SPACE_P = re.compile("(?:put|store|pour|dump|give) ")
        
# Protects from numberFormatException by restricting to 4 digits at most.        
ANY_DIGIT_P = re.compile(r"\d{1,4}$") 
        
# These words are meaningless and removed right away
# as well as the pronoun 'some' (e.g. "take SOME grass").
ARTICLE_P = re.compile(r"\bthe |\ban? |\bsome ")
        
# Used to remove the first word in a sentence.
WORD_SPACE_P = re.compile(r"\w+ ") 
# Used to remove everything but the first word in a sentence.        
SPACE_THEN_ALL_P = re.compile(" .+")
# Used in stripping prepositions.
SPC = re.compile(" ")

# Splits an item from the object it's used on (e.g. cut rope WITH the sword)
INSTRUCTIVE_P = re.compile(" with | using ")  

# In a store command, this pattern splits items from the furniture they are
# to be stored in.
STORE_AREA_P = re.compile(" (?:inside|(?:in|on)(?:to)?|under(?:neath)?|(?:next )?to|beside|over) ")

# Used to get just the first word in s sentence, but NOT with punctuation.
FIRST_WORD_P = re.compile("[a-z]+ ")
        
    
# All of these are used in menus of furniture        
ONE_TO_HUNDRED_P = re.compile("(?:[1-9][0-9]?|100|)$")
VAUE_DOOR_COORDS_P = re.compile("(?:(?:[1-4] ?, ?[1-4])|)$")
ROMAN_NUMERAL_P = re.compile("(?:[1-9]|v?i{1,3}|i[vx]|v|)$")
ONE_TO_NINE = re.compile("[1-9]$")
OBS_SLOTS_A_TO_I = re.compile("(?:[a-i]|)$")
OBS_STATS_ONE_TO_EIGHT = re.compile("[0-8]|")
LABO_BURET_ONE_OR_TWO = re.compile("(?:[12]|)$")
ONE_TO_SIX = re.compile("[1-6]$")
GAL_TOTEM_ONE_TO_FOUR = re.compile("(?:[1-4]|)$")        
UP_DOWN_P = re.compile("[ud]|up|down|")
YES_NO_P = re.compile("[yn]|yes|no|")
        
# Used to delete tower description on tower room description once the lich is dead.        
TOW1_SPHERE_P = re.compile(" (?=Wide)")
        
# Represents a chemical in the alchemy puzzle.
CHEMICAL_P = re.compile(r"[\w\d]+ \d{1,2}mL")
        
# Not safe to teleport the player to these areas.
# LIB4 and LIB5: bad if player teleports to these without leather shoes.
# ESC: bad if player teleports to these without a torch.
# INTR: bad if player teleports here without it being reset by monster.        
# FOR and ENDG: Will let player escape prematurely.
NO_TELEPORT_P = re.compile(r"LIB[45]|ESC\d|INTR|HADS|FOR\d|ENDG")
        
# Represents a dye item in the lens-making puzzle.
DYES_P = re.compile("(?:red|blue|yellow) dye")
        

# USED BY THE DUNGEON MONSTER  
# Match rooms where player can never see monster and sounds are never played.
QUIET_AREA = re.compile("TOR|CRY|ESC|DKC|CAS")
# Match the two halves of sub-level 1 (cistern and tunnels)
CISTERN_AREA = re.compile("OUB|AAR|CIS")
TUNNEL_AREA = re.compile("SEW|PRI|INT") 
# Player can't see the monster from the areas in each pattern, IF the
# player is in an area matched by the other pattern.
NO_SEE_AREA_E = re.compile("SEW[0-5P]|PRIS|INTR")
NO_SEE_AREA_W = re.compile(r"CIS\d|OUB1|AARC")  

# PATTERNS USED BY AUDIOPLAYER   
# Used in tandem with the below pattern.        
CAVES_CAT_P = re.compile(r"C[TV]\d{2}")
# Removes digits from cave and catacomb IDs so that all map to same track.
SINGLE_DIGIT_P = re.compile(r"\d")    
        
# PATTERNS USED BY HELP
CONTROL_CHOICE = re.compile("(?:[1-9]c|10c)$")
PLAYER_CHOICE = re.compile("[1-4]p$")
CASTLE_CHOICE = re.compile("[1-6]a$")
