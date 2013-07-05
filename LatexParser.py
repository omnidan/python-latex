import re


class LatexLine:
    """ This only exists to be able to check if a line is really a LatexLine """
    pass


class LatexCommand(LatexLine):
    def getString(self):
        """ Converts the LatexCommand object into a latex command string and returns it """
        buf = "\\" + self.name
        if self.additional_options != []:
            buf += "[" + ",".join(self.additional_options) + "]"
        if self.options != []:
            buf += "{" + ",".join(self.options) + "}"
        return str(buf)

    def parseOptions(self, options=None, additional_options=None):
        """ Parse the options and additional_options strings into a list and set the values in the object"""
        # if None, set to values from __init__
        if options is None:
            options = self.options
        if additional_options is None:
            additional_options = self.additional_options

        # parse options value
        if self.options is not None:
            # TODO: This if/else block is just a workaround, find a better way to parse options
            self.options = options.split(",")
        else:
            self.options = []

        # parse additional_options value
        if additional_options is None or additional_options == []:
            self.additional_options = []
        else:
            self.additional_options = additional_options.split(",")

    def __init__(self, type, name, options=[], additional_options=[]):
        self.type = type
        self.name = name
        self.options = options
        self.additional_options = additional_options


class LatexText(LatexLine):
    def getString(self):
        """ Converts the LatexText object into a string and returns it """
        return str(self.text)

    def __init__(self, text):
        self.text = text


class LatexComment(LatexLine):
    def getString(self):
        """ Converts the LatexComment object into a latex comment string and returns it """
        return str("%" + self.comment)

    def __init__(self, comment):
        self.comment = comment


class LatexDocument:
    def getDocument(self):
        """ Returns a string that contains the whole document """
        buffer = ""
        for l in self.getLines():
            buffer += l.getString()
            buffer += "\n"
        return str(buffer)

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

    def __init__(self):
        self.__lines_header = []
        self.__lines_content = []


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
        p = re.match(r'\\(.*)\[(.*)\]\{(.*)}', line, re.M|re.I)
        if p is None:
            # match without additional [] arguments
            p = re.match(r'\\(.*)\{(.*)}', line, re.M|re.I)
            if p is None:
                # match without any arguments
                p = re.match(r'\\(.*)', line, re.M|re.I)
                cmd = p.group(1)
            else:
                cmd = p.group(1)
                opt = p.group(2)
        else:
            cmd = p.group(1)
            opt = p.group(2)
            adopt = p.group(3)
        if cmd is None:
            # couldn't parse, invalid latex command
            return False
        else:
            return LatexCommand(cmd, cmd, opt, adopt)

    def __parse(self, tex):
        buffer = []
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
                    buffer.append(latex_command)
            elif line[0] == "%":
                # remove first character from line and create the LatexComment object
                buffer.append(LatexComment("".join(line[1:]).strip()))
            else:
                # this is a normal text line
                buffer.append(LatexText(line))
        return buffer

    def __init__(self, tex):
        # parse document into header and content buffer
        header, content = self.__parseDocument(tex)

        # parse buffers into objects
        ld = LatexDocument()
        ld.setHeader(self.__parse(header))
        ld.setContent(self.__parse(content))

        # return all LatexLines in a list
        print ld.getLines()
        # return the whole document as a string
        print ld.getDocument()


if __name__ == "__main__":
    LatexParser("""
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