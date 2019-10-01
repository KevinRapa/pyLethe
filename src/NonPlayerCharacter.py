from Names import WEAPON
from Furniture import Furniture, Moveable

"""
    Represents an NPC that you can talk to.

    Interacting with the NPC will call converse1, unless the NPC
    has been talked to before, in which case converse2 will be
    called. More converse methods may be defined.

    Converse methods may have differing return types depending on implementation.
"""
class NonPlayerCharacter(Furniture, Moveable): 
    ATTACK_PATTERN = "kill|hit|punch|murder|attack"
    ATTACK_DIALOG = "You really aren't a natural killer..."
    TALK_PATTERN = "speak|talk|converse|chat|greet|listen"
    
    def __init__(self):
        super(NonPlayerCharacter, self).__init__()

        self.firstTime = True # If the player hasn't talked to this before.
        self.useDialog = NonPlayerCharacter.ATTACK_DIALOG
        
        self.addUseKeys(Furniture.ANYTHING)
        self.addActKeys(NonPlayerCharacter.ATTACK_PATTERN, NonPlayerCharacter.TALK_PATTERN)
    
    def converse1():
        pass
    
    def converse2():
        pass   
    
    def firstTime(self): 
        return self.firstTime
    
    def useEvent(self, item): 
        if item.getType() == WEAPON:
            return NonPlayerCharacter.ATTACK_DIALOG
        else:
            return "It looks like it's faring perfectly well without that."
    
    def moveIt(self): 
        return "It probably wouldn't enjoy that too much..."