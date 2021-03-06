from Names import NL

"""
    Organizes the various menus in the game.
"""
INV_COMBINE = (NL +
           "<list> Combine..." + NL +
           "< >    Back")

TRADE_SUB = ("<left/right>  Scroll" + NL +
           "<'s' list>    Store" + NL +
           "<'t' list>    Take" + NL +
           "<'loot'>      Loot!!!" + NL +
           "< > Back  <#> Inspect")

SAVE_QUIT = (NL + NL +
           "<'s'> Save and quit" + NL +
           "<'r'> Reset and quit." + NL +
           "<'b'> No no! Go back!" + NL +
           " < >  Quit")
                  
MAIN_MENU = ("     Enter a command or:" + NL +
           "   <'w'/'s'/'a'/'d'>  Move" + NL +
           "<'k'>  Keys       <'l'>  Loot" + NL +
           "<'h'>  Get help   <'n'>  Note" + NL +
           "<'m'>  Show Map   <'q'>  Quit" + NL +
           "<'o'>  Options    <'save'> Save")
    
OPTIONS = (NL + "<'1'> Movement scheme:  " + NL +
               "      %" + NL +
               "<'2'> Default action on " + NL +
               "      furniture: &" + NL +
               " < >  Back ")

HELP_MAIN = ("     Topics:" + NL +
           "<'1'> Controls" + NL +
           "<'2'> Your player" + NL +
           "<'3'> The castle" + NL +
           " < >   Back")

NOTE_SUB = (NL + "Write a title for" + NL + 
                 "your note, or enter" + NL +
                 "a slot number to" + NL + 
                 "write to an existing" + NL + 
                 "note.")

HELP_SUB1 = ("<'1'> The prompt <'2'> Moving" + NL +
           "<'3'> Describing <'4'> Examining" + NL +
           "<'5'> Searching  <'6'> Commands" + NL +
           "<'7'> Using      <'8'> Combining" + NL +
           "<'9'> Inspecting <'10'> Notes" + NL +
           " < >  Back")

HELP_SUB2 = ("<'1'> Inventory" + NL +
           "<'2'> Key ring" + NL +
           "<'3'> Phylacteries" + NL +
           "<'4'> Loot" + NL +
           " < >  Back")

HELP_SUB3 = (NL +
            "<'1'> Doors     <'2'> Rooms" + NL +
           "<'3'> Furniture <'4'> Items " + NL +
           "<'5'> Keys      <'6'> Phylacteries" + NL +
           " < >  Back")

SAFE_MENU = (NL +
           "<'1'> Turn dial one" + NL +
           "<'2'> Turn dial two" + NL +
           "<'3'> Turn dial three" + NL +
           " < >  Back")

OBS_STAT_MEN = (NL +
           "<'r'#> Rotate statue" + NL +
           "<'m'#> Move statue")

OBS_SLOT_EX = (NL +
           "<'a-i'> Look..." + NL +
           "  < >   Back")

OBS_SLOT_SE = (NL +
           "<'a-i'> Search..." + NL +
           "  < >   Back")

DOUBLE_ST = (NL +
           "There are two flights" + NL +
           "    <'u'> Go up" + NL +
           "    <'d'> Go down")

SEW_VALVE = (NL +
           "<#> Turn valve" + NL +
           "< > Back")

VAEU_DOOR = (NL +
           "<x)y> Push" + NL +
           " < >  Back")

CRY_DRWRS = (NL +
           "<#> Search..." + NL +
           "< > Back")

GAL6_BTTN = (NL +
           "<'y'/'n'> Push?" + NL +
           "< >       Back")

GAL6_HELM = (NL +
           "<'y'/'n'> Wear it?" + NL +
           "< >       Back")
    
OBS_STATS = (NL +
           "<#> Look..." + NL +
           "< > Back")
    
LABO_BURET = (NL +
           "<1> Empty" + NL +
           "<2> Titrate" + NL +
           "< > Back")
    
LABO_DISP = (NL +
           "<#> Dispense")
    
GAL_TOTEM = (NL +
           "<#> Turn head" + NL +
           "< > Back")

ENTER = NL + NL + "Press enter..."
    
BOOK = (NL + NL + 
    "<'y'/'n'>    Turn the page?" + NL +
    "<left/right> Scroll") 
       
    
CREDITS = ("Written in Java on NetBeans 8.1. All " + NL +
           "sounds were processed using audacity. " + NL +
           "Fonts are Magic Medieval (Dave " + NL +
           "Howell) and FixedSys Excelsior (Darien " + NL +
           "Valentine). Title screen designed " + NL +
           "by Stephen Reed.")
    
VERSION = ("This is Lethe / Author: Kevin Rapa / Written on Netbeans 8.1 "
           "/ Sounds obtained from freesound.org) processed in Audacity "
           "/ Title screen by Stephen Reed. Enter 'credits' for more info.")
