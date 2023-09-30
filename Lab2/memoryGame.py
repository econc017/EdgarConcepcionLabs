"""
A basic template file for using the Model class in PicoLibrary
This will allow you to implement simple Statemodels with some basic
event-based transitions.

Currently supports only 4 buttons (hardcoded to BTN1 through BTN4)
and a TIMEOUT event for internal tranisitions.

For processing your own events such as sensors, you can implement
those in your run method for transitions based on sensor events.
"""

# Import whatever Library classes you need - Model is obviously needed
import time
import random
from Model import *
from Button import *
from Counters import *
from Lights import Light
from Buzzer import PassiveBuzzer
from Displays import LCDDisplay

"""
This is the template Model Runner - you should rename this class to something
that is supported by your class diagram. This should associate with your other
classes, and any PicoLibrary classes. If you are using Buttons, you will implement
buttonPressed and buttonReleased.

To implement the model, you will need to implement 3 methods to support entry actions,
exit actions, and state actions.

This template currently implements a very simple state model that uses a button to
transition from state 0 to state 1 then a 5 second timer to go back to state 0.
"""

class MemoryGame:

    def __init__(self):
        
        # Instantiate whatever classes from your own model that you need to control
        # Handlers can now be set to None - we will add them to the model and it will
        # do the handling
        self._lights = [Light(1, "yellow"),Light(2, "green"),Light(3, "blue"),Light(4, "red")]
        self._roundNumber = 0
        self._numberRange = range(4)
        self._ledArray = []
        self._score1 = 0
        self._score2 = 0
        self._counter = 1
        self._index = 0
        self._timer = SoftwareTimer(None)
        self._yellowB = Button(28, "yellow", buttonhandler=self)
        self._greenB = Button(27, "green", buttonhandler=self)
        self._blueB = Button(26, "blue", buttonhandler=self)
        self._redB = Button(22, "red", buttonhandler=self)
        self._buzzer = PassiveBuzzer(15)
        self._display = LCDDisplay(sda = 16, scl = 17, i2cid = 0)
        
        # Instantiate a Model. Needs to have the number of states, self as the handler
        # You can also say debug=True to see some of the transitions on the screen
        # Here is a sample for a model with 4 states
        self._model = Model(5, self, debug=True)
        
        # Up to 4 buttons and a timer can be added to the model for use in transitions
        # Buttons must be added in the sequence you want them used. The first button
        # added will respond to BTN1_PRESS and BTN1_RELEASE, for example
        self._model.addButton(self._yellowB)
        self._model.addButton(self._greenB)
        self._model.addButton(self._blueB)
        self._model.addButton(self._redB)
        
        # Add any timer you have.
        self._model.addTimer(self._timer)
        
        # Now add all the transitions that are supported by my Model
        # obvously you only have BTN1_PRESS through BTN4_PRESS
        # BTN1_RELEASE through BTN4_RELEASE
        # and TIMEOUT
        
        # some examples:
        self._model.addTransition(0, [BTN1_PRESS], 1)
        self._model.addTransition(4, [TIMEOUT], 0)
        # etc.
    
    """
    Create a run() method - you can call it anything you want really, but
    this is what you will need to call from main.py or someplace to start
    the state model.
    """
    def run(self):
        # The run method should simply do any initializations (if needed)
        # and then call the model's run method.
        # You can send a delay as a parameter if you want something other
        # than the default 0.1s. e.g.,  self._model.run(0.25)
        self._model.run()

    """
    stateEntered - is the handler for performing entry/actions
    You get the state number of the state that just entered
    Make sure actions here are quick
    """
    def stateEntered(self, state, event):
        # Again if statements to do whatever entry/actions you need
        if state == 0:
            # entry actions for state 0
            print('State 0 entered')
            self._score1 = 0
            self._score2 = 0
            self._roundNumber = 0
            self._counter = 1
            self._index = 0
            self._buzzer.setVolume = 1
        elif state == 1:
            # entry actions for state 1
            print('State 1 entered')
            time.sleep(1)
            self._buzzer.setVolume = 5
            self._index = 0
            time.sleep(0.1)
            self._roundNumber = self._roundNumber+1
            #Create an array of random LEDs to turn on and stores it so that the player can try to replicate that pattern
            self._ledArray = [random.choice(self._numberRange) for _ in range(self._roundNumber)]
        elif state == 2:
            # entry actions for state 2
            print('State 2 entered')
            self._index = 0
        elif state == 3:
            # entry actions for state 3
            print('State 3 entered')
            self._index = 0
            pass
        elif state == 4:
            # entry actions for state 4
            print('State 4 entered')
            self._timer.start(10)
            self._index = 0

    """
    stateDo - the method that handles the do/actions for each state
    """
    def stateDo(self, state):
        # Now if you want to do different things for each state you can do it:
        if state == 0:
            # State 0 do/actions
            self._lights[self._counter-1].on()
            #time.sleep(0.2)
            if self._counter == 1:
                self._buzzer.beep(tone=259, duration=100)
            elif self._counter == 2: 
                self._buzzer.beep(tone=459, duration=100)
            elif self._counter == 3:
                self._buzzer.beep(tone=659, duration=100)
            elif self._counter == 4:
                self._buzzer.beep(tone=859, duration=100)
            self._lights[self._counter-1].off()
            self._counter += 1
            if self._counter > 4:
                self._counter = 1
        elif state == 1:
            # State1 do/actions
            # You can check your sensors here and perform transitions manually if needed
            # For example, if you want to go from state 1 to state 2 when the motion sensor
            # is tripped you can do something like this
            # if self.motionsensor.tripped():
            # 	gotoState(2)
            print(f"Index: {self._index}")
            # Flashes pattern of lights once along with the sound.
            self._lights[self._ledArray[self._index]].on()
            if self._ledArray[self._index] == 0:
                self._buzzer.beep(tone=259, duration=500)
            elif self._ledArray[self._index] == 1: 
                self._buzzer.beep(tone=459, duration=500)
            elif self._ledArray[self._index] == 2:
                self._buzzer.beep(tone=659, duration=500)
            elif self._ledArray[self._index] == 3:
                self._buzzer.beep(tone=859, duration=500)
            time.sleep(0.1)
            self._lights[self._ledArray[self._index]].off()
            if self._index >= self._roundNumber-1:
                self._model.gotoState(2)
            # Display scores:
            self._display.showText(f"Player 1:{self._score1}\nPlayer 2:{self._score2}")
            
    """
    stateLeft - is the handler for performing exit/actions
    You get the state number of the state that just entered
    Make sure actions here are quick
    
    This is just like stateEntered, perform only exit/actions here
    """
    def stateLeft(self, state, event):
        if state == 0:
            # Exit actions for state 0
            print('State 0 Left')
            self._counter = 1
        elif state == 1:
            # Exit actions for state 1
            print('State 1 Left')
        elif state == 2:
            # Entry actions for state 2
            print('State 2 Left')
        elif state == 3:
            # Entry actions for state 3
            print('State 3 Left')
        elif state == 4:
            # Entry actions for state 4
            print('State 4 Left')
            self._timer.cancel()
            self._counter = 1

    

# Test your model. Note that this only runs the template class above
# If you are using a separate main.py or other control script,
# you will run your model from there.
if __name__ == '__main__':
    MyControllerTemplate().run()