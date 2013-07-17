__author__ = 'Daniel Bugl'
__copyright__ = "Copyright 2013, Daniel Bugl"
__credits__ = ["Daniel Bugl"]

__license__ = "BSD"
__version__ = "0.1.0"
__maintainer__ = "Daniel Bugl"
__email__ = "daniel.bugl@touchlay.com"
__status__ = "Prototype"

from latex import LatexParser, LatexCommand
from LatexBeautifier import LatexBeautifier


class LatexRefactor(LatexBeautifier):
    def __refactorTitle(self, title):
        """ Changes the title of the latex document """
        i = 0
        for l in self.getLinesContent():
            if isinstance(l, LatexCommand):
                if l.command_name == "title":
                    l.command_options = [title]
                    self.setContentLine(i, l)
            i += 1

    def __refactorSection2Subsection(self, section_name):
        """ Refactors a specific section to a subsection """
        i = 0
        for l in self.getLinesContent():
            if isinstance(l, LatexCommand):
                if l.command_name == "section" and l.command_options == [section_name]:
                    l.command_name = "subsection"
                    self.setContentLine(i, l)
            i += 1

    def __refactorSubsection2Section(self, section_name):
        """ Refactors a specific subsection to a section """
        i = 0
        for l in self.getLinesContent():
            if isinstance(l, LatexCommand):
                if l.command_name == "subsection" and l.command_options == [section_name]:
                    l.command_name = "section"
                    self.setContentLine(i, l)
            i += 1

    def __refactorExportCode(self, filename, from_line, to_line=None):
        """ Exports a code block to an external file """
        if from_line == to_line:
            to_line = None
        lines = self.getLinesContent()
        # TODO: create file too
        if to_line is None:
            exported_lines = [lines[from_line]]
        elif from_line < to_line:
            exported_lines = lines[from_line:to_line]
            del lines[from_line+1:to_line]
        else:
            print "WARNING: Couldn't export."
        lines[from_line] = LatexCommand("input", "input", [filename])
        self.setContent(lines)
        print exported_lines


    def getDocument(self):
        """ Returns a string that contains the refactored document """
        # do refactoring tasks
        self.__refactorTitle("Refactored Title")
        self.__refactorSection2Subsection("Displayed Text")
        self.__refactorExportCode("test.tex", 5)
        # now pretty print and return the document using the superclass
        return LatexBeautifier.getDocument(self)

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

\section*{Displayed Text}

\end{document}
    """, LatexRefactor("pretty2.yml"))
    ld = lp.getResult()
    print ld.getDocument()