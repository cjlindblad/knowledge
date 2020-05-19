import unittest
from src.core.parser import Parser
from src.core.knowledge_item import KnowledgeItem


class ParserTest(unittest.TestCase):
    def setUp(self):
        self.fields = {
            'title': 'test title',
            'category': 'test category',
            'content': 'test content\n'
        }

    def __text_representation(self, fields):
        return f'title: {fields["title"]}\ncategory: {fields["category"]}\ncontent: {fields["content"]}'

    def __knowledge_item(self, fields):
        item = KnowledgeItem()
        item.title = self.fields['title']
        item.category = self.fields['category']
        item.content = self.fields['content']
        return item

    def test_parses_plain_knowledge_item(self):
        item = self.__knowledge_item(self.fields)

        text = Parser.knowledge_item_to_text(item)

        expected_result = self.__text_representation(self.fields)

        self.assertEqual(text, expected_result)

    def test_parses_plain_textual_representation(self):
        text = self.__text_representation(self.fields)

        item = Parser.text_to_knowledge_item(text)

        self.assertEqual(self.fields['title'], item.title)
        self.assertEqual(self.fields['category'], item.category)
        self.assertEqual(self.fields['content'], item.content)

    def test_parses_multiline_textual_representation(self):
        content = 'multi\nline\ncontent'
        self.fields['content'] = content
        text = self.__text_representation(self.fields)

        item = Parser.text_to_knowledge_item(text)

        self.assertEqual(content, item.content)

    def test_parses_multiline_textual_representation_with_trailing_newline(self):
        content = 'multi\nline\ncontent\n'
        self.fields['content'] = content
        text = self.__text_representation(self.fields)

        item = Parser.text_to_knowledge_item(text)

        self.assertEqual(content, item.content)

    def test_parses_multiline_item_content(self):
        content = 'multi\nline\ncontent'
        self.fields['content'] = content
        item = self.__knowledge_item(self.fields)

        expected_result = self.__text_representation(self.fields)
        text = Parser.knowledge_item_to_text(item)

        self.assertEqual(expected_result, text)

    def test_parses_multiline_item_content_with_trailing_newline(self):
        content = 'multi\nline\ncontent\n'
        self.fields['content'] = content
        item = self.__knowledge_item(self.fields)

        expected_result = self.__text_representation(self.fields)
        text = Parser.knowledge_item_to_text(item)

        self.assertEqual(expected_result, text)


if __name__ == '__main__':
    unittest.main()
