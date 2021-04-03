
import pyautogui as gui

class Move():
    
    def __init__(self):

        self.mouseHStep = 150
        self.mouseVStep = 140
        gui.FAILSAFE = False

    def move(self, angles):
        if angles[1] < -10.0:
            gui.moveRel(-self.mouseHStep, 0)
        elif angles[1] > 7.0:
            gui.moveRel(self.mouseHStep, 0)
        if angles[0] < -10.0:
            gui.moveRel(0, self.mouseVStep)
        elif angles[0] > 7.0:
            gui.moveRel(0, -self.mouseVStep)
