import unittest
import solution


class TestFileSystem(unittest.TestCase):

    def setUp(self):
        self.fs = solution.FileSystem(32)
        self.test_file_content = 'Nineteen characters'

    def create_directory(self, path):
        self.fs.create(path, directory=True)
        return self.fs.get_node(path)

    def create_data_file(self, path):
        self.fs.create(path, content=self.test_file_content)
        return self.fs.get_node(path)


class TestFileSystemGeneral(TestFileSystem):

    def test_get_node_no_path(self):
        with self.assertRaises(solution.NodeDoesNotExistError):
            self.fs.get_node('')

    def test_minimal(self):
        self.assertEqual(self.fs.size, 32)
        self.assertEqual(self.fs.available_size, 31)

    def test_node_has_is_dir_attr(self):
        self.create_directory('/home')
        self.assertTrue(self.fs.get_node('/home').is_directory)
        self.create_data_file('/data')
        self.assertFalse(self.fs.get_node('/data').is_directory)


class TestFileSystemFile(TestFileSystem):

    def setUp(self):
        super(TestFileSystemFile, self).setUp()
        self.create_data_file('/data')
        self.data = self.fs.get_node('/data')

    def test_file_size(self):
        self.assertEqual(self.data.size, 20)

    def test_append_to_file_content(self):
        self.data.append(' and more')
        self.assertEqual(self.data.content,
                         self.test_file_content + ' and more')

    def test_truncate_file_content(self):
        self.data.truncate('Twentyone characters.')
        self.assertEqual(self.data.content, 'Twentyone characters.')


class TestFileSystemDirectory(TestFileSystem):

    def setUp(self):
        super(TestFileSystemDirectory, self).setUp()
        self.create_directory('/home')
        self.create_data_file('/home/data')
        self.create_directory('/home/user')
        self.home = self.fs.get_node('/home')
        self.data = self.fs.get_node('/home/data')
        self.user = self.fs.get_node('/home/user')

    def test_directory_nodes(self):
        self.assertCountEqual(self.home.nodes, [self.data, self.user])

    def test_directory_files(self):
        self.assertCountEqual(self.home.files, [self.data])

    def test_directory_subdirectories(self):
        self.assertCountEqual(self.home.directories, [self.user])


class TestFileSystemCreate(TestFileSystem):

    def test_create_directory(self):
        home = self.create_directory('/home')
        self.assertTrue(home.is_directory)

    def test_create_file(self):
        data = self.create_data_file('/data')
        self.assertFalse(data.is_directory)
        self.assertEqual(data.content, self.test_file_content)
        self.assertEqual(self.fs.available_size, 11)

    def test_create_file_no_destination(self):
        with self.assertRaises(solution.DestinationNodeDoesNotExistError):
            self.fs.create('/home/data', content='Nineteen characters')

    def test_create_file_not_enough_space(self):
        self.fs = solution.FileSystem(21)
        self.create_data_file('/data')
        with self.assertRaises(solution.NotEnoughSpaceError):
            self.fs.create('/gosho')

    def test_overwrite(self):
        self.fs.create('/i_was_here_first')
        with self.assertRaises(solution.DestinationNodeExistsError):
            self.fs.create('/i_was_here_first')


class TestFileSystemWithNodes(TestFileSystem):

    def setUp(self):
        super(TestFileSystemWithNodes, self).setUp()
        self.home_path = '/home'
        self.data_path = '/home/data'
        self.home = self.create_directory(self.home_path)
        self.data = self.create_data_file(self.data_path)


class TestFileSystemRemove(TestFileSystemWithNodes):

    def test_remove_file(self):
        self.fs.remove(self.data_path)
        self.assertEqual(self.home.nodes, [])

    def test_remove_directory(self):
        root = self.fs.get_node('/')
        self.fs.remove(self.home_path, directory=True)
        self.assertEqual(root.nodes, [])

    def test_remove_not_empty_directory_without_force(self):
        with self.assertRaises(solution.NonEmptyDirectoryDeletionError):
            self.fs.remove(self.home_path, directory=True,  force=False)

    def test_remove_directory_without_flag(self):
        with self.assertRaises(solution.NonExplicitDirectoryDeletionError):
            self.fs.remove(self.home_path)

    def test_remove_non_existent(self):
        with self.assertRaises(solution.NodeDoesNotExistError):
            self.fs.remove('/home/non-existent')


class TestFileSystemMove(TestFileSystemWithNodes):

    def test_move_file(self):
        root = self.fs.get_node('/')
        self.fs.move(self.data_path, '/')
        self.assertEqual(self.home.nodes, [])
        self.assertIn(self.data, root.nodes)

    def test_move_source_does_not_exist(self):
        with self.assertRaises(solution.SourceNodeDoesNotExistError):
            self.fs.move('/home/non-existent', '/')

    def test_move_destination_does_not_exist(self):
        with self.assertRaises(solution.DestinationNodeDoesNotExistError):
            self.fs.move(self.data_path, '/non-existent')

    def test_move_destination_not_directory(self):
        self.fs.create('/home/not-a-directory')
        with self.assertRaises(solution.DestinationNotADirectoryError):
            self.fs.move(self.data_path, '/home/not-a-directory')

    def test_move_source_exists_in_destination(self):
        self.fs.create('/data', content='')
        with self.assertRaises(solution.DestinationNodeExistsError):
            self.fs.move(self.data_path, '/')


