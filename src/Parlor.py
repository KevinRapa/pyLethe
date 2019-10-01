from Structure_gen import Door, StaticWindow, Balcony, Staircase
from Library import Shoes
import re
from Things import Fireplace, BurningBowl
from Names import *
from GUI import GUI
from NonPlayerCharacter import NonPlayerCharacter
import Direction, Id, AudioPlayer
from Room import Room
from Furniture import Openable, SearchableFurniture, Unmoveable, Moveable, Furniture
from Player import Player
from Item import Note, Item, Liquid, Book

"""
    Hides a brass plate for the observatory puzzle.
"""
class Par1_Cushion(SearchableFurniture):
    def __init__(self, plate):
        super(Par1_Cushion,self).__init__(plate)
        
        self.PLATE_REF = plate
        self.description = ("It's a lavender tasseled cushion for sitting on.")
        self.searchDialog = ("You lift the cushion.")
        self.actDialog = ("What a comfortable cushion! Well, the cushion is nice, " +
                         "feels hard underneath though... Could just be the floor.")
        self.addNameKeys("(?:lavender )?(?:tasseled )?(?:cushion|pillow)")
        self.addActKeys(Furniture.SITPATTERN, Furniture.MOVEPATTERN, "lift")

    def interact(self, key):
        if re.match(Furniture.SITPATTERN, key):
            return self.actDialog
        elif self.inv.contains(str(self.PLATE_REF)):
            if Player.getInv().isFull():
                return ("You lift the cushion and discover a clean, shiny " +
                       "plate underneath. Unfortunately, you realize that " +
                       "your inventory is full and thus cannot take the item. " +
                       "You set the cushion back down.")
            else:
                self.inv.give(self.PLATE_REF, Player.getInv())
                return ("You lift the cushion and discover a clean, shiny " +
                       "plate underneath. You gleefuly take it and set the " +
                       "cushion back down.")
        else:
            return ("You lift the pillow to fluff it up a bit and then set it back down.")



"""
    Has a magical ice ward over it. 
    Player must use the sacred fire on this to break the ward.    
"""
class Par1_Door(Door):
    def __init__(self, enchbttl, direct):
        super(Par1_Door,self).__init__(direct)
        self.useDialog = ("You throw the fire on the door. The fire then slowly fades away.")
        self.description = ("It looks like a heavy wooden door.")
        
        self.ENCHNTBTTL_REF = enchbttl
        self.addNameKeys("barrier")
        self.addUseKeys(SACRED_FIRE)

    def getDescription(self):
        if not Player.getRoomObj(Id.PAR1).isAdjacent(Id.BHA3):
            return ("The door has an odd pale-blue tint to it. As you approach, " +
                   "you feel a coldness. Upon closer inspection, you can see the " +
                   "blue tint pulsing.")
        else:
            return self.description

    def useEvent(self, item):
        if str(item) == SACRED_FIRE:
            rep = self.useDialog

            if not Player.getRoomObj(Id.PAR1).isAdjacent(Id.BHA3):
                Player.getRoomObj(Id.PAR1).addAdjacent(Id.BHA3)
                rep = ("You cast the fire onto the door, to which it clings." +
                      " The fire begins to fade away along with the barrier.")
            Player.getInv().remove(item)
            Player.getInv().add(self.ENCHNTBTTL_REF)
            return rep
        elif item.getType() == WEAPON: 
            return ("The door is build too solidly and breaking it down is futile.")
        else:
            return super(Par1_Door,self).useDialog



