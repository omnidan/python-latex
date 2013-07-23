from latex import LatexDocument, LatexCommand, LatexText


class TestLatexDocument:
    def test_set_content_line(self):
        doc = LatexDocument()
        doc.addContentLine(LatexCommand("test", "test"))
        doc.addContentLine(LatexText("text"))
        assert doc.getLinesContent()[0].getString() == r"\test" and doc.getLinesContent()[1].getString() == r"text"

    def test_set_header_line(self):
        doc = LatexDocument()
        doc.addHeaderLine(LatexCommand("test", "test"))
        doc.addHeaderLine(LatexText("text"))
        assert doc.getLinesHeader()[0].getString() == r"\test" and doc.getLinesHeader()[1].getString() == r"text"

    def test_set_content(self):
        doc = LatexDocument()
        doc.setContent([LatexCommand("test", "test"), LatexText("text")])
        assert doc.getLinesContent()[0].getString() == r"\test" and doc.getLinesContent()[1].getString() == r"text"

    def test_set_header(self):
        doc = LatexDocument()
        doc.setHeader([LatexCommand("test", "test"), LatexText("text")])
        assert doc.getLinesHeader()[0].getString() == r"\test" and doc.getLinesHeader()[1].getString() == r"text"

    def test_getlines(self):
        doc = LatexDocument()
        header = [LatexCommand("head", "head"), LatexText("headtext")]
        content = [LatexCommand("content", "content"), LatexText("contenttext")]
        doc.setHeader(header)
        doc.setContent(content)
        assert doc.getLines() == (header + content)

    def test_getdocument(self):
        doc = LatexDocument()
        header = [LatexCommand("head", "head"), LatexText("headtext")]
        content = [LatexCommand("content", "content"), LatexText("contenttext")]
        doc.setHeader(header)
        doc.setContent(content)
        assert doc.getDocument() == r"""\head
headtext
\content
contenttext"""