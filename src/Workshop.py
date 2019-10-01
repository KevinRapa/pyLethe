from GUI import GUI
import Id
from Inventory import Inventory
from Names import *
from Player import Player
import re
from Furniture import *
from Item import Note, Liquid, BreakableItem

class Wrk_Anvil(Furniture, Unmoveable):
    def __init__(self):
        super(Wrk_Anvil,self).__init__()

        self.description = ("It's a quintessential anvil if you've ever seen one. " +
                          "It looks heavily used.")
        self.searchDialog = ("There's nothing to search for on an anvil.")
        self.actDialog = ("There's a plethora of weapons downstairs. No need for that.")
        self.useDialog = self.actDialog
        
        self.addUseKeys(HAMMER)
        self.addActKeys(HAMMER, "hit|bang|use")
        self.addNameKeys("anvil")



class Wrk_Barrel(SearchableFurniture, Openable, Moveable):
    def __init__(self, itemList=[]):
        super(Wrk_Barrel,self).__init__(itemList)
        
        self.description = ("It's not full sized... maybe only three feet high. " +
                           "It has a wooden lid on top.")
        self.searchDialog = ("You open the lid and peer inside.")
        self.addNameKeys("(?:wood(?:en)? )?barrel")



"""
    Used to create lenses and glass sheets.
    Player must use the lens template on this plus molten red glass to 
    make the red lens.    
"""
class Wrk_CastingTable(SearchableFurniture, Moveable):
    def __init__(self, ID, ID2, rdLns, snd, rdDy, blDy, yllwDy, ptsh, ID3):
        super(Wrk_CastingTable,self).__init__()
        
        self.inv = TableInventory(self)
        
        # Inventory references to restock
        self.BRL_ID = ID  
        self.SCK_ID = ID2     
        self.CBNT_ID = ID3 
        
        # Lens to give player
        self.SHEET_REF = BreakableItem(GLASS_SHEET, 0)
        self.BLUE_LENS_REF = BreakableItem(BLUE_LENS, 20)
        self.YELLOW_LENS_REF = BreakableItem(YELLOW_LENS, 20)
        self.RED_LENS_REF = rdLns
        
        # Dyes to restock
        self.RED_DYE_REF = rdDy   
        self.BLUE_DYE_REF = blDy  
        self.YELLOW_DYE_REF = yllwDy 
        
        # Sand and potash to restock
        self.POTASH_REF = ptsh     
        self.SAND_REF = snd 

        self.searchDialog = ("You search the plain metal table.")
        self.description = ("It's a tall metal casting table for shaping solids from molten liquids.")
        self.addUseKeys(LENS_TEMPLATE, MOLTEN_RED_GLASS, MOLTEN_YELLOW_GLASS, MOLTEN_BLUE_GLASS)
        self.addNameKeys("(?:tall )?(?:metal )?(?:casting )?table")

    def useEvent(self, item):
        name = str(item)
        
        if name == LENS_TEMPLATE:
            Player.getInv().give(item, self.inv)
            return ("You fit the template onto the table's surface.")
        else:
            Player.getInv().remove(item)
            
            sackInv = Player.getRoomObj(Id.CLOS).getFurnRef(self.SCK_ID).getInv()
            cbntInv = Player.getRoomObj(Id.WORK).getFurnRef(self.CBNT_ID).getInv()
            brlInv = Player.getRoomObj(Id.WORK).getFurnRef(self.BRL_ID).getInv()
            
            if self.containsItem(LENS_TEMPLATE):   
                color = None
                
                if name == MOLTEN_RED_GLASS:
                    self.inv.add(self.RED_LENS_REF) # Give player red lens.
                    color = ("red")
                elif name == MOLTEN_BLUE_GLASS:
                    self.inv.add(self.BLUE_LENS_REF) # Give player blue lens.
                    sackInv.add(self.SAND_REF) # Restock sand.
                    brlInv.add(self.BLUE_DYE_REF) # Restock dye.
                    cbntInv.add(self.POTASH_REF) # Restock potash.
                    color = ("blue")
                else:
                    self.inv.add(self.YELLOW_LENS_REF) # Give player yellow lens.
                    sackInv.add(self.SAND_REF) # Restock sand.
                    brlInv.add(self.YELLOW_DYE_REF) # Restock dye.
                    cbntInv.add(self.POTASH_REF) # Restock potash.
                    color = ("yellow")
                return ("You pour the molten glass into the mold. In no time " +
                       "at all, the glass dries into a fresh new " + color + 
                        " lens! This is what you needed, right?")
            else:
                self.inv.add(self.SHEET_REF)
                sackInv.add(self.SAND_REF)
                cbntInv.add(self.POTASH_REF)
                
                if name == MOLTEN_RED_GLASS:
                    brlInv.add(self.RED_DYE_REF)
                elif name == MOLTEN_BLUE_GLASS:
                    brlInv.add(self.BLUE_DYE_REF)
                else:
                    brlInv.add(self.YELLOW_DYE_REF)

                return ("You pour the molten glass onto the casting table. " +
                       "As the glass dries, you scratch your head. The square " +
                    "table has curiously yielded a non-round sheet of glass.")

    def getDescription(self):
        if self.containsItem(LENS_TEMPLATE):
            return ("The tall metal casting table has a template fitted to it.")
        else:
            return self.description



