import unittest
import sqlite3
from src.core.knowledge_repository import KnowledgeRepository
from src.core.knowledge_item import KnowledgeItem


class KnowledgeRepositoryTest(unittest.TestCase):
    def setUp(self):
        self.db = sqlite3.connect(':memory:')
        self.__initialize_db(self.db)
        self.repo = KnowledgeRepository(self.db)

    def __initialize_db(self, db):
        with db:
            cursor = self.db.cursor()

            db_script = ''
            with open('./db-scripts') as db_scripts_file:
                db_script = db_scripts_file.read()

            statements = db_script.split(';')
            for statement in statements:
                cursor.execute(f'{statement};')

    def test_add_and_list_one_item(self):
        title = 'test title'
        category = 'test category'
        content = 'test content'
        created = '2010-10-10'

        item = KnowledgeItem()
        item.title = title
        item.category = category
        item.content = content
        item.created = created

        self.repo.add(item)

        result = self.repo.list()

        self.assertEqual(1, len(result))
        self.assertEqual(title, result[0].title)
        self.assertEqual(category, result[0].category)
        self.assertEqual(content, result[0].content)
        self.assertEqual(created, result[0].created)

    def tearDown(self):
        self.db.close()
