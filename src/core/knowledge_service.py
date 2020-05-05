import sqlite3
import re
from datetime import datetime

from src.core.knowledge_item import KnowledgeItem

class KnowledgeService:
    def list_knowledge(self, search_string):
        connection = sqlite3.connect('./db/knowledge.db')
        cursor = connection.cursor()

        query = '''
        SELECT ki.created_ts as created, ki.title, ki.content, c.name as category
        FROM knowledge_item ki
        JOIN category c ON c.id = ki.category_id
        ORDER BY ki.created_ts DESC;
        '''

        knowledge = []

        result = cursor.execute(query)
        for created, title, content, category in result:
            knowledge.append(KnowledgeItem(
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
