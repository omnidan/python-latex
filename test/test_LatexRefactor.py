import os
import subprocess


class TestLatexRefactor:
    def test_result(self):
        assert self.result == "done.\n"

    def __init__(self):
        os.chdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "scripts"))
        self.result = str(subprocess.check_output(["python", "LatexRefactor.py", "example.tex", "output.tex"],
                                                  universal_newlines=True))