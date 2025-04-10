import unittest
from src.utils.text_processing import bionic_word, process_text

class TestTextProcessing(unittest.TestCase):

    def test_bionic_word_single_character(self):
        self.assertEqual(bionic_word('a'), 'a')

    def test_bionic_word_two_characters(self):
        self.assertEqual(bionic_word('ab'), '<b>a</b>b')

    def test_bionic_word_three_characters(self):
        self.assertEqual(bionic_word('abc'), '<b>ab</b>c')

    def test_bionic_word_four_characters(self):
        self.assertEqual(bionic_word('abcd'), '<b>ab</b>cd')

    def test_process_text(self):
        input_text = "This is a test."
        expected_output = "This is <b>a</b> test."
        self.assertEqual(process_text(input_text), expected_output)

    def test_process_text_with_unicode(self):
        input_text = "Café"
        expected_output = "C<b>a</b>fé"
        self.assertEqual(process_text(input_text), expected_output)

if __name__ == '__main__':
    unittest.main()