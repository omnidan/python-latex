__author__ = 'Daniel Bugl'
__copyright__ = "Copyright 2013, Daniel Bugl"
__credits__ = ["Daniel Bugl"]

__license__ = "BSD"
__version__ = "0.1.0"
__maintainer__ = "Daniel Bugl"
__email__ = "daniel.bugl@touchlay.com"
__status__ = "Prototype"

from latex import LatexParser, LatexDocument, LatexCommand, LatexText, LatexComment
import yaml


class LatexBeautifier(LatexDocument):
    def __beautifyCommand(self, l):
        """ Returns a string that contains the beautified/pretty printed LatexCommand """
        document_buffer = self.__config["LatexCommand"]["indentation"]
        document_buffer += l.getString()
        return document_buffer

    def __limitChars(self, text, charlimit, indentation, newline="\n"):
        """ Returns a string that contains the beautified/pretty text with a char limit per line """
        document_buffer = ""
        i = 0
        for c in text:
            document_buffer += c
            i += 1
            # TODO: code a better in-word algorithm than 'if c == " "'
            if i >= charlimit and c == " ":
                document_buffer += newline
                document_buffer += indentation
                i = 0
        return document_buffer

    def __beautifyText(self, l):
        """ Returns a string that contains the beautified/pretty printed LatexText """
        document_buffer = self.__config["LatexText"]["indentation"]
        document_buffer += self.__limitChars(l.getString(),
                                             self.__config["LatexText"]["charlimit"],
                                             self.__config["LatexText"]["indentation"])
        return document_buffer

    def __beautifyComment(self, l):
        """ Returns a string that contains the beautified/pretty printed LatexComment """
        document_buffer = self.__config["LatexComment"]["indentation"]
        document_buffer += self.__limitChars(l.getString(),
                                             self.__config["LatexComment"]["charlimit"],
                                             self.__config["LatexComment"]["indentation"])
        return document_buffer

    def __init__(self, config_file="pretty.yml"):
        LatexDocument.__init__(self)
        self.__config = yaml.load(open(config_file, "r").read())
        self.text_append_prefix = self.__config["LatexText"]["append_prefix"]
        self.text_append_suffix = self.__config["LatexText"]["append_suffix"]
        self.comment_prefix = self.__config["LatexComment"]["prefix"]
        self.comment_append_prefix = self.__config["LatexComment"]["append_prefix"]
        self.comment_append_suffix = self.__config["LatexComment"]["append_suffix"]

    def getDocument(self):
        """ Returns a string that contains the beautified/pretty printed document """
        document_buffer = ""
        for l in self.getLines():
            document_buffer += self.__config["LatexLine"]["prefix"]
            if isinstance(l, LatexCommand):
                document_buffer += self.__beautifyCommand(l)
            elif isinstance(l, LatexText):
                document_buffer += self.__beautifyText(l)
            elif isinstance(l, LatexComment):
                document_buffer += self.__beautifyComment(l)
            document_buffer += self.__config["LatexLine"]["suffix"]
        return str(document_buffer)

if __name__ == "__main__":
    lp = LatexParser("""
\documentclass[11pt,a4paper,oneside]{report}

\usepackage{pslatex,palatino,avant,graphicx,color}
\usepackage[margin=2cm]{geometry}

% test
% test
% test
% test

\\begin{document}
\\title{\color{red}Practical Typesetting}
\\author{\color{blue}Name\\ Work}
\date{\color{green}December 2005}
\maketitle

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam dapibus consectetur tellus. Duis vehicula, tortor
gravida sollicitudin eleifend, erat eros feugiat nisl, eget ultricies risus magna ac leo. Ut est diam, faucibus
tincidunt ultrices sit amet, congue sed tellus. Donec vel tellus vitae sem mattis congue. Suspendisse faucibus
semper faucibus. Curabitur congue est arcu, nec sollicitudin odio blandit at. Nullam tempus vulputate aliquam.
Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Duis tempus ligula eu nulla
pharetra eleifend. Pellentesque eget nisi gravida, faucibus justo ac, volutpat elit. Praesent egestas posuere elit,
et imperdiet magna rhoncus eget. Donec porttitor enim lectus, quis egestas quam dignissim in. Donec dignissim sapien
odio, nec molestie enim imperdiet ac. Praesent venenatis quis mi nec pretium.

\end{document}
    """, LatexBeautifier())
    ld = lp.getResult()
    for l in ld.getLines():
        print l
    print ld.getDocument()