from Player import Player
from Foyer import LootSack
from Lichs_Quarters import Lich_Room
from Room import Room
import Id

class Endg(Room): 
    def __init__(self, name, ID): 
        super(Endg, self).__init__(name, ID)
    
    def getDescription(self): 
        if not (Player.hasVisited(Id.COU3) or Player.getLastVisited() == Id.FOR1): 
            return ""
        else:
            return super(Endg, self).getDescription()
    
    def triggeredEvent(self): 
        if not Player.hasVisited(Id.COU3): 
            # If player is disobedient at the game's start.
            Player.setOccupies(Id.FOR1)
            return ""
        
        AudioPlayer.playTrack(Id.SOUL)
        GUI.clearDialog()
        GUI.menOut(Menus.ENTER)
        GUI.invOut("")
        GUI.promptOut()
        
        lichDead = Player.getRoomObj(Id.LQU1).lichIsDead()
        message, finalMsg = "", ""
        score = Player.getScore()
        t, p = 0, Player.getInv().countPhylacteries()
        
        if Player.hasItem(Names.LOOT_SACK): 
            sack = Player.getInv().get(Names.LOOT_SACK)
            p  = sack.countPhylacteries()
            t  = sack.countTreasures()
        
        if score >= 19000:
            message = "Your wealth transcends all understanding that exists."
        elif score >= 15000:
            message = ("You possess the wealth, cunning, and power to overcome " +
                      "any holy or unholy force that dare challenge you.")
        elif score >= 13000:
            message = ("Your wealth is beyond the dreams of avarice and " +
                      "will earn you a divine seat in the afterlife.")
        elif score >= 11000:
            message = "Your wealth is legendary and would bring a tear to Plutus' eye."
        elif score >= 9000:
            message = ("Your wealth is nearly insurmountable and would " +
                      "stun any man, woman, and God alike.")
        elif score >= 7750:
            message = ("Your wealth is nearly insurmountable and would " +
                      "stun all men and women alike.")
        elif score >= 6500:
            message = ("You have amassed a grand fortune which will certainly " +
                      "grant you any Earthly desire.")
        elif score >= 5250:
            message = ("You have amassed a grand fortune which instills fear in " +
                      "all kings and queens.")
        elif score >= 4000:
            message = "Your riches would earn you the respect of many kings."
        elif score >= 2750:
            message = "You are a top contender in the hunt for treasure."
        elif score >= 1500:
            message = ("You're skilled in the hunt for treasure, though " +
                      "you have such a long way to go.")
        elif score >= 750:
            message = ("Your eye for wealth is strong. You will likely have much " +
                      "to pawn off, should you return.")
        elif score >= 500:
            message = ("You abide by your manly ethics to work hard and provide " +
                      "for your family. Although, the thought of wealth visits you frequently.")
        elif score >= 250:
            message = ("You are rich in character, a True fortune to be respected. " +
                      "Material possessions are secondary, of course.")
        elif score >= 0:
            message = "You have a humble spirit, and long not for possessions."
        else:
            message = "You have eccentric, perplexing tastes."
        
        if p > 0:
            message = (" Watch yourself, for you hold the soul of a powerful mage, " +
                      "and it may warp you the same way it did him.")
        
        suff = (" and all 5 of the phylacteries. " if lichDead else ". ")

        finalMsg = ("Evaluation: Your score is " + str(score) + ". You have " +
                    "discovered " + str(t) + " out of 15 legendary treasures" + suff + message)
        
        GUI.out(finalMsg)
        GUI.promptOut()

        # Exits the game after player types enter.
        Player.eraseGame()
        Player.endGameProcedure()
        exit(0)