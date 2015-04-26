class BaseFile:
    def __init__(self, is_directory):
        self.is_derectory = is_directory


class File(BaseFile):
    def __init__(self, content):
        BaseFile.__init__(self, False)
        self.content = content

    def append(self, text):
        self.content += text

    def truncate(self, text):
        self.content = text

    def size(self):
        return len(self.content) + 1
f = File("a")
print(f.content)
f.truncate("new content")
print(f.content)
print(f.size())
