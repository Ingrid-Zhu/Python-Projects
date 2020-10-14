"""
Primary module for Alien Invaders

This module contains the main controller class for the Alien Invaders app.
There is no need for any additional classes in this module.  If you need
more classes, 99% of the time they belong in either the wave module or the
models module. If you are unsure about where a new class should go, post a
question on Piazza.

# Yan Zhu yz2477
# 12/10/2019
"""
from consts import *
from game2d import *
from wave import *


# PRIMARY RULE: Invaders can only access attributes in wave.py via getters/setters
# Invaders is NOT allowed to access anything in models.py

class Invaders(GameApp):
    """
    The primary controller class for the Alien Invaders application

    This class extends GameApp and implements the various methods necessary
    for processing the player inputs and starting/running a game.

        Method start begins the application.

        Method update either changes the state or updates the Play object

        Method draw displays the Play object and any other elements on screen

    Because of some of the weird ways that Kivy works, you SHOULD NOT create
    an initializer __init__ for this class.  Any initialization should be done
    in the start method instead.  This is only for this class.  All other
    classes behave normally.

    Most of the work handling the game is actually provided in the class Wave.
    Wave should be modeled after subcontrollers.py from lecture, and will
    have its own update and draw method.

    The primary purpose of this class is to manage the game state: which is
    when the game started, paused, completed, etc. It keeps track of that in
    an internal (hidden) attribute.

    For a complete description of how the states work, see the specification
    for the method update.

    Attribute view: the game view, used in drawing
    Invariant: view is an instance of GView (inherited from GameApp)

    Attribute input: user input, used to control the ship or resume the game
    Invariant: input is an instance of GInput (inherited from GameApp)
    """
    # HIDDEN ATTRIBUTES:
    # Attribute _state: the current state of the game represented as an int
    # Invariant: _state is one of STATE_INACTIVE, STATE_NEWWAVE, STATE_ACTIVE,
    # STATE_PAUSED, STATE_CONTINUE, or STATE_COMPLETE
    #
    # Attribute _wave: the subcontroller for a single wave, managing aliens
    # Invariant: _wave is a Wave object, or None if there is no wave currently
    # active. It is only None if _state is STATE_INACTIVE.
    #
    # Attribute _text: the currently active message
    # Invariant: _text is a GLabel object, or None if there is no message to
    # display. It is onl None if _state is STATE_ACTIVE.
    #
    # You may have new attributes if you wish (you might want an attribute to
    # store any score across multiple waves). But you must document them.

    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY

    # DO NOT MAKE A NEW INITIALIZER!

    # THREE MAIN GAMEAPP METHODS
    def start(self):
        """
        Initializes the application.

        This method is distinct from the built-in initializer __init__ (which
        you should not override or change). This method is called once the
        game is running. You should use it to initialize any game specific
        attributes.

        This method should make sure that all of the attributes satisfy the
        given invariants. When done, it sets the _state to STATE_INACTIVE and
        create a message (in attribute _text) saying that the user should press
        to play a game.
        """
        self._wave = None
        self._state = 0

    def update(self,dt):
        """
        Animates a single frame in the game.

        It is the method that does most of the work. It is NOT in charge of
        playing the game.  That is the purpose of the class Wave. The primary
        purpose of this game is to determine the current state, and -- if the
        game is active -- pass the input to the Wave object _wave to play the
        game.

        As part of the assignment, you are allowed to add your own states.
        However, at a minimum you must support the following states:
        STATE_INACTIVE, STATE_NEWWAVE, STATE_ACTIVE, STATE_PAUSED,
        STATE_CONTINUE, and STATE_COMPLETE.  Each one of these does its own
        thing and might even needs its own helper.  We describe these below.

        STATE_INACTIVE: This is the state when the application first opens.
        It is a paused state, waiting for the player to start the game.  It
        displays a simple message on the screen. The application remains in
        this state so long as the player never presses a key.  In addition,
        this is the state the application returns to when the game is over
        (all lives are lost or all aliens are dead).

        STATE_NEWWAVE: This is the state creates a new wave and shows it on
        the screen. The application switches to this state if the state was
        STATE_INACTIVE in the previous frame, and the player pressed a key.
        This state only lasts one animation frame before switching to
        STATE_ACTIVE.

        STATE_ACTIVE: This is a session of normal gameplay.  The player can
        move the ship and fire laser bolts.  All of this should be handled
        inside of class Wave (NOT in this class).  Hence the Wave class
        should have an update() method, just like the subcontroller example
        in lecture.

        STATE_PAUSED: Like STATE_INACTIVE, this is a paused state. However,
        the game is still visible on the screen.

        STATE_CONTINUE: This state restores the ship after it was destroyed.
        The application switches to this state if the state was STATE_PAUSED
        in the previous frame, and the player pressed a key. This state only
        lasts one animation frame before switching to STATE_ACTIVE.

        STATE_COMPLETE: The wave is over, and is either won or lost.

        You are allowed to add more states if you wish. Should you do so, you should
        describe them here.

        STATE_WIN: This state announces that the player win the game when all
        aliens are destroyed before they reach the defence line and the player
        is still alive.

        STATE_LOSE: This state announces that the player lose the game when alien(s)
        cross the defence line or the player lost all live before clear all
        aliens.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        self._DetermineState()
        self._NewWAVE()
        self._Active(dt)
        self._Resume()

    def draw(self):
        """
        Draws the game objects to the view.

        Every single thing you want to draw in this game is a GObject.  To
        draw a GObject g, simply use the method g.draw(self.view).  It is
        that easy!

        Many of the GObjects (such as the ships, aliens, and bolts) are
        attributes in Wave. In order to draw them, you either need to add
        getters for these attributes or you need to add a draw method to
        class Wave.  We suggest the latter.  See the example subcontroller.py
        from class.
        """
        GRectangle(x = 400,y=400,width=800,height=800,
                    fillcolor='navy').draw(self.view)
        if self._state == STATE_INACTIVE:
            self._text = GLabel(text="Press S to Play",font_size = 70,font_name
                        ='Arcade',x = 400,y = 400,linecolor = 'white')
            self._text.draw(self.view)
        if self._state == STATE_ACTIVE:
            self._wave.draw(self.view)
            self._text = GLabel(text="Press F/O to turn off/on the music",
            font_size=20,font_name='ComicSans',x=620,y=680,linecolor='grey')
            self._text.draw(self.view)
        if self._state== STATE_PAUSED:
            self._text = GLabel(text= "You are Still Alive!",font_size = 65,
                        font_name='Arcade',x = 400,y =400,linecolor='yellow')
            self._text2 = GLabel(text = "Press C to continue", font_size = 55,
                        font_name ='Arcade',x = 400,y = 330,linecolor ='yellow')
            self._text.draw(self.view)
            self._text2.draw(self.view)
        if self._state == STATE_WIN:
            self._text = GLabel(text = "Congratulation!", font_size = 65,
                        font_name='Arcade',x = 400,y = 400,linecolor='pink')
            self._text2 = GLabel(text= "You have finished the game :)",font_size=55,
                        font_name = 'Arcade',x = 400,y = 350,linecolor='pink')
            self._text.draw(self.view)
            self._text2.draw(self.view)
        if self._state == STATE_LOSE:
            self._text = GLabel(text = "Oops, You Lost :(", font_size = 80,
                        font_name ='Arcade',x = 400,y = 400,linecolor ='green')
            self._text.draw(self.view)

    # HELPER METHODS FOR THE STATES GO HERE
    def _DetermineState(self):
        """
        Determines the current state and make change when necessary

        Checks if a key is pressed for the first time and changes
        the state, back ground music accordingly
        """
        curr_keys = self.input.key_count
        change = curr_keys > 0 and self.input.is_key_down('s') == True
        if change and self._state == STATE_INACTIVE:
            self._state = STATE_NEWWAVE
            self._text = None 
        change2 = self.input.is_key_down('c') == True
        if change2 and self._state == STATE_PAUSED:
            self._wave._shouldPause = False
            self._state = STATE_CONTINUE
            self._text= None   
        change3 = self.input.is_key_down('f') == True
        if change3 and self._state == STATE_ACTIVE:
            self._wave._bgmstop = True      
        change4 = self.input.is_key_down('o') == True
        if (change4 and self._wave._bgmstop == True 
            and self._state == STATE_ACTIVE):
            self._wave._bgmstop = False

    def _NewWAVE(self):
        '''
        Make change to the game state

        Modifies the view (draw method) and the state of alien waves
        and game state when the current state is STATE_NEWWAVE
        '''
        if self._state == STATE_NEWWAVE:
            self._text = None
            self._wave = Wave()
            self._state=STATE_ACTIVE

    def _Active(self,dt):
        '''
        Make change to the game state

        Modifies the the state of alien waves and the game state
        when the current state is STATE_ACTIVE, and discuss the
        appropriate state to change to by looking at methods in
        Wave which check if the aliens are all destroyed(win),
        the player has lost his/her life (pause), or the player has
        no live or the aliens cross the defence line before the player
        is able to clear them all (lose)
        '''
        if self._state == STATE_ACTIVE:
            self._wave.update(self.input,dt)
            if self._wave._AlienClear() == True:
                self._state = STATE_WIN
            elif self._wave._shouldPause == True:
                self._state = STATE_PAUSED
                self._DetermineState()
            elif self._wave._founddeath() == True or self._wave._AlienCrossedDL():
                self._state = STATE_LOSE
        
    def _Resume(self):
        '''
        Make change to the game state 

        Modify the state of the game to active state to continue 
        the game at where it is at before pausedand restore a 
        new ship for the game.
        '''
        if self._state == STATE_CONTINUE:
            self._wave._ship = Ship()
            self._state = STATE_ACTIVE
