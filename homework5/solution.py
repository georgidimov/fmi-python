class FileSystemError(Exception):
    def __init__(self, message=''):
        self.message = message


class DestinationNodeExistsError(FileSystemError):
    pass


class NodeDoesNotExistError(FileSystemError):
    pass


class SourceNodeDoesNotExistError(NodeDoesNotExistError):
    pass


class DestinationNodeDoesNotExistError(NodeDoesNotExistError):
    pass


class FileSystemMountError(FileSystemError):
    pass


class MountPointDoesNotExistError(FileSystemMountError):
    pass


class MountPointNotADirectoryError(FileSystemMountError):
    pass


class MountPointNotEmptyError(FileSystemMountError):
    pass


class NotEnoughSpaceError(FileSystemError):
    pass


class FileSystemDirectoryError(FileSystemError):
    pass


class NonExplicitDirectoryDeletionError(FileSystemDirectoryError):
    pass


class NonEmptyDirectoryDeletionError(FileSystemDirectoryError):
    pass


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
        self.files_pool = {}
        self.dirs_pool = {}

    def __getattribute__(self, name):
        def get_objects(name):
            return list(object.__getattribute__(self, name).values())

        def get_pool(name):
            return object.__getattribute__(self, name)

        attributes = {
            'files': get_objects('files_pool'),
            'directories': get_objects('dirs_pool'),
            'nodes': get_objects('files_pool') + get_objects('dirs_pool'),
            'nodes_pool': dict(get_pool('files_pool'), **get_pool('dirs_pool'))
        }

        if name in attributes:
            return attributes[name]
        else:
            return BaseFile.__getattribute__(self, name)

    def __getattr__(self, name):
        def get_size():
            size = 1

            for current_file in self.files:
                size += current_file.size

            for current_directory in self.directories:
                size += current_directory.size

            return size

        attributes = {
            'size': get_size()
        }

        return attributes['size']

    def __getitem__(self, current_object):
        if current_object in self.nodes_pool:
            return self.nodes_pool[current_object]
        else:
            raise NodeDoesNotExistError

    def add_file(self, file_name, file_object):
        self.files_pool.update({file_name: file_object})

    def add_directory(self, directory_name, directory_object):
        self.dirs_pool.update({directory_name: directory_object})

    def remove(self, object_to_remove, directory=False, force=True):
        if object_to_remove not in self.__dict__['directories']:
            raise NodeDoesNotExistError
        '''
        if object_to_remove not in self.__dict__['files']:
            raise NodeDoesNotExistError

        if object_to_remove in self.directories:
            if not directory:
                raise NonExplicitDirectoryDeletionError

            if not object_to_remove.nodes == []:
                raise NonEmptyDirectoryDeletionError

            ###
            irectory_to_remove = self.__dict__['directories'][object_to_remove]

            for node in directory_to_remove.nodes:
                del nod

        else:
            del self.__dict__['files'][object_to_remove]
        '''

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
        if not size > 0:
            raise NotEnoughSpaceError

        self.home = Directory()
        self.size = size
        self.available_size = self.size - self.home.size

    def __find_object(self, current_directory, path):
        if path.count('/') < 2:
            if len(path) > 1:
                current_object = path.split('/')[-1]
                return current_directory[current_object]
            else:
                return current_directory
        else:
            current_path, rest_path = path.lstrip('/').split('/', 1)
            current_directory = current_directory[current_path.lstrip('/')]
            return self.__find_object(current_directory, '/' + rest_path)

    def get_node(self, path):
        if path == '':
            raise NodeDoesNotExistError
        else:
            return self.__find_object(self.home, path)

    def create(self, path, directory=False, content=''):
        current_path, object_name = path.rsplit('/', 1)

        try:
            parent_directory = self.__find_object(self.home, current_path)
        except NodeDoesNotExistError:
            raise DestinationNodeDoesNotExistError

        try:
            self.get_node(path)
        except NodeDoesNotExistError:
            pass
        else:
            raise DestinationNodeExistsError

        if not directory:
            new_file = File(content)
            new_object_size = new_file.size

            if not self.available_size - new_object_size >= 0:
                raise NotEnoughSpaceError

            parent_directory.add_file(object_name, new_file)
        else:
            new_directory = Directory()
            new_object_size = new_directory.size

            if not self.available_size - new_object_size >= 0:
                raise NotEnoughSpaceError
            parent_directory.add_directory(object_name, new_directory)

        self.available_size -= new_object_size

d = Directory()
d.add_directory('dir1', Directory())
d.add_directory('dir2', Directory())
d.add_file('file1', File('some text'))
print(d.size)
