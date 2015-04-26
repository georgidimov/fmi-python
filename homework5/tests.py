import unittest
import solution


class TestFileSystem(unittest.TestCase):
    def test_minimal(self):
        fs = solution.FileSystem(10)
        self.assertEqual(fs.size, 10)
        self.assertEqual(fs.available_size, 9)

    def test_create_directory(self):
        fs = solution.FileSystem(16)
        fs.create('/home', directory=True)
        home = fs.get_node('/home')
        self.assertTrue(home.is_directory)

    def test_create_file(self):
        fs = solution.FileSystem(50)
        content = "Nineteen characters"
        fs.create('/data', content=content)
        file_ = fs.get_node('/data')
        self.assertFalse(file_.is_directory)
        self.assertEqual(file_.content, content)

    def test_overwrite(self):
        fs = solution.FileSystem(32)
        fs.create('/i_was_here_first')
        with self.assertRaises(solution.DestinationNodeExistsError):
            fs.create('/i_was_here_first')

    def test_dir_creation(self):
        fs = solution.FileSystem(50)
        fs.create("/home", True)
        home = fs.get_node("/home")
        self.assertTrue(home.is_directory)



    def test_file_creation(self):
        fs = solution.FileSystem(50)
        content = "123456"
        fs.create("/file", False, content=content)
        file_size = 7
        file_ = fs.get_node("/file")
        self.assertFalse(file_.is_directory)
        self.assertEqual(file_.content, content)
        self.assertEqual(file_.size, file_size)

    def test_dir_nested_creation(self):
        fs = solution.FileSystem(50)
        fs.create("/home", True)
        fs.create("/home/pavel", True)
        fs.create("/home/pafi", False, "pavelll")
        pavel = fs.get_node("/home/pavel")
        pafi = fs.get_node("/home/pafi")
        self.assertTrue(pavel.is_directory)
        self.assertFalse(pafi.is_directory)

    def test_dir_nested_removal(self):
        fs = solution.FileSystem(50)
        root = fs.get_node("/")

        fs.create("/home", True)

        fs.remove("/home", True, True)
        self.assertEqual(root.nodes, [])
        self.assertEqual(root.directories, [])

        fs.create("/home", False, "123")
        fs.remove("/home", False, True)
        self.assertEqual(root.nodes, [])
        self.assertEqual(root.directories, [])

    def test_fs_size_upon_creating_files(self):
        fs = solution.FileSystem(50)
        initial_avb_size = fs.available_size

        fs.create("/home", True)
        fs.create("/home/pavel", True)
        fs.create("/justfile", False, "1234")

        all_sizes = 7
        self.assertEqual(fs.available_size, initial_avb_size - all_sizes)

        fs.create("/home/trip", False, "123")
        fs.create("/home/oshte", True)
        fs.create("/home/oshte/malko", True)
        home = fs.get_node("/home")

        self.assertEqual(home.size, 8)

    def test_creation_exceptions_dest_nodes(self):
        fs = solution.FileSystem(10)
        root = fs.get_node("/")

        with self.assertRaises(solution.DestinationNodeDoesNotExistError):
            fs.create("/tovar/dd", True)

        with self.assertRaises(solution.DestinationNodeDoesNotExistError):
            fs.create("/home/pavel", False, "pipi")

        fs.create("/home", True)
        fs.create("/home/pavel", False, "da")

        with self.assertRaises(solution.DestinationNodeExistsError):
            fs.create("/home")
        with self.assertRaises(solution.DestinationNodeExistsError):
            fs.create("/home/pavel")

    def test_creation_not_enougnh_space(self):
        fs = solution.FileSystem(10)

        fs.create("/home", True)
        fs.create("/file_", False, "12345")
        fs.create("/bin", False, "a")

        with self.assertRaises(solution.NotEnoughSpaceError):
            fs.create("/init", True)

    def test_removing_exceptions(self):
        fs = solution.FileSystem(10)

        fs.create("/home", True)

        with self.assertRaises(solution.NonExplicitDirectoryDeletionError):
            fs.remove("/home", False, True)

        fs.create("/home/pavel", False, "opa")

        with self.assertRaises(solution.NonEmptyDirectoryDeletionError):
            fs.remove("/home", True, False)

        with self.assertRaises(solution.NodeDoesNotExistError):
            fs.remove("/random/random", True, True)

            # CHECK THOSE
    def test_fs_upon_removing_no_nesting_directory(self):
        fs = solution.FileSystem(50)
        fs.create("/dir_", True)
        self.assertEqual(48, fs.available_size)
        fs.remove("/dir_", True)
        root = fs.get_node("/")
        self.assertEqual(root.directories, [])
        self.assertEqual(root.nodes, [])

    def test_fs_size_upon_removing_no_nesting_file(self):
        fs = solution.FileSystem(50)
        fs.create("/file_", False, "12345")
        self.assertEqual(43, fs.available_size)
        fs.remove("/file_", False)
        root = fs.get_node("/")
        self.assertEqual(root.files, [])
        self.assertEqual(root.nodes, [])

    def test_multiple_dir_nesting(self):

        fs = solution.FileSystem(50)
        fs.create("/home", True)
        fs.create("/home/oshte", True)
        fs.create("/home/oshte/malko", True)

    def test_size_on_remove(self):

        fs = solution.FileSystem(50)
        root = fs.get_node("/")
        fs.create("/home" , True)
        home = fs.get_node("/home")
        self.assertEqual(home.size, 1)
        fs.create("/home/pavel", True)
        self.assertEqual(home.size, 2)
        fs.create("/home/file", False, "123")
        self.assertEqual(home.size, 6)
        fs.remove("/home/file", False)
        self.assertEqual(home.size, 2)
        fs.create("/home/file", False, "123")
        self.assertEqual(home.size, 6)
        fs.remove("/home", True, True)
        self.assertEqual(root.size, 1)

    def test_move_exceptions(self):
        fs = solution.FileSystem(50)

        fs.create("/home", True)
        fs.create("/home/folder", True)
        fs.create("/home/home_file", False, "12")
        fs.create("/folder", True)
        fs.create("/home_file", False, "1111")

        with self.assertRaises(solution.SourceNodeDoesNotExistError):
            fs.move("/not_here", "/home")

        with self.assertRaises(solution.DestinationNodeDoesNotExistError):
            fs.move("/home", "/not_here")

        with self.assertRaises(solution.DestinationNotADirectoryError):
            fs.move("/home", "/home_file")

        with self.assertRaises(solution.DestinationNodeExistsError):
            fs.move("/folder", "/home")

        fs.remove("/home/home_file")
        fs.create("/home/home_file", True)
        with self.assertRaises(solution.DestinationNodeExistsError):
            fs.move("/home_file", "/home")

    def test_move_directory(self):

        fs = solution.FileSystem(50)

        fs.create("/home", True)
        fs.create("/bin", True)
        fs.create("/bin/pavel", True)

        fs.move("/bin", "/home")
        home = fs.get_node("/home")
        self.assertEqual(len(home.directories), 1)


    def test_move_file(self):
        fs = solution.FileSystem(50)
        fs.create("/home", True)
        fs.create("/home/pavel", False, "132")

        fs.move("/home/pavel", "/")
        self.assertEqual(len(fs.root.files), 1)
        self.assertEqual(len(fs.root.directories), 1)
        self.assertEqual(len(fs.root.nodes), 2)

    def test_move_sizes(self):
        fs = solution.FileSystem(50)
        root = fs.get_node("/")
        fs.create("/home", True)
        home = fs.get_node("/home")
        fs.create("/bin", True)
        fs.create("/bin/bash", False, "123")
        bin_ = fs.get_node("/bin")
        self.assertEqual(root.size, 7)
        self.assertEqual(home.size, 1)
        self.assertEqual(bin_.size, 5)
        fs.move("/bin/bash", "/home")
        self.assertEqual(root.size, 7)
        self.assertEqual(home.size, 5)
        self.assertEqual(bin_.size, 1)



if __name__ == '__main__':
    unittest.main()