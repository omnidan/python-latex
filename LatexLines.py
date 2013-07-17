__author__ = 'Daniel Bugl'
__copyright__ = "Copyright 2013, Daniel Bugl"
__credits__ = ["Daniel Bugl"]

__license__ = "BSD"
__version__ = "0.1.0"
__maintainer__ = "Daniel Bugl"
__email__ = "daniel.bugl@touchlay.com"
__status__ = "Prototype"


class LatexLine:
    """ This is a prototype for the various line objects """
    def getString(self):
        """ Prototype for the getString function """
        return str("")


class LatexCommand(LatexLine):
    def getString(self):
        """ Converts the LatexCommand object into a latex command string and returns it """
        buf = "\\" + self.command_name
        if self.asterisk:
            buf += "*"
        if self.additional_options:
            buf += "[" + ",".join(self.additional_options) + "]"
        if self.command_options:
            buf += "{" + ",".join(self.command_options) + "}"
        return str(buf)

    def parseOptions(self, options=None, additional_options=None):
        """ Parse the command_options and additional_options strings into a list and set the values in the object"""
        # if None, set to values from __init__
        if options is None:
            options = self.command_options
        if additional_options is None:
            additional_options = self.additional_options

        # parse options value
        if self.command_options is not None:
            # TODO: This if/else block is just a workaround, find a better way to parse options
            self.command_options = options.split(",")
        else:
            self.command_options = []

        # parse additional_options value
        if additional_options is None or additional_options == []:
            self.additional_options = []
        else:
            self.additional_options = additional_options.split(",")

    def __init__(self, command_type, command_name, command_options=None, additional_options=None, asterisk=False):
        self.command_type = command_type
        self.command_name = command_name
        self.command_options = command_options
        self.additional_options = additional_options
        self.asterisk = asterisk


class LatexText(LatexLine):
    def getString(self):
        """ Converts the LatexText object into a string and returns it """
        return str(self.text)

    def append(self, text):
        """ Appends string to LatexText object """
        self.text += self.__append_prefix + str(text) + self.__append_suffix

    def __init__(self, text, append_prefix="", append_suffix=""):
        self.__append_prefix = str(append_prefix)
        self.__append_suffix = str(append_suffix)
        self.text = str(text)


class LatexComment(LatexLine):
    def getString(self):
        """ Converts the LatexComment object into a latex comment string and returns it """
        return str(self.__comment_prefix + self.comment)

    def append(self, comment):
        """ Appends string to LatexComment object """
        self.comment += self.__append_prefix + str(comment) + self.__append_suffix

    def __init__(self, comment, comment_prefix="%", append_prefix="", append_suffix=""):
        self.__comment_prefix = str(comment_prefix)
        self.__append_prefix = str(append_prefix)
        self.__append_suffix = str(append_suffix)
        self.comment = str(comment)