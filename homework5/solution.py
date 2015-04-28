class BaseFile:
    def __init__(self, is_directory):
        self.is_directory = is_directory


class File(BaseFile):
    def __init__(self, content):
        BaseFile.__init__(self, False)
        self.content = content

    def __getattr__(self, name):
        if name == 'size':
            return len(self.content) + 1

    def append(self, text):
        self.content += text

    def truncate(self, text):
        self.content = text


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

    def __getitem__(self, current_object):
        if current_object in self.__dict__['files']:
            return self.__dict__['files'][current_object]
        elif current_object in self.__dict__['directories']:
            return self.__dict__['directories'][current_object]
        else:
            raise "no such file or directory"

    def __getattr__(self, name):
        if name == 'size':
            return 1

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

'''


class FileSystem:
    def __init__(self, size):
        self.home = Directory()
        self.size = size
        self.available_size = self.size - self.home.size

    def __find_object(self, current_directory, path):
        if path.count('/') <= 2:
            if len(path) > 1:
                path = path.lstrip('/')
                return current_directory[path]
            else:
                return current_directory
        else:
            current_path, rest_path = path.split('/', 1)
            print(rest_path)
            current_directory = current_directory[current_path]
            return self.find_object(current_directory, '/' + rest_path)

    def get_node(self, path):
        return self.__find_object(self.home, path)

    def create(self, path, directory=False, content=''):
        path, object_name = path.split('/', 1)
        parent_directory = self.__find_object(self.home, '/' + path)

        if not directory:
            new_file = File(content)
            parent_directory.add_file(object_name, new_file)
            new_object_size = new_file.size
        else:
            new_directory = Directory()
            parent_directory.add_directory(object_name, new_directory)
            new_object_size = new_directory.size

        self.available_size -= 1


#fs = FileSystem(50)
#fs.create('/home', directory=True)
#print(fs.get_node('/home').is_directory)


'''
d = Directory()
f = File("first_File_content_here")
d.add_file("first_file", f)
d.add_file("second_file", File("second file"))

d.add_directory("dir 1", Directory())

print(d['dir 1/'].files)
'''
