import Id, Direction
from Endg import Endg 
from Item import *
from Structure_gen import *         
from Names import *
from Vestibule import *        
from Closet import *             
from Foyer import *
from Back_Balcony import *     
from Rotunda import *            
from Lookout import * 
from West_Outer_Wall import *  
from West_Balcony import *       
from Servants_Quarters import *
from Servants_Hall import *    
from Ransacked_Quarters import * 
from Courtyard import *
from Front_Balcony import *    
from Scorched_Room import *      
from Study import * 
from Marble_Hall import *      
from Library import *            
from East_Outer_Wall import * 
from Secret_Archives import *  
from Workshop import *           
from Dining_Room import * 
from Drawing_Room import *     
from Trophy_Room import *        
from Kitchen import * 
from West_Antechamber import * 
from Iron_Hall import *          
from Gallery import *
from Observatory import *      
from Dungeon_Stairs import *     
from Parlor import *
from Chapel_Stairs import *    
from Chapel import *             
from Back_Hall import *
from Jade_Hall import *        
from Secret_Stairs import *      
from Garden import *
from Catacombs import *        
from Caves import *              
from Tomb import *
from Oubliette import *        
from Ancient_Tomb import *       
from Tunnels import *
from Catacomb_Entrance import *
from Mystical_Chamber import *   
from Attic import *
from Laboratory import *       
from Cistern import *            
from Cell import *
from Escape_Tunnel import *    
from Strange_Pool import *       
from Prison import *
from Torture_Chamber import *  
from Crypt import *              
from Ancient_Archives import *
from Vault import *            
from Tower import *              
from Kampe_Quarters import *
from Black_Staircase import *  
from Top_Balcony import *        
from Lichs_Quarters import *
from Soul_Chamber import *     
from Hades import *              
from Cellar import *
from Forest import *
import random

PATH = W_DIR + SEP + "data" + SEP + "img" + SEP
EXT = ".jpg"