class TestFileSystemSymbolicLink(TestFileSystemWithNodes):

    def test_link_file_symbolic(self):
        self.fs.link(self.data_path, '/home/more-data')
        link = self.fs.get_node('/home/more-data')
        self.assertEqual(link.content, 'Nineteen characters')
        self.assertIn(link, self.home.files)

    def test_link_directory_symbolic(self):
        self.fs.link(self.home_path, '/other-dir')
        link = self.fs.get_node('/other-dir')
        self.assertEqual(link.nodes, [self.data])
        self.assertEqual(link.files, [self.data])
        self.assertEqual(link.directories, [])
        self.assertIn(link, self.fs.get_node('/').directories)

    def test_link_path_error(self):
        self.fs.link(self.home_path, '/other-dir')
        link = self.fs.get_node('/other-dir')
        with self.assertRaises(solution.LinkPathError):
            link.content

    def test_no_source(self):
        with self.assertRaises(solution.NodeDoesNotExistError):
            self.fs.link('/non-existent', '/other-dir')

    def test_available_size(self):
        self.fs.link(self.data_path, '/more-data')
        self.assertEqual(self.fs.available_size, 9)


class TestFileSystemHardLink(TestFileSystemWithNodes):

    def test_link_file_hard(self):
        self.fs.link(self.data_path, '/same-data', symbolic=False)
        link = self.fs.get_node('/same-data')
        self.assertEqual(link.content, self.test_file_content)
        self.assertIsNot(link, self.data)
        self.assertIs(link.content, self.data.content)

    def test_append_to_link(self):
        self.fs.link(self.data_path, '/same-data', symbolic=False)
        link = self.fs.get_node('/same-data')
        self.data.append(' and more')
        self.assertEqual(link.content, self.data.content)
        link.append(' and more')
        self.assertEqual(link.content, self.data.content)

    def test_truncate_link_content(self):
        self.fs.link(self.data_path, '/same-data', symbolic=False)
        link = self.fs.get_node('/same-data')
        self.data.truncate('Twentyone characters.')
        self.assertEqual(link.content, self.data.content)
        link.truncate('Something else...')
        self.assertEqual(link.content, self.data.content)

    def test_link_no_source_node(self):
        with self.assertRaises(solution.SourceNodeDoesNotExistError):
            self.fs.link('/non-existent', '/other-dir', symbolic=False)

    def test_link_hard_is_directory(self):
        with self.assertRaises(solution.DirectoryHardLinkError):
            self.fs.link(self.home_path, '/other-dir', symbolic=False)

    def test_available_size(self):
        self.fs.link(self.data_path, '/more-data', symbolic=False)
        self.assertEqual(self.fs.available_size, 9)


class TestFileSystemMount(TestFileSystemWithNodes):

    def setUp(self):
        super(TestFileSystemMount, self).setUp()
        self.other_fs = solution.FileSystem(5)

    def test_mount_file_system(self):
        self.fs.create('/mount_dir', directory=True)
        self.fs.mount(self.other_fs, '/mount_dir')
        self.assertIs(self.other_fs.get_node('/'),
                      self.fs.get_node('/mount_dir'))

    def test_mount_point_non_existent(self):
        with self.assertRaises(solution.MountPointDoesNotExistError):
            self.fs.mount(self.other_fs, '/non-existent')

    def test_mount_point_not_directory(self):
        with self.assertRaises(solution.MountPointNotADirectoryError):
            self.fs.mount(self.other_fs, self.data_path)

    def test_mount_point_not_empty(self):
        with self.assertRaises(solution.MountPointNotEmptyError):
            self.fs.mount(self.other_fs, self.home_path)


class TestFileSystemUnmount(TestFileSystemWithNodes):

    def setUp(self):
        super(TestFileSystemUnmount, self).setUp()
        self.other_fs = solution.FileSystem(5)
        self.mount_path = '/mount_dir'
        self.fs.create(self.mount_path, directory=True)
        self.fs.mount(self.other_fs, self.mount_path)

    def test_unmount_file_system(self):
        self.fs.unmount(self.mount_path)
        self.assertIsNot(self.other_fs.get_node('/'),
                         self.fs.get_node(self.mount_path))

    def test_unmount_not_mount_point(self):
        with self.assertRaises(solution.NotAMountpointError):
            self.fs.unmount(self.home_path)


if __name__ == '__main__':
    unittest.main()
