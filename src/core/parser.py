from src.core.knowledge_item import KnowledgeItem
from datetime import datetime


class Parser:
    @staticmethod
    def knowledge_item_to_text(item: KnowledgeItem) -> str:
        text = f'title: {item.title}\ncategory: {item.category}\ncontent: {item.content}'

        return text

    @staticmethod
    def text_to_knowledge_item(input: str) -> KnowledgeItem:
        item = KnowledgeItem()
        for line in input.split('\n'):
            if 'title:' in line:
                item.title = line.replace('title: ', '')
            elif 'category:' in line:
                item.category = line.replace('category: ', '')
            elif 'content:' in line:
                item.content = line.replace('content: ', '')
            else:
                item.content = item.content + '\n' + line

        item.created = datetime.now().strftime('%Y-%m-%d')

        return item
