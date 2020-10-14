"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in
the Alien Invaders game.  Instances of Wave represent a single wave. Whenever
you move to a new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on
screen. These are model objects.  Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or
models.py. Whether a helper method belongs in this module or models.py is
often a complicated issue.  If you do not know, ask on Piazza and we will
answer.

# Yan Zhu yz2477
# 12/10/2019
"""
from game2d import *
from consts import *
from models import *
import random

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)


class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.

    This subcontroller has a reference to the ship, aliens, and any laser bolts
    on screen. It animates the laser bolts, removing any aliens as necessary.
    It also marches the aliens back and forth across the screen until they are
    all destroyed or they reach the defense line (at which point the player
    loses). When the wave is complete, you  should create a NEW instance of
    Wave (in Invaders) if you want to make a new wave of aliens.

    If you want to pause the game, tell this controller to draw, but do not
    update.  See subcontrollers.py from Lecture 24 for an example.  This
    class will be similar to than one in how it interacts with the main class
    Invaders.

    All of the attributes of this class are to be hidden. You may find that
    you want to access an attribute in class Invaders. It is okay if you do,
    but you MAY NOT ACCESS THE ATTRIBUTES DIRECTLY. You must use a getter
    and/or setter for any attribute that you need to access in Invaders.
    Only add the getters and setters that you need for Invaders. You can keep
    everything else hidden.

    """
    # HIDDEN ATTRIBUTES:
    # Attribute _ship: the player ship to control
    # Invariant: _ship is a Ship object or None
    #
    # Attribute _aliens: the 2d list of aliens in the wave
    # Invariant: _aliens is a rectangular 2d list containing Alien objects or None
    #
    # Attribute _bolts: the laser bolts currently on screen
    # Invariant: _bolts is a list of Bolt objects, possibly empty
    #
    # Attribute _dline: the defensive line being protected
    # Invariant : _dline is a GPath object
    #
    # Attribute _lives: the number of lives left
    # Invariant: _lives is an int >= 0
    #
    # Attribute _time: the amount of time since the last Alien "step"
    # Invariant: _time is a float >= 0s
    #
    # You may change any attribute above, as long as you update the invariant
    # You may also add any new attributes as long as you document them.
    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY

    # Attribute _direction: tracting the movement of the aliens, return True
    # if the current direction is right and False otherwise
    # Invariant: _direction is a bool

    # Attribute _rfire: the rate of aliens firing the bolt
    # Invariant: _rfire is an int > 0

    # Attribute _asteps: the steps that aliens have moved since last fire
    # Invariant: _asteps is an int >= 0

    # Attribute _shouldPause: return True if the player lost a life and the game
    # should pause False otherwise
    # Invariant: _shouldPause is a bool

    # Attribute _dead: return True if self._live == 0, False other wise
    # Invariant: _dead is a bool

    # Attribute _bgm: the sound that is played at given time
    # Invariant: _bgm is a list

    # Attribute _bgmstop: check if current bgm is on or off
    # Invariant: _bgmstop is a bool

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)

    # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS
    def __init__(self):
        '''
        Initialize the Ship, a new wave of Aliens, and all other attributes.
        '''
        self._aliens = self._newAliens()
        self._ship = Ship()
        self._dline = GPath(points = [0,80,800,80],
                            linewidth = 2, linecolor = 'white')
        self._bolts = []
        self._lives = SHIP_LIVES
        self._time = 0
        self._direction = True
        self._rfire = random.randint(1,BOLT_RATE)
        self._asteps = 0
        self._shouldPause = False
        self._dead = False
        self._bgm = [Sound('pew2.wav'),Sound('blast1.wav'),Sound('pop2.wav')]
        self._bgm[0].volume = 0.4
        self._bgm[1].volume = 0.3
        self._bgm[2].volume = 0.4
        self._bgmstop = False

    # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS
    def update(self,input,dt):
        '''
        Update the state of the Ship and Alien per animatiion frame
        The method determines the movement of ship, aliens and bolts
        and pass them to the update method in app.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        '''
        self._ShipMovement(input)
        self._AliensMovement(dt)
        self._ShBolt(input)
        self._AlBolt()
        self._removeBolt()
        self._Boltsmove()
        self._Collision()
        self._founddeath()

    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw(self,view):
        '''
        Draws the game objects (ship, defence line, aliens, bolt) to the view.
        '''
        for row in self._aliens:
            for alien in row:
                if alien != None:
                    alien.draw(view)
        if self._ship != None:
            self._ship.draw(view)
        self._dline.draw(view)

        if len(self._bolts) > 0:
            for b in self._bolts:
                b.draw(view)

    # METHODS
    def _newAliens(self):
        '''
        Return the 2-D list of Alien.

        The Aliens are positioned at certain distance from each other from bottom
        to the top with 3 different image for different rows of aliens.
        '''
        x = ALIEN_H_SEP + 0.5*ALIEN_WIDTH
        y = (GAME_HEIGHT - ALIEN_CEILING - (0.5*ALIEN_HEIGHT)
            - (ALIEN_ROWS-1)*ALIEN_HEIGHT - (ALIEN_ROWS-1)*ALIEN_V_SEP)
        aliens = []
        rolnum = 0
        for row in range(ALIEN_ROWS):
            row = []
            rolnum = rolnum +1
            for alien in range(ALIENS_IN_ROW):
                alien = Alien(x, y, self._alienImage(rolnum))
                row.append(alien)
                x = x + ALIEN_H_SEP + ALIEN_WIDTH
            aliens.append(row)
            x = ALIEN_H_SEP + 0.5*ALIEN_WIDTH
            y = y + ALIEN_V_SEP + ALIEN_HEIGHT
        return aliens

    def _alienImage(self,rolnum):
        '''
        Return the image to be used for this row of Aliens.

        It should be using the same image for each 2 adjacent rows from
        the bottom to the top.

        Parameter rolnum: the number of row
        Precondition: rolnum is an int, 0 < rolnum <= ALIEN_ROWS
        '''
        if rolnum%6 == 1 or rolnum%6 == 2:
            return ALIEN_IMAGES[0]
        elif rolnum%6 == 3 or rolnum%6 == 4:
            return ALIEN_IMAGES[1]
        elif rolnum%6 == 5 or rolnum%6 == 0:
            return ALIEN_IMAGES[2]

    def _ShipMovement(self,input):
        '''
        Control the direction of player's ship movement.

        Move the ship leftward everytime the player presses the left arrow
        on the keyboard and move the ship rightward when the player presses
        the right arrow.
        '''
        if input.is_key_down('left'):
            self._ship.x = max(self._ship.x - SHIP_MOVEMENT,(0.5*SHIP_WIDTH))
        if input.is_key_down('right'):
            self._ship.x = min(self._ship.x + SHIP_MOVEMENT,
                                GAME_WIDTH-(0.5*SHIP_WIDTH))

    def _AliensMovement(self,dt):
        '''
        Control the direction of aliens' movement.

        Move the Aliens from left to right initially and change to opposite
        direction every time the leftmost/rightmost alien(s) reaches the
        left/right edge.

        When the leftmost/rightmost alien(s) hit the left/right edge, the
        whole group of aliens should be moving downward.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        '''
        if self._direction:
            self._AliensmoveRight(dt)
        if self._direction and (GAME_WIDTH - self._RightMostA()
                                <= ALIEN_H_SEP + 0.5*ALIEN_WIDTH):
            self._direction = False
            self._AliensgoDown()
        if self._direction == False:
            self._AliensmoveLeft(dt)
        if self._direction == False and self._LeftMostA() <= (ALIEN_H_SEP
                                                        + 0.5*ALIEN_WIDTH):
            self._direction = True
            self._AliensgoDown()

    def _LeftMostA(self):
        '''
        Return the x coordinate of the leftmost alien(s).

        To get the leftmost position and help determine if any of the aliens
        is too close to the edge and change direction accordingly.
        '''
        left = GAME_WIDTH
        for row in self._aliens:
                for alien in row:
                    if alien != None:
                        if alien.get_x() < left:
                            left = alien.get_x()
        return left

    def _RightMostA(self):
        '''
        Return the x coordinate of the rightmost alien(s).

        To get the rightmost position and help determine if any of the aliens
        is too close to the edge and change direction accordingly.
        '''
        right = 0
        for row in self._aliens:
            for alien in row:
                if alien != None:
                    if alien.get_x() > right:
                        right = alien.get_x()
        return right

    def _AliensmoveRight(self,dt):
        '''
        Move the alien(s) to right.

        Move the aliens when the number of seconds since the last step
        are bigger than ALIEN_SPEED, and move them rightward when their
        current direction is right.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        '''
        self._time =  self._time + dt
        if self._time > ALIEN_SPEED:
            self._asteps = self._asteps + 1
            for row in self._aliens:
                for alien in row:
                    if alien != None:
                            alien.setRight()
            self._time = 0

    def _AliensmoveLeft(self,dt):
        '''
        Move the alien(s) to left.

        Move the aliens when the number of seconds since the last step
        are bigger than ALIEN_SPEED, and move them leftward when their
        current direction is left.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        '''
        self._time =  self._time + dt
        if self._time > ALIEN_SPEED:
            self._asteps = self._asteps + 1
            for row in self._aliens:
                for alien in row:
                    if alien != None:
                        alien.setLeft()
            self._time = 0

    def _AliensgoDown(self):
        '''
        Move the alien(s) down.

        Move the aliens down when the leftmost/rightmost alien(s) reach
        the left/right edge.
        '''
        for row in self._aliens:
            for alien in row:
                if alien != None:
                    alien.setDown()

    def _ShBolt(self,input):
        '''
        Create a laser bolt shooting from player's ship.

        Fire a bolt from the ship when there is no other laser bolt from
        the ship on the screen and when the player press the spacebar
        on their keyboard at the same time.
        '''
        fire = True
        for bolt in self._bolts:
            if bolt._isSBolt() == True:
                fire = False
        if fire == True and input.is_key_down('spacebar'):
            newB = Bolt(x = self._ship.x, y = self._ship.y + 0.5*BOLT_HEIGHT,
                        color = 'yellow', direction = 1)
            self._bolts.append(newB)
            if self._bgmstop != True:
                self._bgm[0].play()

    def _Boltsmove(self):
        '''
        Move the Bolts fire from aliens and the ship.

        Check each bolt in the list of bolts and move the bolt in
        the correct direction accordingly. If the bolt is from the player
        the y coordinate of the bolt shall be added with the velocity
        if the bolt. Otherwise if the bolt is from the alien, the y-
        coordinate of the bolt shall be subtracted from the velocity.
        '''
        if len(self._bolts) > 0:
            for bolt in self._bolts:
                if bolt._isSBolt() == True:
                    bolt.MoveSBolt()
                if bolt._isSBolt() == False:
                    bolt.MoveABolt()

    def _removeBolt(self):
        """
        Deletes a bolt if it goes off the screen.

        If the alien's bolts go below the bottom of the game screen,
        or if the player's bolts go beyond the upper edge of the screen,
        delete the bolts from the list.
        """
        bolt = 0
        activebolts = len(self._bolts)
        while bolt < activebolts:
            check = self._bolts[bolt]
            if (check.get_y() - 0.5*BOLT_HEIGHT >= GAME_HEIGHT
                or check.get_y() + 0.5*BOLT_HEIGHT < 0):
                self._bolts.pop(bolt)
                activebolts = activebolts - 1
            else:
                bolt = bolt + 1

    def _AlBolt(self):
        '''
        Create laser bolts shooting from the aliens.

        Pick a random column from available columns and fire a bolt from
        the alien with the lowest y position at that column. The bolt should
        be fire at random rate between 1 and BOLT_RATE, and should only be
        fired when the number of alien steps from last fire is equal to the
        number of the random number generated after each time the alien fire
        the bolt.
        '''
        if self._asteps == self._rfire:
            cols = []
            for row in range(len(self._aliens)):
                for col in range(len(self._aliens[row])):
                    if self._aliens[row][col] != None and col not in cols:
                        cols.append(col)
            firecol = random.randint(0,len(cols)-1)
            lowy = GAME_HEIGHT
            for row in range(len(self._aliens)):
                fighter = self._aliens[row][firecol]
                if fighter != None:
                    if fighter.get_y() < lowy:
                        lowy = fighter.get_y()
                    newB = Bolt(x = fighter.get_x(),y = lowy - 0.5*BOLT_HEIGHT,
                                color = 'red', direction = -1)
                    self._bolts.append(newB)
        self._asteps = 0
        self._rfire = random.randint(1,BOLT_RATE)

    def _Collision(self):
        '''
        Manage the player's live, bolts, and aliens after collision is found.

        Remove the bolt and the alien collided with that bolt if the bolt is
        from the ship and collision happened.
        Delete the bolt and subtract 1 life from the player's live if the
        bolt is from the aliens and collision happened.
        '''
        for bolt in self._bolts:
            if self._ship != None:
                if self._ship.collides(bolt) == True:
                    self._bolts.remove(bolt)
                    self._ship = None
                    self._lives = self._lives - 1
                    if self._lives > 0:
                        self._shouldPause = True
                    if self._bgmstop != True:
                        self._bgm[1].play()
                elif bolt._isSBolt():
                    for row in range(len(self._aliens)):
                        for col in range(len(self._aliens[row])):
                            alien = self._aliens[row][col]
                            if alien != None and alien.collides(bolt) == True:
                                self._aliens[row][col] = None
                                self._bolts.remove(bolt)
                                if self._bgmstop != True:
                                    self._bgm[2].play()

    def _AlienClear(self):
        '''
        Check if there is any alien left in the game.

        If there is no alien in this wave, return True as all
        aliens cleared by the player, False if there is still
        alien(s) left on the screen.
        '''
        cleared = True
        for row in self._aliens:
            for alien in row:
                if alien != None:
                    cleared = False
        return cleared

    def _AlienCrossedDL(self):
        '''
        Check if any alien cross the defence line.

        Check if any y-coordinate of the aliens is below the position
        of the defence line.
        '''
        lowy = GAME_HEIGHT
        for x in range(len(self._aliens)):
            for y in range(len(self._aliens[x])):
                alien = self._aliens[x][y]
                if alien != None:
                    if alien.get_y() < lowy:
                        lowy = alien.get_y()
        if lowy - 0.5*ALIEN_HEIGHT < DEFENSE_LINE:
            return True
        return False

    def _founddeath(self):
        '''
        Check if the player's ship is dead.

        If the player has no life anymore, it is determined that the
        game is over.
        '''
        if self._lives == 0:
            self._dead = True
        return self._dead