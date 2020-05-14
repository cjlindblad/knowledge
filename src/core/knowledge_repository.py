import sqlite3
import re
from datetime import datetime
import time

from src.core.knowledge_item import KnowledgeItem


class KnowledgeRepository:
    def add(self, item):
        connection = sqlite3.connect('./db/knowledge.db')
        cursor = connection.cursor()

        cursor.execute('''
            SELECT name FROM category
            WHERE name = ?
            ''',
                       (item.category,))

        if cursor.fetchone() is None:
            cursor.execute('''
                INSERT INTO category (name)
                VALUES (?)
                ''',
                           (item.category,))

        cursor.execute('''
            SELECT id FROM category
            WHERE name = ?
            ''',
                       (item.category,))

        category_id = cursor.fetchone()[0]

        cursor.execute('''
            INSERT INTO knowledge_item (title, category_id, created_ts, content)
            VALUES (?, ?, ?, ?)
            ''',
                       (item.title,
                        category_id,
                        time.mktime(datetime.strptime(
                            item.created, '%Y-%m-%d').timetuple()),
                        item.content))

        connection.commit()
        connection.close()

    def list(self, search_string=''):
        connection = sqlite3.connect('./db/knowledge.db')
        cursor = connection.cursor()

        query = '''
        SELECT ki.id, ki.created_ts as created, ki.title, ki.content, c.name as category
        FROM knowledge_item ki
        LEFT JOIN category c ON c.id = ki.category_id
        WHERE ki.deleted != 1
        ORDER BY ki.created_ts DESC;
        '''

        knowledge = []

        result = cursor.execute(query)
        for id, created, title, content, category in result:
            knowledge.append(KnowledgeItem(
                id,
                datetime.utcfromtimestamp(created).strftime('%Y-%m-%d'),
                title,
                content,
                category
            ))

        connection.close()

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

    def update(self, item):
        connection = sqlite3.connect('./db/knowledge.db')
        cursor = connection.cursor()

        cursor.execute('''
            SELECT name FROM category
            WHERE name = ?
            ''',
                       (item.category,))

        if cursor.fetchone() is None:
            cursor.execute('''
                INSERT INTO category (name)
                VALUES (?)
                ''',
                           (item.category,))

        cursor.execute('''
            SELECT id FROM category
            WHERE name = ?
            ''',
                       (item.category,))

        category_id = cursor.fetchone()[0]

        cursor.execute('''UPDATE knowledge_item
        SET title = ?, content = ?, category_id = ?
        WHERE id = ?
        ''', (item.title, item.content, category_id, item.id))

        connection.commit()
        connection.close()

    def delete(self, item):
        connection = sqlite3.connect('./db/knowledge.db')
        cursor = connection.cursor()

        cursor.execute('''
        UPDATE knowledge_item
        SET deleted = 1
        WHERE id = ?
        ''', (item.id,))

        connection.commit()
        connection.close()
