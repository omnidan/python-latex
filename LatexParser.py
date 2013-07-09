__author__ = 'Daniel Bugl'
__copyright__ = "Copyright 2013, Daniel Bugl"
__credits__ = ["Daniel Bugl"]

__license__ = "BSD"
__version__ = "0.1.0"
__maintainer__ = "Daniel Bugl"
__email__ = "daniel.bugl@touchlay.com"
__status__ = "Prototype"

import re
from LatexDocument import LatexDocument
from LatexLines import LatexCommand, LatexText, LatexComment


class LatexParser:
    def __parseDocument(self, tex):
        """ Parse a latex document and return the header and content buffer in a tuple """
        header_buffer = []  # buffer for the header lines
        content_buffer = []  # buffer for the content lines
        header = True  # are we still parsing the header?
        # run through all lines but strip the lines and remove empty lines
        for line in [line.strip() for line in tex.split('\n') if line.strip()]:
            # document started, that means we are no longer in the header
            if "\\begin{document}" in line:
                header = False
            if header:
                header_buffer.append(line)
            else:
                content_buffer.append(line)
        return header_buffer, content_buffer

    def __matchTeX(self, line):
        """ Some regex magic to parse TeX commands """
        cmd = None
        opt = None
        adopt = None
        p = re.match(r'\\(.*)\[(.*)\]\{(.*)}', line, re.M | re.I)
        if p is None:
            # match without additional [] arguments
            p = re.match(r'\\(.*)\{(.*)}', line, re.M | re.I)
            if p is None:
                # match without any arguments
                p = re.match(r'\\(.*)', line, re.M | re.I)
                cmd = p.group(1)
            else:
                cmd = p.group(1)
                opt = p.group(2)
        else:
            cmd = p.group(1)
            adopt = p.group(2)
            opt = p.group(3)
        if cmd is None:
            # couldn't parse, invalid latex command
            return False
        else:
            return LatexCommand(cmd, cmd, opt, adopt)

    def __parse(self, tex):
        parse_buffer = []
        for line in tex:
            # firstly, strip the line to remove whitespace
            line = line.strip()
            # now check if command, comment or text
            if line[0] == '\\':
                # this is a latex command, parse it as such
                latex_command = self.__matchTeX(line)
                if latex_command is False:
                    print "WARNING: Couldn't parse LaTeX command: " + line
                else:
                    latex_command.parseOptions()
                    parse_buffer.append(latex_command)
            elif line[0] == "%":
                # remove first character from line and create the LatexComment object
                comment = "".join(line[1:]).strip()
                if isinstance(self.__last_line, LatexComment):
                    # last line was a LatexComment too, append to this object
                    self.__last_line.append(comment)
                else:
                    # create new LatexComment object
                    parse_buffer.append(LatexComment(comment, self.__ld.comment_prefix, self.__ld.comment_append_prefix,
                                                     self.__ld.comment_append_suffix))
            else:
                # this is a normal text line
                if isinstance(self.__last_line, LatexText):
                    # last line was a LatexText too, append to this object
                    self.__last_line.append(line)
                else:
                    # create new LatexText object
                    parse_buffer.append(LatexText(line, self.__ld.text_append_prefix, self.__ld.text_append_suffix))
            self.__last_line = parse_buffer[-1]
        return parse_buffer

    def getResult(self):
        return self.__ld

    def __init__(self, tex, obj=LatexDocument):
        # init last_line variable
        self.__last_line = None

        # parse document into header and content buffer
        header, content = self.__parseDocument(tex)

        # parse buffers into objects
        self.__ld = obj()
        self.__ld.setHeader(self.__parse(header))
        self.__ld.setContent(self.__parse(content))

if __name__ == "__main__":
    lp = LatexParser("""
\documentclass[11pt,a4paper,oneside]{report}

\usepackage{pslatex,palatino,avant,graphicx,color}
\usepackage[margin=2cm]{geometry}

\\begin{document}
\\title{\color{red}Practical Typesetting}
\\author{\color{blue}Name\\ Work}
\date{\color{green}December 2005}
\maketitle

\end{document}
    """)
    ld = lp.getResult()
    print ld.getLines()
    print ld.getDocument()