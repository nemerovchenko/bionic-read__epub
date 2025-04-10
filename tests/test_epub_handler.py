import os
import zipfile
import unittest
from src.epub.epub_handler import read_epub, write_epub

class TestEpubHandler(unittest.TestCase):

    def setUp(self):
        self.test_input_path = 'samples/sample.epub'
        self.test_output_path = 'samples/output.epub'

    def test_read_epub(self):
        content = read_epub(self.test_input_path)
        self.assertIsNotNone(content)
        self.assertTrue(len(content) > 0)

    def test_write_epub(self):
        content = b'Test content for EPUB'
        write_epub(self.test_output_path, content)
        self.assertTrue(os.path.exists(self.test_output_path))

    def tearDown(self):
        if os.path.exists(self.test_output_path):
            os.remove(self.test_output_path)

if __name__ == '__main__':
    unittest.main()