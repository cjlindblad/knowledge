import unittest
from src.core.parser import knowledge_item_to_text, text_to_knowledge_item
from src.core.knowledge_item import KnowledgeItem


class Test_TestParser(unittest.TestCase):
    def test_parses_plain_knowledge_item(self):
        title = 'test title'
        category = 'test category'
        content = 'test content'

        item = KnowledgeItem()
        item.title = title
        item.category = category
        item.content = content

        text = knowledge_item_to_text(item)

        expected_result = f'title: {title}\ncategory: {category}\ncontent: {content}\n'

        self.assertEqual(text, expected_result)


if __name__ == '__main__':
    unittest.main()
