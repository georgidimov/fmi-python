class BaseFile:
    def __init__(self, is_directory):
        self.is_derectory = is_directory


class File(BaseFile):
    def __init__(self, content):
        BaseFile.__init__(self, False)
        self.content = content
        self.size = len(content) + 1

    def append(self, text):
        self.content += text
        self.size += len(text)

    def truncate(self, text):
        self.content = text
        self.size = len(text)


class Directory(BaseFile):
    def __init__(self):
        BaseFile.__init__(self, True)
        self.files = []
        self.directories = []
        self.nodes = []


class BaseLink:
    def __init__(self, link_path, symbolic=True):
        self.link_path = link_path
        self.symbolic = symbolic


class SymbolicLink(BaseLink):
    def __init__(self, link_path):
        BaseLink.__init__(self, link_path)


class HardLink(BaseLink):
    def __init__(self, link_path, symbolic):
        BaseLink.__init__(self, link_path, symbolic)

h = HardLink("/", False)
print(h.link_path)
