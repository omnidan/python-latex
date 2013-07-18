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
    def refactorTitle(self, title):
        """ Changes the title of the latex document """
        i = 0
        for l in self.getLinesContent():
            if isinstance(l, LatexCommand):
                if l.command_name == "title":
                    l.command_options = [title]
                    self.setContentLine(i, l)
            i += 1

    def refactorSection2Subsection(self, section_name):
        """ Refactors a specific section to a subsection """
        i = 0
        for l in self.getLinesContent():
            if isinstance(l, LatexCommand):
                if l.command_name == "section" and l.command_options == [section_name]:
                    l.command_name = "subsection"
                    self.setContentLine(i, l)
            i += 1

    def refactorSubsection2Section(self, section_name):
        """ Refactors a specific subsection to a section """
        i = 0
        for l in self.getLinesContent():
            if isinstance(l, LatexCommand):
                if l.command_name == "subsection" and l.command_options == [section_name]:
                    l.command_name = "section"
                    self.setContentLine(i, l)
            i += 1

    def refactorExportCode(self, filename, from_line, to_line=None):
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
        ld = LatexBeautifier()
        ld.setHeader([])
        ld.setContent(exported_lines)
        return ld

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=str,
                        help="the LaTeX input file")
    parser.add_argument("output", type=str,
                        help="the LaTeX output file")
    parser.add_argument("-c", "--config", action="store", default="pretty.yml",
                        help="set the config file")
    parser.add_argument("-d", "--debug", action="store_true",
                        help="enable debug mode")
    args = parser.parse_args()
    lp = LatexParser(open(args.input, "r").read(), LatexRefactor(args.config))
    ld = lp.getResult()
    ld.refactorTitle("Refactored Title")
    ld.refactorSection2Subsection("Displayed Text")
    testtex = ld.refactorExportCode("test.tex", 5)
    if args.debug:
        print "DEBUG OUTPUT (" + args.input + "):"
        for l in ld.getLines():
            print l, ":", l.getString()
        print "--"
        print "OUTPUT (" + args.input + "):"
        print ld.getDocument()
        print "--"
        if args.debug:
            print "DEBUG OUTPUT (test.tex):"
            for l in testtex.getLines():
                print l, ":", l.getString()
            print "--"
        print "OUTPUT (test.tex):"
        print testtex.getDocument()
        print "--"
    open(args.output, "w").write(ld.getDocument())
    open("test.tex", "w").write(testtex.getDocument())
    print "done."