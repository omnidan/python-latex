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
    def __beautifyCommand(self, l, no_prefix=True):
        """ Returns a string that contains the beautified/pretty printed LatexCommand """
        document_buffer = self.__config["LatexCommand"]["indentation"]
        document_buffer += l.getString(no_prefix)
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

    def __beautifyText(self, l, no_prefix=True):
        """ Returns a string that contains the beautified/pretty printed LatexText """
        document_buffer = self.__config["LatexText"]["indentation"]
        document_buffer += self.__limitChars(l.getString(no_prefix),
                                             self.__config["LatexText"]["charlimit"],
                                             self.__config["LatexText"]["indentation"])
        return document_buffer

    def __beautifyComment(self, l, no_prefix=True):
        """ Returns a string that contains the beautified/pretty printed LatexComment """
        document_buffer = self.__config["LatexComment"]["indentation"]
        document_buffer += self.__limitChars(l.getString(no_prefix),
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

    def getDocument(self, no_prefix=True):
        """ Returns a string that contains the beautified/pretty printed document """
        document_buffer = ""
        for l in self.getLines():
            document_buffer += self.__config["LatexLine"]["prefix"]
            if isinstance(l, LatexCommand):
                document_buffer += self.__beautifyCommand(l, no_prefix=no_prefix)
            elif isinstance(l, LatexText):
                document_buffer += self.__beautifyText(l, no_prefix=no_prefix)
            elif isinstance(l, LatexComment):
                document_buffer += self.__beautifyComment(l, no_prefix=no_prefix)
            document_buffer += self.__config["LatexLine"]["suffix"]
        suffix_chars = len(self.__config["LatexLine"]["suffix"])
        document_buffer = document_buffer[:-suffix_chars]
        return str(document_buffer)

if __name__ == "__main__":
    import argparse
    import os
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=str,
                        help="the LaTeX input file")
    parser.add_argument("output", type=str,
                        help="the LaTeX output file")
    parser.add_argument("-c", "--config", action="store",
                        default=os.path.join(os.path.dirname(os.path.realpath(__file__)), "pretty.yml"),
                        help="set the config file")
    parser.add_argument("-d", "--debug", action="store_true",
                        help="enable debug mode")
    parser.add_argument("-p", "--stdout", action="store_true",
                        help="print result to stdout (suppresses 'done.' message, overrides output argument)")
    args = parser.parse_args()
    lp = LatexParser(open(args.input, "r").read(), LatexBeautifier(args.config))
    ld = lp.getResult()
    if args.debug:
        print("DEBUG OUTPUT:")
        for l in ld.getLines():
            print(str(l) + ": " + l.getString())
        print("--")
        print("OUTPUT (" + args.input + "):")
        print(ld.getDocument())
        print("--")
    if args.stdout:
        print(ld.getDocument())
    else:
        open(args.output, "w").write(ld.getDocument())
    if not args.stdout:
        print("done.")