"""
    Used to make the shrouded shoes to traverse the back hall and the
    enchanted bottle to access the back hall.
    Recipes are scattered around the parlor. Player must visit previous areas
    of the castle to collect the ingredients.
"""
class Par1_EnchantingTable(SearchableFurniture, Moveable): 
    def __init__(self, enchtBttl, itemList=[]):
        super(Par1_EnchantingTable,self).__init__(itemList)
        
        self.REF_ENCH_BTTL = enchtBttl 
        self.actDialog = ("You pound your hands on the table.")
        self.useDialog = ("You place it on the table.")
        self.searchDialog = ("You look on the table.")
        self.description = ("The black pentagonal table bears many carvings of strange " +
                           "runes and writing that seem to glow from the fire. Two " +
                           "circular runes decorate either side of the table.")
        
        self.addUseKeys(Furniture.ANYTHING) # Accepts any item to be put on it.
        self.addNameKeys("enchanting table", "table")
        self.addActKeys("pound", "hit", "activate", "enchant")

    def useEvent(self, item):
        if item.getType() == PHYLACTERY:
            return ("You probably shouldn't get rid of that.")
        
        if Player.getShoes() == str(item):
            Player.setShoes(Furniture.NOTHING)
            
        Player.getInv().give(item, self.inv)
        return self.useDialog

    def interact(self, key):          
        outcome = self.enchant()

        if outcome == 1:
            return (actDialog + " As you do, a loud bang startles you and a bright flash blinds you momentarily. You look away. " +
                                "As you turn back, you see that three of the four ingredients have vanished. The bottle, bearing a " +
                                "certain magical aura, sits alone at the table's center.")
        elif outcome == 2:
            return (actDialog + " As you do, a loud bang startles you and a bright flash blinds you momentarily. You look away, " +
                                "and as you turn back, you see that the three ingredients have vanished. A delicate pair of " +
                                "slippers shrouded in a fine dark mist take their place.")
        else:
            return (actDialog + " To your disappointment, the table only jostles a small amount " +
                                "from the force. Perhaps you aren't the wizard you thought you were.")

    def enchant(self):
        if self.inv.size() == 4 and self.containsItem(FIRE_SALTS) and \
                self.containsItem(MANDRAGORA) and self.containsItem(SPRUCE_EXTRACT) and \
                self.containsItem(GLASS_BOTTLE):
            self.inv = []
            AudioPlayer.playEffect(32)
            AudioPlayer.playEffect(29)
            self.inv.add(self.REF_ENCH_BTTL)
            return 1
        elif self.inv.size() == 3 and self.containsItem(RAVEN_FEATHER) and \
                self.containsItem(AETHER_VIAL) and self.containsItem(NIGHT_SLIPPERS):
            self.inv = []
            AudioPlayer.playEffect(32)
            AudioPlayer.playEffect(29)
            inv.add(Shoes(SHROUDED_SHOES, 100, use="You slip on the shoes. " +
                "They are perhaps the most comfortable pair you've ever worn."))
            return 2
        else:
            AudioPlayer.playEffect(40)
            return 0



"""
    Gives the player sacred fire if the player uses the enchanted bottle on self.
"""
class Par1_FirePlace(Fireplace):
    def __init__(self, bckt, bttl):       
        super(Par1_FirePlace,self).__init__(bckt)
        
        self.ENCHT_BTTL_REF = bttl
        self.SCRDFR_REF = Liquid(SACRED_FIRE, 150, "The fire burns enigmatically inside " +
                         "the bottle. To your surprise, the fire gives off no heat.")
        
        self.descLit = ("It's a large sandstone fireplace, about your height. " +
                       "Its mantle is supported on both sides by short columns " +
                       "carved into angelic figures. The fire burns aggressively, " +
                       "but to your amazement, gives off no heat.")

        self.useDialog = ("Holding the magical bottle over the fire, some of the flames seep " +
                         "inside. You quickly cork the bottle and stare at it, mesmerized.")
        
        self.addUseKeys(GLASS_BOTTLE, ENCHANTED_BOTTLE)

    def getIt():
        if Player.getInv().contains(str(self.ENCHT_BTTL_REF)):
            Player.getInv().remove(self.ENCHT_BTTL_REF)
            Player.getInv().add(self.SCRDFR_REF)
            return self.useDialog
        else:
            return super(Par1_FirePlace,self).getIt()

    def useEvent(self, item):
        if str(item) == BUCKET_OF_WATER:
            Player.getInv().remove(item)
            Player.getInv().add(self.BCKT_REF)
            AudioPlayer.playEffect(39)
            return ("The water steams aggressively upon contact, but fails to douse the flames.")
        elif str(item) == ENCHANTED_BOTTLE:
            Player.getInv().remove(item)
            Player.getInv().add(self.SCRDFR_REF)
            return self.useDialog
        else:
            return ("You manage to do nothing but burn your hand. What were you thinking?")



"""
    Wakes up the orb NPC if played.    
"""
class Par1_Harp(Furniture, Moveable):
    def __init__(self, ID):
            super(Par1_Harp,self).__init__()

            self.addNameKeys("harp", "renaissance-era harp")
            self.description = ("It's a renaissance-era harp. It looks gold plated, " +
                               "but you're no metallurgist. It sure does look " +
                               "tempting to play though.")
            self.ORB_ID = ID
            self.addActKeys("play", "strum")

    def interact(self, key):       
        o = Player.getRoomObj(Id.PAR1).getFurnRef(self.ORB_ID)
        AudioPlayer.playEffect(54)

        if not o.woken():    
            o.wake()
            return ("You slouch next to the harp and give it a jarring strum. Suddenly, you " +
                   "hear a nearby voice. \"Hey! Stop playing that, you'll break something!\" " +
                   "The voice is echoey, and you have a hunch it's emanating from the orb.")
        else:
            return ("You sit down again and play some more notes. \"Stop playing " +
                   "that before you break it!\" The orb yells. \"I'm the only " +
                   "experienced musician in this castle!\"")



