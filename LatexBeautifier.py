__author__ = 'Daniel Bugl'
__copyright__ = "Copyright 2013, Daniel Bugl"
__credits__ = ["Daniel Bugl"]

__license__ = "BSD"
__version__ = "0.1.0"
__maintainer__ = "Daniel Bugl"
__email__ = "daniel.bugl@touchlay.com"
__status__ = "Prototype"

from LatexDocument import LatexDocument
from LatexLines import LatexCommand, LatexText, LatexComment
import yaml


class LatexBeautifier(LatexDocument):
    def __init__(self):
        LatexDocument.__init__(self)
        self.__config = yaml.load(open("pretty.ini", "r").read())
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
                document_buffer += self.__config["LatexCommand"]["indentation"]
                document_buffer += l.getString()
            elif isinstance(l, LatexText):
                document_buffer += self.__config["LatexText"]["indentation"]
                i = 0
                for c in l.getString():
                    if i >= self.__config["LatexText"]["charlimit"]:
                        document_buffer += "\n"
                        document_buffer += self.__config["LatexText"]["indentation"]
                        i = 0
                    document_buffer += c
                    i += 1
            elif isinstance(l, LatexComment):
                document_buffer += self.__config["LatexComment"]["indentation"]
                document_buffer += l.getString()
            document_buffer += self.__config["LatexLine"]["suffix"]
        return str(document_buffer)

if __name__ == "__main__":
    from LatexParser import LatexParser
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
    """, LatexBeautifier)
    ld = lp.getResult()
    for l in ld.getLines():
        print l
    print ld.getDocument()