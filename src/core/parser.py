from src.core.knowledge_item import KnowledgeItem
from datetime import datetime


def knowledge_item_to_text(item):
    text = f'title: {item.title}\ncategory: {item.category}\ncontent: {item.content}\n'

    return text


def text_to_knowledge_item(input):
    item = KnowledgeItem()
    for line in input.split('\n'):
        if 'title:' in line:
            item.title = line.replace('title: ', '').replace('\n', '')
        elif 'category:' in line:
            item.category = line.replace('category: ', '').replace('\n', '')
        elif 'content:' in line:
            item.content = line.replace('content: ', '')
        else:
            item.content = item.content + line

    item.created = datetime.now().strftime('%Y-%m-%d')

    return item
