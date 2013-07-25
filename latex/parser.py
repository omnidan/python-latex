from __future__ import print_function
__author__ = 'Daniel Bugl'
__copyright__ = "Copyright 2013, Daniel Bugl"
__credits__ = ["Daniel Bugl"]

__license__ = "BSD"
__version__ = "0.1.0"
__maintainer__ = "Daniel Bugl"
__email__ = "daniel.bugl@touchlay.com"
__status__ = "Prototype"

from .document import LatexDocument
from .lines import LatexCommand, LatexText, LatexComment, LatexMacro, LatexEnvironmentMacro
from .environment import LatexEnvironment
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
            elif "\\end{document}" in line:
                header = True
            else:
                if header:
                    header_buffer.append(line)
                else:
                    content_buffer.append(line)
        return header_buffer, content_buffer

    # noinspection PyUnusedLocal
    def __matchTeXMacro(self, line, prefix="", suffix=""):
        """ Some regex magic to parse TeX macros """
        # TODO: macros can occupy multiple lines, add support for this
        cmd = None
        opt = None
        argc = None
        p = re.match(r'\\newcommand\{(.*)}\[(.*)]\{(.*)}', line, re.M | re.I)
        if p is None:
            # match without additional [] arguments
            p = re.match(r'\\newcommand\{(.*)}\{(.*)}', line, re.M | re.I)
            if p is None:
                # invalid macro
                return False
            else:
                cmd = p.group(1)
                opt = p.group(2)
        else:
            cmd = p.group(1)
            try:
                argc = int(p.group(2))
            except ValueError:
                return False
            opt = p.group(3)
        if cmd is None:
            # couldn't parse, invalid latex macro
            return False
        elif opt is None:
            # couldn't parse, invalid latex macro
            return False
        else:
            # regex is a finite state machine, it can't match nested commands
            # TODO: rewrite this to work for macros
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
            if not argc:
                argc = 0
            return LatexMacro(cmd, opt, argc, prefix, suffix)

    # noinspection PyUnusedLocal
    def __matchTeXEnvironmentMacro(self, line, prefix="", suffix=""):
        """ Some regex magic to parse TeX macros """
        # TODO: macros can occupy multiple lines, add support for this
        cmd = None
        opt = None
        argc = None
        adopt = None
        p = re.match(r'\\newenvironment\{(.*)}\[(.*)]\{(.*)}\{(.*)}', line, re.M | re.I)
        if p is None:
            # match without additional [] arguments
            p = re.match(r'\\newenvironment\{(.*)}\{(.*)}\{(.*)}', line, re.M | re.I)
            if p is None:
                # invalid macro
                return False
            else:
                cmd = p.group(1)
                opt = p.group(2)
                adopt = p.group(3)
        else:
            cmd = p.group(1)
            try:
                argc = int(p.group(2))
            except ValueError:
                return False
            opt = p.group(3)
            adopt = p.group(4)
        if cmd is None:
            # couldn't parse, invalid latex macro
            return False
        elif opt is None:
            # couldn't parse, invalid latex macro
            return False
        elif adopt is None:
            # couldn't parse, invalid latex macro
            return False
        else:
            # regex is a finite state machine, it can't match nested commands
            # TODO: rewrite this to work for macros
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
            if not argc:
                argc = 0
            return LatexEnvironmentMacro(cmd, opt, adopt, argc, prefix, suffix)

    # noinspection PyUnusedLocal
    def __matchTeX(self, line, prefix="", suffix=""):
        """ Some regex magic to parse TeX commands """
        cmd = None
        opt = None
        adopt = None
        # TODO: add support for multiple arguments
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
            # regex is a finite state machine, it can't match nested commands
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
            return LatexCommand(cmd, opt, adopt, asterisk, prefix, suffix)

    def appendline(self, line):
        if self.__current_environment:
            self.__current_environment.addLine(line)
        else:
            self.__parse_buffer.append(line)

    def __parse(self, tex, keep_empty_lines=False, do_not_concat_text=False):
        self.__parse_buffer = []
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
                    self.appendline(LatexText(nonstripped))
                    self.__last_line = self.__parse_buffer[-1]
            else:
                # now check if command, comment or text
                if line[0] == '\\':
                    # this is a latex command, parse it as such
                    latex_command = self.__matchTeX(line, prefix, suffix)
                    if latex_command is False:
                        import sys
                        print("WARNING: Couldn't parse LaTeX command: " + line, file=sys.stderr)
                    else:
                        if latex_command.command_name == "newcommand":
                            # this is a LatexMacro, not a LatexCommand
                            latex_macro = self.__matchTeXMacro(line, prefix, suffix)
                            self.appendline(latex_macro)
                        elif latex_command.command_name == "newenvironment":
                            # this is a LatexEnvironmentMacro, not a LatexCommand
                            latex_macro = self.__matchTeXEnvironmentMacro(line, prefix, suffix)
                            self.appendline(latex_macro)
                        elif latex_command.command_name == "begin":
                            # this is a LatexEnvironment, not a LatexCommand
                            latex_environment = LatexEnvironment(latex_command.command_options)
                            self.appendline(latex_environment)
                            self.__current_environment = self.__parse_buffer[-1]
                        elif latex_command.command_name == "end":
                            # this is the end of a LatexEnvironment, not a LatexCommand
                            # TODO: environments inside environments do not work yet
                            self.__current_environment = None
                        else:
                            latex_command.parseOptions()
                            self.appendline(latex_command)
                elif line[0] == "%":
                    # remove first character from line and create the LatexComment object
                    comment = "".join(line[1:]).strip()
                    if not do_not_concat_text and isinstance(self.__last_line, LatexComment):
                        # last line was a LatexComment too, append to this object
                        self.__last_line.append(comment)
                    else:
                        # create new LatexComment object
                        self.appendline(LatexComment(comment, self.__ld.comment_prefix,
                                                         self.__ld.comment_append_prefix,
                                                         self.__ld.comment_append_suffix,
                                                         prefix=prefix, suffix=suffix))
                else:
                    # this is a normal text line
                    if not do_not_concat_text and isinstance(self.__last_line, LatexText):
                        # last line was a LatexText too, append to this object
                        self.__last_line.append(line)
                    else:
                        # create new LatexText object
                        self.appendline(LatexText(line, self.__ld.text_append_prefix, self.__ld.text_append_suffix,
                                                      prefix=prefix, suffix=suffix))
                self.__last_line = self.__parse_buffer[-1]
        return self.__parse_buffer

    def getResult(self):
        return self.__ld

    def __init__(self, tex, obj=None, keep_empty_lines=False, do_not_concat_text=False):
        # init last_line variable
        self.__last_line = None
        self.__current_environment = None
        self.__parse_buffer = []

        # parse document into header and content buffer
        header, content = self.__parseDocument(tex)

        # parse buffers into objects
        if obj is None:
            obj = LatexDocument()
        self.__ld = obj
        self.__ld.setHeader(self.__parse(header, keep_empty_lines, do_not_concat_text))
        self.__ld.setContent(self.__parse(content, keep_empty_lines, do_not_concat_text))