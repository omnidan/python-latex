__author__ = 'Daniel Bugl'
__copyright__ = "Copyright 2013, Daniel Bugl"
__credits__ = ["Daniel Bugl"]

__license__ = "BSD"
__version__ = "0.1.0"
__maintainer__ = "Daniel Bugl"
__email__ = "daniel.bugl@touchlay.com"
__status__ = "Prototype"

from LatexBeautifier import LatexBeautifier
from LatexLines import LatexCommand, LatexText, LatexComment


class LatexRefactor(LatexBeautifier):
    def getDocument(self):
        """ Returns a string that contains the refactored document """
        # do refactoring tasks
        i = 0
        for l in self.getLinesContent():
            if isinstance(l, LatexCommand):
                if l.command_name == "title":
                    l.command_options = ["Refactored Title"]
                    print l
                    self.setContentLine(i, l)
            i += 1
        # now pretty print and return the document using the superclass
        return LatexBeautifier.getDocument(self)

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
    """, LatexRefactor("pretty2.yml"))
    ld = lp.getResult()
    print ld.getDocument()