import unittest
from src.core.parser import knowledge_item_to_text, text_to_knowledge_item
from src.core.knowledge_item import KnowledgeItem


class ParserTest(unittest.TestCase):
    def setUp(self):
        self.fields = {
            'title': 'test title',
            'category': 'test category',
            'content': 'test content'
        }

    def __text_representation(self, fields):
        return f'title: {fields["title"]}\ncategory: {fields["category"]}\ncontent: {fields["content"]}\n'

    def test_parses_plain_knowledge_item(self):
        item = KnowledgeItem()
        item.title = self.fields['title']
        item.category = self.fields['category']
        item.content = self.fields['content']

        text = knowledge_item_to_text(item)

        expected_result = self.__text_representation(self.fields)

        self.assertEqual(text, expected_result)

    def test_parses_plain_textual_representation(self):
        text = self.__text_representation(self.fields)

        item = text_to_knowledge_item(text)

        self.assertEqual(self.fields['title'], item.title)
        self.assertEqual(self.fields['category'], item.category)
        self.assertEqual(self.fields['content'], item.content)


if __name__ == '__main__':
    unittest.main()
