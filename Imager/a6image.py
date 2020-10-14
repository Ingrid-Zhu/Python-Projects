"""
The main class for our imager application.

This modules contains a single class.
Instances of this class support an image that can be modified.
This is the main class needed to display images in the viewer.

Based on an original file by Dexter Kozen (dck10) and Walker White (wmw2)

Author: Yan Zhu yz2477  Aroma Dong jd778
Date:   11/20/2019
"""

def _is_pixel(item):
    """
    Returns True if item is a pixel, False otherwise.

    A pixel is a tuple of 3 ints in the range 0..255

    Parameter item: The item to check
    Precondition: NONE (item can be anything)(
    """
    if type(item) != tuple or len(item) != 3:
        return False

    for ii in range(3):
        if type(item[ii]) != int or item[ii] < 0 or item[ii] > 255:
            return False

    return True


# TASK 0: IMPLEMENT THIS HELPER
def _is_pixel_list(data):
    """
    Returns True if data is a pixel list, False otherwise.

    A pixel list is a 1-dimensional list of pixels where a pixel is a tuple
    of 3 ints in the range 0..255

    Parameter data: The data to check
    Precondition: NONE (data can be anything)(
    """
    bool1=(type(data)==list)
    n=len(data)
    bool2=True
    for x in range(n):
        bool2=bool2 and _is_pixel(data[x])
    return bool1 and bool2


