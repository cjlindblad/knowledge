import sqlite3
from datetime import datetime

from knowledge_item import KnowledgeItem

class KnowledgeService:
    def list_knowledge(self):
        connection = sqlite3.connect('../../db/knowledge.db')
        cursor = connection.cursor()

        query = '''
        SELECT * FROM knowledge_item
        ORDER BY created_ts DESC;
        '''

        knowledge = []

        result = cursor.execute(query)
        for id, created, title, content in result:
            knowledge.append(KnowledgeItem(
                datetime.utcfromtimestamp(created).strftime('%Y-%m-%d'),
                title,
                content
            ))

        connection.close()

        return knowledge
