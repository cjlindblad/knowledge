import sqlite3
from src.core.category import Category


class CategoryRepository:
    def __init__(self, db=None):
        if db is None:
            self.db = sqlite3.connect('./db/knowledge.db')
        else:
            self.db = db

    def get_by_name(self, name):
        with self.db:
            cursor = self.db.cursor()
            cursor.execute(
                'SELECT id, name FROM category WHERE name = ?', (name,))

            row = cursor.fetchone()

            if row is None:
                return False

            id, name = row
            return Category(id, name)

    def list(self):
        categories = []

        with self.db:
            cursor = self.db.cursor()
            result = cursor.execute('SELECT id, name FROM category')

            for id, name in result:
                categories.append(Category(id, name))

        return categories

    def add(self, name):
        with self.db:
            cursor = self.db.cursor()
            cursor.execute(
                'INSERT INTO category (name) VALUES (?)', (name,))
