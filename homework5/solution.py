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
