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

    def test_should_not_add_empty_item(self):
        item = KnowledgeItem()

        self.repo.add(item)

        result = self.repo.list()

        self.assertEqual(0, len(result))

    def test_should_handle_item_without_date(self):
        item = KnowledgeItem()
        item.title = 'test title'
        item.content = 'test content'

        self.repo.add(item)

        result = self.repo.list()

        self.assertEqual(1, len(result))
        self.assertFalse(result[0].created.isspace())

    def test_updates_single_item(self):
        item = KnowledgeItem()
        item.title = 'test title'
        item.content = 'test content'
        item.category = 'test category'
        self.repo.add(item)

        db_item = self.repo.list()[0]
        db_item.title = 'updated title'
        db_item.content = 'updated content'
        db_item.category = 'updated category'
        self.repo.update(db_item)

        result = self.repo.list()[0]

        self.assertEqual('updated title', result.title)
        self.assertEqual('updated content', result.content)
        self.assertEqual('updated category', result.category)

    def test_does_not_update_invalid_item(self):
        item = KnowledgeItem()
        item.title = 'test title'
        item.content = 'test content'
        item.category = 'test category'
        self.repo.add(item)

        db_item = self.repo.list()[0]
        db_item.title = None
        db_item.content = None
        db_item.created = None
        self.repo.update(db_item)

        result = self.repo.list()[0]

        self.assertEqual('test title', result.title)
        self.assertEqual('test content', result.content)

    def test_deletes_single_item(self):
        item = KnowledgeItem()
        item.title = 'test title'
        item.content = 'test content'
        item.category = 'test category'

        self.repo.add(item)
        id = self.repo.list()[0].id
        self.repo.delete(id)
        result = self.repo.list()

        self.assertEqual(0, len(result))

    def test_does_not_delete_invalid_id(self):
        item = KnowledgeItem()
        item.title = 'test title'
        item.content = 'test content'
        item.category = 'test category'

        self.repo.add(item)
        id = self.repo.list()[0].id
        self.repo.delete(id + 1)
        result = self.repo.list()

        self.assertEqual(1, len(result))

    def tearDown(self):
        self.db.close()
