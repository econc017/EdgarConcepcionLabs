import random
from Lights import Light
import time
from Button import *
from Buzzer import PassiveBuzzer
from Displays import LCDDisplay

"""An instance of the memory game... Initiating all attributes"""
class MemoryGame:
    def __init__ (self):
        self._lights = [Light(1, "yellow"),Light(2, "green"),Light(3, "blue"),Light(4, "red")]
        self._roundNumber = 1
        self._numberRange = range(4)
        self._lost = False
        self._yellowB = Button(28, "yellow", buttonhandler=self)
        self._greenB = Button(27, "green", buttonhandler=self)
        self._blueB = Button(26, "blue", buttonhandler=self)
        self._redB = Button(22, "red", buttonhandler=self)
        self._buzzer = PassiveBuzzer(15)
        self._display = LCDDisplay(sda = 16, scl = 17, i2cid = 0)

    """Gameplay loop logic"""
    def play(self):
        """While the player hasn't lost yet, continue increasing the rounds and play again"""
        while not self._lost:
            """Creates an array of random LEDs to turn on and stores it so that the player can try to replicate that pattern"""
            ledArray = [random.choice(self._numberRange) for _ in range(self._roundNumber)]
            #print(f"Array of numbers: {ledArray}")
            for i in ledArray:
                self._lights[i].on()
                time.sleep(1)
                self._lights[i].off()

            """Logic for button checks here"""

            self._roundNumber += 1
            time.sleep(5)

    """Helper method for me to test the light functionality"""
    def _testLights(self):
        counter = 0
        while True:
            self._lights[counter].on()
            time.sleep(0.5)
            self._lights[counter].off()
            counter += 1
            counter %= 4

    """Button Press logic"""
    def buttonPressed(self, name):
        """ Handle the button presses """
        if name == "yellow":
            self._display.showText("                   ")
            self._display.showText("Yellow")
            print("yellowPressed")
            self._buzzer.beep(tone=259, duration=60)
        elif name == "green":
            self._display.showText("                   ")
            self._display.showText("Green")
            print("greenPressed")
            self._buzzer.beep(tone=459, duration=60)
        elif name == "blue":
            self._display.showText("                   ")
            self._display.showText("Blue")
            print("bluePressed")
            self._buzzer.beep(tone=659, duration=60)
        elif name == "red":
            self._display.showText("                   ")
            self._display.showText("Red")
            print("redPressed")
            self._buzzer.beep(tone=859, duration=60)

    """Takes care of the button release"""
    def buttonReleased(self, name):
        """ Handle button releases """
        pass