# TASK 1: IMPLEMENT THIS CLASS
class Image(object):
    """
    A class that allows flexible access to an image pixel list

    One of the things that we will see in this assignment is that sometimes
    you want to treat an image as a flat 1D list and other times you want to
    treat it as a 2D list. This class has methods that allow you to go back
    and forth between the two.

    If you want to treat the image like a 2D list, you use the methods
    `getPixel` and `setPixel`. As with the Pixels class, pxels are represented
    as 3-element tuples, with each element in the range 0..255.  For example,
    red is (255,0,0). These methods are used by many of the Instagram-style
    filter functions.

    If you want to treat the image like a 1D list you just use list brackets
    like it was a normal list:

        image[pos] = (255,0,0)

    The methods `__getitem__` and `__getitem__` provide operator
    overloading for [].
    So the call above is the same as the image call

        image.__setitem__(pos, (255,0,0))

     These operations are used by the greyscale filters and
     the stenography methods.
    """
    # IMMUTABLE ATTRIBUTES (Fixed after initialization)
    # Attribute _data: The underlying list of pixels
    # Invariant: _data is a pixel list (see _is_pixel_list)
    #
    # MUTABLE ATTRIBUTES (Can be changed at any time, via the setters)
    # Attribute _width:  The image width, which is the number of columns
    # Invariant: _width is an int > 0, _width*_height = len(_data)
    # width = 0 only if len(_data) = 0
    #
    # Attribute _height:  The image height, which is the number of rows
    # Invariant: _height is an int > 0, _width*_height = len(_data)
    # height = 0 only if len(_data) = 0
    # Note that if you change width, you must change height
    #(to satisfy the invariant)

    # PART A
    # GETTERS AND SETTERS
    def getData(self):
        """
        Returns a COPY of the image data.

        The image data is a 1-dimensional list of 3-element tuples.  The list
        returned by this method is a copy of the one managed by this object.
        """
        return self._data.copy()

    def getWidth(self):
        """
        Returns the image width

        A value width is an int evenly dividing the number of pixels in the
        image. Width can only be 0 if the image is empty.
        """
        return self._width

    def setWidth(self,value):
        """
        Sets the image width to value, assuming it is valid.

        If the width changes, then height must change to so that we preserve
        width*height == # of pixels.
        This can only happen if the value is valid.

        The value is valid if it is an int and it evenly divides the number of
        pixels in the image. If the pixel list has 10 pixels, a valid width is
        1, 2, 5, or 10. Width can only be 0 if the image is empty.

        Parameter value: the new width value
        Precondition: value is a valid width >= 0
        """
        assert type(value)==int and value>=0
        assert (value==0 and len(self.getData())==0) or (value>0)
        assert (len(self.getData())/value)==int(len(self.getData())/value)
        if len(self.getData())==0:
            if value==0:
                self._width=value
            else:
                self._width=value
                self._height=0
        else:
            self._width=value
            self._height=(int(len(self.getData())/value))

    def getHeight(self):
        """
        Returns the image height

        A value height is an int evenly dividing the number of pixels in the
        image. Height can only be 0 if the image is empty.
        """
        return self._height

    def setHeight(self,value):
        """
        Sets the image height to value, assuming it is valid.

        If the height changes, then width must change to so that we preserve
        width*height == # of pixels.
        This can only happen if the value is valid.

        The value is valid if it is an int and it evenly divides the number of
        pixels in the image. If the pixel list has 10 pixels, a valid height is
        1, 2, 5, or 10. Height can only be 0 if the image is empty.

        Parameter value: the new height value
        Precondition: value is a valid height >= 0
        """
        assert type(value)==int and value>=0
        assert (value==0 and len(self.getData())==0) or (value>0)
        assert (len(self.getData())/value)==int(len(self.getData())/value)
        if len(self.getData())==0:
            if value==0:
                self._height=value
            else:
                self._height=value
                self._width=0
        else:
            self._height=value
            self._width=(int(len(self.getData())/value))

    # INITIALIZER
    def __init__(self, data, width):
        """
        Initializes an Image from the given pixel list.

        A pixel list is a 1-dimensional list of pixels where a pixel is a
        tuple of 3 ints in the range 0..255. The pixel list contains the
        image data. You do not need to worry about loading an image file.
        That happens elsewhere in the application (in code that you did not
        write).

        However, in order to be valid, the width  must evenly divide the
        number of pixels in the image. So if the pixel list has 10 pixels, a
        valid width is 1, 2, 5, or 10.

        The height is not given explicitly, but you must compute it from the
        width and pixel list length.

        This initializer stores a reference to the original image data; it
        does not copy it. So changes to the image will change the data
        parameter as well.

        Parameter data: The image data as a pixel list
        Precondition: data is a pixel list

        Parameter width: The image width
        Precondition: width is an int > 0 and evenly
        divides the length of pixels
        """
        assert _is_pixel_list(data)
        assert type(width)==int and width>0
        assert (len(data)/width)==int(len(data)/width)
        self._data=data
        self.setWidth(width)
        self.setHeight(int(len(self.getData())/self.getWidth()))

    # PART B
    # OPERATOR OVERLOADING
    def __len__(self):
        """
        Returns the number of pixels in this image

        This special method supports the built-in len function.
        """
        return len(self._data)

    def __getitem__(self, pos):
        """
        Returns the pixel at the given position.

        This special method supports the [] operator for accessing pixels.
        It is better than direct access because it enforces its precondition.

        This method is used when you want to treat an image as a flat,
        one-dimensional list rather than a 2-dimensional image. It is useful
        for the steganography part of the assignment.

        The value returned is a 3-element tuple (r,g,b).

        Parameter pos: The position in the pixel list
        Precondition: pos is an int and a valid position >= 0
        in the pixel list.
        """
        assert type(pos)==int and pos>=0
        assert pos<len(self._data)
        return self._data[pos]

    def __setitem__(self, pos, pixel):
        """
        Sets the pixel at the given position to the given value.

        This special method supports the [] operator for accessing pixels.
        It is better than direct access because it enforces its precondition.

        Parameter pos: The position in the pixel list
        Precondition: pos is an int and a valid position >= 0
        in the pixel list.

        Parameter pixel: The pixel value
        Precondition: pixel is a 3-element tuple (r,g,b) of ints in 0..255
        """
        assert type(pos)==int and pos>=0
        assert pos<len(self._data)
        assert _is_pixel(pixel)
        self._data[pos]=pixel

    # PART C
    # TWO-DIMENSIONAL ACCESS METHODS
    def getPixel(self, row, col):
        """
        Returns a copy of the pixel value at (row, col)

        Remember that this way of accessing a pixel is essentially (y,x) since
        height is the number of rows and width is the number of columns.

        The value returned is a 3-element tuple (r,g,b).

        Parameter row: The pixel row
        Precondition: row is an int >= 0 and < height

        Parameter col: The pixel column
        Precondition: col is an int >= 0 and < width
        """
        assert type(row)==int and row>=0 and row<self.getHeight()
        assert type(col)==int and col>=0 and col<self.getWidth()
        return self[row*self.getWidth()+col]

    def setPixel(self, row, col, pixel):
        """
        Sets the pixel value at (row, col) to (a copy of) pixel

        Remember that this way of setting a pixel is essentially (y,x) since
        height is the number of rows and width is the number of columns.

        Parameter row: The pixel row
        Precondition: row is an int >= 0 and < height

        Parameter col: The pixel column
        Precondition: col is an int >= 0 and < width

        Parameter pixel: The pixel value
        Precondition: pixel is a 3-element tuple (r,g,b) of ints in 0..255
        """
        assert type(row)==int and row>=0 and row<self.getHeight()
        assert type(col)==int and col>=0 and col<self.getWidth()
        assert _is_pixel(pixel)
        self[row*self.getWidth()+col]=pixel

    # PART D
    def __str__(self):
        """
        Returns: The string representation of this image.

        The string should be displayed as a 2D list of pixels in row-major
        order. For example, suppose the image data is

            [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 0, 0),
            (128, 0, 0), (0, 128, 0)]

        If the width (which is the number of columns) is two, the string
        should be

            '[[(255, 0, 0), (0, 255, 0)],\n[(0, 0, 255), (0, 0, 0)],
            \n[(128, 0, 0), (0, 128, 0)]]

        Note the newlines (\n) after each row. That is because
        when you print this string, it will look like this:

            [[(255, 0, 0), (0, 255, 0)],
            [(0, 0, 255), (0, 0, 0)],
            [(128, 0, 0), (0, 128, 0)]]

        This is useful for debugging, since it allows us to see each row of the
        image on its own line.

        There should be spaces after the commas but no where else. Tuples
        (the individual pixels) handle this  part for you automatically,
        but you need to handle the commas between pixels and the
        newlines between rows.
        """
        m=self.getHeight()
        n=self.getWidth()
        c=''
        for i in range(m):
            a=''
            for j in range(n):
                a=a+', '+str(self.getPixel(i,j))
            b=',\n['+a[2:]+']'
            c=c+b
        d=c[2:]
        result='['+d+']'
        return result


    # ADDITIONAL METHODS
    def swapPixels(self, row1, col1, row2, col2):
        """
        Swaps the pixel at (row1, col1) with the pixel at (row2, col2)

        Parameter row1: The pixel row to swap from
        Precondition: row1 is an int >= 0 and < height

        Parameter col1: The pixel column to swap from
        Precondition: col1 is an int >= 0 and < width

        Parameter row2: The pixel row to swap to
        Precondition: row1 is an int >= 0 and < height

        Parameter col2: The pixel column to swap to
        Precondition: col2 is an int >= 0 and < width
        """
        # NOTE: DO NOT enforce any preconditions here.
        # They should be enforced already in getPixel and setPixel.
        pixel1=self.getPixel(row1,col1)
        pixel2=self.getPixel(row2,col2)
        self.setPixel(row1,col1,pixel2)
        self.setPixel(row2,col2,pixel1)

    def copy(self):
        """
        Returns a copy of this image object.

        The underlying pixel data must be copied (e.g. the copy cannot refer
        to the same list of pixels that this object does).
        """
        return Image(self.getData(), self.getWidth())
