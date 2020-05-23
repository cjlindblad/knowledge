import sqlite3
import re
from datetime import datetime
import time

from src.core.knowledge_item import KnowledgeItem
from src.core.category_repository import CategoryRepository


class KnowledgeRepository:
    def __init__(self, db=None):
        if db is None:
            self.db = sqlite3.connect('./db/knowledge.db')
        else:
            self.db = db

    def add(self, item):
        if not item.created:
            item.created = datetime.now().strftime('%Y-%m-%d')

        if not item.valid:
            return

        with self.db:
            cursor = self.db.cursor()

            category_repo = CategoryRepository(self.db)
            db_category = category_repo.get_by_name(item.category)

            if not db_category:
                category_repo.add(item.category)
                db_category = category_repo.get_by_name(item.category)

            cursor.execute('''
                INSERT INTO knowledge_item (title, category_id, created_ts, content)
                VALUES (?, ?, ?, ?)
                ''',
                           (item.title,
                            db_category.id,
                            time.mktime(datetime.strptime(
                                item.created, '%Y-%m-%d').timetuple()),
                            item.content))

    def list_archived(self):
        knowledge = self.__list(active=False)
        return knowledge

    def list(self, search_string=''):
        knowledge = self.__list()

        if search_string:
            # filter result
            terms = [re.escape(word) for word in search_string.split()]
            # (?=.*word)
            regex_terms = [f'(?=.*{term})' for term in terms]
            regex = f'{"".join(regex_terms)}.*'
            knowledge = [item for item in knowledge if
                         re.search(regex,
                                   f'{item.category} {item.title}', re.IGNORECASE)]

        return knowledge

    def __list(self, active=True):
        knowledge = []

        with self.db:
            cursor = self.db.cursor()

            query = '''
            SELECT ki.id, ki.created_ts as created, ki.title, ki.content, c.name as category
            FROM knowledge_item ki
            LEFT JOIN category c ON c.id = ki.category_id
            WHERE ki.archived != ?
            ORDER BY ki.created_ts DESC;
            '''

            result = cursor.execute(query, (active,))
            for id, created, title, content, category in result:
                knowledge.append(KnowledgeItem(
                    id,
                    datetime.fromtimestamp(created).strftime('%Y-%m-%d'),
                    title,
                    content,
                    category
                ))

        return knowledge

    def update(self, item):
        if not item.valid:
            return

        with self.db:
            cursor = self.db.cursor()
            category_repo = CategoryRepository(self.db)
            db_category = category_repo.get_by_name(item.category)

            if not db_category:
                category_repo.add(item.category)
                db_category = category_repo.get_by_name(item.category)

            cursor.execute('''UPDATE knowledge_item
            SET title = ?, content = ?, category_id = ?
            WHERE id = ?
            ''', (item.title, item.content, db_category.id, item.id))

            category_repo.clean_unused()

    def archive(self, id):
        with self.db:
            cursor = self.db.cursor()

            cursor.execute('''
            UPDATE knowledge_item
            SET archived = 1
            WHERE id = ?
            ''', (id,))
