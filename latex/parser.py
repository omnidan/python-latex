__author__ = 'Daniel Bugl'
__copyright__ = "Copyright 2013, Daniel Bugl"
__credits__ = ["Daniel Bugl"]

__license__ = "BSD"
__version__ = "0.1.0"
__maintainer__ = "Daniel Bugl"
__email__ = "daniel.bugl@touchlay.com"
__status__ = "Prototype"

from .document import LatexDocument
from .lines import LatexCommand, LatexText, LatexComment
import re


class LatexParser:
    def __parseDocument(self, tex):
        """ Parse a latex document and return the header and content buffer in a tuple """
        header_buffer = []  # buffer for the header lines
        content_buffer = []  # buffer for the content lines
        header = True  # are we still parsing the header?
        # run through all lines
        for line in [line for line in tex.split('\n') if True]:
            # document started, that means we are no longer in the header
            if "\\begin{document}" in line:
                header = False
            if header:
                header_buffer.append(line)
            else:
                content_buffer.append(line)
        return header_buffer, content_buffer

    # noinspection PyUnusedLocal
    def __matchTeX(self, line, prefix="", suffix=""):
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
            # TODO: maybe fix the regex instead of using this workaround
            if "{" in cmd:
                real_cmd = cmd.split("{")
                cmd = real_cmd[0]
                opt = "{".join(real_cmd[1:]) + "{" + opt
            cmd = cmd.replace(" ", "")  # remove whitespace from the command
            if cmd[-1] == "*":
                cmd = ''.join(cmd[:-1])
                asterisk = True
            else:
                asterisk = False
            return LatexCommand(cmd, cmd, opt, adopt, asterisk, prefix, suffix)

    def __parse(self, tex, keep_empty_lines=False, do_not_concat_text=False):
        parse_buffer = []
        for line in tex:
            # firstly, strip the line to remove whitespace
            nonstripped = line
            line = line.strip()
            if nonstripped == line or line == "":
                prefix = ""
                suffix = ""
            else:
                prefix, suffix = nonstripped.split(line)
            # check if the line is empty
            if line == "":
                if keep_empty_lines:
                    parse_buffer.append(LatexText(nonstripped))
                    self.__last_line = parse_buffer[-1]
            else:
                # now check if command, comment or text
                if line[0] == '\\':
                    # this is a latex command, parse it as such
                    latex_command = self.__matchTeX(line, prefix, suffix)
                    if latex_command is False:
                        print("WARNING: Couldn't parse LaTeX command: " + line)
                    else:
                        latex_command.parseOptions()
                        parse_buffer.append(latex_command)
                elif line[0] == "%":
                    # remove first character from line and create the LatexComment object
                    comment = "".join(line[1:]).strip()
                    if not do_not_concat_text and isinstance(self.__last_line, LatexComment):
                        # last line was a LatexComment too, append to this object
                        self.__last_line.append(comment)
                    else:
                        # create new LatexComment object
                        parse_buffer.append(LatexComment(comment, self.__ld.comment_prefix, self.__ld.comment_append_prefix,
                                                         self.__ld.comment_append_suffix, prefix=prefix, suffix=suffix))
                else:
                    # this is a normal text line
                    if not do_not_concat_text and isinstance(self.__last_line, LatexText):
                        # last line was a LatexText too, append to this object
                        self.__last_line.append(line)
                    else:
                        # create new LatexText object
                        parse_buffer.append(LatexText(line, self.__ld.text_append_prefix, self.__ld.text_append_suffix,
                                                      prefix=prefix, suffix=suffix))
                self.__last_line = parse_buffer[-1]
        return parse_buffer

    def getResult(self):
        return self.__ld

    def __init__(self, tex, obj=None, keep_empty_lines=False, do_not_concat_text=False):
        # init last_line variable
        self.__last_line = None

        # parse document into header and content buffer
        header, content = self.__parseDocument(tex)

        # parse buffers into objects
        if obj is None:
            obj = LatexDocument()
        self.__ld = obj
        self.__ld.setHeader(self.__parse(header, keep_empty_lines, do_not_concat_text))
        self.__ld.setContent(self.__parse(content, keep_empty_lines, do_not_concat_text))