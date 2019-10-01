import Id, Direction, AudioPlayer
from Player import Player
from Furniture import Furniture, Gettable, Unmoveable
from Room import Room

"""
    Creates amusing dialog if the player decides to not venture towards the castle.
"""
class Forest(Room):    
    def __init__(self, ID):
        super(Forest,self).__init__("Dark forest", ID)

    def getBarrier(self, direct):
        return ("There's an impenetrable thicket that way. See? Nothing interesting! Let's go back now.")


        
class For1(Forest):
    def __init__(self, ID):
        super(For1,self).__init__(ID)

    def getBarrier(self, direct):
        if direct == Direction.NORTH:
            Player.setOccupies(Id.COU4)
            AudioPlayer.playEffect(0)
            return ""
        else:
            return super(For1, self).getBarrier(dir)

    def getDescription(self):
        if Player.getLastVisited() == Id.ENDG:
            return ("What are you doing? You were expected to venture forth. " +
                    super(For1, self).getDescription())
        else:
            return super(For1, self).getDescription()



class For2_Elk(Furniture, Gettable):
    def __init__(self):
        super(For2_Elk,self).__init__()

        self.description = ("The elk stands still in the distance, silently " +
                 "mocking your pompous, rebellious attitude.")
        self.actDialog = ("Of course I didn't program this game that way.")
        self.searchDialog = ("There is definitely nothing there to search.")

        self.addNameKeys("(?:sauntering )?elk")
        self.addActKeys("ride", "eat", "kill", Furniture.GETPATTERN)
    
    def interact(self, key):              
        if key == "ride":
            return self.actDialog
        elif key == "eat":
            return ("You aren't even hungry. Stop it.")
        elif key == "kill":
            return ("This is not a hunting game!")
        else:
            return self.getIt()



class For2(Forest):
    def __init__(self, ID):
        super(For2,self).__init__(ID)

    def getDescription(self):
        if Player.getLastVisited() == Id.FOR1:
            return ("Did you not read the last description? This isn't what " +
                "you are supposed to do. " + super(For2,self).getDescription())
        else:
            return ("Yes, indeed. Let's make our way back to the castle and " +
                "stop this nonsense. " + super(For2,self).getDescription())



class For3(Forest):
    def __init__(self, ID):
        super(For3,self).__init__(ID)

    def getDescription(self):
        if Player.getLastVisited() == Id.FOR2:
            return ("Ah, hold on, perhaps an adventure still awaits... Wait for it... Alright. " + 
                super(For3, self).getDescription())
        else:
            return super(For3, self).getDescription()



"""
    Player dies if the player wanders too far from the castle. Ah well!    
"""
class For5(Forest):
    def __init__(self, ID):
        super(For5,self).__init__(ID)

    def triggeredEvent():
        Player.commitSuicide("All of the sudden, a clumsy step sends the player " +
                  "tumbling down a shallow easterly hill. Sheer unluck sends " +
                  "the player straight into the open mouth of a nearby " +
                  "yawning python. You are dead.")
        return ""



class For_Forest(Furniture):
    def __init__(self):
        super(For_Forest,self).__init__()
        
        self.description = ("The woods are dark and spooky. What did you expect?")
        self.searchDialog = self.actDialog = ("Rest assured there is absolutely nothing there.")
        self.addNameKeys("forest", "woods")
        self.addActKeys("explore")



class For_Thicket(Furniture):
    def __init__(self):
        super(For_Thicket,self).__init__()
        
        self.description = ("Just unsightly brambles. Definitely not relevent to the plot in any way.")
        self.searchDialog = ("There's absolutely nothing there.")
        self.addNameKeys("(?:impenetrable )?thicket", "(?:unsightly )?brambles")



class For_Trees(Furniture, Unmoveable):
    def __init__(self):
        super(For_Trees,self).__init__()
        
        self.description = ("Glorious, majestic trees are scattered all over. " +
                  "As much as you wish to coninually admire, you cannot draw " +
                  "your attention from the castle back north.")
        self.actDialog = ("There is nothing up there. There is just really nothing up there.")
        self.searchDialog = ("You find exactly nothing. Let us stroll back to the the castle now.")

        self.addNameKeys("trees?")
        self.addActKeys("climb")