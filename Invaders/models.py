"""
Models module for Alien Invaders

This module contains the model classes for the Alien Invaders game. Anything
that you interact with on the screen is model: the ship, the laser bolts, and
the aliens.

Just because something is a model does not mean there has to be a special
class for it. Unless you need something special for your extra gameplay
features, Ship and Aliens could just be an instance of GImage that you move
across the screen. You only need a new class when you add extra features to
an object. So technically Bolt, which has a velocity, is really the only model
that needs to have its own class.

With that said, we have included the subclasses for Ship and Aliens. That is
because there are a lot of constants in consts.py for initializing the
objects, and you might want to add a custom initializer.  With that said,
feel free to keep the pass underneath the class definitions if you do not want
to do that.

You are free to add even more models to this module.  You may wish to do this
when you add new features to your game, such as power-ups.  If you are unsure
about whether to make a new class or not, please ask on Piazza.

# Yan Zhu yz2477
# 12/10/2019
"""
from consts import *
from game2d import *

# PRIMARY RULE: Models are not allowed to access anything in any module other
# than consts.py.  If you need extra information from Gameplay, then it should
# be a parameter in your method, and Wave should pass it as a argument when it
# calls the method.


class Ship(GImage):
    """
    A class to represent the game ship.

    At the very least, you want a __init__ method to initialize the ships
    dimensions. These dimensions are all specified in consts.py.

    You should probably add a method for moving the ship.  While moving a
    ship just means changing the x attribute (which you can do directly),
    you want to prevent the player from moving the ship offscreen.  This
    is an ideal thing to do in a method.

    You also MIGHT want to add code to detect a collision with a bolt. We
    do not require this.  You could put this method in Wave if you wanted to.
    But the advantage of putting it here is that Ships and Aliens collide
    with different bolts.  Ships collide with Alien bolts, not Ship bolts.
    And Aliens collide with Ship bolts, not Alien bolts. An easy way to
    keep this straight is for this class to have its own collision method.

    However, there is no need for any more attributes other than those
    inherited by GImage. You would only add attributes if you needed them
    for extra gameplay features (like animation).
    """
    #  IF YOU ADD ATTRIBUTES, LIST THEM BELOW

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)

    # INITIALIZER TO CREATE A NEW SHIP
    def __init__(self):
        '''
        Initialize the ship at the given coordinate of x and y.
        '''
        super().__init__(x= GAME_WIDTH/2, y= SHIP_BOTTOM , height=SHIP_HEIGHT,
                        width=SHIP_WIDTH, source= 'ship.png')
    # METHODS TO MOVE THE SHIP AND CHECK FOR COLLISIONS
    def collides(self,bolt):
        """
        Returns True if the bolt from alien collides with the ship.

        Parameter bolt: The laser bolt in the list
        Precondition: a bolt object of class Bolt
        """
        corners = []
        leftx = bolt.x - 0.5*BOLT_WIDTH
        upper = bolt.y + 0.5*BOLT_HEIGHT
        rightx = bolt.x + 0.5*BOLT_WIDTH
        lower = bolt.y - 0.5*BOLT_HEIGHT
        fir = [leftx,upper]
        sec = [rightx,upper]
        thi = [leftx,lower]
        fou = [rightx,lower]
        corners.append(fir)
        corners.append(sec)
        corners.append(thi)
        corners.append(fou)
        for c in corners:
            if self.contains(c) and bolt._isSBolt() == False:
                return True
        return False

    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


