class BaseFile:
    def __init__(self, is_directory):
        self.is_directory = is_directory


class File(BaseFile):
    def __init__(self, content):
        BaseFile.__init__(self, False)
        self.content = content

    def append(self, text):
        self.content += text

    def truncate(self, text):
        self.content = text

    def __getattr__(self, name):
        if name == 'size':
            return len(self.content) + 1


class Directory(BaseFile):
    def __init__(self):
        BaseFile.__init__(self, True)
        self.files = {}
        self.directories = {}

    def __getattribute__(self, name):
        if name == 'files' or name == 'directories':
            return list(self.__dict__[name].keys())
        else:
            return BaseFile.__getattribute__(self, name)

    def add_file(self, file_name, file_object):
        self.__dict__['files'].update({file_name: file_object})

    def add_directory(self, directory_name, directory_object):
        self.__dict__['directories'].update({directory_name: directory_object})
'''
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


class FileSystem:
    def __init__(self, size):
        self.size = size
        self.available_size = size
        self.home = {"/": Directory()}

    def get_node(self, path):
        path = path.split('/', 1)[-1]
        print(path)

        if path in self.home:
            return self.home[path]
        else:
            #print(path.split('/', 1)[-1])
            print("f")
f = FileSystem(5)
f.get_node('/home/georgi/usr/share')
'''
d = Directory()
f = File("first_File_content_here")
d.add_file("first_file", f)
d.add_file("second_file", File("second file"))
print(d.files)

d.add_directory("dir 1", Directory())
print(d.directories)
