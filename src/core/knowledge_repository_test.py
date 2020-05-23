import unittest
import sqlite3
from src.core.knowledge_repository import KnowledgeRepository
from src.core.category_repository import CategoryRepository
from src.core.knowledge_item import KnowledgeItem


class KnowledgeRepositoryTest(unittest.TestCase):
    def setUp(self):
        self.db = sqlite3.connect(':memory:')
        self.__initialize_db(self.db)
        self.knowledge_repo = KnowledgeRepository(self.db)
        self.category_repo = CategoryRepository(self.db)

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

        self.knowledge_repo.add(item)

        result = self.knowledge_repo.list()

        self.assertEqual(1, len(result))
        self.assertEqual(title, result[0].title)
        self.assertEqual(category, result[0].category)
        self.assertEqual(content, result[0].content)
        self.assertEqual(created, result[0].created)

    def test_should_not_add_empty_item(self):
        item = KnowledgeItem()

        self.knowledge_repo.add(item)

        result = self.knowledge_repo.list()

        self.assertEqual(0, len(result))

    def test_should_handle_item_without_date(self):
        item = KnowledgeItem()
        item.title = 'test title'
        item.content = 'test content'

        self.knowledge_repo.add(item)

        result = self.knowledge_repo.list()

        self.assertEqual(1, len(result))
        self.assertFalse(result[0].created.isspace())

    def test_updates_single_item(self):
        item = KnowledgeItem()
        item.title = 'test title'
        item.content = 'test content'
        item.category = 'test category'
        self.knowledge_repo.add(item)

        db_item = self.knowledge_repo.list()[0]
        db_item.title = 'updated title'
        db_item.content = 'updated content'
        db_item.category = 'updated category'
        self.knowledge_repo.update(db_item)

        result = self.knowledge_repo.list()[0]

        self.assertEqual('updated title', result.title)
        self.assertEqual('updated content', result.content)
        self.assertEqual('updated category', result.category)

    def test_does_not_update_invalid_item(self):
        item = KnowledgeItem()
        item.title = 'test title'
        item.content = 'test content'
        item.category = 'test category'
        self.knowledge_repo.add(item)

        db_item = self.knowledge_repo.list()[0]
        db_item.title = None
        db_item.content = None
        db_item.created = None
        self.knowledge_repo.update(db_item)

        result = self.knowledge_repo.list()[0]

        self.assertEqual('test title', result.title)
        self.assertEqual('test content', result.content)

    def test_archives_single_item(self):
        item = KnowledgeItem()
        item.title = 'test title'
        item.content = 'test content'
        item.category = 'test category'

        self.knowledge_repo.add(item)
        id = self.knowledge_repo.list()[0].id
        self.knowledge_repo.archive(id)
        result = self.knowledge_repo.list()

        self.assertEqual(0, len(result))

    def test_does_not_archive_invalid_id(self):
        item = KnowledgeItem()
        item.title = 'test title'
        item.content = 'test content'
        item.category = 'test category'

        self.knowledge_repo.add(item)
        id = self.knowledge_repo.list()[0].id
        self.knowledge_repo.archive(id + 1)
        result = self.knowledge_repo.list()

        self.assertEqual(1, len(result))

    def test_cleans_up_unused_categories_on_update(self):
        item = KnowledgeItem()
        item.title = 'test title'
        item.content = 'test content'
        item.category = 'initial category'
        self.knowledge_repo.add(item)

        db_item = self.knowledge_repo.list()[0]
        db_item.category = 'updated category'
        self.knowledge_repo.update(db_item)
        categories = self.category_repo.list()

        self.assertEqual(1, len(categories))
        self.assertEqual('updated category', categories[0].name)

    def tearDown(self):
        self.db.close()
