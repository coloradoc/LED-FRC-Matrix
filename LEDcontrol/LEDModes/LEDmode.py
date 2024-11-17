class LEDmode:
    """ 
    A general-purpose class for managing LED modes.
    """

    def startup(self):
        """ Called once when the mode is first activated. """
        pass


    def periodic(self) -> bool:
        """ Called repeatedly by the main file. Returns True if the mode has finished. """
        pass


    def onEnd(self):
        """ Called once when the mode is supposed to stop. """
        pass
