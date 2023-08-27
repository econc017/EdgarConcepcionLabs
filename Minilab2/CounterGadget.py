from Buzzer import *
from Button import *
from Displays import *
import time

class CounterGadget:
    """
    This is the class for the counter gadget that can count up,
    reset, and display a count on an LCD.
    """

    def __init__ (self):
        self._number = 0
        self._display = LCDDisplay(sda = 0, scl = 1, i2cid = 0)
        self._buzzer = PassiveBuzzer(15)
        self._buttonUp = Button(17, "up", buttonhandler=self)
        self._buttonReset = Button(16, "reset", buttonhandler=self)
        self.display()
        self._buzzer.setVolume(50)

    def increment(self):
        """ Add one to the number attribute, and play a high pitch sound """

        self._number += 1
        self._buzzer.beep(tone=659, duration=50)

    def reset(self):
        """ Reset the number attribute, and play low pitch sound """

        self._number = 0
        self._buzzer.beep(tone=330, duration=50)

    def display(self):
        """ Show the number on the display """

        self._display.showNumber(self._number)

    def run(self):
        """ Keep this app running so it does not stop """

        while True:
            time.sleep(0.5)

    def buttonPressed(self, name):
        """ Handle the button presses """
        if name == "up":
            self.increment()
        elif name == "reset":
            self.reset()
        self.display()

    def buttonReleased(self, name):
        """ Handle button releases """
        pass