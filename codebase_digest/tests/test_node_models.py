import unittest
from models import NodeAnalysis, DirectoryAnalysis, TextFileAnalysis

class TestNodeAnalysis(unittest.TestCase):
    
        def test_node_analysis(self):
            node = NodeAnalysis("test")
            self.assertEqual(node.name, "test")
    
        def test_directory_analysis(self):
            directory = DirectoryAnalysis("test")
            self.assertEqual(directory.name, "test")
            self.assertEqual(directory.type, "directory")
    
        def test_text_file_analysis(self):
            text_file = TextFileAnalysis("test")
            self.assertEqual(text_file.name, "test")
            self.assertEqual(text_file.type, "text_file")

        def test_empty_directory_analysis(self):
            directory = DirectoryAnalysis("test")
            self.assertEqual(directory.get_file_count(), 0)
            self.assertEqual(directory.get_dir_count(), 0)
            self.assertEqual(directory.get_total_tokens(), 0)
            self.assertEqual(directory.get_non_ignored_text_content_size(), 0)
            self.assertEqual(directory.size, 0)
        
        def test_directory_with_one_text_file(self):
            directory = DirectoryAnalysis("test")
            text_file = TextFileAnalysis("test")
            text_file.file_content = "length of this string is 27"

            directory.children.append(text_file)
            self.assertEqual(directory.get_file_count(), 1)
            self.assertEqual(directory.get_dir_count(), 0)
            self.assertEqual(directory.get_non_ignored_text_content_size(), 27)
            self.assertEqual(directory.size, 27)

        def test_directory_with_ten_files(self):
            directory = DirectoryAnalysis("test")
            for i in range(10):
                text_file = TextFileAnalysis("test")
                text_file.file_content = "length of this string is 27"
                directory.children.append(text_file)
            self.assertEqual(directory.get_file_count(), 10)
            self.assertEqual(directory.get_dir_count(), 0)
            self.assertEqual(directory.get_non_ignored_text_content_size(), 270)
            self.assertEqual(directory.size, 270)

        def test_directory_with_one_sub_directory(self):
            directory = DirectoryAnalysis("test")
            sub_directory = DirectoryAnalysis("test")
            text_file = TextFileAnalysis("test")
            text_file.file_content = "length of this string is 27"
            sub_directory.children.append(text_file)
            directory.children.append(sub_directory)
            self.assertEqual(directory.get_file_count(), 1)
            self.assertEqual(directory.get_dir_count(), 1)
            self.assertEqual(directory.get_non_ignored_text_content_size(), 27)
            self.assertEqual(directory.size, 27)

        def test_directory_with_one_ignored_file(self):
            directory = DirectoryAnalysis("test")
            text_file = TextFileAnalysis("test")
            text_file.is_ignored = True
            text_file.file_content = "length of this string is 27"
            directory.children.append(text_file)
            self.assertEqual(directory.get_file_count(), 0)
            self.assertEqual(directory.get_dir_count(), 0)
            self.assertEqual(directory.get_non_ignored_text_content_size(), 0)
            self.assertEqual(directory.size, 27)

        def test_directory_with_one_ignored_sub_directory(self):
            directory = DirectoryAnalysis("test")
            sub_directory = DirectoryAnalysis("test")
            sub_directory.is_ignored = True
            text_file = TextFileAnalysis("test")
            text_file.file_content = "length of this string is 27"
            sub_directory.children.append(text_file)
            directory.children.append(sub_directory)
            self.assertEqual(directory.get_file_count(), 0)
            self.assertEqual(directory.get_dir_count(), 0)
            self.assertEqual(directory.get_non_ignored_text_content_size(), 0)
            self.assertEqual(directory.size, 27)

        def test_directory_with_one_ignored_file_and_one_text_file(self):
            directory = DirectoryAnalysis("test")
            text_file = TextFileAnalysis("test")
            text_file.is_ignored = True
            text_file.file_content = "length of this string is 27"
            directory.children.append(text_file)
            text_file = TextFileAnalysis("test")
            text_file.file_content = "length of this string is 27"
            directory.children.append(text_file)
            self.assertEqual(directory.get_file_count(), 1)
            self.assertEqual(directory.get_dir_count(), 0)
            self.assertEqual(directory.get_non_ignored_text_content_size(), 27)
            self.assertEqual(directory.size, 54)