class TableInventory(Inventory):
    def __init__(self, ref):
        super(TableInventory,self).__init__()
        self.TABLE_REF = ref

    def add(self, item): 
        n = str(item)
        
        if n in (RED_LENS, YELLOW_LENS, BLUE_LENS, GLASS_SHEET): 
            return super(TableInventory,self).add(item)
        elif not n in (MOLTEN_RED_GLASS, MOLTEN_BLUE_GLASS, MOLTEN_YELLOW_GLASS, LENS_TEMPLATE): 
            if item.getType() == LIQUID:
                GUI.out("Interesting... but that probably isn't going to form anything useful.")
            else:
                GUI.out("You're fairly sure the professionals don't put things like that onto casting tables.")
            
            return False
        elif n == LENS_TEMPLATE:
            GUI.out("You fit the lens template onto the table.")
            return super(TableInventory,self).add(item)
        else:
            GUI.out(self.TABLE_REF.useEvent(item))
            return True



class Wrk_Cbnt(SearchableFurniture, Openable, Unmoveable):
    def __init__(self, itemList=[]):
        super(Wrk_Cbnt,self).__init__(itemList)
        self.description = ("The row of cabinets hang over the workbench.")
        self.searchDialog = ("You open the cabinets.")
        self.addNameKeys("cabinets?")




class Wrk_Forge(Furniture, Gettable, Unmoveable):
    def __init__(self):
        super(Wrk_Forge,self).__init__()

        self.description = ("The brick forge's heat envelops the room. Though " +
                           "there's no fire in it, the smoldering ashes have only begun to cool.")
        self.actDialog = ("You're smart enough not to put your hand in there.")
        self.useDialog = ("You'd much rather work with wood than metal...")
        
        self.addActKeys(Furniture.GETPATTERN, Furniture.FEELPATTERN)
        self.addUseKeys(HAMMER)
        self.addNameKeys("(?:brick )?forge", "(?:smoldering )?ash(?:es)?")

    def interact(self, key):
        if re.match(Furniture.FEELPATTERN, key):
            return self.actDialog
        else:
            return self.getIt()



"""
    Used to create molten glass with dye, sand, and potash.
    Player must go back to the closet to get sand.
"""
class Wrk_Kiln(SearchableFurniture, Openable, Unmoveable):
    def __init__(self):
        super(Wrk_Kiln,self).__init__()
        
        self.inv = KilnInventory()
        
        self.REFGLSSR = Liquid(MOLTEN_RED_GLASS, -15)
        self.REFGLSSB = Liquid(MOLTEN_BLUE_GLASS, -15)
        self.REFGLSSY = Liquid(MOLTEN_YELLOW_GLASS, -15)
       
        self.actDialog = ("A search would be a good action to try instead.")
        self.useDialog = (" You let the sand and the dye bake for a bit. In no time, the " +
                          "mixture has blended into hot molten glass. Delicious!")
        self.searchDialog = ("You look into the scorching hot kiln.")
        self.description = ("The kiln resembles a ceramic oven. Its intense heat " +
                           "keeps this room roasting. Inside is a small ceramic " +
                           "crucible sitting on a metal rack.")
        
        self.addActKeys(Furniture.GETPATTERN, "climb", "jump")
        self.addUseKeys(RED_DYE, YELLOW_DYE, BLUE_DYE, SAND, POTASH)
        self.addNameKeys("(?:ceramic )?(?:oven|kiln|crucible)", "(?:metal )?rack")

    def interact(self, key):
        if key == "climb" or key == "jump":
            return ("Are you not warm enough?")
        else:
            return self.actDialog

    def useEvent(self, item):
        Player.getInv().give(item, self.inv)
        return Furniture.NOTHING

    def makeGlass(self):
        if self.containsItem(RED_DYE):
            self.inv = []
            self.inv.add(self.REFGLSSR)
        elif self.containsItem(BLUE_DYE):
            self.inv = []
            self.inv.add(self.REFGLSSB)
        else:
            self.inv = []
            self.inv.add(self.REFGLSSY)

        return self.useDialog

    def hasDye(self):
        return (self.containsItem(RED_DYE) or self.containsItem(BLUE_DYE) \
            or self.containsItem(YELLOW_DYE))

    def check(self):
        return self.hasDye() and self.containsItem(POTASH) and self.containsItem(SAND)



class KilnInventory(Inventory):       
    def __init__(self):
        super(KilnInventory,self).__init__()

    def add(self, item): 
        n = str(item)
        
        if n in (MOLTEN_RED_GLASS, MOLTEN_BLUE_GLASS, MOLTEN_YELLOW_GLASS):
            return super(KilnInventory,self).add(item)
        elif not n in (RED_DYE, BLUE_DYE, YELLOW_DYE, SAND, POTASH): 
            GUI.out("You're fairly sure the professionals don't put things like that into kilns.")
        elif self.size() < 3 and (
                ((n == RED_DYE)    and not self.containsItem(RED_DYE))    or \
                ((n == BLUE_DYE)   and not self.containsItem(BLUE_DYE))   or \
                ((n == YELLOW_DYE) and not self.containsItem(YELLOW_DYE)) or \
                ((n == SAND)       and not self.containsItem(SAND))       or \
                ((n == POTASH)     and not self.containsItem(POTASH))):
            result = ("You pour it in.")
            super(KilnInventory,self).add(item)
            
            if self.check():
                result += self.makeGlass()
            
            GUI.out(result)
            return True
        elif self.size() == 3: 
            GUI.out("The crucible is full to the brim.")
        else:
            GUI.out("The kiln already has that in it.")
        
        return False