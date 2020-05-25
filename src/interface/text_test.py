import unittest
from src.interface.text import Text


class TextTest(unittest.TestCase):
    def test_renders_list_comprehension_without_wrapping(self):
        text = "[item.id for item in items if item.name = 'certain_item']"
        width = len(text)

        result = Text.format(text, width)
        self.assertEqual(text, result)
