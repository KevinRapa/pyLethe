# Room images are located here.

# MAP LABELS AND FRAMES

# SET MAP FRAME ATTRBITUS

def disposeMap():
    pass

"""
    Displays a map for when the player enters 'm'.
    Displays current floor.
"""
def displayMap():
    pass
    """
    updateMap()

    if ! MAP_FRAME.isVisible()) {
        GUI.out("Enter 'close' to hide the map.")
        AudioPlayer.playEffect(2)
        MAP_FRAME.setVisible(True)
    }
    else {
        MAP_FRAME.toFront()
    }
    }

    static void hideMap() {
    MAP_FRAME.setVisible(False)
    }

    static void disposeMap() {
    # Disposes map on game's end
    MAP_FRAME.setVisible(False)
    MAP_FRAME.dispose()
    """

"""
    Displays a new image in the map frame depending on the player's position.
"""
def updateMap():
    pass
    """
    ImageIcon icon
    String id = Player.getPosId()

    if Player.getCurrentFloor() == 6) {
        if id.equals(Id.MS65) || id.equals(Id.MS66))
            icon = ImageIcon(PATH   "MS" + EXT)
        else    
            icon = ImageIcon(PATH   "CAVE" + EXT)
    }
    else {
        icon = ImageIcon(PATH + id + EXT)
        
        if icon.getImage().getWidth(MAP_LABEL) == -1)
            # Room does not have an associated picture.
            icon = ImageIcon(PATH + UNKN + EXT)
    }

    MAP_LABEL.setIcon(icon)
    MAP_FRAME.pack()
    """
