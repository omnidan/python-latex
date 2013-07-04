class LatexDocument:
    def __init__(self, documentclass="report", packages={}, content="", title="", author="", date=""):
        self.documentclass = documentclass
        self.packages = packages
        self.content = content
        self.title = title
        self.author = author
        self.date = date

