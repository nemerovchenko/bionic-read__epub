import os
import unittest
from src.converter import process_text, process_html_content, bionic_word

class TestConverter(unittest.TestCase):

    def test_bionic_word(self):
        self.assertEqual(bionic_word("a"), "a")
        self.assertEqual(bionic_word("ab"), "<b>a</b>b")
        self.assertEqual(bionic_word("abc"), "<b>a</b>bc")
        self.assertEqual(bionic_word("abcd"), "<b>ab</b>cd")
        self.assertEqual(bionic_word("abcdef"), "<b>abc</b>def")

    def test_process_text(self):
        input_text = "This is a test."
        expected_output = "This is a <b>te</b>st."
        self.assertEqual(process_text(input_text), expected_output)

    def test_process_html_content(self):
        input_html = "<p>This is a <strong>test</strong>.</p>"
        expected_output = "<p>This is a <strong>te</strong>st.</p>"
        self.assertEqual(process_html_content(input_html), expected_output)

if __name__ == '__main__':
    unittest.main()