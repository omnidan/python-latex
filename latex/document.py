__author__ = 'Daniel Bugl'
__copyright__ = "Copyright 2013, Daniel Bugl"
__credits__ = ["Daniel Bugl"]

__license__ = "BSD"
__version__ = "0.1.0"
__maintainer__ = "Daniel Bugl"
__email__ = "daniel.bugl@touchlay.com"
__status__ = "Prototype"

from . import environment


class LatexDocument:
    def getDocument(self, no_prefix=True):
        """ Returns a string that contains the whole document """
        return self.__header.getString(no_prefix) + self.__content.getString(no_prefix)

    def getLines(self):
        """ Returns a list of all lines """
        return self.__header.getLines() + self.__content.getLines()

    def getLinesHeader(self):
        """ Returns a list of all lines of the header """
        return self.__header.getLines()

    def getLinesContent(self):
        """ Returns a list of all lines of the content """
        return self.__content.getLines()

    def addHeaderLine(self, line):
        """ Adds a LatexLine to the LatexDocument object header """
        return self.__header.addLine(line)

    def addContentLine(self, line):
        """ Adds a LatexLine to the LatexDocument object content """
        return self.__content.addLine(line)

    def setHeader(self, header):
        """ Set the LatexDocument header to a specific list """
        return self.__header.setLines(header)

    def setContent(self, content):
        """ Set the LatexDocument content to a specific list """
        return self.__content.setLines(content)

    def setHeaderLine(self, index, line):
        """ Set a line with a specific index in the LatexDocument header list """
        return self.__header.setLine(index, line)

    def setContentLine(self, index, line):
        """ Set a line with a specific index in the LatexDocument content list """
        return self.__content.setLine(index, line)

    def __init__(self):
        self.__header = environment.LatexEnvironment()  # global environment
        self.__content = environment.LatexEnvironment("document")  # document environment
        self.text_append_prefix = ""
        self.text_append_suffix = ""
        self.comment_prefix = "% "
        self.comment_append_prefix = ""
        self.comment_append_suffix = ""