class Par1_Orb(NonPlayerCharacter):
    def __init__(self):
        super(Par1_Orb,self).__init__()

        self.woken = False
        self.searchDialog = "There's nothing hidden here."
        self.actDialog = ("You give the orb a rub with no effect. This is no magical " +
                         "crystal ball as you thought.")
        self.description = ("The small glass orb is filled with a smokey gas. " +
                           "The smoke churns slowly inside the orb.")
        self.addActKeys("rub", "feel", "touch")
        self.addNameKeys("(?:small )?(?:glass )?orb")

    def interact(self, key):
        if re.match(NonPlayerCharacter.ATTACK_PATTERN, key):
            return NonPlayerCharacter.ATTACK_DIALOG
        elif re.match(NonPlayerCharacter.TALK_PATTERN, key):
            if self.firstTime and self.woken:
                self.firstTime = False
                return self.converse1()
            elif not self.firstTime and self.woken: 
                return self.converse2()
            else:
                return ("You mutter a soft 'Hullo?' But hear no response")
        else:
            return self.actDialog

    def converse1():
        GUI.out("\"You should ask permission before playing with things that " +
                "aren't yours!\" Shouts the voice...")
        GUI.promptOut()
        
        GUI.out("\"... And so what if I can't even play music anymore? It would " +
                "be music nonetheless, and not that cacophonous symphony of hyenas " +
                "screwing you produced. I'll have you know that I used to be an " +
                "accomplished organist. In fact, I used to play in the chapel, " +
                "in the upper-east wing. That was... quite long ago.\"")
        GUI.promptOut()
        
        GUI.out("\"You thought it would open a way out of here? That's proposterous. " +
                "The architecture here wouldn't allow it. You shouldn't have gotten " +
                "yourself locked in here to begin with. Perhaps if you weren't as " +
                "clumsy as you play...\"")
        GUI.promptOut()
        
        GUI.out("\"It wasn't you? Who else could it be? The original inhabitants of " +
                "this castle died long ago. Who are you anyway?...\"")
        GUI.promptOut()
        
        GUI.out("\"Okay, okay, I'm SORRY for asking. It is none of my business, " +
                "but then again, nothing is, except my work. It just feels nice " +
                "to order people around time and again...\"")
        GUI.promptOut()
        
        GUI.out("\"... Don't worry about it! That's none of your business!...\"")
        GUI.promptOut()
        
        GUI.out("\"NO, of course I don't get bored in here. Though it has been " +
                "... perhaps 500 years since I played? It doesn't matter. I'm " +
                "a musical THEORIST. At my level of experience, the notion of " +
                "creating music to be PLAYED is juvenile fuff. My creations are " +
                "too complex to be understood by playing. But I digress...\"")
        GUI.promptOut()
        
        GUI.out("\"I don't know about any magical barrier. But I'm not surprised " +
                "\"this castle isn't brimming with power. Eurynomos could " +
                "do anything he pleased.")
        GUI.promptOut()     
        
        GUI.out("I requested Eurynomos to bind me here so that " +
                "I could write music and live eternally like him... or so I thought. " +
                "I promised to write music for him as long as he wished to " +
                "keep me alive in self... whatever I'm in. It's actually quite " +
                "nice in here.")
        GUI.promptOut()
        
        GUI.out("\"Anyway, I'm sorry to say that their power is just as a mystery to me. " +
                "Perhaps you could find a way to dispell it, for I am only " +
                "an artisan of sound. But don't touch that enchanting table over " +
                "there! I don't want this whole room charred...\"")
        GUI.promptOut()
        
        return ("\"Now, if you don't mind, I would like to get back to writing " +
               "this twelve-hundred part symphony.\"")

    def converse2(self): 
        return ("\"Egh... uhh... I'm not sure... on the shelf over there??? " +
                "Ah! That's what this needs, more bassoons!\"")

    def woken(self):
        return self.woken

    def wake(self):
        self.woken = True



class Par1_Pillars(Furniture):
    def __init__(self):
            super(Par1_Pillars,self).__init__()

            self.addNameKeys("(?:tan )?(?:grooved )?(?:pillars?|columns?)")
            self.description = ("The tan, grooved columns support the loft extension.")



