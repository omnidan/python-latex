__author__ = 'Daniel Bugl'
__copyright__ = "Copyright 2013, Daniel Bugl"
__credits__ = ["Daniel Bugl"]

__license__ = "BSD"
__version__ = "0.1.0"
__maintainer__ = "Daniel Bugl"
__email__ = "daniel.bugl@touchlay.com"
__status__ = "Prototype"

from . import lines


class LatexEnvironment(lines.LatexLine):
    # TODO: This should probably replace the LatexDocument
    def getString(self, no_prefix=True):
        """ Converts the LatexEnvironment object and all objects part of it into a latex string and returns it """
        if self.name:
            buf = "\\begin{" + self.name + "}"
        for l in self.lines:
            buf += l.getString(no_prefix)
            buf += "\n"
        if self.name:
            buf += "\\end{" + self.name + "}"
        if no_prefix:
            return str(buf)
        else:
            return self.prefix + str(buf) + self.suffix

    def getLines(self):
        """ Returns a list of all lines """
        return self.lines

    def addLine(self, line):
        """ Adds a LatexLine to the LatexEnvironment object """
        if not isinstance(line, lines.LatexLine):
            return False
        else:
            self.lines.append(line)
            return True

    def __init__(self, name=None, lines=[], prefix="", suffix=""):
        self.name = name  # if name is None, it's the global environment
        self.lines = lines
        # compatibility with obsolete LatexDocument
        self.text_append_prefix = ""
        self.text_append_suffix = ""
        self.comment_prefix = "% "
        self.comment_append_prefix = ""
        self.comment_append_suffix = ""
        # these are needed when not pretty printing
        self.prefix = str(prefix)
        self.suffix = str(suffix)