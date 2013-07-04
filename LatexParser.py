from LatexDocument import LatexDocument
import re

class LatexParser:
    def __parseDocument(self, tex):
        header_buffer = []  # buffer for the header lines
        content_buffer = []  # buffer for the content lines
        header = True  # are we still parsing the header?
        # run through all lines but strip the lines and remove empty lines
        for line in [line.strip() for line in tex.split('\n') if line.strip()]:
            # TODO: There is also \begin{abstract} and maybe other possibilities, check that too
            if "\\begin" in line:
                header = False
            if header:
                header_buffer.append(line)
            else:
                content_buffer.append(line)
        return (header_buffer, content_buffer)

    def __matchTeX(self, command, line):
        p = re.match(r'\\' + command + '\[(.*)\]\{(.*)}', line, re.M|re.I)
        if p is None:
            # match without additional [] arguments
            p = re.match(r'\\' + command + '\{(.*)}', line, re.M|re.I)
            return (p.group(1), None)
        return (p.group(2), p.group(1))

    def __parseHeader(self, tex):
        for line in tex:
            print line
            if "\\documentclass" in line:
                print self.__matchTeX("documentclass", line)
            elif "\\usepackage" in line:
                packages, config = self.__matchTeX("usepackage", line)
                if config is None:
                    for p in packages.split(","):
                        self.latexdoc.packages[p] = None
                else:
                    self.latexdoc.packages[packages] = config



    def __init__(self, tex):
        self.latexdoc = LatexDocument()
        header, content = self.__parseDocument(tex)
        self.__parseHeader(header)
        print self.latexdoc.packages
        print content


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