class Alien(GImage):
    """
    A class to represent a single alien.

    At the very least, you want a __init__ method to initialize the alien
    dimensions. These dimensions are all specified in consts.py.

    You also MIGHT want to add code to detect a collision with a bolt. We
    do not require this.  You could put this method in Wave if you wanted to.
    But the advantage of putting it here is that Ships and Aliens collide
    with different bolts.  Ships collide with Alien bolts, not Ship bolts.
    And Aliens collide with Ship bolts, not Alien bolts. An easy way to
    keep this straight is for this class to have its own collision method.

    However, there is no need for any more attributes other than those
    inherited by GImage. You would only add attributes if you needed them
    for extra gameplay features (like giving each alien a score value).
    """
    #  IF YOU ADD ATTRIBUTES, LIST THEM BELOW

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def get_x(self):
        """
        Returns the x coordinate of the alien
        """
        return self.x

    def setRight(self):
        """
        Sets a new x coordinate for the alien by adding certain distance
        to current position
        """
        self.x = self.x + ALIEN_H_WALK

    def setLeft(self):
        """
        Sets a new x coordinate for the alien by subtracting certain distance
        from current position
        """
        self.x = self.x - ALIEN_H_WALK

    def get_y(self):
        """
        Returns the y coordinate of the alien
        """
        return self.y

    def setDown(self):
        """
        Sets a new y coordinate for the alien by subtracting certain distance
        from current position
        """
        self.y = self.y - ALIEN_V_WALK

    # INITIALIZER TO CREATE AN ALIEN
    def __init__(self, x, y, source):
        """
        Initializes an alien with an image at a given coordinate of x and y

        Parameter x: the x coordinate of the alien
        Precondition: a number greater than 0 and less than GAME_WIDTH

        Parameter y: the y coorinate of the alien
        Precondition: a number less than GAME_HEIGHT and greater than the
        the y coordinate of the defence line

        Parameter source: the alien image
        Precondition: source is a jpg file
        """
        super().__init__(x = x, y = y, width = ALIEN_WIDTH,
                        height = ALIEN_HEIGHT, source = source)

    # METHOD TO CHECK FOR COLLISION (IF DESIRED)
    def collides(self,bolt):
        """
        Returns True if the bolt from player collides with a alien.

        Parameter bolt: The laser bolt in the list
        Precondition: a bolt object of class Bolt
        """
        corners = []
        leftx = bolt.x - 0.5*BOLT_WIDTH
        upper = bolt.y + 0.5*BOLT_HEIGHT
        rightx = bolt.x + 0.5*BOLT_WIDTH
        lower = bolt.y - 0.5*BOLT_HEIGHT
        fir = [leftx,upper]
        sec = [rightx,upper]
        thi = [leftx,lower]
        fou = [rightx,lower]
        corners.append(fir)
        corners.append(sec)
        corners.append(thi)
        corners.append(fou)
        for c in corners:
            if self.contains(c):
                return True
        return False

    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


class Bolt(GRectangle):
    """
    A class representing a laser bolt.

    Laser bolts are often just thin, white rectangles. The size of the bolt
    is determined by constants in consts.py. We MUST subclass GRectangle,
    because we need to add an extra (hidden) attribute for the velocity of
    the bolt.

    The class Wave will need to look at these attributes, so you will need
    getters for them.  However, it is possible to write this assignment with
    no setters for the velocities.  That is because the velocity is fixed and
    cannot change once the bolt is fired.

    In addition to the getters, you need to write the __init__ method to set
    the starting velocity. This __init__ method will need to call the __init__
    from GRectangle as a  helper.

    You also MIGHT want to create a method to move the bolt.  You move the
    bolt by adding the velocity to the y-position.  However, the getter
    allows Wave to do this on its own, so this method is not required.
    """
    # INSTANCE ATTRIBUTES:
    # Attribute _velocity: the velocity in y direction
    # Invariant: _velocity is an int or float

    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    # Attribute _Bdirection: the direction of the bolt (going up or down)
    # Invariant: _Bdirection is an int, either 1 for up or -1 for down

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def get_x(self):
        """
        Returns the x coordinate of the bolt
        """
        return self.x

    def get_y(self):
        """
        Returns the y coordinate of the bolt
        """
        return self.y

    def MoveSBolt(self):
        '''
        Sets the new y coordinate to the bolt by adding velocity
        '''
        self.y = self.y + self._velocity

    def MoveABolt(self):
        '''
        Sets the new y coordinate to the bolt by subtracting velocity
        '''
        self.y = self.y - self._velocity

    # INITIALIZER TO SET THE VELOCITY
    def __init__(self,x,y,direction,color,speed = BOLT_SPEED):
        '''
        Initialize the bolt at given positon (x,y)

        Parameter x: the x coordinate of the bolt
        Precondition: a number greater than 0 and less than GAME_WIDTH

        Parameter y: the y coorinate of the bolt
        Precondition: a number greater than 0 and less than GAME_HEIGHT

        Parameter direction: the direction of the bolt
        Precondition: direction is an int

        Parameter color: the color of the bolt
        Precondition: a str of valid color name

        Parameter speed: the speed of the bolt
        Precondition: speed = BOLT_SPEED
        '''
        super().__init__(x = x, y = y, width=BOLT_WIDTH,
                        height=BOLT_HEIGHT,fillcolor= color)
        self._Bdirection = direction
        self._velocity = speed

    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    def _isSBolt(self):
        '''
        Returns if the bolt being checked is fired from the ship(player)

        If the direction is negative, meaning that the bolt is moveing down
        and is from the aliens. Else if the direction is positive, meaning
        that the bolt is moving upward and is from the ship.
        '''
        if self._Bdirection > 0:
            return True
        elif self._Bdirection < 0:
            return False

# IF YOU NEED ADDITIONAL MODEL CLASSES, THEY GO HERE
