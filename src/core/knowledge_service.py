import sqlite3
import re
from datetime import datetime

from src.core.knowledge_item import KnowledgeItem

class KnowledgeService:
    def list_knowledge(self, search_string):
        connection = sqlite3.connect('./db/knowledge.db')
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

        if search_string:
            # filter result
            terms = [re.escape(word) for word in search_string.split()]
            # (?=.*word)
            regex_terms = [f'(?=.*{term})' for term in terms]
            regex = f'{"".join(regex_terms)}.*'
            knowledge = [item for item in knowledge if
                    re.search(regex,
                item.title, re.IGNORECASE)] 

        return knowledge