"""
    Creates everything in the game, then saves them all to files. 
    Files are organized by floor, then row, then by room. Each room is 
    serialized with all furniture currently in it and all items in the 
    furniture. This is only called when a new game starts. When a game 
    loads, rooms are read in as they are needed.
    Every room, furniture, and item is instantiated here. For each area, 
    each room is instantiated, then each item is, then each furniture
    is and the items are added to the respective furniture. 
    @param fileDest: Where the room objects will be written.
"""
def createMap():  
    ### INITIALIZE PHYLACTERIES
    # The player may instead keep them as loot and have a different message
    # at the end of the game.
    # TOTAL: 11000 points
    
    studBkPhy = Stud_BookPhylactery(BOOK_PHYL, 2000, "Stud_BookPhylactery")
    kitcFrtPhy = Kitc_FrtPhy(GLOWING_FRUIT, 2000)
    factumPhy = Factum(FACTUM, 3000)
    vauChlPhy = Vau_ChalicePhylactery(GLOWING_CHALICE, 2000)
    towScptrPhy = Tow_ScepterPhylactery(GLOWING_SCEPTER, 2000)
  
    ### INITIALIZE SPECIAL TREASURE
    # Finding treasure is a secondary objective. All items have value, but
    # these have the highest of all non-phylactery items. Player must put
    # them in the loot sack to raise score. TOTAL: 15 treasures, 9000 points

    # Found in a box in the attic.
    attcVln = BreakableItem(STRADIVARIUS, 500, use="Surely you could never play...")
    # Found in a box in Kampe's quarters. Player may give it to the prison ghost for a hint.
    watch = Item(SHINY_WATCH, 500)
    # Found in a vase inside a tomb in catacombs.
    ring = Clothing(DIAMOND_RING, 500, use="You slip the beautiful ring on your finger.")
    # Found in a skeleton in the oubliette pit.
    gldKnf = Weapon(JEWELED_KNIFE, 500)
    # Found on altar in the chapel
    gldUrn = Item(GOLDEN_URN, 500)
    # Found in the vault in a chest
    dmnd = BreakableItem(LARGE_DIAMOND, 500)
    # Found on drawing room chess table.
    qn = Item(JEWELED_QUEEN, 500, use="Isn't this the strongest piece?")
    # Found on drawing room chess table.
    kng = Item(JEWELED_KING, 500, use="You have no idea how to play that.")
    # Found by entering "take fork" in Id.COU3.
    couFrk = Item(GOLDEN_FORK, 500)
    # Found on an altar in the crypt
    jetSkull = BreakableItem(JET_SKULL, 500)
    # Found by opening the crate in the cellar.
    celTblt = BreakableItem(BRONZE_TABLET, 500)
    # Found on a shelf in the second-floor observatory.
    astrLabe = BreakableItem(ASTROLABE, 500)
    # Found in a protected case in Id.GAL4
    monaLisa = Item(MONA_LISA, 500)
    # Obtained by committing suicide, finding it in a pile of bodies, and returning using the Factum.
    typhos = Item(TYPHOS, 1500)
    # Philosopher's stone set. These items create the philosopher's stone treasure.
    # Each is found by watering a potted plant.
    philSn = BreakableItem(PHILOSOPHERS_STONE, 1000)
    stnBs = BreakableItem("philosopher's stone base", 200, forms=philSn, thresh=3)
    stnBdy = BreakableItem("philosopher's stone body", 200, forms=philSn, thresh=3)
    stnHd = BreakableItem("philosopher's stone head", 200, forms=philSn, thresh=3)
    
    ### INITIALIZE KEYS AND GENERIC FURNITURE
    studKey = Key("crude molded key", Id.STUD)        
    gal1Key = Key("key with a bearded face on its bow", Id.GAL1)       
    eow3Key = Key("workshop key", Id.WORK)       
    par2Key = Key("key with a rose on its bow", Id.PAR2) 
    garChstKey = Key("chest key", Id.GCHS)
    kitcKey = Key("kitchen key", Id.KITC)
    closKey = Key("closet key", Id.CLOS)
    wow2Key = Key("rusty key", Id.WOW2)
    sha1CbtKey = Key("tiny key", Id.CBNT)
    gal5CbtKey = Key("small golden key", Id.GCBT)
    servKey = Key("servant's quarters key", "XXXX")
    dngnKey = Key("key with a skull on its bow", "XXXX")
    drwKey = Key("drawing room key", Id.DRAR)
    chs1Key = Key("key with a cross on its bow", Id.CHS1)
    ou62Key = Key("oubliette key", Id.OU62)
    archKey = Key("Kampe's key", Id.DKCH)
    bal1Key = Key("key with a chalice on its bow", Id.TOW1) 
    rotuKey = Key("key with a cobra head on its bow", Id.ROTU)   

    northDoor = Door(Direction.NORTH) # Generic directional doors.
    southDoor = Door(Direction.SOUTH)
    eastDoor = Door(Direction.EAST)
    westDoor = Door(Direction.WEST)
    genDoor = GenDoor() # Generic door, for rooms with multiple doors.
    wallEx = ExteriorWall() # Generic exterior castle wall.
    clng = Ceiling() # Generic ceiling

    """ 
        INITIALIZE ITEM SETS
        These items all go together and must be high up in initialization
        in order to be distributed around the castle.
    """
    # Dampening staff set. These create the dampening staff needed to obtain the final phylactery.
    lquaStf = BreakableItem(DAMPENING_STAFF, 250)
    stffHndl = BreakableItem("dampening staff handle", 100, forms=lquaStf, thresh=2)
    onyxSphr = BreakableItem("onyx sphere", 150, forms=lquaStf, thresh=2)
    onyxFrag1 = Item(ONYX_FRAGMENT, 50, forms=onyxSphr, thresh=3)
    onyxFrag2 = Item(ONYX_FRAGMENT, 50, forms=onyxSphr, thresh=3)
    onyxFrag3 = Item(ONYX_FRAGMENT, 50, forms=onyxSphr, thresh=3)
    
    # Mandragora set. Instantiated before courtyard because soil can be found in the courtyard.
    mndrk = Item(MANDRAGORA, 60)
    hlyWtr = Liquid(HOLY_WATER, 15, forms=mndrk, thresh=2)
    pttdMndrk = BreakableItem(POTTED_MANDRAGORA, 45, forms=mndrk, thresh=2)
    mndrkBlb = Item("mandragora bulb", 35, forms=pttdMndrk, thresh=2)
    mndrkPt = BreakableItem(POTTED_SOIL_AND_FERTILIZER, 15, forms=pttdMndrk, thresh=2)
    pot = BreakableItem("clay pot", 25, forms=mndrkPt, thresh=2)
    mxtr = Item(FERTILIZED_SOIL, 15, forms=mndrkPt, thresh=2)
    snd = Item(SAND, 0, forms=mxtr, thresh=3)
    sl = Item(SOIL, -25, forms=mxtr, thresh=3)
    frt = Item(FERTILIZER, 10, forms=mxtr, thresh=3)
    
    #####################################################################################  
    ### AREA 1: CASTLE FRONT
    #####################################################################################

    bckt = Item(METAL_BUCKET, 25) # Used with all fireplaces
    vial = BreakableItem(EMPTY_VIAL, 25)
    ram = Weapon(BATTERING_RAM, 35)
    torch = Item(HAND_TORCH, 10)

    ### INITIALIZE WEST ANTECHAMBER
    foy1Gt = Foy_Gate(False, Direction.WEST)
    foy2Gt = Foy_Gate(True, Direction.NORTH)
    foy2Bttn = Foy2_Button(foy1Gt.getID(), foy2Gt.getID())
    #-----------------------------THE ROOM---------------------------------
    foyw = Want("Antechamber", Id.FOYW)     
    #-----------------------------FURNITURE--------------------------------        
    wantLvr = Want_Lever()
    wantStat = Want_Statue()
    wantPllrs = Want_Pillars()
    wantTrchs = Want_Torches()
    wWW = Wall("It's made of heavy sandstone blocks stacked in a staggered fashion.")
    wantF = Floor("A sandstone tiled floor. Small, loose grains grind against your shoes as you walk.")
    wantRmp = Want_Ramp()
    wantDr = Want_Door(Direction.WEST)
    wantGt = Want_Gate(Direction.EAST)
    wantBttn = Want_Button(foy2Bttn.getID())

    ### INITIALIZE BACK BALCONY
    #-----------------------------THE ROOM---------------------------------
    foyb = Bba1("Back balcony", Id.FOYB)
    foyc = Bba2("Back balcony", Id.FOYC)      
    #-------------------------------ITEMS----------------------------------        
    bbaNote = Note("note from a visitor")
    #-----------------------------FURNITURE--------------------------------                       
    bbaF = Floor("The floor is built of many lavender and gray shale rocks mortared together.")
    bbaClmns = Bba_Columns()   
    bbaRlng = Bba_Rlng()  
    bbaVllg = Bba_Village()
    bbaScnc = Bba_Sconce()   
    bbaBnch = Bba_Bench([bbaNote])
    bbaClff = Bba_Cliff()
    bbaShrln = Bba_Shoreline()
    bbaSea = Bba_Sea()
    bba2Dr = Bba2_Door(Direction.SOUTH)
    bba1Gt = Want_Gate(Direction.SOUTH)

    ### INITIALIZE FOYER
    #-----------------------------THE ROOM---------------------------------
    foy1 = Foy1("Foyer", Id.FOY1)
    foy2 = Foy2("Grand staircase", Id.FOY2) 
    foy3 = Foy3("Second floor landing", Id.FOY3)
    foy4 = Foy4("Third floor landing", Id.FOY4) 
    #-------------------------------ITEMS---------------------------------- 
    lootSack = LootSack()
    foy1Note = Note("short letter")
    cndlStck = Weapon("brass candlestick", 40)
    bskt = Item("wicker basket", 15)
    bwlrHat = Clothing("wool bowler hat", 30, use="You slip the warm hat on your head.")
    umbr = BreakableItem("umbrella", 30, use="Is it raining out? You somehow must have not noticed.")
    #-----------------------------FURNITURE--------------------------------    
    foyW = Wall("A dark wood-paneled wall.")
    foyF = Floor("Salmon-colored tiled marble. Its glint stuns you.")
    foyFrntDr = Entr_Door(Direction.SOUTH)
    foy1Chnd = Foy_Chandelier()
    foy1Tbl = Foy1_Table([bskt, foy1Note, cndlStck])
    foy1Crpt = Foy1_Carpet()
    foy1Strs = Foy1_Stairs()    
    foy1Armr = Foy1_Armoire([umbr, bwlrHat, lootSack])
    foy2Stat = Foy2_Stat(foy2Bttn)
    foy2Alc = Foy2_Alcove(foy2Stat.getID())
    foy2Strcs = Foy2_Staircase(Direction.UP, Id.FOY3)
    foy3Strs = Foy3_Stairs()
    foy3F = Floor("The floor is a salmon-colored tile run with a red carpet, " +
              "which continues along the staircase.")
    foy34Crpt = Foy34_Carpet()
    foy4Strs = Foy2_Staircase(Direction.DOWN, Id.FOY3)
    foy4F = Floor("The floor is a salmon-colored tile run with a red carpet, " +
              "which continues along the staircase.")
    foy4Dr = Foy4_Door(Direction.SOUTH)
    
    ### INITIALIZE VESTIBULE
    #-----------------------------THE ROOM---------------------------------
    vest = Vest("Vestibule", Id.VEST) 
    #-------------------------------ITEMS----------------------------------
    pen = BreakableItem(PEN, 40, use="You could write momentos to yourself if you had some paper.")
    ppr = Item(NOTEPAD, 15, use="You could write momentos with this if you had a pen.")
    lttrOpnr = Item("letter opener", 30)
    #-----------------------------FURNITURE--------------------------------
    vesOrb = Vest_Orb()
    vesFire = Vest_Fireplace(bckt)
    vesBtn = Vest_Button(vesFire.getID())
    vesWin = Vest_Window(vesFire.getID())
    vesDr = Vest_Dr(Direction.WEST)      
    vesDsk = Vest_Desk([pen, lttrOpnr, ppr])
    vesEtbl = Vest_EndTable()
    vesCase = Vest_Case([rotuKey])
    vesTpstr = Vest_Tpstr()
    vesChr = Vest_Chair()
    vesF = Floor("A cold, shale tile floor. It's slightly dusty.")       

    ### INITIALIZE COURTYARD
    #-----------------------------THE ROOM---------------------------------
    cou1 = Cou1("Northwest courtyard", Id.COU1)
    cou2 = Cou2("Southwest courtyard", Id.COU2)
    cou3 = Cou3("Castle courtyard", Id.COU3)
    cou4 = Cou4("Front gate", Id.COU4)
    cou5 = Room("Southeast courtyard", Id.COU5)
    cou6 = Cou6("Northeast courtyard", Id.COU6)
    cou8 = Cou8("Spruce tree", Id.COU8)
    #-------------------------------ITEMS----------------------------------
    krnsPlt = Obs1_Plate("brass plate")
    soldMed = BreakableItem(STONE_DISK, 30)
    rck = Item(ROCK, 0)
    grss = Item(GRASS, -25)
    clvr = Item("clover", -25)
    trs = Item(STATUE_TORSO, 40)
    hd = Item(STATUE_HEAD, 40)
    sprcExtrct = Liquid(SPRUCE_EXTRACT, 35, use="Evergreens are widely known to be resistant to burning.")
    pnCn = Item("pine cone", 0, use="This looks painful to eat...")
    brrs = Item("bright red berry", 0, use="You realize, the brightest, reddest berries are the most poisonous of all.");
    fthr = Item(RAVEN_FEATHER, 20)
    strng = Item("string", 10)
    ham = Item(COOKED_HAM, 300)
    leaflet = Note("small leaflet")
    #-----------------------------FURNITURE--------------------------------
    couCstl = Cou_Castle()
    couW = Wall("The castle walls are several stories tall and made of rough granite blocks.")
    couStps = Cou_Steps()
    coutWlkwy = Cou_Tiles()
    couRvns = Cou_Ravens()
    cou1Bnch = Cou1_Bench()
    cou1Thrns = Cou1_Thorns()
    cou1Hl = Cou1_Hole(krnsPlt)
    cou1F = Cou1_Floor(sl, grss, clvr, cou1Hl, [sl, sl, sl])
    cou2Fntn = Cou2_Fountain([rck, rck, rck, rck])
    cou2Bshs = Cou2_Bushes(brrs)
    cou2F = Cou_Floor(sl, grss, clvr, [sl, sl, sl])
    cou3Stps = Cou3_Steps(Direction.UP, Id.COU7)
    cou3Ivy = Cou3_Ivy()
    cou3Gt = Cou3_Gate()
    cou3F = Cou_Floor(sl, grss, clvr, [sl, sl])
    cou3Frk = Cou3_Fork(couFrk)
    cou4Gt = Cou4_Gate()
    cou4Frst = Cou4_Forest()
    cou4Trl = Cou4_Trail()
    cou4Mlbx = Cou4_Mailbox([leaflet, ham])
    cou5Fntn = Cou5_Fountain([rck, soldMed, rck])
    cou5Sprc = Cou5_Spruce(vial, sprcExtrct, [pnCn, pnCn, pnCn])
    cou5F = Cou_Floor(sl, grss, clvr, [hd, sl])
    cou6F = Cou_Floor(sl, grss, clvr, [sl, clvr, trs])
    cou6Stat = Cou6_Statue(cou6F)
    cou6Ghst = Cou6_BlackJackGhost()
    cou8Sprc = Cou8_Spruce(vial, sprcExtrct, [pnCn, pnCn, pnCn])
    cou8Nest = Cou8_Nest([fthr, strng])

    ### INITIALIZE ENTRANCE
    #-----------------------------THE ROOM---------------------------------
    cou7 = Entr("Front portico", Id.COU7)  
    #-----------------------------FURNITURE--------------------------------
    entrF = Floor("The balcony is laid with a brown shale tile.")
    entrBlcny = Entr_Balcony()
    entrClmns = Entr_Columns()
    entrRf = Entr_Roof()
    entrStats = Entr_Statues()
    entrDr = Entr_Door(Direction.NORTH)
    entrStps = Cou3_Steps(Direction.DOWN, Id.COU3)

    ### INITIALIZE FOREST
    #-----------------------------THE ROOM---------------------------------
    for1 = For1(Id.FOR1)
    for2 = For2(Id.FOR2)
    for3 = For3(Id.FOR3)
    for4 = Forest(Id.FOR4)
    for5 = For5(Id.FOR5)
    #-------------------------------ITEMS----------------------------------
    untrRck = Item("uninteresting rock", -50)
    untrBrch = Item("uninteresting branch", -50)
    #-----------------------------FURNITURE--------------------------------
    forTrs = For_Trees()
    forThckt = For_Thicket()
    forFrst = For_Forest()
    forF = Cou_Floor(sl, grss, clvr, [sl, untrRck, untrBrch, untrRck])
    for2Elk = For2_Elk()
    

    #####################################################################################     
    ### AREA 2: WEST WING
    #####################################################################################

    brRam = Item("broken battering ram", 5, use="It's useless now.")
    rdFcs = Focus(RED_FOCUS)   

    ### INITIALIZE ROTUNDA
    #-----------------------------THE ROOM---------------------------------
    rotu = Rotu("Rotunda", Id.ROTU)      
    #-------------------------------ITEMS----------------------------------
    crmcShrd = Weapon("ceramic shard", 10)
    #-----------------------------FURNITURE-------------------------------- 
    rotuFntn = Rotu_Fountain()
    rotuW = Wall("A clean white marble wall, polished smoothed and run with carved molding.")
    rotuF = Floor("It's a dirty white-tiled floor littered with plant matter.", [crmcShrd, crmcShrd])
    rotuPlnts = Rotu_Plants(sl, onyxFrag1)
    rotuHl = Rotu_Hole()
    rotuStat = Rotu_Statue()
    rotuScnc = Rotu_Sconce()
    rotuFrms = Rotu_Frames()
    rotuSky = Rotu_Sky()
    rotuRock = Rotu_Rock()    

    ### INITIALIZE CELLAR
    #-----------------------------THE ROOM---------------------------------
    cel1 = Room("Under the balcony", Id.CEL1)
    cel2 = Room("Cellar", Id.CEL2)
    cel3 = Room("Cellar", Id.CEL3)
    cel4 = Room("Cellar", Id.CEL4)
    cel5 = Room("Cellar", Id.CEL5)
    cel6 = Cel6("Suspended platform", Id.CEL6)
    #-------------------------------ITEMS----------------------------------
    hmmr = Weapon(HAMMER, 30)
    greasyRag = Item("greasy rag", -20)
    wrench = Weapon(MONKEY_WRENCH, 15)
    loopedRope = Item(LOOPED_ROPE, 25, thresh=3, forms=ram)
    coal = Item(COAL, -20)
    #-----------------------------FURNITURE--------------------------------
    celLntrn = Cel_Lantern()
    celPp = Cel_Pipe()
    celF = Floor("This floor is unkept. It's made of old,  dusty floorboards that reflect nearly no light at all.")
    nrthCelClng = Ceiling("The ceiling is arched and made of cobblestone here.")
    cel2Clng = Ceiling("Many parallel wooden spines give support  to the ceiling here.")
    cel1Lddr = Cel_Ladder(Id.LOOK, Direction.UP)
    cel2Shft = Cel2_Shaft()
    cel2Vlv = Cel_Valve(ID=rotuFntn.getID())
    cel3Crt = Cel3_Crate(celTblt)
    cel3Vlv = Cel3_Valve(ID=rotuFntn.getID(), ref=wrench)
    cel4Coal = Cel4_Coal(coal)
    cel4Wrkbnch = Gqua_Workbench([hmmr, greasyRag, wrench, loopedRope, vial])
    cel4Bd = Cel4_Bed()
    cel5Frnc = Cel5_Furnace()
    cel5Lck = Cel5_Lock()
    cel5Grt = Cel5_Grate()
    cel6Pltfrm = Cel6_Platform()
    cel6Lddr = Cel_Ladder(Id.CEL5, Direction.UP)
    cel6Vlv = Cel_Valve(ID=rotuFntn.getID())
    cel6Clmns = Cel6_Columns()
    cel6Lghts = Cel6_Lights()
    cel6Pp = Cel6_Pipe()
       
    ### INITIALIZE LOOKOUT
    #-----------------------------THE ROOM--------------------------------- 
    look = Look("Lookout", Id.LOOK)       
    #-----------------------------FURNITURE-------------------------------- 
    lookDr = Look_TrapDoor()
    lookLghths = Look_Lighthouse()
    lookClff = Look_Cliff()
    lookRlng = Look_Railing()
    lookF = Floor("Just a wet shale floor.") 

    ### INITIALIZE SIDE HALL
    #-----------------------------THE ROOM---------------------------------
    iha1 = Iha1("North side hall", Id.IHA1)
    iha2 = Iha2("South side hall", Id.IHA2)
    #-------------------------------ITEMS----------------------------------
    iha2plArm = Weapon(POLEARM, 30)
    #-----------------------------FURNITURE--------------------------------
    iha1Lvr = Iha1_Lever()
    iha1Armr = Iha1_Armor()
    iha2Armr = Iha2_Armor(iha2plArm)     
    ihaF = Floor("A sandstone tiled floor. Small, loose grains grind against your shoes as you walk.")
    ihaWndw = Iha_Window()
    iha1Bwl = Iha1_Bowl(ihaF.getID(), wow2Key)
    iha2Bwl = Iha2_Bowl()

    ### INITIALIZE WEST OUTER WALL
    #-----------------------------THE ROOM---------------------------------
    wow1 = Room("West outer wall", Id.WOW1)
    wow2 = Wow2("West outer wall", Id.WOW2)
    #-------------------------------ITEMS----------------------------------
    vinegar = Liquid(BOTTLE_OF_VINEGAR, 25)
    wowLddr = BreakableItem(FIXED_LADDER, 25)   
    wow1Spk = Item(WHEEL_SPOKE, 0, thresh=3, forms=wowLddr)
    clngSoln = Liquid(CLEANING_SOLUTION, 25)
    rppdBrlp = Item("ripped burlap", 5)
    actn = Liquid(ACETONE, 25)
    #-----------------------------FURNITURE--------------------------------
    wow2Lddr = Wow2_Ladder(Direction.UP, Id.WOW3) # Not in Id.WOW2 to start.
    wow2Armr = Wow2_Armor()
    wow1Crt = Wow1_Cart([wow1Spk, rppdBrlp])
    wow1F = Floor("A sandstone tiled floor. Small, loose grains grind against your shoes as you walk.")
    wow2Blcny = Wow2_Balcony(wow2Lddr, wowLddr) # Fixed ladder can be used on this.
    wow2F = Wow2_Floor(wow2Lddr, wowLddr) # Fixed ladder can be used on this.
    wow2Dr = Wow2_Door(Direction.EAST)
    wow2Hole = Wow2_Hole()
    wowWndw = Wow_Window()
    wowHrth= Wow_Hearth(bckt)
    wow2Strcs = Wow2_Stairs() 
    wow1NDr = Sha_Door(Direction.NORTH)
    wow1Shlvs = Wow1_Shelves([vial, vinegar, clngSoln, actn])
    ### INITIALIZE BEACON

    #-----------------------------THE ROOM---------------------------------
    wbal = Wbal("Beacon", Id.WBAL)   
    #-------------------------------ITEMS----------------------------------
    wbalch = Item("rotted wooden chunk", -50)
    wbalsp = Item("wood splinter", -25)
    wbalbr = Item("branch", -25)
    wbalBrg = Item("broken rod", -25)
    wbalRng = Item("wooden rod", 10, thresh=3, forms=wowLddr)
    #-----------------------------FURNITURE--------------------------------
    wbalF = Floor("A shale tile floor. Many pieces of wood litter it.", 
                        [wbalch, wbalbr, wbalBrg, wbalsp, wbalsp, wbalRng, wbalbr, wbalch, wbalch])
    wbalBcn = Wbal_Beacon()
    wbalFrst = Wbal_Forest()

    ### INITIALIZE SERVANTS QUARTERS
    #-----------------------------THE ROOM---------------------------------
    squa = Room("Servant's quarters", Id.SQUA)
    #-------------------------------ITEMS----------------------------------
    squaLddr = Squa_Ladder("broken ladder", thresh=3, forms=wowLddr)
    squaJrnl = Note("note: ladder")
    rags = Clothing("worn rags", 5, use="You are perfectly content with the clothes you have on now.")
    aprn = Clothing("kitchen apron", 25, use="You are perfectly content with the clothes you have on now.")
    shs = Shoes("moccasins", 10, use="You put on the moccasins. They're quite uncomfortable.")
    #-----------------------------FURNITURE--------------------------------
    squaF = Floor("A sandstone tiled floor.")
    squaDr = Sha_Door(Direction.EAST)
    squaBd = Squa_Bed([squaLddr])
    squaDsk = Squa_Desk([squaJrnl, sha1CbtKey])
    squaWndw = Squa_Window()
    squaCndl = Squa_Candle()
    squaWrdrb = Squa_Wardrobe([rags, rags, aprn, shs])

    ### INITIALIZE CLOSET
    #-----------------------------THE ROOM---------------------------------
    # Used to be called "Groundskeeper's quarters" +
    clos = Room("Utility closet", Id.CLOS)
    #-------------------------------ITEMS----------------------------------
    closCrwbr = Weapon(CROWBAR, 30)
    shvl = Weapon(SHOVEL, 30)
    sd = Item(SEED, 0)
    gl = Liquid(GLUE_BOTTLE, 15)
    closGlv = Clothing(RUBBER_GLOVES, 15, use="It's difficult, but you manage to fit them on your hands.")
    closStrw = Item("straw", 5)
    scrwDrvr = Item(SCREWDRIVER, 25, use="The tool seems perhaps a tad out of place in an old establishment like this.")
    scrw2 = Item("2mm screw", 15)
    scrw5 = Item("5mm screw", 15)
    #-----------------------------FURNITURE--------------------------------
    closDr = Wow2_Door(Direction.WEST)
    closLddr = Gqua_Ladder(Direction.DOWN, Id.COUS)
    closClng = Gqua_Ceiling()
    closF = Floor("It's a cold, hard, cobblestone floor", [closStrw])
    closScks = Gqua_Sacks([sd, sd, sd, frt, frt, frt, snd, snd, snd, snd, snd])
    closShlf = Gqua_Shelf([bckt, closGlv, vial, shvl, pot, pot])
    closWrkbnch = Gqua_Workbench([gl, hmmr, scrw2, scrwDrvr, scrw2, scrw5, scrw5])
    closStl = Gqua_Stool()
    closBrrl = Gqua_Barrel()
    closW = Wall("It's a plain cobblestone wall.")
    closSkltn = Gqua_Skeleton([closCrwbr])

    ### INITIALIZE WEST OUTER WALL BALCONY
    #-----------------------------THE ROOM---------------------------------
    wow3 = Wow3("Balcony", Id.WOW3, wow2Lddr, wow2F.getID(), wowLddr)
    #-------------------------------ITEMS----------------------------------
    wowRope = Item("rope", 15, thresh=3, forms=ram)
    #-----------------------------FURNITURE--------------------------------
    wow3Shlf = Wow3_Shelf([wowRope, closKey])
    wow3F = Floor("A sandstone tiled floor. Small, loose grains grind against your shoes as you walk.")
    wow3NDr = Wow3_NorthDoor()
    wow3Dr = Wow3_Door(Direction.EAST)

    ### INITIALIZE RANSACKED QUARTERS
    #-----------------------------THE ROOM---------------------------------
    shar = Room("Ransacked quarters", Id.SHAR)
    #-------------------------------ITEMS----------------------------------
    cmb = Item("comb", 25, use="You comb your beard for several seconds until it's nice and kept.")
    cndlStk = Weapon("candlestick", 40)
    sht = Item("sheet", 15)
    #-----------------------------FURNITURE--------------------------------
    rquaBd = Rqua_Bed()
    rquaWmn = Rqua_WomanNPC()
    rquaClths = Rqua_Clothes()
    rquaMttrss = Rqua_Mattress()
    rquaTbl = Rqua_Table()
    rquaDrssr = Rqua_Dresser()
    rquaF = Floor("A sandstone tiled floor. Small, loose grains grind against your shoes as you walk.", 
            [rags, cmb, rags, sht, cndlStk, rags, shs])
    rquaPnl = Rqua_Panel(studKey, rquaBd.getID())
    
    ### INITIALIZE SERVANTS HALL
    #-----------------------------THE ROOM---------------------------------
    sha2 = Room("North servant's hall", Id.SHA2)
    sha1 = Sha1("South servant's hall", Id.SHA1)
    #-------------------------------ITEMS----------------------------------
    wdChnk = Item(WOOD_LOG, 0, forms=ram, thresh=3)       
    shaMp = Item(MOP, 25, use="Yes, let's just make this a game about cleaning some madman's castle.")
    shaSpng = Item("sponge", 5, use="I'm a lumberjack, not a maid!")
    #-----------------------------FURNITURE--------------------------------       
    sha2Cbnt = Sha2_Cabinet([wdChnk, shaSpng, shvl, shaMp, bckt])
    shaF = Floor("A sandstone tiled floor. Small, loose grains grind against your shoes as you walk.")
    sha2Dr = Sha_Door(Direction.WEST)
    sha1SDr = Sha_Door(Direction.SOUTH)
    sha1Trch = Torch_Holder(torch)
    sha2Trch = Torch_Holder(torch)
    sha1Dr = Sha1_Door(ram, brRam, genDoor.getID())

    ### INITIALIZE SCORCHED ROOM
    #-----------------------------THE ROOM---------------------------------
    cous = Cous("Scorched room", Id.COUS)
    #-------------------------------ITEMS----------------------------------
    wrhmmr = Item(WARHAMMER, 35)
    ash = Item(ASH, -30)
    wd = Item("charred wood", -25)
    #-----------------------------FURNITURE-------------------------------- 
    searFssr = Sear_Fissure()
    searDr = Sear_Door()
    searAsh = Sear_Ash(ash)
    searWood = Sear_Wood(wd)
    searSkltn = Sear_Skeleton([closCrwbr])
    searLddr = Gqua_Ladder(Direction.UP, Id.CLOS)
    searF = Floor("It's a cold, hard, cobblestone floor", [ash, wd, ash, wrhmmr, wd, ash])

    ### INITIALIZE STUDY
    #-----------------------------THE ROOM---------------------------------
    stud = Stud("Study", Id.STUD)
    #-------------------------------ITEMS----------------------------------
    studBkPi = Book("book, 'An Essential Pi'", "Stud_PiBook")
    studNote = Note("personal note")
    studNote2 = Note("sketches")
    #-----------------------------FURNITURE-------------------------------- 
    studSafe = Stud_Safe(367, [studBkPhy, gal1Key])
    studF = Floor("The floor is a weathered dark hickory that creaks slowly as you walk. How nice!")
    studPrtrt = Stud_Portrait(studSafe)
    studFire = Stud_Fireplace(bckt)
    studDsk = Stud_Desk([pen, ppr, studNote2, servKey, studNote])
    studBkCs = Stud_BookCase([studBkPi])
    studCch = Stud_Couch()
    studCrpt = Stud_Carpet()

    #####################################################################################     
    ### AREA 3: EAST WING
    #####################################################################################

    ### INITIALIZE TROPHY ROOM
    #-----------------------------THE ROOM---------------------------------
    gal5 = Room("Trophy room", Id.GAL5)
    #-------------------------------ITEMS----------------------------------
    zsPlt = Obs1_Plate("brass plate, \"Jupiter\"")
    emrld = BreakableItem(GLOWING_EMERALD, 300, use="This belongs to someone important.")
    aqmrn = BreakableItem(AQUAMARINE, 225)
    rby1 = BreakableItem(RUBY, 200)
    #-----------------------------FURNITURE--------------------------------
    gal5Dr = Gal4_Door(Direction.SOUTH)
    gal5Dsply = Gal5_Display([rby1, emrld, aqmrn])
    gal5Chndlr = Gal5_Chandelier()
    gal5Cbwbs = Cobweb()
    gal5Clng = Gal5_Ceiling()
    gal5F = Floor("The floor is a gray and white checkered tile lightly coated in dust.")
    gal5W = Wall("The walls are just plain granite brick, supported by curved wooden struts which meet at the room's apex in an arch.")
    gal5Cbt = Gal5_Cabinet([zsPlt])

    ### INITIALIZE GALLERY
    gal3Lddr = Gal3_Ladder()
    gal3Rp = Gal3_Rope(gal3Lddr.getID())
    #-----------------------------THE ROOM---------------------------------    
    gal1 = Gal1("First floor gallery", Id.GAL1)
    gal2 = Room("Central chamber", Id.GAL2)      
    gal3 = Gal3("Second floor gallery", Id.GAL3, gal3Rp)
    gal4 = Room("Second floor balcony", Id.GAL4)
    gal6 = Gal6("Gallery loft", Id.GAL6)
    gal7 = Room("Gallery loft", Id.GAL7)
    #-------------------------------ITEMS----------------------------------
    scrw1 = Item("1mm screw", 0, forms=rdFcs, thresh=3)
    blFcs = Focus(BLUE_FOCUS)
    yllwFcs = Focus(YELLOW_FOCUS)
    drkFcs = Focus(DARK_FOCUS)
    fnnyOrb = BreakableItem(CRYSTAL_ORB, 150)
    bxThngy = BreakableItem(DEAD_BATTERY, 150)
    #-----------------------------FURNITURE--------------------------------         
    gal7Stat = Gal7_Statue()
    gal4Stat = Gal4_Statue(gal7Stat)
    gal2Stat = Gal2_Statue(gal4Stat)
    gal2Mchn = Gal2_Machine([bxThngy])
    gal1Dr = Bba2_Door(Direction.NORTH)
    gal1Drgn = Gal1_Dragon(gal2Stat.getID(), [yllwFcs])
    gal2Stat.addDragonRef(gal1Drgn)
    gal1KtnFurn = Gal1_KatanaFurniture()
    gal1Swtch = Gal1_Switch(gal1Drgn.getID())
    gal1Bttn = Gal1_Button(gal1Drgn.getID())
    gal1Lghts = Gal1_Lights()
    gal1Scr = Gal1_Scroll(gal1Bttn)
    gal1Scrn = Gal1_Screen(gal1Swtch)
    gal1Armr = Gal1_Armor()
    gal1F = Floor("The floor is a dark hardwood.")
    gal1W = Wall("The wall is tiled a dark green and purple. Interesting choice...")
    gal1Sclptrs = Gal1_Sculptures()
    gal1Pntngs = Gal1_Paintings()
    gal1Pntng3 = Gal1_Painting3()
    gal1Pntng2 = Gal1_Painting2()
    gal1Pntng = Gal1_Painting1()
    gal1Hrth = Gal1_Hearth(bckt)
    gal3Ttm = Gal3_Totem(gal4Stat.getID())
    gal3Peg = Gal3_Peg(gal3Ttm.getID())
    gal3Sgmnt = Gal3_Segment(gal3Ttm.getID())
    gal3Swtch = Gal3_Switch()
    gal3InstFurn = Gal3_KoraFurniture()
    gal3Msk = Gal3_Mask1()
    gal3Msk2 = Gal3_Mask2()
    gal3Msk3 = Gal3_Mask3()
    gal3Msks = Gal3_Masks()
    gal3Hrth = Gal3_Hearth(bckt)
    gal3F = Floor("The floor is a dark hardwood.")
    gal3W = Wall("The wall an off-white plaster, creating an atmospheric warmth.")
    gal3Art = Gal3_Artifact1()
    gal3Art2 = Gal3_Artifact2()
    gal3Art3 = Gal3_Artifact3()
    gal3Arts = Gal3_Artifacts()
    gal3Htch = Gal3_Hatch()
    gal3Hl = Gal3_Hole()
    galDm = Gal_Dome()
    gal2Clmns = Gal2_Columns()
    galBalc = Gal_Balcony()
    gal2F = Floor("This room's floor is magnificent. It's solid marble and resembles a giant compass.")
    gal2W = Wall("The wall here is an ornate white-paneled wood.")
    gal2Strcs = Gal2_Staircase(Direction.UP, Id.GAL4)
    gal4Glss = Gal4_Glass()
    gal4Cs = Gal4_Case([monaLisa])
    gal4Lck = Gal4_Padlock(gal4Cs.getID())
    gal4Dr = Gal4_Door(Direction.NORTH)
    gal4Lft = Gal4_Loft()
    gal4Strcs = Gal2_Staircase(Direction.DOWN, Id.GAL2)
    gal4Rdo = Gal4_Radio(scrw1)
    gal4F = Floor("The floor here is checkered gray and tan in a smooth rock. Running along the floor around the balcony is a royal blue carpet-runner.")
    gal4Crpt = Gal4_Carpet()
    gal4Lvr = Gal4_Lever()
    gal6Htch = Gal6_Hatch()
    gal6Cnn = Gal6_Canon(gal7Stat.getID())
    gal6Lddr = Gal6_Ladder()
    gal6Hlmt = Gal6_Helmet()
    gal6Mchn = Gal6_Machine()
    gal6Bttn = Gal6_Button()
    gal6App = Gal6_Apparatus()
    gal6F = Floor("The floor is a dark hardwood.")
    gal6W = Wall("The wall is paneled in a classy mahogany.")
    gal6Tech = Gal6_Technology()
    gal6Elec = Gal6_Technology()
    gal6Tbl = Gal6_Table()

    ### INITIALIZE DINING ROOM
    #-----------------------------THE ROOM---------------------------------
    din1 = Din1("Dining room", Id.DIN1)  
    din2 = Din2("Dining room balcony", Id.DIN2)
    #-------------------------------ITEMS----------------------------------
    aphrdtPlt = Obs1_Plate("brass plate, \"Venus\"")
    frk = Item("silver fork", 75, use="You comb your beard with the fork until it's straight and tidy.")
    plt = Item("silver platter", 80)
    spn = Item("silver spoon", 75, use="You attempt to comb your beard with the spoon, but it's not working so well.")
    npkn = Item("napkin", 60, use="You wipe the sweat off your forehead. Carrying all these items has taken its toll on you.")
    #-----------------------------FURNITURE--------------------------------  
    din1Clmns = Din1_Columns()
    din1Blcny = Din1_Balcony()
    din1Wndw = Din1_Window()
    din1Chrs = Din1_Chairs()
    din1Tbl = Din1_Table([frk, spn, plt, npkn, cndlStck, frk, spn, plt, npkn, cndlStck])
    din1Chndlr = Din1_Chandelier()
    din1Mnlght = Din1_Moonlight()
    din1Crvc = Din1_Crevice([aphrdtPlt])
    din1Tpstry = Din1_Tapestry(din1Crvc)
    din1Strs = Din1_Stairs(Direction.UP, Id.DIN2)
    din1Crpt = Din1_Carpet()
    din1F = Floor("The floor is a light gray stone. A large rectangular lavender carpet covers much of it.")
    din1W = Wall("The walls of this room are gray stone with dark wood paneling at the bottom.")
    din1Dr = Din1_Door(Direction.WEST)
    din2F = Floor("The floor is laid with square light-gray tiles.")
    din2W = Wall("The walls up here are smooth rock paneled on the lower half with vertical wooden slats.")
    din2Pntng = Din2_Painting()
    din2Strs = Din1_Stairs(Direction.DOWN, Id.DIN1)

    ### INITIALIZE MARBLE HALL
    #-----------------------------THE ROOM---------------------------------
    mha1 = Mha1("North marble hall", Id.MHA1)
    mha2 = Room("Marble hall", Id.MHA2)
    mha3 = Room("South marble hall", Id.MHA3)
    #-------------------------------ITEMS----------------------------------       
    angMed = Item(ANGEL_MEDALLION, 130)
    horMed = Item(HORSE_MEDALLION, 90)
    #-----------------------------FURNITURE--------------------------------  
    mhaChndlr = Mha_Chandelier()
    mhaF = Floor("Large tiles running diagonally to the hall cover the floor. " +
              "Their bright green hue is uncanny and must be artificial.")
    mhaW = Wall("The walls are plain white granite. All that occupy them are the tall windows.")
    mhaNWndw1 = Mha1_Window()
    mhaNWndw2 = Mha1_Window()
    mhaSWndw = Mha3_Window()
    mhaNChaDr = Mha1_Door(Direction.EAST)
    mhaNDr = Mha_Door(Direction.NORTH)
    mhaSDr = Mha_Door(Direction.SOUTH)
    mhaWDr = Mha_Door(Direction.WEST)
    mha3KitcDr = Mha3_Door(Direction.EAST)
    mhaMDr = Mha2_Door(Direction.EAST)
    mha1Plnt = Mha_Plant(sl, stnHd)
    mha2Plnt = Mha_Plant(sl, onyxFrag2)
    mha3Plnt = Mha_Plant(sl, stnBs)
    mhaChr = Mha_Chair()
    mhaRStat = Mha2_RightStatue([angMed])
    mhaLStat = Mha2_LeftStatue()
    mhaStats = Mha2_Statues(mhaRStat.getID())

    ### INITIALIZE WORKSHOP
    #-----------------------------THE ROOM---------------------------------
    work = Room("Workshop", Id.WORK)
    #-------------------------------ITEMS----------------------------------
    redLns = BreakableItem("red lens", 60, thresh=3, forms=rdFcs)
    rdDy = Item(RED_DYE, 15)
    blDy = Item(BLUE_DYE, 15)
    yllwDy = Item(YELLOW_DYE, 15)
    stncl = Item(LENS_TEMPLATE, 20)
    wrkNt = Note("ingredient order")
    ptsh = Item(POTASH, 5)
    #-----------------------------FURNITURE--------------------------------
    wrkF = Floor("A sandstone tiled floor, blackened and dirty from ash.", [snd])
    wrkBrl = Wrk_Barrel([rdDy, rdDy, blDy, blDy, yllwDy, yllwDy])
    wrkCbnt = Wrk_Cbnt([hmmr, gl, ptsh, ptsh])
    wrkCstTbl = Wrk_CastingTable(wrkBrl.getID(), closScks.getID(), 
            redLns, snd, rdDy, blDy, yllwDy, ptsh, wrkCbnt.getID())
    wrkKln = Wrk_Kiln()
    wrkBnch = Gqua_Workbench([stncl, wrkNt])        
    wrkAnvl = Wrk_Anvil()
    wrkFrg = Wrk_Forge()

    ### INITIALIZE EAST OUTER WALL
    #-----------------------------THE ROOM---------------------------------
    eow1 = Room("East outer wall", Id.EOW1)
    eow2 = Room("East outer wall", Id.EOW2)
    eow4 = Eow4("Balcony", Id.EOW4)
    #-------------------------------ITEMS----------------------------------
    wtrBckt = Liquid(BUCKET_OF_WATER, 25)
    eowSwrd1 = Weapon("silver sword", 100)
    eowSwrd2 = Weapon("rusty sword", 20)
    eowSwrd3 = Weapon("broken sword", 10)
    eowSSpr = Weapon(SILVER_SPEAR, 100)
    woodSpr = Weapon("wooden spear", 15)
    eowPlArm = Weapon(POLEARM, 30)
    eowAx = Weapon("war ax", 40) 
    eowBtlAx = Weapon("battle ax", 40)
    #-----------------------------FURNITURE--------------------------------
    eowF = Floor("It's a sandstone tiled floor, just like that of the west wing.")
    eow1Dr = Eow1_Door(Direction.WEST)
    eow1Rck = Eow1_Rack([eowSwrd1, eowBtlAx, eowSwrd2, eowSwrd3, eowSwrd2, eowAx])
    eow1Bskt = Eow1_Basket([eowPlArm, woodSpr, woodSpr, eowPlArm])
    eow1Trch = Torch_Holder(torch)
    eow2Fntn = Eow2_Fountain()
    wtr = Water(wtrBckt)
    eow2Rck = Eow1_Rack([eowSwrd1, eowSwrd2, eowSSpr, woodSpr, eowBtlAx])
    eow2Strs = Eow2_Stairs(Direction.UP, Id.EOW4)
    eow2Blcny = Eow2_Balcony()
    eow2Cbnt = Eow2_Cabinet([bckt, shaMp, shvl, vinegar])
    eow2Trch = Torch_Holder(torch)
    eow4F = Floor("It's a sandstone tiled floor.")
    eow4Strs = Eow2_Stairs(Direction.DOWN, Id.EOW2)

    ### INITIALIZE LIBRARY
    lib4Tbl = Lib4_Table(fnnyOrb)
    #-----------------------------THE ROOM---------------------------------
    lib2 = Lib2("North library", Id.LIB2)
    lib3 = Lib3("South library", Id.LIB3)
    lib4 = Lib4("North upper library", Id.LIB4, lib4Tbl)
    lib5 = Lib5("South upper library", Id.LIB5)
    #-------------------------------ITEMS----------------------------------
    cndl = BreakableItem(CANDLE, 15)
    shs1 = Shoes(LEATHER_SHOES, 60, use="You put on the shoes. They're a little big, but comfortable!")
    shs2 = Shoes("worn shoes", 10, use="You put on the shoes. These aren't too comfortable.")
    shs3 = Shoes(NIGHT_SLIPPERS, 60, use="You wear the slippers. You could wear these all day!")
    shs4 = Shoes(WORK_BOOTS, 15, use="You put on the boots.")
    fin = Book("language, 'The Essential Finnish'", "Lib_FinnishBook")
    bbl = Book(BIBLE, "Lib_GenesisBook")
    ody = Book(ODYSSEY, "Lib_OdysseyBook")
    ili = Book(ILIAD, "Lib_IlliadBook")
    inf = Book(DANTES_INFERNO, "Lib_DantesInfernoBook")
    par = Book(PARADISE_LOST, "Lib_ParadiseLostBook")
    bkGlss = Book("guide, 'The Master Glasser'", "Lib_GlassBook")
    bkNts = Book("self help, 'Note To Self'", "Lib_NotesBook")
    bkGlsswr = Book("manual, 'You Aren't Chemist'", "Labo_GlasswareBook")
    #-----------------------------FURNITURE--------------------------------
    libLF = Floor("The floor is a rough, dark blue stone.")
    libUF = Floor("The floor is a rough, dark blue stone.")
    libW = Wall("A classy mahogany paneled wall. Mahogany, having the highest IQ of any wood.")
    libCch = Lib_Couch()
    libBkShlf = Lib_BookShelf()
    libScncs = Lib_Sconces()
    lib3Stat = Lib3_Statue(horMed)
    lib2ShRck = Lib2_ShoeRack([shs3, shs2, shs1, shs4])
    lib2Stat = Lib2_Statue()
    lib2Frplc = Lib2_Fireplace(bckt)
    lib2Bttn = Lib2_Button(lib2Frplc.getID(), lib3Stat.getID())
    lib2WrFr = Lib2_WarefareShelf([inf, fin])
    lib2Wndw = Lib2_Window()
    lib3Pllr = Lib_Pillar()
    lib3Strs = Lib_Stairs(Direction.UP, Id.LIB4)
    lib3Crtn = Lib3_CreationShelf([ody, bkGlsswr])
    lib3Blcny = Lib_Balcony()
    lib3Wndw = Lib3_Window()
    lib3Pntng = Lib3_Painting()
    lib4Frplc = Lib2_Fireplace(bckt)
    lib4Bttn = Lib4_Button(lib4Frplc.getID(), lib3Stat.getID())
    lib4Prdtn = Lib4_PerditionShelf([ili, bkNts])
    lib4Glb = Lib4_Globe()
    lib4Stat = Lib4_Statue()
    lib4Strs = Lib_Stairs(Direction.DOWN, Id.LIB3)
    lib5Bnshmnt = Lib5_BanishmentShelf([bbl])
    lib5Cndlbr = Lib5_Candelabra([cndl, cndl, cndl, cndl])
    lib2Vyg = Lib2_VoyageShelf(lib2WrFr.getID(), lib3Crtn.getID(), lib4Prdtn.getID(), lib5Bnshmnt.getID(), [par, bkGlss])

    ### INITIALIZE SECRET ARCHIVES
    #-----------------------------THE ROOM---------------------------------
    lib1 = Room("Secret archives", Id.LIB1)
    #-------------------------------ITEMS----------------------------------
    lib1Schmtc = Note("architectural plan")
    lib1Nt1 = Note("account, page 1")
    lib1Nt2 = Note("account, page 2")
    lib1Nt3 = Note("account, page 3")
    lib1Nt4 = Note("account, page 4")
    lib1Lst = Note("artifact report")
    lib1ImpNt = Note("schematic: disc")
    lib1Pln = Note("schematic: vessel")
    brkLns = Item("cracked lens", 5, use="You think this has lost its purpose by now.")
    brssRng = Item("brass ring", 25, thresh=3, forms=rdFcs)
    #-----------------------------FURNITURE--------------------------------
    lib1Docs = Lib1_Documents()
    lib1F = Floor("It's a dusty wood parquet floor. Years of neglect " +
              "have reduced its shine to a dull matte finish.", lib1Nt1)
    lib1W = Wall("The walls are just horizontal wood slats, separated " +
              "slightly as to see the underlying structural rock.")
    lib1Art = Lib1_Artifact([blFcs])
    lib1Dsk = Lib1_Desk(lib1Art.getID(), [lib1Schmtc, ppr, pen, lib1Lst, lib1ImpNt])
    lib1Rg = Lib1_Rug()
    lib1Rck = Lib1_Rack([lib1Nt2, lib1Nt4, lib1Nt3])
    lib1Tbl = Lib1_Table([lib1Pln])
    lib1Lght = Lib1_Light()
    lib1Mrrr = Lib1_Mirror()
    lib1Wndw = Lib1_Window()
    lib1Sf = Lib1_Safe(712, [eow3Key, brkLns, brssRng])

    ### INITIALIZE DRAWING ROOM
    #-----------------------------THE ROOM---------------------------------
    drar = Drar("Drawing room", Id.DRAR)
    #-------------------------------ITEMS----------------------------------
    wine = Liquid(BOTTLE_OF_WINE, 15)
    rk = Item("rook", 30, use="You have no idea how to play chess.")
    knght = Item("knight", 30, use="You have no idea how to play chess.")
    bshp = Item("bishop", 30, use="You have no idea how to play chess.")
    pwn = Item("pawn", 15, use="This is the weakest piece right? Hmph. Better not ask a chess player that.")
    rdBl = Item(RED_BALL, 30, use="This is nonsense. Where are the numbers?")
    cBl = Item(CUE_BALL, 30, use="You'd rather break a window with this and jump out rather than play this witchcraft.")
    #-----------------------------FURNITURE--------------------------------
    drarBr = Drar_Bar([wine, wine, wine])
    drarGhst = Drar_Ghost(drkFcs, kitcKey, emrld, drarBr.getID())
    drarF = Floor("The room is carpeted in lavender with tenuous gold lines curving intricately along the edges.")
    drarW = Wall("This is the first time you've seen wallpaper in here. It's striped vertical in purple and lavender.")
    drarWndw = Lib3_Window()
    drarBllrds = Drar_Billiards(drarGhst.getID(), [rdBl, cBl, cBl])
    drarChss = Drar_Chess(drarGhst.getID(), [rk, knght, bshp, qn, kng, bshp, knght, rk, pwn, pwn, pwn, pwn, pwn, pwn, pwn, pwn])
    drarCch = Drar_Couch(drarGhst.getID())
    drarTbl = Drar_Table(drarGhst.getID())
    drarPno = Drar_Piano()

    ### INITIALIZE KITCHEN 
    kitcTrch = Kitc_Torch(torch)
    #-----------------------------THE ROOM---------------------------------
    kitc = Kitc("Kitchen", Id.KITC, kitcTrch.getID())
    #-------------------------------ITEMS----------------------------------
    rtnFrt = Item("rotten fruit", -50, use="Whatever you expect him to do with that, he isn't going to.")
    petFrt = Item("petrified vegetable", -50, use="Whatever you expect him to do with that, he isn't going to.")
    brly = Item("barley", -50)
    rye = Item("rye", -50)
    cpprPt = Weapon(COPPER_POT, 30)
    cpprPn = Weapon(COPPER_PAN, 30)
    #-----------------------------FURNITURE--------------------------------
    kitcF = Floor("The floor is dirty brown stone, composed of differently sized bricks. " +
              "The bricks are nicked all over, as if pelted numerous times with heavy objects.")
    kitcW = Wall("The wall is mostly cobblestone supported by wooden vertical beams along the walls.")
    kitcWndw = Kitc_Window()
    kitcDr = Mha3_Door(Direction.WEST)
    kitcRck = Kitc_Rack([drwKey, par2Key, dngnKey])
    kitcPts = Kitc_Pots(cpprPt, cpprPn, [cpprPt, cpprPn, cpprPt, cpprPn])
    kitcHrth = Kitc_Hearth([wbalch, wbalch, wbalch, wbalch])
    kitcBrls = Kitc_Barrels([brly, brly, brly, rye, rye, rye])
    kitcPntry = Kitc_Pantry([rtnFrt, rtnFrt, petFrt, kitcFrtPhy, petFrt])
    kitcShlf = Kitc_Shelf([wine, wine, wine, wine, wine, wine, wine])
    kitcCntr = Kitc_Cntr([shaSpng, vinegar, vial, vial])   

    ### INITIALIZE DUNGEON STAIRCASE
    #-----------------------------THE ROOM---------------------------------
    dst1 = Dst1("Eerie chamber", Id.DST1)
    #-----------------------------FURNITURE--------------------------------
    dst1Dr = Eow1_Door(Direction.EAST)
    dst1Strs = Dst1_Stairs()
    dstW = Wall("The walls in here are a mossy cobblestone.")
    dst1F = Floor("The stone floor is mossy and dank from the humidity.")
    dst1Lntrn = Dst1_Lantern()

    #####################################################################################     
    ### AREA 4: CASTLE REAR
    #####################################################################################

    ### INITIALIZE OBSERVATORY 
    #-----------------------------THE ROOM---------------------------------
    obs1 = Room("Observatory", Id.OBS1)
    obs2 = Obs2("Observatory balcony", Id.OBS2)
    obs3 = Obs3("Aerie", Id.OBS3)
    #-------------------------------ITEMS----------------------------------  
    hlsPlt = Obs1_Plate("brass plate, \"Sol\"")
    hrmsPlt = Obs1_Plate("brass plate, \"Mercury\"")
    gaeaPlt = Obs1_Plate("brass plate, \"Terra\"")
    aresPlt = Obs1_Plate("brass plate, \"Mars\"")
    urnsPlt = Obs1_Plate("brass plate, \"Caelus\"")
    psdnPlt = Obs1_Plate("brass plate, \"Neptune\"")
    rby2 = BreakableItem(RUBY, 200)
    gr = Item("small gear", 15)
    glssLns = BreakableItem("glass lens", 30)
    mchnPc = Item("machine piece", 15)
    obs1Nt = Note("scribbly note")
    obsBk = Book("tome, 'Planets and Myth'", "Obs2_Book")
    obs2Nt = Note("journal page, Factum")
    obs3Nt = Note("momento: plate locations")
    #-----------------------------FURNITURE--------------------------------
    obs3Chndlr = Obs3_Chandelier("chandelier", [cndl, cndl, cndl, rby2, cndl, cndl])
    obsStats = Obs1_Statues(obs3Chndlr.getID())
    obsSlts = Obs1_Slots(hlsPlt, obsStats)
    obsF = Floor("The floor in here is gray and dark blue checkered " +
              "tile with thin veins of gold running between them.")
    obsW = Wall("The walls are mahogany wood paneled, " +
              "with each panel bearing a large round cavity displaying a painted constellation.")
    obsWndw = Obs_Window()
    obs1Strs = Obs13_Stairs(Direction.UP, Id.OBS2)
    obs1Tlscp = Obs1_Telescope([gr, mchnPc, glssLns])
    obs1Lmp = Obs1_Lamp()
    obs1St = Obs1_Seat(obs1Nt)
    obsBlcny = Obs_Balcony()
    obs2Strs = Obs2_Stairs()
    obs2BkShlf = Obs2_BkShlf([obsBk, obs2Nt, astrLabe, obs3Nt])
    obs2Pntng = Obs2_Painting()
    obs2Rlng = Obs2_Railing()
    obs2Chr = Obs2_Chair()
    obs2Tbl = Bha1_Table([lttrOpnr, pen, ppr])
    obs2Lmp = Obs2_Lamp()
    obs2F = Floor("The balconies are laid with polished brightly stained wood.")
    obs3Strs = Obs13_Stairs(Direction.DOWN, Id.OBS2)
    obs3Chst = Obs3_Chest([psdnPlt])
    obs3Tlscps = Obs3_Telescopes()
    obs3F = Floor("The balconies are laid with polished brightly stained wood.")

    ### INITIALIZE JADE HALL
    #-----------------------------THE ROOM---------------------------------
    jha1 = Room("Jade hallway", Id.JHA1)
    jha2 = Jha2("Jade hallway", Id.JHA2) # Adds hidden door to room
    #-----------------------------FURNITURE--------------------------------  
    jhaLntrn = Jha_Lantern()
    jha1Pntng = Jha1_Painting()
    jhaF = Floor("The floor is a polished birch stained a rust color. It gives off a pleasant fragrance.")
    jhaW = Wall("These walls look expensive and one-of-a-kind. The lower third is a reddish birch wainscoting " +
                              "and the upper part is solid rock resembling jade or marble.")
    jhaJd = Jha_Jade()
    jha1Ln = Jha_Lion()
    jha2Ln = Jha_Lion()

    ### INITIALIZE GARDENS 
    #-----------------------------THE ROOM---------------------------------
    gar1 = Gar1("Rooftop garden", Id.GAR1)
    gar2 = Room("Rooftop garden", Id.GAR2)
    gar3 = Gar3("Rooftop garden", Id.GAR3)
    gar4 = Gar4("Rooftop garden", Id.GAR4)   
    #-------------------------------ITEMS----------------------------------
    hose = Item(LEATHER_HOSE, 5)
    brknHose = Item("broken hose", 5)
    hoe = Item(HOE, 30, use="The long wood handle is beginning to split along the grain.")
    trowel = Item(TROWEL, 30, use="Cute, and functional to the extent of digging only smaller holes.")
    #-----------------------------FURNITURE-------------------------------- 
    gar13Plntr = Gar13_Planter([sl, mndrkBlb, sl])
    gar1Stat = Gar1_Statue()
    gar2Hs = Gar2_Hose(brknHose)
    gar2Hl = Gar2_Hole(gar2Hs)
    garF = Floor("The floor out here is made of large shale slabs. " +
              "It's a miracle this castle's architecture can hold this area up.")
    gar2Clmn = Gar2_Columns()
    gar2Dm = Gar2_Dome()
    gar3Chst = Gar3_Chest([hoe, trowel, hose, sd])
    gal3Fntn = Gar3_Fountain([garChstKey])
    gar4Plq = Gar4_Plaque()
    gar4Plntr = Gar4_Planter(gar4Plq.getID(), urnsPlt, [urnsPlt, sl, sl])
    gar24Scnc = Gar24_Sconce()

    ### INITIALIZE PARLOR 
    #-----------------------------THE ROOM---------------------------------
    par2 = Par2("Parlor loft", Id.PAR2)
    par1 = Par1("Parlor", Id.PAR1) 
    #-------------------------------ITEMS----------------------------------   
    bttl = BreakableItem(GLASS_BOTTLE, 25)
    enchntdBttl = BreakableItem(ENCHANTED_BOTTLE, 70)
    stlWr = Item(STEEL_WIRE, 5)
    hndDrll = Item(HAND_DRILL, 25)
    athr = Liquid(AETHER_VIAL, 60)
    frSlts = Item(FIRE_SALTS, 70)
    parNt = Note("notice: vials")
    parBkMndrk = Book("tome, 'The Care of Mandragora'", "Par_MandrakeBook")
    parBkEncht = Book("tome, 'Enchanting for the Naive'", "Par_EnchantingBook")
    parNtBttl = Note("'Novice Enchanting: Bottles'")
    parNtShs = Note("'Novice Enchanting: Footwear'")
    parNtWpn = Note("'Expert Enchanting: Weaponry'")
    parNtKey = Note("'Expert Enchanting: Skeleton Keys'")
    parLchNt = Note("note: binding")
    #-----------------------------FURNITURE--------------------------------  
    parLft = Par_Loft()
    par1Orb = Par1_Orb()
    par1F = Floor("It's a sandstone tiled floor, much like that in the west wing. " +
              "The floor here does appear noticeably cleaner and more refined, however.")
    par1FrPlc = Par1_FirePlace(bckt, enchntdBttl)
    par1Dr = Par1_Door(enchntdBttl, Direction.NORTH)
    par1EnchntTbl = Par1_EnchantingTable(enchntdBttl, [bttl, chs1Key, parLchNt])
    par1Strs = Par_Stairs(Direction.UP, Id.PAR2)
    par1Pllrs = Par1_Pillars()
    par1Hrp = Par1_Harp(par1Orb.getID())
    par1Shlf = Wow3_Shelf([hndDrll, athr, parBkEncht, frSlts])
    par1Cshn = Par1_Cushion([aresPlt])
    par2F = Floor("It's a sandstone tiled floor, much like that in the west wing. " +
              "The floor here does appear noticeably cleaner and more refined, however.")
    par2Wndw = Par2_Window()
    par2Strs = Par_Stairs(Direction.DOWN, Id.PAR1)
    par2Bwl = Par2_Bowl()
    par2Frplc = Par2_Fireplace()
    par2Pno = Par2_Piano(par1Orb.getID(), [stlWr])
    par2Shlf = Wow3_Shelf([vial, parNt, parNtShs, parNtWpn, parNtBttl, parBkMndrk, parNtKey, gaeaPlt])

    ### INITIALIZE SECRET STAIRS 
    #-----------------------------THE ROOM---------------------------------
    sst1 = Room("Secret stairwell", Id.SST1)
    sst2 = Room("Small landing", Id.SST2)  
    #-----------------------------FURNITURE--------------------------------  
    sst1Strs = Sst_Stairs(Direction.UP, Id.SST2)
    sst2Strs = Sst_Stairs(Direction.DOWN, Id.SST1)
    sstLndng = Sst_Landing()
    sst1F = Floor("The flooring in here is rudimentary. Just gray weathered planks of wood.")
    sst2F = Floor("The flooring in here is rudimentary. Just gray weathered planks of wood.")
    sstWndw = Sst_Window()
    sst1Dr = Jha_HiddenDoor(Direction.EAST)
    sst2Dr = Sst_Door(Direction.EAST)

    ### INITIALIZE LABORATORY 
    #-----------------------------THE ROOM---------------------------------
    labo = Labo("Laboratory", Id.LABO)
    #-------------------------------ITEMS---------------------------------- 
    rbbrTube = Item(RUBBER_HOSE, 25)
    tstTb = BreakableItem(TEST_TUBE, 25)
    bkr = BreakableItem(BEAKER, 25)
    strkr = Item(STRIKER, 30)
    scale = BreakableItem("scale",  30)
    balance = BreakableItem("balance", 30)
    flrcFlsk = BreakableItem(FLORENCE_FLASK, 25)
    laboBrnrBk = Book("manual, 'Playing With Fire'", "Labo_BurnerManual")
    laboRcp = Note("phase door potion recipe")
    laboIngNt = Note("note: missing ingredients")
    labDstllrNt = Note("note: contraption")
    #-----------------------------FURNITURE--------------------------------  
    iceBrrl = Labo_IceBarrel([flrcFlsk])
    laboRck = Labo_Shelf([vial, laboRcp, tstTb, laboIngNt, vial, tstTb, bkr, tstTb, laboBrnrBk, actn])
    laboGsPipe = Labo_GasPipe()
    cndsr = Labo_Condenser(bkr)
    laboDstllr = Labo_Distiller(laboGsPipe.getID(), cndsr.getID(), tstTb, vial)
    laboDspnsrs = Labo_Dispensers(vial, tstTb)
    laboBrtt = Labo_Burette(vial, tstTb)
    laboStpCck = Labo_StopCock()
    laboF = Floor("It's a black and white checkered tile. A predictable floor for a laboratory. " +
              "A few burn marks taint the floor just at the foot of the counter to the north.", tstTb)
    laboSnk = Labo_Sink(vial, bkr, bckt, wtr)
    laboCntrptn = Labo_Contraption()
    laboTbl = Labo_Table()
    laboDvcs = Labo_Devices()
    laboCntr = Labo_Counter([strkr, labDstllrNt, scale, rbbrTube, balance])

    ### INITIALIZE ATTIC 
    prisCbnt = Pris_Cabinet()
    #-----------------------------THE ROOM---------------------------------
    att1 = Att1("Attic", Id.ATT1, prisCbnt)       
    att2 = Att2("Attic", Id.ATT2)    
    #-------------------------------ITEMS----------------------------------  
    attcDll = Item("doll", 15)
    attcSphn = BreakableItem("sousaphone", 35, use="You can't fit it around your waist.")
    attcAntLmp = BreakableItem("antique lamp", 5)
    attcMrrr = BreakableItem("mirror", 50, use="You're afraid to look in it.")
    attcGlb = BreakableItem("globe", 35)
    attcGChSt = Clothing("green checkered suit", 40, use="Maybe if it were red-plaid, you'd wear it.")
    attcDrss = Clothing("dress", 15, use="You aren't too accustomed to wearing dresses.")
    attcOldRgs = Item("old rags", 0)
    attcTrchCt = Clothing("black trench coat", 15, use="There's no time for dress up right now.")
    attcStPt = Clothing("suit pants", 25, use="You really don't feel like removing your pants right now.")
    #-----------------------------FURNITURE--------------------------------  
    attW = Wall("The gray wood plank walls in here angle up forming a roof.")
    attF = Floor("The flooring in here is rudimentary. Just gray weathered planks of wood with rot in a few areas.")
    att2Dr = Sst_Door(Direction.WEST)
    attCss = Att_Cases([attcTrchCt, attcGChSt, attcDrss, attcOldRgs, attcStPt])
    attBxs = Att_Boxes([attcSphn, attcMrrr, attcGlb, attcDll, attcVln, attcAntLmp])
    attVnts = Att_Vents()
    attClng = Att_Ceiling()
    
    ### INITIALIZE BACK HALL 
    #-----------------------------THE ROOM---------------------------------
    bha1 = Room("Demonic hallway", Id.BHA1)
    bha2 = Bha2("???", Id.BHA2)
    bha3 = Room("Demonic hallway", Id.BHA3)
    #-------------------------------ITEMS----------------------------------   
    tblLg = Weapon("broken table leg", -25)
    orgMttr = Item("organic matter", 10)
    bhaNt = Note("note: plates")
    #-----------------------------FURNITURE--------------------------------  
    bha1Hrzn = Bha1_Horizon()
    bha1Plnt = Bha1_Plant(sl, stnBdy)
    bha1Tbl = Bha1_Table([hrmsPlt])
    bhaW = Wall("The walls are covered in a brown and red vertically " +
              "striped wallpaper with wainscoting on the bottom. The wallpaper " +
              "has torn and peeled at the seams it some areas.")
    bha1F = Floor("The wood-plank floor bends with the hallway. " +
              "The planks bend with it without prying up. Could this all be an illusion?")
    bha2F = Floor("The floor has changed. Most of the wood planks have been removed " +
              "revealing a dirt-like ground below... But it's not dirt.", 
            [wbalsp, wbalch, orgMttr, orgMttr, tblLg, wbalsp])
    bha2W = Wall("The walls are still intact, though much more of the wallpaper has been ripped off.")
    bha2Frm = Bha2_Frame([gal5CbtKey, bhaNt])
    bha3Wndw = Bha3_Window()
    bha3F = Floor("The wood-plank floor bends with the hallway. " +
              "The planks bend with it without prying up. Could this all be an illusion?")


    #####################################################################################     
    ### AREA 5: SUB-LEVELS
    #####################################################################################

    sewDrN = Sew_Door(Direction.NORTH)
    sewDrS = Sew_Door(Direction.SOUTH)
    sewDrE = Sew_Door(Direction.EAST)
    sewDrW = Sew_Door(Direction.WEST)   
    dngnW = Wall("The walls are rough gray stone brick, covered in moss and wet to the touch from the humid air.")
    dungMonst = DungeonMonsterFurniture()
    
    oar = Item(WOODEN_OAR, 10, use="You will need to be in a boat to use this.")
    
    ### INITIALIZE TUNNELS
    pipePc = Weapon(PIECE_OF_PIPE, 15)
    sew1Rvr = Sew1_River(pipePc, wtrBckt)
    sew4Pp = Sew4_Pipe(sew1Rvr.getID(), pipePc) # RESETABLE
    #-----------------------------THE ROOMS--------------------------------
    sew0 = Dungeon_Tunnel("Tunnel's end", Id.SEW0)
    sew1 = Sew1("Underground tunnel", Id.SEW1)
    sew2 = Sew2("Underground tunnel", Id.SEW2)
    sew3 = Dungeon_Tunnel("Underground tunnel", Id.SEW3)
    sew4 = Sew4("Underground tunnel", Id.SEW4, sew4Pp.getID())
    sew5 = Sew5("Tunnel's end", Id.SEW5)
    #-----------------------------FURNITURE-------------------------------- 
    sewF = Dungeon_Floor()
    sewTnnl = Sew_Tunnel()
    sewRvr = Sew2345_River(sew1Rvr.getID(), wtrBckt)
    sewMss = Sew_Moss()
    sew0Trch = Torch_Holder(torch)
    sew0Strs = Sew0_Stairs()
    sew15Gt = Sew15_Gate()
    sew1Trch = Torch_Holder(torch)
    sew2Vlvs = Sew2_Valves() # RESETABLE
    sew2Trch = Torch_Holder(torch)
    sew2BrdgW = Sew_Bridge(Direction.WEST)
    sew2Pp = Sew235_Pipe(2)
    sew3Trch = Torch_Holder(torch)
    sew3BrdgN = Sew_Bridge(Direction.NORTH)
    sew3BrdgE = Sew_Bridge(Direction.EAST)
    sew3Pp = Sew235_Pipe(3)
    sew4Trch = Torch_Holder(torch)
    sew5Trch = Torch_Holder(torch)
    sew5BrdgE = Sew_Bridge(Direction.EAST)
    sew5Pp = Sew235_Pipe(5)
    sew5Vlv = Sew5_Valve(sew2Vlvs.getID(), sew4Pp.getID())

    ### INITIALIZE ANCIENT CISTERN
    #-----------------------------THE ROOMS--------------------------------
    cis1 = Cis1("Fetid cistern", Id.CIS1) # RESETABLE
    cis2 = Cis2("Fetid cistern", Id.CIS2)
    cis3 = Cis3("Fetid cistern", Id.CIS3)
    cis4 = Cis4("Fetid cistern", Id.CIS4) 
    cis5 = Cis5("Secret platform", Id.CIS5)
    #-------------------------------ITEMS----------------------------------  
    oarTl = Item("broken wood handle", 5, thresh=3, forms=oar)
    pdLck = Item("broken padlock", -10)
    #-----------------------------FURNITURE-------------------------------- 
    cis2Bt = Cis2_Boat([oarTl])
    cis1Trch = Torch_Holder(torch)
    cis3Trch = Torch_Holder(torch)
    cis4Trch = Torch_Holder(torch)
    cis5F = Floor("The floor here is the same as the rest of the cistern.", [pdLck])
    cis5Fgr = Cis5_FigureNPC()
    cisF = Dungeon_Floor()
    cisWtr = Cis_Water(wtrBckt)
    cisClmns = Cis_Columns()
    cisDrknss = Cis_Darkness()

    ### INITIALIZE TORTURE CHAMBER
    #-----------------------------THE ROOM---------------------------------
    torc = Torc("Torture chamber", Id.TORC)
    #------------------------------ITEMS-----------------------------------
    thmScrws = Item("odd clamp", 35)
    #-----------------------------FURNITURE-------------------------------- 
    torcF = Dungeon_Floor()
    torcTrchs = Torch_Holder(torch)
    torcSwhrses = Torc_Sawhorses(torc) # RESETABLE
    torcRck = Torc_Rack([thmScrws])
    torcCgs = Torc_Cages([ou62Key])
    torcWhl = Torc_Wheel()
    torcWd = Torc_Wood()
    torcTls = Torc_Tools()
    torcScythF = Torc_ScytheFurniture() # RESETABLE

    ### INITIALIZE CRYPT
    #-----------------------------THE ROOM---------------------------------
    cry2 = Cry2("Crypt", Id.CRY2)
    cry1 = Room("Crypt", Id.CRY1)
    #-------------------------------ITEMS----------------------------------      
    drdFlwr = Item("dried flower", 10)
    ncklc = Clothing("silver necklace", 170, use="You put it around your neck. The heavy coldness fills you with feelings of luxury.")
    brnzCn = Item("bronze coin", 50)
    knife = Weapon("knife", 20)
    #-----------------------------FURNITURE-------------------------------- 
    cryF = Dungeon_Floor()
    cryDummy = Cry_Dummy()
    cryDrwrs = Cry_Drawers()
    cry1Crvng = Cry1_Carving()
    cryLghts = Cry_Lights()
    cry2Engrvng = Cry2_Engraving()
    cry2Altr = Cry2_Altar([drdFlwr, jetSkull, knife, ncklc, brnzCn])
    cry1Stat = Cry1_Statue(torcScythF) # RESETABLE
    cry2Psswd = Cry2_Password(cry1Stat.getID())

    ### INITIALIZE CELL
    #-----------------------------THE ROOM---------------------------------
    intr = Intr("Noisy chamber", Id.INTR)      
    #-----------------------------ITEMS-------------------------------- 
    mtlBt = Item("metal bit", 0)
    scrw = Item("screw", 0)
    sgyWdChnk = Item("soggy wood chunk", 0)
    #-----------------------------FURNITURE-------------------------------- 
    intrF = Dungeon_Floor([sgyWdChnk, scrw, scrw, mtlBt]) 
    intrGrt = Intr_Grate() # RESETABLE
    intrTrch = Intr_Torch(torch) # RESETABLE
    intrWhl = Intr_Wheel()
    intrGrs = Intr_Gears()
    intrDr = Intr_Door()
    intrWtr = Intr_Water() # RESETABLE

    ### INITIALIZE SUB-TUNNELS
    #-----------------------------THE ROOMS--------------------------------
    esc1 = Esc("Small tunnel", Id.ESC1)
    esc2 = Esc("Small tunnel", Id.ESC2)
    esc3 = Esc("Small tunnel", Id.ESC3)
    esc4 = Esc("Small tunnel", Id.ESC4)
    esc5 = Esc("Small tunnel", Id.ESC5)
    esc6 = Esc("Small tunnel", Id.ESC6)       
    #-----------------------------FURNITURE-------------------------------- 
    esc1Lddr = Esc1_Ladder() # RESETABLE
    esc6Grt = Esc6_Grate() # RESETABLE
    esc6Lddr = Esc6_Ladder(esc6Grt.getID()) # RESETABLE

    ### INITIALIZE CATACOMBS ACCESS
    #-----------------------------THE ROOM---------------------------------
    cas1 = Cas1("Catacombs access", Id.CAS1)      
    #-----------------------------FURNITURE-------------------------------- 
    casW = Wall("The walls are large granite blocks reflecting a flickering bluish hue from the flame.")
    casStrs = Cas_Stairs(Direction.DOWN, Id.CS35)
    casF = Floor("The floor is comprised of many large blocks, illuminated blue from the fire.")

    ### INITIALIZE OUBLIETTE
    #-----------------------------THE ROOM---------------------------------
    oub1 = Room("Oubliette", Id.OUB1)       
    #-----------------------------FURNITURE--------------------------------  
    oub1F = Dungeon_Floor()
    oub1Pt = Oub1_Pit()

    ### INITIALIZE PRISON
    #-----------------------------THE ROOM---------------------------------
    pris = Pris("Prison", Id.PRIS)
    #-------------------------------ITEMS----------------------------------   
    oarHd = Item("broken wood paddle", 5, thresh=3, forms=oar)
    #-----------------------------FURNITURE--------------------------------  
    prisClls = Pris_Cells()
    prisF = Dungeon_Floor()
    prisCndlbrs = Pris_Candelabra([cndl, cndl])
    prisTbl = Pris_Table([oarHd])
    prisGts = Pris_Gates()
    prisFgr = Pris_Ghost()

    #KAMPE'S QUARTERS
    #-----------------------------THE ROOM---------------------------------
    dkch = Room("Kampe's quarters", Id.DKCH)
    #-------------------------------ITEMS---------------------------------- 
    tape = Item("duck tape", 15, thresh=3, forms=oar)
    whip = Weapon("leather whip", 25)
    lthrHat = Clothing("shiny leather hat", 25, use="You put it on.")
    shoeBx = Kampe_Box([tape, whip, lthrHat, watch])
    lngChn = Weapon("chain", 35)
    dkchNt2 = Note("illegible note")
    #-----------------------------FURNITURE-------------------------------- 
    dkchF = Dungeon_Floor()
    dkchBd = Dkch_Bed([lngChn, shoeBx])
    dkchAxl = Dkch_Axle()
    dkchDsk = Dkch_Desk([dkchNt2])
    dkchClng = Dkch_Ceiling()

    ### INITIALIZE STRANGE POOL
    #-----------------------------THE ROOM---------------------------------
    sewp = Sewp("Pool of water", Id.SEWP, prisCbnt.getID(), 
            (intrWtr.getID(), intrGrt.getID(), intrTrch.getID(), sew2Vlvs.getID(), torcSwhrses.getID(), 
                torcScythF.getID(), cry1Stat.getID(), esc6Grt.getID(), sew4Pp.getID(), esc6Lddr.getID()), 
            (Id.INTR, Id.INTR, Id.INTR, Id.SEW2, Id.TORC, Id.TORC, Id.CRY1, Id.ESC6, Id.SEW4, Id.ESC6)
    )        
    #-----------------------------FURNITURE--------------------------------  
    sewpCl = Sewp_Ceiling()
    sewpGrt = Sewp_Grate()
    sewpWtr = Sewp_Water(wtrBckt)
    sewpTrch = Torch_Holder(torch)
    sewpF = Dungeon_Floor()
    sewpTnnl = Sewp_Tunnel()

    ### INITIALIZE ANCIENT ARCHIVES
    #-----------------------------THE ROOM---------------------------------
    aarc = Aarc("Ruined archives", Id.AARC)
    #-------------------------------ITEMS----------------------------------
    algBk = Item("algae covered book", -30, use="This is completely unreadable.")
    rndBk = Item("ruined book", -30, use="Whatever knowledge this book held is now lost.")
    stnBlck = BreakableItem(STONE_BLOCK, 10)
    slmyAlg = Item("slimy algae", -35)
    aarcNt = Note("note: Factum")
    #-----------------------------FURNITURE--------------------------------  
    aarcAlg = Aarc_Algae(slmyAlg)
    aarcBks = Aarc_Books(rndBk, [algBk, slmyAlg, rndBk])
    aarcChndlr = Aarc_Chandelier()
    aarcDsk = Aarc_Desk([wbalch, archKey, aarcNt, rndBk])
    aarcF = Aarc_Floor([algBk, wbalch, stnBlck, algBk, slmyAlg, algBk, stnBlck])
    aarcW = Aarc_Wall()
    aarcWd = Aarc_Wood(wbalch)
    aarcShlvs = Aarc_Shelves([slmyAlg, wbalch, wbalch])

    ### INITIALIZE CATACOMBS 
    # ROOMS --------------------------------------------------------------
    cs35 = Room("Catacombs entrance", Id.CS35)
    ou62 = Room("Oubliette", Id.OU62)
    my18 = My18("Sandstone chamber", Id.MY18)
    tm16 = Tomb(Id.TM16)
    tm66 = Tomb(Id.TM66)
    tm32 = Tomb(Id.TM32)
    an55 = An55("Ancient tomb", Id.AN55)
    an65 = An65("Ancient tomb", Id.AN65)
    
    c = Ceiling(desc="It's a dripping, rocky ceiling.")
    w = Wall("The walls are wet and rocky.")

    # Instantiate all catacomb rooms --------------------------------
    ct11 = Catacomb(Id.CT11, w, c)
    ct12 = Catacomb(Id.CT12, w, c)
    ct13 = Catacomb(Id.CT13, w, c)
    ct14 = Catacomb(Id.CT14, w, c)
    ct15 = Catacomb(Id.CT15, w, c)
    ct17 = Catacomb(Id.CT17, w, c)
    ct21 = Catacomb(Id.CT21, w, c)
    ct22 = Catacomb(Id.CT22, w, c)
    ct23 = Catacomb(Id.CT23, w, c)
    ct24 = Catacomb(Id.CT24, w, c)
    ct25 = Catacomb(Id.CT25, w, c)
    ct26 = Catacomb(Id.CT26, w, c)
    ct27 = Catacomb(Id.CT27, w, c)
    ct28 = Catacomb(Id.CT28, w, c)
    ct31 = Catacomb(Id.CT31, w, c)
    ct33 = Catacomb(Id.CT33, w, c)
    ct34 = Catacomb(Id.CT34, w, c)
    ct36 = Catacomb(Id.CT36, w, c)
    ct37 = Catacomb(Id.CT37, w, c)
    ct38 = Catacomb(Id.CT38, w, c)
    ct41 = Catacomb(Id.CT41, w, c)
    ct42 = Catacomb(Id.CT42, w, c)
    ct43 = Catacomb(Id.CT43, w, c)
    ct44 = Catacomb(Id.CT44, w, c)
    ct45 = Catacomb(Id.CT45, w, c)
    ct46 = Catacomb(Id.CT46, w, c)
    ct47 = Catacomb(Id.CT47, w, c)
    ct48 = Catacomb(Id.CT48, w, c)
    ct51 = Catacomb(Id.CT51, w, c)
    ct52 = Catacomb(Id.CT52, w, c)
    ct53 = Catacomb(Id.CT53, w, c)
    ct54 = Catacomb(Id.CT54, w, c)
    ct56 = Catacomb(Id.CT56, w, c)
    ct57 = Catacomb(Id.CT57, w, c)
    ct58 = Catacomb(Id.CT58, w, c)
    ct61 = Catacomb(Id.CT61, w, c)
    ct63 = Catacomb(Id.CT63, w, c)
    ct64 = Catacomb(Id.CT64, w, c)
    ct67 = Catacomb(Id.CT67, w, c)
    ct68 = Catacomb(Id.CT68, w, c)

    #-------------------------------ITEMS----------------------------------
    coin = Item("stone coins", 35, use="Where do you expect to spend these?")
    nckLc = Clothing("beaded necklace", 40, use="You fit the old ceremonial necklace over your head.")
    jwl = BreakableItem(IRIDESCENT_JEWEL, 250)
    med1 = BreakableItem(KEY_OF_ANCESTRY, 35)
    med2 = BreakableItem(KEY_OF_INTELLECT, 35)
    med3 = BreakableItem(KEY_OF_CONTINUITY, 35)
    
    def getRandomJewelLocation():
        room = random.choice((ct11, ct12, ct13, ct14, ct15, ct17, ct21, ct22, ct23, ct24, ct25, 
            ct26, ct27, ct28, ct31, ct33, ct34, ct36, ct37, ct38, ct41, ct42, ct43, ct44, ct45, 
            ct46, ct47, ct48, ct51, ct52, ct53, ct54, ct56, ct57, ct58, ct61, ct63, ct64, ct67, 
            ct68)) # get random room

        room.getFurnishings()[0].getInv().add(jwl)  # add the jewel to that room.
        y = abs(room.getCoords()[1] - 7)            # get y-coord of that room.
        return (str(room.getCoords()[2]) + ", " + str(y) + ", -2") # make the message that appears on the casket note.

    tmbNt = TombNote("torn parchment", getRandomJewelLocation())
    #-----------------------------FURNITURE-------------------------------- 
    catDrN = Ct_Door(Direction.NORTH)
    catDrS = Ct_Door(Direction.SOUTH)
    catDrE = Ct_Door(Direction.EAST)
    catDrW = Ct_Door(Direction.WEST)

    tmb1Cskt = Tmb1_Casket([med1])
    tm1Vs = Tmb_Vases([coin])
    tm1Bwl = Tmb1_Bowl()
    tm1Effgy = Tmb1_Effigy()
    tmb2Cskt = Tmb2_Casket([med2])
    tm2Vs = Tmb_Vases([nckLc, coin, ring])
    tm2Orb = Tmb2_Light()
    tmb3Cskt = Tmb3_Casket([med3])
    tm3Vs = Tmb_Vases([coin, nckLc])
    tm3Tpstry = Tmb3_Tapestry()
    tm3Cndl = Tmb3_Cndl()
    tm1F = Floor("It's a damp dirt floor.")
    tm2F = Floor("It's a damp dirt floor.")
    tm3F = Floor("It's a damp dirt floor.")
    catW = Wall("The walls are wet and rocky.")
    
    oubStrw = Ou62_Straw()
    oubSpk = Ou62_Spike()
    oubSkltn = Ou62_Skeleton([gldKnf])
    oub2F = Dungeon_Floor([closStrw, closStrw, closStrw])
    
    antF = Floor("The floor in here is dusty sandstone.")
    antNPC = Ant_Zombie(antF, cryDrwrs.DRAWER_NUM)
    antCskt = Ant_Casket([tmbNt])
    antW = Wall("They are carved sandstone.")
    antCskts = Ant_Caskets()
    ant1Trch = Torch_Holder(torch)
    ant2Trch = Torch_Holder(torch)
    antClng = Ant_Ceiling()
    
    my18F = Floor("The floor is brick with a round seam circling around the central pedestal.")
    my18Pdstl = My18_Pedestal()
    my18Clng = My18_Ceiling()
    
    cs35Dr = Cs35_Door(Direction.WEST)
    ct34Dr = Cs35_Door(Direction.EAST)
    ct34.removeFurniture(ct34.getFurnishings()[0].getID()) # Removes old door 
    cs35F = Floor("The floor is comprised of many large blocks, illuminated blue from the fire.")
    cs35Trchs = Cs35_Torches()
    cs35Stat = Cs35_Statue()
    cs35Strs = Cas_Stairs(Direction.UP, Id.CAS1)

    ### INITIALIZE CAVES 
    #-----------------------------THE ROOMS--------------------------------
    cw = Wall("The wall is damp, plain rock.")
    cc = Ceiling("It's a dripping, rocky ceiling.")
    cv34 = CV34("Ancient well", Id.CV34, cw, cc)
    ms65 = Deep_Chamber("aykl xvldml fwe", Id.MS65)
    ms66 = Deep_Chamber("d5 rl x:!e ifxJ", Id.MS66)

    # Instantiate all caves ------------------------------------
    cv18 = Cave(Id.CV18, cw, cc)
    cv11 = Cave(Id.CV11, cw, cc)
    cv12 = Cave(Id.CV12, cw, cc)
    cv13 = Cave(Id.CV13, cw, cc)
    cv14 = Cave(Id.CV14, cw, cc)
    cv15 = Cave(Id.CV15, cw, cc)
    cv16 = Cave(Id.CV16, cw, cc) 
    cv17 = Cave(Id.CV17, cw, cc)
    cv21 = Cave(Id.CV21, cw, cc) 
    cv22 = Cave(Id.CV22, cw, cc)
    cv23 = Cave(Id.CV23, cw, cc) 
    cv24 = Cave(Id.CV24, cw, cc)
    cv25 = Cave(Id.CV25, cw, cc) 
    cv26 = Cave(Id.CV26, cw, cc)
    cv27 = Cave(Id.CV27, cw, cc) 
    cv28 = Cave(Id.CV28, cw, cc)
    cv31 = Cave(Id.CV31, cw, cc) 
    cv32 = Cave(Id.CV32, cw, cc)
    cv33 = Cave(Id.CV33, cw, cc) 
    cv35 = Cave(Id.CV35, cw, cc)
    cv36 = Cave(Id.CV36, cw, cc) 
    cv37 = Cave(Id.CV37, cw, cc)
    cv38 = Cave(Id.CV38, cw, cc) 
    cv41 = Cave(Id.CV41, cw, cc)
    cv42 = Cave(Id.CV42, cw, cc) 
    cv43 = Cave(Id.CV43, cw, cc)
    cv44 = Cave(Id.CV44, cw, cc) 
    cv45 = Cave(Id.CV45, cw, cc)
    cv46 = Cave(Id.CV46, cw, cc) 
    cv47 = Cave(Id.CV47, cw, cc)
    cv48 = Cave(Id.CV48, cw, cc) 
    cv51 = Cave(Id.CV51, cw, cc)
    cv52 = Cave(Id.CV52, cw, cc) 
    cv53 = Cave(Id.CV53, cw, cc)
    cv54 = Cave(Id.CV54, cw, cc) 
    cv55 = Cave(Id.CV55, cw, cc)
    cv56 = Cave(Id.CV56, cw, cc) 
    cv57 = Cave(Id.CV57, cw, cc)
    cv58 = Cave(Id.CV58, cw, cc) 
    cv61 = Cave(Id.CV61, cw, cc)
    cv62 = Cave(Id.CV62, cw, cc) 
    cv63 = Cave(Id.CV63, cw, cc)
    cv67 = Cave(Id.CV67, cw, cc) 
    cv68 = Cave(Id.CV68, cw, cc)
    cv64 = Cave(Id.CV64, cw, cc)
    #-----------------------------FURNITURE-------------------------------- 
    cv18Strs = My18_Stairs(Direction.UP, Id.MY18)
    omnDr = OminousDoor(Direction.EAST)
    dmmyFurniture = Dummy_Furniture()
    factum = FactumDummy(factumPhy)
    cvWell = Cv_Well()

    #####################################################################################     
    ### AREA 6 VAULT
    #####################################################################################

    ### INITIALIZE CHAPEL STAIRS 
    #-----------------------------THE ROOM---------------------------------
    chs1 = Room("Chapel stairwell", Id.CHS1)  
    chs3 = Chs3("Top landing", Id.CHS3)  
    #-----------------------------FURNITURE-------------------------------- 
    chsWndws = Chs_Windows("windows")
    chsW = Wall("The walls are clean, paneled in white and orange with gold leaf accents.")
    chs1Strs = Chs1_Stairs(Direction.UP, Id.CHS3)
    chs1F = Floor("The dark red carpet covers the whole floor. It's a bit dusty from neglect.")
    chs1Stat = Chs1_Statue()
    chs3Strs = Chs1_Stairs(Direction.DOWN, Id.CHS1)
    chs3F = Floor("The dark red carpet covers the whole floor. It's a bit dusty from neglect.")

    ### INITIALIZE CHAPEL 
    #-----------------------------THE ROOM---------------------------------
    cha1 = Room("Nave", Id.CHA1)
    cha2 = Room("Chancel", Id.CHA2)
    #-------------------------------ITEMS---------------------------------- 
    chaNt = Note("malevolent note")
    #-----------------------------FURNITURE-------------------------------- 
    chaF = Floor("Faded, dusty boards line the length of the floor from north to south.")
    chaW = Wall("The walls are mostly carved wood paneling. " +
              "Several religious scenes are painted at fixed distances along the wall.")
    chaPws = Cha_Pews()
    chaHz = Cha_Haze()
    chaCrpt = Cha_Carpet()
    chaWndws = Cha_Windows()
    chaClng = Cha_Ceiling()
    cha1Cylx = Cha1_Cylix()
    cha1Wtr = Cha1_Water(hlyWtr)
    cha1Cndlbr = Cha1_Candelabra([cndl])
    cha2Alt = Cha2_Altar([gldUrn, chaNt])

    ### INITIALIZE VAULT  
    vau1Tbl = Vau1_Table([vauChlPhy, bal1Key])
    #-----------------------------THE ROOM---------------------------------
    vau1 = Vau1("Vault", Id.VAU1, vau1Tbl)
    vau2 = Vau2("Vault", Id.VAU2, vau1Tbl)
    vaue = Room("Curious wall", Id.VAUE)
    #-------------------------------ITEMS---------------------------------- 
    grl = Item("grail", 300)
    cns = Item("leather coin bag", 300)
    crwn = Clothing("crown", 300, use="You position the crown on your head. You've never felt so wealthy.")
    brclt = Clothing("bracelet", 300, "You put the bracelet on your wrist.")
    jdStat = BreakableItem("jade statue", 300)
    #-----------------------------FURNITURE-------------------------------- 
    vau2Chsts = Vau_Chsts([cns, dmnd, jdStat])
    vauF = Floor("The floors are sandstone blocks and covered in treasure.", [brclt, grl, crwn])
    vauBwls = Vau_Bowls()
    vauClng = Vau_Ceiling()
    vaueF = Floor("The walls here are sandstone blocks, much like those in the west wing, but seemingly older.")
    vauW = Wall("The walls here are sandstone blocks, much like those in the west wing, but seemingly older.")
    vaueBttns = Vaue_Door()


    #####################################################################################     
    ### AREA 7: TOWER
    #####################################################################################

    ### INITIALIZE BLACK STAIRCASE
    #-----------------------------THE ROOM---------------------------------
    bls1 = Room("Atrium", Id.BLS1)
    bls2 = Bls2("Second-floor atrium", Id.BLS2) 
    #-----------------------------FURNITURE-------------------------------- 
    blsWndw = Bls_Windows()
    blsBlcny = Bls_Balcony()
    bls1Stat = Bls1_Statue()
    bls1Dr = AtriumDoor(Direction.EAST)
    bls1Strs = Bls_Staircase(Direction.UP, Id.BLS2)
    bls1_Plnts = Bls1_Plants(sl, onyxFrag3)
    bls1F = Floor("The floor is a gray mosaic formed from many tiny pieces of glossy ceramic.")
    bls2Strs = Bls_Staircase(Direction.DOWN, Id.BLS1)
    bls2F = Floor("The floor is iron lattice.")

    ### INITIALIZE TOWER
    tow1Pdstl = Tow1_Pedestal(towScptrPhy)
    #-----------------------------THE ROOM---------------------------------
    tow1 = Tow1("Tower", Id.TOW1, tow1Pdstl)
    tow2 = Tow2("Upper-tower", Id.TOW2)
    #-----------------------------FURNITURE-------------------------------- 
    towWndw = Tow_Windows()
    towBlcny = Tow_Balcony()
    towSphr = Tow_Sphere()
    tow1F = Floor("The floor is checkered white and blue, and very clean.")
    tow1Dr = Foy4_Door(Direction.NORTH)
    tow1BlckDr = AtriumDoor(Direction.WEST)
    tow2DrN = Tow2_NorthDoor(Direction.NORTH)
    tow2F = Floor("An iron cage-like material forms the floor and railings of the circular balcony.")

    ### INITIALIZE LICH'S QUARTERS
    #-----------------------------THE ROOM---------------------------------
    lqu1 = Lqu1("Lich's quarters", Id.LQU1)
    lqu2 = Room("Lich's bed", Id.LQU2)
    #-------------------------------ITEMS----------------------------------
    # Items for the dampening staff are at higher up in this method.
    lchClths = Clothing("lich clothes", 150, use="You really don't feel comfortable putting these on.")
    #-----------------------------FURNITURE-------------------------------- 
    lquF = Floor("The floor around the carpet is hard and cold stone.")
    lquW = Wall("The walls are clean smooth stone and decorated with faux columns.")
    lqu1Mrrr = Lqu1_Mirror()
    lqu1Cbnt = Lqu1_Cabinet([stffHndl])
    lqu1_Bd = Lqu1_Bed()
    lqu_Crpt = Lqu_Carpet()
    lqu1Lvr = Lqu2_Lever(cou3Gt.getID())
    lqu2Bd = Lqu2_Bed([lchClths])

    ### INITIALIZE TOP BALCONY
    #-----------------------------THE ROOM---------------------------------
    tbal = Tbal("High balcony", Id.TBAL)
    #-----------------------------FURNITURE--------------------------------
    tbalStrs = Tbal_Stairs()
    tbalPllr = Tbal_Pillar()
    tbalDrS = Tow2_NorthDoor(Direction.SOUTH)
    tbalF = Floor("The floor is a gray mosaic formed from many tiny pieces of glossy ceramic.")

    ### INITIALIZE SOUL CHAMBER
    #-----------------------------THE ROOM---------------------------------
    soul = Room("Soul chamber", Id.SOUL)
    #-----------------------------FURNITURE-------------------------------- 
    soulPl = Soul_Pool(towSphr.getID(), (lqu1, tow1, tow2))
    soulStat = Soul_Statues()
    soulF = Floor("It's a light-gray tiled floor.")
    soulWndw = Soul_Window()

    ### INITIALIZE END ROOM
    endg = Endg("", Id.ENDG)

    ### INITIALIZE HADES
    #-----------------------------THE ROOM---------------------------------
    hads = Hades("Entrance to Hades", Id.HADS)
    #-------------------------------ITEMS----------------------------------
    leg = Item("mangled leg", -1000)
    torso = Item("mangled torso", -1000)
    hand = Item("mangled hand", -1000)
    arm = Item("mangled arm", -1000)
    #-----------------------------FURNITURE-------------------------------- 
    hadsCrpses = Hads_Corpses([leg, torso, hand, leg, typhos ,arm, torso, hand])
    hadsSprts = Hads_Spirits()
    hadsVcs = Hads_Voices()
    hadsGtwy = Hads_Gateway()
    hadsF = Floor("The scorched brimstone burns beneath your feet.")
    hadsW = Wall("High rock walls hopelessly bar you from escape.")

    #####################################################################################
    ### PUT FURNITURE IN ROOMS
    #####################################################################################

    #AREA 1: CASTLE FRONT
    for1.addFurniture(forTrs, rotuSky, forThckt, forFrst, cou4Trl, forF)
    for2.addFurniture(forTrs, for2Elk, rotuSky, forThckt, forFrst, cou4Trl, forF)
    for3.addFurniture(forTrs, rotuSky, forThckt, forFrst, cou4Trl, forF)
    for4.addFurniture(forTrs, rotuSky, forThckt, forFrst, cou4Trl, forF)
    foy1.addFurniture(foyFrntDr, genDoor, foy1Gt, foy1Armr, foyF, foyW, foy1Chnd, eastDoor, foy1Tbl, foy1Crpt, foy1Strs, clng)
    foy2.addFurniture(foy2Gt, foy2Stat, foy2Alc, foyF, foyW, foy2Strcs, clng)
    foy3.addFurniture(foy3Strs, westDoor, foyW, foy3F, foy34Crpt, clng)
    foy4.addFurniture(foy4Strs, foyW, foy4F, foy34Crpt, foy4Dr, clng)
    vest.addFurniture(vesFire, vesBtn, vesWin, vesDsk, vesEtbl, vesCase, vesTpstr, vesChr, vesF, vesDr, wallEx, vesOrb)
    foyb.addFurniture(bbaF, wallEx, bbaClmns, bbaRlng, bbaVllg, clng, bbaBnch, bbaScnc, bbaClff, bbaShrln, bbaSea, bba1Gt, wantBttn)
    foyc.addFurniture(bbaF, wallEx, bbaClmns, bbaRlng, bbaVllg, clng, bbaScnc, bbaClff, bbaShrln, bbaSea, bba2Dr)
    cou1.addFurniture(couStps, cou1Bnch, cou1Thrns, couW, cou1F, couCstl, couRvns)
    cou2.addFurniture(couW, cou2F, cou2Bshs, cou2Fntn, couCstl, coutWlkwy, couRvns)
    cou5.addFurniture(couW, cou5F, cou2Bshs, cou5Fntn, couCstl, cou5Sprc, coutWlkwy, couRvns)
    cou6.addFurniture(couStps, cou1Bnch, cou1Thrns, couW, cou6F, cou6Stat, couCstl, cou6Ghst, couRvns)
    cou3.addFurniture(cou3F, couW, cou3Stps, cou3Gt, cou3Ivy, cou3Frk, couCstl, couRvns)
    cou4.addFurniture(cou3F, couW, cou4Gt, cou4Frst, cou4Mlbx, cou4Trl, couCstl, couRvns)
    cou7.addFurniture(couCstl, entrF, entrDr, entrStats, entrClmns, bbaRlng, entrRf, entrStps, entrBlcny, couRvns)
    cou8.addFurniture(cou8Nest, cou8Sprc, couW)
    foyw.addFurniture(genDoor, wantStat, wantTrchs, wantLvr, wantPllrs, wWW, wantF, wantRmp, wantDr, wantGt, wantBttn, clng)

    #AREA 2: WEST WING    
    rotu.addFurniture(genDoor, rotuFntn, rotuW, rotuF, rotuPlnts, rotuHl, rotuStat, rotuScnc, rotuFrms, rotuSky, rotuRock, clng)
    cel1.addFurniture(cel1Lddr, celLntrn, wallEx, celPp, celF, clng)
    cel2.addFurniture(cel2Vlv, celLntrn, cel2Shft, wallEx, celPp, celF, cel2Clng)
    cel3.addFurniture(cel3Vlv, celLntrn, cel3Crt, wallEx, celPp, celF, nrthCelClng)
    cel4.addFurniture(celLntrn, cel4Wrkbnch, cel4Bd, wallEx, celPp, cel4Coal, celF, nrthCelClng)
    cel5.addFurniture(cel5Grt, cel5Lck, celLntrn, wallEx, celPp, celF, cel5Frnc, nrthCelClng)
    cel6.addFurniture(cel6Vlv, cel6Lddr, cel6Pltfrm, cel6Clmns, cel6Pp, cisDrknss, cel6Lghts, clng)
    look.addFurniture(lookDr, lookLghths, lookClff, lookRlng, lookF, wallEx, eastDoor, iha1Lvr, bbaSea)
    iha1.addFurniture(northDoor, wWW, ihaF, iha1Armr, iha1Bwl, ihaWndw, iha1Lvr, clng)
    iha2.addFurniture(southDoor, wWW, ihaF, iha2Armr, iha2Bwl, ihaWndw, clng)
    wow1.addFurniture(genDoor, wWW, westDoor, wow1NDr, wow1Crt, wow1F, wowWndw, wowHrth, wow1Shlvs, clng)
    wow2.addFurniture(genDoor, wow2Blcny, wow2Armr, wow2F, wow2Dr, northDoor, wow2Hole, wowWndw, wowHrth, wow2Strcs, clng)
    wbal.addFurniture(wallEx, eastDoor, lookLghths, lookClff, lookRlng, wbalF, wbalBcn, wbalFrst, bbaSea)
    squa.addFurniture(wWW, squaF, squaBd, squaDsk, squaWndw, lookLghths, lookClff, bbaSea, squaWrdrb, squaCndl, squaDr, clng)
    wow3.addFurniture(genDoor, wWW, wow3Shlf, wow3F, wow3Dr, bbaRlng, wow3NDr, clng)
    sha1.addFurniture(wWW, shaF, sha1Trch, sha1Dr, sha1SDr, clng)
    sha2.addFurniture(wWW, sha2Cbnt, shaF, sha2Dr, sha2Trch, clng)
    clos.addFurniture(closW, closF, closShlf, closStl, closBrrl, closWrkbnch, closLddr, closScks, closClng, closSkltn, closDr)  
    cous.addFurniture(searFssr, searDr, searLddr, searAsh, searSkltn, searF, searAsh, closW, clng, searWood)
    shar.addFurniture(wWW, rquaF, rquaBd, rquaTbl, rquaMttrss, rquaDrssr, squaWndw, rquaWmn, lookLghths, lookClff, bbaSea, rquaPnl, clng, rquaClths)
    stud.addFurniture(wWW, studF, studPrtrt, studFire, studDsk, vesChr, studCch, studBkCs, studCrpt, southDoor, iha1Lvr, clng)

    #AREA 3: EAST WING     
    gal1.addFurniture(gal1Dr, gal1F, gal1W, gal1Drgn, gal1KtnFurn, gal1Pntng, gal1Pntng2, gal1Pntng3, gal1Armr, gal1Scr, 
            gal1Scrn, gal1Pntngs, gal1Lghts, gal1Sclptrs, gal1Hrth, clng)
    gal2.addFurniture(genDoor, gal2Stat, gal2Strcs, gal2Mchn, gal2F, gal2W, galBalc, 
            gal1Lghts, rotuSky, galDm, gal2Clmns, mhaSDr, eastDoor)
    gal3.addFurniture(gal3Ttm, gal3Peg, gal3Hl, gal3Sgmnt, gal3Htch, gal3Lddr, 
            gal3Rp, gal3Swtch, gal3InstFurn, gal3Msk, gal3Msk2, gal3Msk3, gal3Msks, 
            gal3Hrth, gal3F, gal3W, gal3Art, gal3Art2, gal3Art3, gal3Arts, clng)
    gal4.addFurniture(gal4Strcs, galBalc, rotuSky, gal2W, galDm, gal4Lck,  gal2Clmns, gal4Dr, gal4Glss, gal4Cs, gal4Lft, gal4Rdo, gal4F, gal4Crpt, gal4Lvr)
    gal6.addFurniture(gal6Cnn, gal6Lddr, gal6Mchn, gal6Hlmt, gal6Bttn, gal6App, gal6F, gal6W, gal6Htch, gal6Tech, gal6Elec, gal6Tbl, clng)
    gal7.addFurniture(wWW)
    mha1.addFurniture(genDoor, mhaChndlr, mhaChr, mha1Plnt, mhaF, mhaW, mhaNWndw1, mhaNDr, mhaNChaDr, clng)
    mha2.addFurniture(mhaChndlr, mhaChr, mha2Plnt, mhaF, mhaW, mhaNWndw2, mhaMDr, mhaRStat, mhaLStat, mhaStats, clng)
    mha3.addFurniture(genDoor, mhaChndlr, mhaChr, mha3Plnt, mhaF, mhaW, mhaSWndw, mha3KitcDr, mhaSDr, clng)
    lib2.addFurniture(libLF, libW, libCch, lib2ShRck, lib2Stat, lib2Frplc, lib2Bttn, lib2WrFr, lib2Vyg, libBkShlf, libScncs, lib2Wndw, clng)
    lib3.addFurniture(libLF, libW, westDoor, lib3Strs, libCch, lib3Stat, lib3Crtn, libScncs, lib3Blcny, lib3Wndw, lib3Pllr, lib3Pntng)
    lib4.addFurniture(libUF, libW, libCch, lib4Frplc, lib4Bttn, lib4Prdtn, libScncs, lib3Pllr, lib4Stat, lib4Glb, lib3Blcny, lib4Tbl, lib4Strs, clng)
    lib5.addFurniture(libUF, libW, lib5Bnshmnt, libScncs, lib3Pllr, lib5Cndlbr, clng)
    eow1.addFurniture(genDoor, wWW, eowF, eow1Dr, eow1Rck, eow1Bskt, eow1Trch, wowWndw, mhaNDr, clng)
    eow2.addFurniture(wWW, eowF, eow2Fntn, wtr, eow2Rck, wowWndw, eow2Strs, eow2Blcny, eow2Cbnt, eow2Trch)
    eow4.addFurniture(wWW, eow4F, eow4Strs, bbaRlng, westDoor, clng)
    dst1.addFurniture(dst1F, dstW, dst1Strs, dst1Dr, dst1Lntrn, clng)
    lib1.addFurniture(lib1F, lib1W, vesChr, lib1Dsk, lib1Art, lib1Docs, lib1Rg, lib1Wndw, lib1Rck, lib1Tbl, lib1Lght, lib1Mrrr, lib1Sf, clng)
    work.addFurniture(wWW, wrkF, eastDoor, wowWndw, wrkBrl, wrkCstTbl, wrkKln, wrkBnch, wrkCbnt, wrkFrg, wrkAnvl, clng)
    din1.addFurniture(din1Clmns, din1Blcny, din1Tbl, din1Tpstry, din1F, din1W, din1Wndw, din1Chrs, din1Chndlr, din1Mnlght, din1Strs, din1Crpt, din1Dr)
    din2.addFurniture(din2W, din2F, southDoor, din2Pntng, din2Strs, clng)
    drar.addFurniture(northDoor, drarGhst, drarF, drarW, din1Mnlght, drarChss, drarBr, drarPno, drarBllrds, drarWndw, drarCch, drarTbl, clng)
    gal5.addFurniture(gal5Dsply, gal5Chndlr, gal5Cbwbs, gal5F, gal5W, gal5Clng, gal5Cbt, gal5Dr, clng)
    kitc.addFurniture(kitcTrch, kitcF, kitcW, kitcWndw, kitcDr, kitcRck, kitcPts, kitcHrth, kitcBrls, kitcPntry, kitcShlf, kitcCntr, laboSnk, clng)

    #AREA 4: CASTLE REAR
    par2.addFurniture(genDoor, wWW, par2F, par2Wndw, westDoor, eastDoor, par2Strs, parLft, par2Bwl, par2Frplc, par2Pno, par2Shlf)
    par1.addFurniture(par1F, par1Dr, par1FrPlc, wWW, par1EnchntTbl, par1Strs, parLft,
            par1Pllrs, par1Orb, par1Hrp, par1Shlf, lib1Rg, par1Cshn, vesChr, clng)
    bha3.addFurniture(southDoor, bha1Hrzn, bha1Plnt, bha1Tbl, bha1F, bhaW, clng)
    bha2.addFurniture(bha2F, bha2W, bha2Frm, clng)
    bha1.addFurniture(bha3F, bhaW, southDoor, bha3Wndw, clng)
    jha1.addFurniture(eastDoor, jhaF, jhaW, par2Wndw, jha1Pntng, jhaLntrn, jhaJd, jha1Ln, clng)
    jha2.addFurniture(southDoor, jhaF, jhaW, jhaLntrn, jhaJd, jha2Ln, clng)
    sst1.addFurniture(wallEx, sst1Strs, sstLndng, sst1F, sst1Dr, clng)
    sst2.addFurniture(wallEx, sst2Strs, sstLndng, sst2F, sstWndw, sst2Dr)
    gar1.addFurniture(lookClff, bbaSea, wallEx, bbaRlng, garF, gar1Stat, gar13Plntr)
    gar2.addFurniture(wallEx, gar2Hl, northDoor, garF, gar2Dm, gar2Clmn, gar24Scnc)
    gar3.addFurniture(lookClff, bbaSea, wallEx, bbaRlng, garF, gar13Plntr, gar3Chst, gal3Fntn, wtr, gar2Dm, gar2Clmn)
    gar4.addFurniture(wallEx, southDoor, gar4Plq, gar4Plntr, garF, gar24Scnc)
    obs1.addFurniture(obsSlts, obsStats, obsF, obsW, obsWndw, obs1Strs, obs1Tlscp, obs1Lmp, lib4Glb, obs1St, obsBlcny, northDoor)
    obs2.addFurniture(obsW, obs2F, obsWndw, obs2Strs, obsBlcny, obs2BkShlf, obs2Pntng, obs2Rlng, obs2Chr, obs2Tbl, obs2Lmp)
    obs3.addFurniture(obs3Chndlr, obsW, obs3F, obsWndw, obs3Strs, obsBlcny, obs2Rlng, obs3Chst, obs3Tlscps, clng)
    att1.addFurniture(attF, attW, sst2Dr, attCss, attBxs, gal5Cbwbs, attVnts, attClng)
    att2.addFurniture(attF, attW, att2Dr, attBxs, attCss, gal5Cbwbs, attVnts, attClng)
    labo.addFurniture(laboF, att2Dr, wallEx, laboStpCck, laboBrtt, laboGsPipe, laboCntr, iceBrrl, laboRck, laboDspnsrs, 
            laboDstllr, laboSnk, laboCntrptn, cndsr, laboTbl, laboDvcs, clng) 

    #AREA 5: SUB-LEVELS
    #Tunnels and dungeon
    sew0.addFurniture(sew0Strs, dngnW, sewF, sew0Trch, sewTnnl, sewMss)
    sew1.addFurniture(sew1Rvr, sewF, dngnW, sewTnnl, sew15Gt, sew1Trch, sewMss)
    sew2.addFurniture(sewRvr, sewF, dngnW, sewTnnl, sew2Trch, sewMss, sew2BrdgW, sew2Pp, sew2Vlvs)
    sew3.addFurniture(sewRvr, sewF, sewDrN, dngnW, sewTnnl, sew3Trch, sewMss, sew3BrdgE, sew3BrdgN, sew3Pp)
    sew4.addFurniture(sewRvr, sewF, sew4Pp, dngnW, sewTnnl, sew4Trch, sewMss)
    sew5.addFurniture(genDoor, sewRvr, sewF, sewDrW, sewDrE, dngnW, sewTnnl, sew15Gt, sew5Trch, sewMss, sew5BrdgE, sew5Pp, sew5Vlv)
    cis1.addFurniture(cis1Trch, dngnW, sewDrE, cisF, cisWtr, cisClmns, cisDrknss)
    cis2.addFurniture(dngnW, cisF, cisWtr, cis2Bt, cisClmns, cisDrknss)
    cis3.addFurniture(cis3Trch, dngnW, sewDrE, cisF, cisWtr, cisClmns, cisDrknss)
    cis4.addFurniture(cis4Trch, dngnW, sewDrE, cisF, cisWtr, cisClmns, cisDrknss)
    cis5.addFurniture(cis2Bt, cis5Fgr, cisClmns, cisDrknss, cisWtr, cis5F)
    oub1.addFurniture(sewDrW, tm1Bwl, oub1F, dngnW, oub1Pt, dungMonst, clng)
    intr.addFurniture(intrDr, intrWhl, intrGrs, intrF, dngnW, intrGrt, intrWtr, intrTrch, dungMonst, clng)
    esc1.addFurniture(esc1Lddr)
    esc6.addFurniture(esc6Grt, esc6Lddr)
    cas1.addFurniture(casW, casStrs, casF, cs35Trchs, cs35Stat, sewDrE, clng)
    sewp.addFurniture(genDoor, sewpCl, sewpGrt, sewpWtr, sewpF, dngnW, sewDrE, sewDrW, sewpTrch, sewpTnnl)
    pris.addFurniture(genDoor, prisClls, prisFgr, dngnW, sewDrS, sewDrW, prisF, prisCndlbrs, prisTbl, prisCbnt, prisGts, dungMonst, clng)
    torc.addFurniture(genDoor, sewDrE, sewDrW, dngnW, torcF, torcTrchs, torcSwhrses, torcScythF, torcRck, torcCgs, torcWhl, torcWd, torcTls, dungMonst, clng)
    cry1.addFurniture(sewDrW, dngnW, cryF, cry1Stat, cryDrwrs, cry1Crvng, cryLghts, dungMonst, cryDummy, clng)
    cry2.addFurniture(dngnW, cryF, cryDrwrs, cryLghts, cry2Engrvng, cry2Altr, dungMonst, cry2Psswd, cryDummy, clng)
    aarc.addFurniture(sewDrW, aarcF, aarcW, aarcWd, aarcBks, aarcChndlr, aarcDsk, aarcAlg, aarcShlvs, dungMonst, clng)
    dkch.addFurniture(sewDrW, dkchF, dngnW, dkchBd, dkchAxl, dkchDsk, squaCndl, dkchClng, dungMonst)

    #Catacombs and caves
    tm16.addFurniture(tmb1Cskt, catW, tm1F, catDrS, tm1Vs, tm1Bwl, tm1Effgy, clng)
    tm66.addFurniture(tmb2Cskt, catW, tm2F, catDrE, tm2Vs, tm2Orb, clng)
    tm32.addFurniture(tmb3Cskt, catW, tm3F, catDrW, tm3Vs, tm3Tpstry, tm3Cndl, clng)
    ou62.addFurniture(catDrN, oubSpk, oubStrw, oub2F, dngnW, tm1Bwl, oubSkltn)
    an65.addFurniture(catW, antF, antCskt, antNPC, antClng, antCskts, ant2Trch, antW)
    an55.addFurniture(catW, antF, antCskt, catDrN, antClng, antCskts, ant1Trch, antW)
    my18.addFurniture(antW, my18F, my18Pdstl, tm1Bwl, my18Clng)
    ct34.addFurniture(ct34Dr)
    cv18.addFurniture(cv18Strs)
    cv34.addFurniture(cvWell)
    cs35.addFurniture(cs35Dr, cs35F, cs35Trchs, casW, cs35Stat, cs35Strs)
    cv64.addFurniture(omnDr)
    ms65.addFurniture(dmmyFurniture)
    ms66.addFurniture(factum, dmmyFurniture)

    #AREA 6: CHAPEL AND VAULT
    chs1.addFurniture(chs1Strs, chsWndws, chs1F, chsW, din1Mnlght, chs1Stat, mhaWDr)
    chs3.addFurniture(chs3Strs, chsWndws, chsW, din1Mnlght, chs3F, southDoor, clng)
    cha1.addFurniture(cha1Cylx, cha1Wtr, northDoor, chaW, chaF, din1Mnlght, chaPws, cha1Cndlbr, chaHz, chaCrpt, chaWndws, chaClng)
    cha2.addFurniture(chaF, chaW, din1Mnlght, chaPws, chaHz, chaCrpt, chaWndws, cha2Alt, chaClng)
    vau1.addFurniture(vauF, vauBwls, vau1Tbl, vauClng)
    vau2.addFurniture(vau2Chsts, vauF, vauBwls, vauClng)
    vaue.addFurniture(vaueF, vauBwls, vaueBttns, vauW, clng)

    #AREA 7: TOWER
    tow1.addFurniture(tow1F, wallEx, towWndw, towBlcny, tow1Pdstl, tow1Dr, tow1BlckDr, towSphr)
    tow2.addFurniture(genDoor, towWndw, wallEx, towBlcny, eastDoor, towSphr, tow2DrN, clng, tow2F)
    bls1.addFurniture(bls1Dr, bls1Strs, bls1_Plnts, blsWndw, bls1F, bls1Stat)
    bls2.addFurniture(eastDoor, bls2Strs, blsWndw, bls2F, blsBlcny)
    tbal.addFurniture(genDoor, tbalStrs, bbaSea, tbalPllr, northDoor, tbalDrS, tbalF)
    lqu1.addFurniture(westDoor, lquF, lqu1Mrrr, lqu1Lvr, lquW, lqu1Cbnt, lqu1_Bd, lqu_Crpt, clng)
    lqu2.addFurniture(lquF, lquW, lqu_Crpt, lqu2Bd, clng)
    soul.addFurniture(soulPl, soulStat, soulF, wallEx, soulWndw, clng)
    hads.addFurniture(hadsVcs, hadsGtwy, hadsSprts, hadsCrpses, hadsF, hadsW)

    #####################################################################################
    ### LOCK ROOMS 
    #####################################################################################

    def lockRooms():
        for room in (rotu, stud, gal5, gal1, par2, clos, din1, kitc, ou62, chs1, 
                work, tow1, sewp, dkch, wow2, vau2, cou4):
            room.setLocked(True)
    lockRooms()
    
    #####################################################################################
    ### WRITE ROOMS TO FILES
    ### This is done so rooms don't remain in main memory when you haven't
    ### visited them yet in the current game instance.
    #####################################################################################

    def _writeAllRooms():
        allRooms = (                        
            cel5,cel6,soul,hads,cel3,cel4,tbal,cel1,cel2,bls2,tow2,lqu1,lqu2,obs3,att1,labo,
            foy4,gal6,gal7,sst2,att2,bls1,tow1,chs3,for1,for2,for3,for4,cha2,for5,gal5,lib4,
            obs2,jha1,par2,foy3,gal3,gal4,lib5,sst1,jha2,gar1,gar2,din2,gar3,gar4,cou8,drar,
            wow3,clos,work,eow4,bha1,bha2,bha3,foyb,foyc,lib1,lib2,obs1,stud,par1,foy2,gal1,
            gal2,lib3,look,rotu,foyw,foy1,vest,mha1,chs1,squa,sha2,iha1,cou1,cou7,cou6,mha2,
            din1,shar,sha1,iha2,cou2,cou3,cou5,mha3,kitc,wbal,wow1,wow2,cous,cou4,dst1,eow1,
            eow2,endg,esc3,esc4,esc5,cis5,esc2,esc1,esc6,cas1,cry2,vau1,cis2,cis1,sew5,pris,
            torc,cry1,vau2,cis3,aarc,sew4,sew3,sew2,sew1,vaue,cis4,oub1,intr,sewp,dkch,sew0,
            ct11,ct12,ct13,ct14,ct15,tm16,ct17,my18,ct21,ct22,ct23,ct24,ct25,ct26,ct27,ct28,
            ct31,tm32,ct33,ct34,cs35,ct36,ct37,ct38,ct41,ct42,ct43,ct44,ct45,ct46,ct47,ct48,
            ct51,ct52,ct53,ct54,an55,ct56,ct57,ct58,ct61,ou62,ct63,ct64,an65,tm66,ct67,ct68,
            cv11,cv12,cv13,cv14,cv15,cv16,cv17,cv18,cv21,cv22,cv23,cv24,cv25,cv26,cv27,cv28,
            cv31,cv32,cv33,cv34,cv35,cv36,cv37,cv38,cv41,cv42,cv43,cv44,cv45,cv46,cv47,cv48,
            cv51,cv52,cv53,cv54,cv55,cv56,cv57,cv58,cv61,cv62,cv63,cv64,ms65,ms66,cv67,cv68,
            cha1, Room(Id.NULL, Id.NULL))

        base = NEW_GAME_DATA_PATH + SEP

        for room in allRooms:
            i = room.getCoords()
            path = base + "lvl_" + str(i[0]) + str(SEP) + "row_" + str(i[1]) + SEP + room.getID() + ".data"
            
            with open(path, "wb") as file:
                pickle.dump(room, file)

    _writeAllRooms()