"""
    Contains the enchanting table used to make a couple items to progress further.
    Connects to Par2 and Bha3.    
"""
class Par1(Room):
    def __init__(self, name, ID):
        super(Par1,self).__init__(name, ID)

    def getDescription(self):
        if not self.isAdjacent(Id.BHA3):
            return super(Par1,self).getDescription()
        else:
            return super(Par1,self).getDescription().replace(", but something about it appears off", ".", 1)

    def getBarrier(self, direct):
        if direct == Direction.NORTH and not self.isAdjacent(Id.BHA3):
            return ("The door here feels ice cold and the doorknob won't turn " +
                   "despite your strength.")
        else:
            return self.bumpIntoWall()



class Par2_Bowl(BurningBowl):
    def __init__(self):
        super(Par2_Bowl,self).__init__()

        self.description = ("It's a steel bowl of fire hanging from the ceiling " +
                           "by a chain. A draft from the outside causes it to swing gently.")



class Par2_Fireplace(Furniture):
    def __init__(self):
            super(Par2_Fireplace,self).__init__()

            self.addNameKeys("fireplace", "hearth")
            self.description = ("The fireplace crackles down below. Who keeps these things lit?")
            self.searchDialog = ("It's much too far away to do that...")



"""
    Wakes up the orb NPC if played.    
"""
class Par2_Piano(SearchableFurniture, Openable, Unmoveable): 
    def __init__(self, ID, itemList=[]):
        super(Par2_Piano,self).__init__(itemList)
        
        self.description = ("The black grand piano sits solemnly on the loft " +
                           "extension. You're surprised anybody here has time for music!")
        
        self.useDialog = ("You have little knowledge of musical instruments, much less in instrument repair.")
        self.searchDialog = ("You look under the piano's cover.")
        self.ORB_ID = ID
        
        self.addNameKeys("(?:black )?(?:grand )?piano", "(?:piano )?keys?")
        self.addUseKeys(STEEL_WIRE)
        self.addActKeys("play", "press")

    def interact(self, key): 
        orb = Player.getRoomObj(Id.PAR1).getFurnRef(self.ORB_ID)
        AudioPlayer.playEffect(53)

        if not orb.woken():
            orb.wake()
            return ("You sit at the piano and produce a few notes. Suddenly, you " +
                   "hear a voice from down below. \"Hey! Who is playing my piano?\" " +
                   "The voice is echoey, and you have a hunch it's emanating from the orb below.")
        else:
            return ("You sit down again and play some more notes. \"Stop playing " +
                   "that before you break it!\" The orb yells. \"I'm the only " +
                   "experienced musician in this castle!\"")



"""
    Player is locked in the castle rear upon entering this room.
    Connects to Jha1 and Par1.    
"""
class Par2(Room):
    def __init__(self, name, ID):
        super(Par2,self).__init__(name, ID)

    def getDescription(self):
        if not self.isAdjacent(Id.JHA1):
            return (super(Par2,self).getDescription() + " However, there is something odd about this door.")
        else:
            return super(Par2,self).getDescription()

    def triggeredEvent(self):
        if not Player.hasVisited(self.ID):
            AudioPlayer.playEffect(8, 80)
            GUI.out("After stepping into the room, the door slams shut behind you. " +
                    "Startled, you spin around and miss a breath. You are alone.")
            Player.getRoomObj(Id.FOY3).setLocked(True)

        return self.NAME

    def getBarrier(direct):
        if direct == Direction.SOUTH:
            return ("There's nothing but a railing and open space over the lower level parlor.")
        else:
            return self.bumpIntoWall()



class Par2_Window(StaticWindow):
    def __init__(self):
        super(Par2_Window,self).__init__()
        self.description = ("The window gives view to the expansive ocean behind " +
                           "the castle. Now, more than ever, you wish you could " +
                           "climb out and jump.")
        self.addNameKeys("windows", "barred windows")



class Par_Loft(Balcony):
    def __init__(self):
        super(Par_Loft,self).__init__()

        self.description = ("The loft partially(over the north wall of " +
                           "the first-floor parlor. In the middle, the loft bends a little " +
                           "further outwards.")
        self.addNameKeys("balcony", "loft", "extension")



class Par_Stairs(Staircase):
    def __init__(self, direction, dest):
        super(Par_Stairs,self).__init__(direction, dest, 15)
        self.description = ("The thin sandstone stairs lead to the balcony above. ")

    def getDescription(self):
        if self.DIR == Direction.DOWN: 
            return ("The thin sandstone stairs lead down to the first floor.")
        else:
            return self.description
