__author__ = 'Daniel Bugl'
__copyright__ = "Copyright 2013, Daniel Bugl"
__credits__ = ["Daniel Bugl"]

__license__ = "BSD"
__version__ = "0.1.0"
__maintainer__ = "Daniel Bugl"
__email__ = "daniel.bugl@touchlay.com"
__status__ = "Prototype"

from LatexLines import LatexLine


class LatexDocument:
    def getDocument(self):
        """ Returns a string that contains the whole document """
        document_buffer = ""
        for l in self.getLines():
            document_buffer += l.getString()
            document_buffer += "\n"
        return str(document_buffer)

    def getLines(self):
        """ Returns a list of all lines """
        return self.__lines_header + self.__lines_content

    def getLinesHeader(self):
        """ Returns a list of all lines of the header """
        return self.__lines_header

    def getLinesContent(self):
        """ Returns a list of all lines of the content """
        return self.__lines_content

    def addHeaderLine(self, line):
        """ Adds a LatexLine to the LatexDocument object header """
        if not isinstance(line, LatexLine):
            return False
        else:
            self.__lines_header.append(line)
            return True

    def addContentLine(self, line):
        """ Adds a LatexLine to the LatexDocument object content """
        if not isinstance(line, LatexLine):
            return False
        else:
            self.__lines_content.append(line)
            return True

    def setHeader(self, header):
        """ Set the LatexDocument header to a specific list """
        if type(header) == list:
            self.__lines_header = header
            return True
        else:
            return False

    def setContent(self, content):
        """ Set the LatexDocument content to a specific list """
        if type(content) == list:
            self.__lines_content = content
            return True
        else:
            return False

    def setHeaderLine(self, index, line):
        """ Set a line with a specific index in the LatexDocument header list """
        if not isinstance(line, LatexLine):
            return False
        else:
            self.__lines_header[index] = line
            return True

    def setContentLine(self, index, line):
        """ Set a line with a specific index in the LatexDocument content list """
        if not isinstance(line, LatexLine):
            return False
        else:
            self.__lines_content[index] = line
            return True


    def __init__(self):
        self.text_append_prefix = ""
        self.text_append_suffix = ""
        self.comment_prefix = "% "
        self.comment_append_prefix = ""
        self.comment_append_suffix = ""
        self.__lines_header = []
        self.__lines_content = []