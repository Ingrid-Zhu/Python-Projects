"""
Steganography methods for the imager application.

This module provides all of the test processing operations (encode, decode)
that are called by the application.
 Note that this class is a subclass of Filter.
This allows us to layer this functionality on top of the Instagram-filters,
providing this functionality in one application.

Based on an original file by Dexter Kozen (dck10) and Walker White (wmw2)

Author: Yan Zhu yz2477  Aroma Dong jd778
Date:   11/20/2019
"""
import a6filter


class Encoder(a6filter.Filter):
    """
    A class that contains a collection of image processing methods

    This class is a subclass of Filter.  That means it inherits all of the
    methods and attributes of that class too. We do that separate the
    steganography methods from the image filter methods, making the code
    easier to read.

    Both the `encode` and `decode` methods should work with the most recent
    image in the edit history.
    """

    def encode(self, text):
        """
        Returns True if it could hide the text; False otherwise.

        This method attemps to hide the given message text in the current
        image. This method first converts the text to a byte list using the
        encode() method in string to use UTF-8 representation:

            blist = list(text.encode('utf-8'))

        This allows the encode method to support all text, including emoji.

        If the text UTF-8 encoding requires more than 999999 bytes or the
        picture does  not have enough pixels to store these bytes this method
        returns False without storing the message. However, if the number of
        bytes is both less than 1000000 and less than (# pixels - 10), then
        the encoding should succeed.  So this method uses no more than 10
        pixels to store additional encoding information.

        Parameter text: a message to hide
        Precondition: text is a string
        """
        # You may modify anything in the above specification EXCEPT
        # The first line (Returns True...)
        # The last paragraph (If the text UTF-8 encoding...)
        # The precondition (text is a string)
        assert type(text) == str

        current = self.getCurrent()

        blist = list(text.encode('utf-8'))
        bnum = len(blist)
        if bnum>999999 or len(current)-10< bnum:
            return False

        self._encode_pixel_str(0,'314')
        self._encode_pixel_str(1,'159')
        self._encode_pixel_str(2,'265')
        self._encode_pixel_str(3,'358')
        self._encode_pixel_str(4,'979')

        bnum2 = '0'*(6-len(str(bnum)))+str(bnum)
        self._encode_pixel_str(5,bnum2[:3])
        self._encode_pixel_str(6,bnum2[3:])

        for p in range(bnum):
            num = str(blist[p])
            if len(num) < 3:
                num = '0'*(3-len(num))+num
            self._encode_pixel_str(7+p,num)
        return True

    def decode(self):
        """
        Returns the secret message (a string) stored in the current image.

        The message should be decoded as a list of bytes. Assuming that a list
        blist has only bytes (ints in 0.255), you can turn it into a string
        using UTF-8 with the decode method:

            text = bytes(blist).decode('utf-8')

        If no message is detected, or if there is an error in decoding the
        message, this method returns None
        """
        # You may modify anything in the above specification EXCEPT
        # The first line (Returns the secret...)
        # The last paragraph (If no message is detected...)
        marker = ''
        for n in range(5):
            marker = marker + str(self._decode_pixel(n))
        if marker != '314159265358979':
            return None

        try:
            blist = []
            len = self._decode_pixel(5)*1000 + self._decode_pixel(6)
            if len == 0:
                return ''
            for n in range(len):
                blist.append(self._decode_pixel(n+7))
            text = bytes(blist).decode('utf-8')
            return text
        except:
            return None

    # HELPER METHODS
    def _decode_pixel(self, pos):
        """
        Return: the number n hidden in pixel pos of the current image.

        This function assumes that the value was a 3-digit number encoded as
        the last digit in each color channel (e.g. red, green and blue).

        Parameter pos: a pixel position
        Precondition: pos is an int with  0 <= p < image length (as a 1d list)
        """
        # This is helper. You do not have to use it.
        #You are allowed to change it.
        # There are no restrictions on how you can change it.
        rgb = self.getCurrent()[pos]
        red   = rgb[0]
        green = rgb[1]
        blue  = rgb[2]
        return  (red % 10) * 100  +  (green % 10) * 10  +  blue % 10

    def _encode_pixel_str(self, pos, str):
        """
        Encodes the 3-digit number represented by the string in the pixel at
        the position pos in the current image.
        This function will take the string that represents a 3-digit
        number and encode it at the given position.
        The first digit will be encoded in red, the second
        will be encoded in green, and the third be encoded in blue.
        Encoding a byte value will result in an invalid rgb value (> 255)
        thus will be substracted from the tens place of the appropriate
        color value.

        Parameter pos: a pixel position
        Precondition: pos is an int and 0 <= p < image length
        Parameter str: a string representation of a number to encode
        Precondition: a str of a 3-digit integer
        """
        rgb = self.getCurrent()[pos]
        red = rgb[0]
        green = rgb[1]
        blue = rgb[2]

        d1 = int(str[0])
        d2 = int(str[1])
        d3 = int(str[2])

        red = (red//10)*10 +d1
        green = (green//10)*10 +d2
        blue = (blue//10)*10 +d3

        if red>255:
            red = red-10
        if green>255:
            green = green-10
        if blue>255:
            blue = blue-10

        self.getCurrent()[pos] = (red,green,blue)
