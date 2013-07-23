from __future__ import print_function
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
        exported_lines = []
        if to_line is None:
            exported_lines = [lines[from_line]]
        elif from_line < to_line:
            exported_lines = lines[from_line:to_line]
            del lines[from_line+1:to_line]
        else:
            import sys
            print("WARNING: Couldn't export.", file=sys.stderr)
        lines[from_line] = LatexCommand("input", "input", [filename])
        self.setContent(lines)
        ld = LatexBeautifier()
        ld.setHeader([])
        ld.setContent(exported_lines)
        return ld

if __name__ == "__main__":
    import argparse
    import os
    parser = argparse.ArgumentParser()

    # basic arguments
    parser.add_argument("input", type=str,
                        help="the LaTeX input file")
    parser.add_argument("output", type=str,
                        help="the LaTeX output file")
    parser.add_argument("-c", "--config", action="store",
                        default=os.path.join(os.path.dirname(os.path.realpath(__file__)), "pretty.yml"),
                        help="set the config file")
    parser.add_argument("-d", "--debug", action="store_true",
                        help="enable debug mode")
    parser.add_argument("-b", "--beautify", action="store_true",
                        help="beautify code too")

    # refactoring tasks
    parser.add_argument("--refactor-title", "--refactor-title", action="store")
    parser.add_argument("--refactor-section2subsection", "--refactor-section2subsection", action="store")
    parser.add_argument("--refactor-subsection2section", "--refactor-subsection2section", action="store")

    args = parser.parse_args()

    if args.beautify:
        lp = LatexParser(open(args.input, "r").read(), LatexRefactor(args.config))
    else:
        lp = LatexParser(open(args.input, "r").read(), LatexRefactor(args.config),
                         keep_empty_lines=True, do_not_concat_text=True)
    ld = lp.getResult()

    # execute refactoring tasks
    if args.refactor_title:
        ld.refactorTitle(args.refactor_title)
    if args.refactor_section2subsection:
        ld.refactorSection2Subsection(args.refactor_section2subsection)
    if args.refactor_subsection2section:
        ld.refactorSubsection2Section(args.refactor_subsection2section)

    # output and save
    if args.beautify:
        document = ld.getDocument()
    else:
        document = ld.getDocument(no_prefix=False)
    # TODO: Implement
    # testtex = ld.refactorExportCode("test.tex", 5)
    if args.debug:
        print("DEBUG OUTPUT (" + args.input + "):")
        for l in ld.getLines():
            print(str(l) + ": " + l.getString())
        print("--")
        print("OUTPUT (" + args.input + "):")
        print(document)
        print("--")
        #if args.debug:
        #    print("DEBUG OUTPUT (test.tex):")
        #    for l in testtex.getLines():
        #        print(str(l) + ": " + l.getString())
        #    print("--")
        #print("OUTPUT (test.tex):")
        #print(testtex.getDocument())
        #print("--")
    open(args.output, "w").write(document)
    #open("test.tex", "w").write(testtex.getDocument())
    print("done.")