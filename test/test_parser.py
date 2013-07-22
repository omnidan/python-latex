from latex import LatexParser


class TestLatexParser:
    def test_parser(self):
        self.parser = LatexParser(self.document)
        assert self.parser.getResult().getDocument() == r"""\documentclass[11pt,a4paper,oneside]{report}
\usepackage{pslatex,palatino,avant,graphicx,color}
\usepackage[margin=2cm]{geometry}
% testtesttesttest
\begin{document}
\title{\color{red}Practical Typesetting}
\author{\color{blue}Name}
\date{\color{green}December 2005}
\maketitle
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam dapibus consectetur tellus. Duis vehicula, tortorgravida sollicitudin eleifend, erat eros feugiat nisl, eget ultricies risus magna ac leo. Ut est diam, faucibustincidunt ultrices sit amet, congue sed tellus. Donec vel tellus vitae sem mattis congue. Suspendisse faucibussemper faucibus. Curabitur congue est arcu, nec sollicitudin odio blandit at. Nullam tempus vulputate aliquam.Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Duis tempus ligula eu nullapharetra eleifend. Pellentesque eget nisi gravida, faucibus justo ac, volutpat elit. Praesent egestas posuere elit,et imperdiet magna rhoncus eget. Donec porttitor enim lectus, quis egestas quam dignissim in. Donec dignissim sapienodio, nec molestie enim imperdiet ac. Praesent venenatis quis mi nec pretium.
\section*{Displayed Text}
\end{document}
"""

    def test_parser_keep_empty_lines(self):
        # FIXME: There's always a newline at the end of the document, is this okay?
        self.parser = LatexParser(self.document, keep_empty_lines=True)
        assert self.parser.getResult().getDocument() == r"""
\documentclass[11pt,a4paper,oneside]{report}

\usepackage{pslatex,palatino,avant,graphicx,color}
\usepackage[margin=2cm]{geometry}



% testtesttesttest

\begin{document}
\title{\color{red}Practical Typesetting}
\author{\color{blue}Name}
\date{\color{green}December 2005}
\maketitle
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam dapibus consectetur tellus. Duis vehicula, tortorgravida sollicitudin eleifend, erat eros feugiat nisl, eget ultricies risus magna ac leo. Ut est diam, faucibustincidunt ultrices sit amet, congue sed tellus. Donec vel tellus vitae sem mattis congue. Suspendisse faucibussemper faucibus. Curabitur congue est arcu, nec sollicitudin odio blandit at. Nullam tempus vulputate aliquam.Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Duis tempus ligula eu nullapharetra eleifend. Pellentesque eget nisi gravida, faucibus justo ac, volutpat elit. Praesent egestas posuere elit,et imperdiet magna rhoncus eget. Donec porttitor enim lectus, quis egestas quam dignissim in. Donec dignissim sapienodio, nec molestie enim imperdiet ac. Praesent venenatis quis mi nec pretium.

\section*{Displayed Text}

\end{document}
"""

    def test_parser_do_not_concat_text(self):
        self.parser = LatexParser(self.document, do_not_concat_text=True)
        assert self.parser.getResult().getDocument() == r"""\documentclass[11pt,a4paper,oneside]{report}
\usepackage{pslatex,palatino,avant,graphicx,color}
\usepackage[margin=2cm]{geometry}
% test
% test
% test
% test
\begin{document}
\title{\color{red}Practical Typesetting}
\author{\color{blue}Name}
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
"""

    def test_parser_do_not_concat_and_empty_lines(self):
        self.parser = LatexParser(self.document, keep_empty_lines=True, do_not_concat_text=True)
        assert self.parser.getResult().getDocument() == r"""
\documentclass[11pt,a4paper,oneside]{report}

\usepackage{pslatex,palatino,avant,graphicx,color}
\usepackage[margin=2cm]{geometry}



% test
% test
% test
% test

\begin{document}
\title{\color{red}Practical Typesetting}
\author{\color{blue}Name}
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
"""

    def test_parser_with_prefixes(self):
        self.parser = LatexParser(self.document, do_not_concat_text=True)
        assert self.parser.getResult().getDocument(no_prefix=False) == r"""\documentclass[11pt,a4paper,oneside]{report}
\usepackage{pslatex,palatino,avant,graphicx,color}
   \usepackage[margin=2cm]{geometry}
  % test
% test
      % test
% test
\begin{document}
        \title{\color{red}Practical Typesetting}
\author{\color{blue}Name}
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
"""

    def test_parser_do_not_beautify(self):
        self.parser = LatexParser(self.document, keep_empty_lines=True, do_not_concat_text=True)
        assert self.parser.getResult().getDocument(no_prefix=False) == r"""
\documentclass[11pt,a4paper,oneside]{report}

\usepackage{pslatex,palatino,avant,graphicx,color}
   \usepackage[margin=2cm]{geometry}



  % test
% test
      % test
% test

\begin{document}
        \title{\color{red}Practical Typesetting}
\author{\color{blue}Name}
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
"""

    def __init__(self):
        self.document = r"""
\documentclass[11pt,a4paper,oneside]{report}

\usepackage{pslatex,palatino,avant,graphicx,color}
   \usepackage[margin=2cm]{geometry}



  % test
% test
      % test
% test

\begin{document}
        \title{\color{red}Practical Typesetting}
\author{\color{blue}Name}
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

\end{document}"""