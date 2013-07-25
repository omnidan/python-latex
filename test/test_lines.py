from latex import LatexLine, LatexCommand, LatexText, LatexComment, LatexMacro, LatexEnvironmentMacro


class TestLatexLine:
    def test_init(self):
        assert self.obj.getString() == ""

    def __init__(self):
        self.obj = LatexLine()


class TestLatexCommand:
    def test_name(self):
        assert self.obj.command_name == "test"

    def test_options(self):
        assert self.obj.command_options == ["option1", "option2"]

    def test_adoptions(self):
        assert self.obj.additional_options == ["test1", "test2", "option3"]

    def __init__(self):
        self.obj = LatexCommand("test", ["option"], ["additional_option"], True)
        self.obj.parseOptions("option1,option2", "test1,test2,option3")
        # the command_options and additional_options lists should have changed now


class TestLatexMacro:
    def test_name(self):
        assert self.obj.macro_name == "test"

    def test_string(self):
        assert self.obj.getString() == r"\newcommand{\test}{\rule{1ex}{1ex}\hspace{\stretch{1}}}"

    def test_string_argc(self):
        assert self.obj_argc.getString() == r"\newcommand{\test}[2]{\rule{1ex}{1ex} #1 \hspace #2 {\stretch{1}}}"

    def __init__(self):
        self.obj = LatexMacro("test", r"\rule{1ex}{1ex}\hspace{\stretch{1}}")
        self.obj_argc = LatexMacro("test", r"\rule{1ex}{1ex} #1 \hspace #2 {\stretch{1}}", 2)


class TestLatexEnvironmentMacro:
    def test_name(self):
        assert self.obj.macro_name == "test"

    def test_string(self):
        assert self.obj.getString() == \
            r"\newenvironment{\test}{\rule{1ex}{1ex}\hspace{\stretch{1}}}{\rule{1ex}{1ex}\vspace{\stretch{1}}}"

    def test_string_argc(self):
        assert self.obj_argc.getString() == \
            r"\newenvironment{\test}[2]{#1 \hspace #2 {\stretch{1}}}{#1 \vspace #2 {\stretch{1}}}"

    def __init__(self):
        self.obj = LatexEnvironmentMacro("test", r"\rule{1ex}{1ex}\hspace{\stretch{1}}",
                                         r"\rule{1ex}{1ex}\vspace{\stretch{1}}")
        self.obj_argc = LatexEnvironmentMacro("test", r"#1 \hspace #2 {\stretch{1}}",
                                              r"#1 \vspace #2 {\stretch{1}}", 2)


class TestLatexText:
    def test_init(self):
        assert self.obj.getString() == "Hello World."

    def __init__(self):
        self.obj = LatexText("Hello", append_prefix=" ", append_suffix=".")
        self.obj.append("World")


class TestLatexComment:
    def test_init(self):
        assert self.obj.getString() == "% Hello World."

    def __init__(self):
        self.obj = LatexComment("Hello", append_prefix=" ", append_suffix=".", comment_prefix="% ")
        self.obj.append("World")
