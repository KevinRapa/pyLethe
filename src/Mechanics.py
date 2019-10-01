import AudioPlayer
from Furniture import Furniture

"""
    Defines the mechanisms of a generic button.
    Pushing a button causes an event, but does not have an on or off state.
"""
class Button(Furniture): 
    def __init__(self):
        super(Button, self).__init__()

        self.description = "It's a small button, the pushy kind."
        self.searchDialog = "There's a sword here! No not really, just a button."
        self.addActKeys("push", "hit", "activate", "press")
        self.addNameKeys("button") 
   
    def interact(self, key):
        AudioPlayer.playEffect(11)
        return self.event(key)
   
    def event(self, key):
        pass

"""
  Defines the mechanisms of a generic lever.
  Levers, unlike buttons, can be on or off.

  event defines what the lever does.
"""
class Lever(Furniture):
    def __init__(self): 
        super(Lever, self).__init__()
        self.isOn = False
        self.addActKeys("pull", "push", "flick", "hit", "move")
    
    def interact(self, key): 
        self.swtch()
        AudioPlayer.playEffect(12)
        return self.event(key)
    
    def swtch(self):
        self.isOn = not self.isOn
    
    # Defines what happens when this lever is pulled.
    def event(self, key):
        pass