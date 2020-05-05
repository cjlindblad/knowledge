import sqlite3
from datetime import datetime
import os

def backup():
    connection = sqlite3.connect('../db/knowledge.db')
    cursor = connection.cursor()

    query = '''
    SELECT ki.created_ts as created, ki.title, ki.content, c.name as category
    FROM knowledge_item ki
    LEFT JOIN category c ON c.id = ki.category_id
    ORDER BY ki.created_ts DESC;
    '''

    knowledge = []

    result = cursor.execute(query)

    for created, title, content, category in result:
        knowledge.append({
                'created_ts': created,
                'created':
                datetime.utcfromtimestamp(created).strftime('%Y-%m-%d'),
                'title': title,
                'content': content,
                'category': category
            })

    connection.close()

    if not os.path.isdir('./backups'):
        os.mkdir('backups')

    os.chdir('backups')

    for item in knowledge:
        category = item['category'] or 'NULL'
        if not os.path.isdir(f'./{category}'):
            os.mkdir(category)
        with open(f"./{category}/{item['title'].replace(' ', '_')}_{item['created_ts']}.txt", 'w') as file:
            file.write(f"title: {item['title']}\n")
            file.write(f"category: {item['category']}\n")
            file.write(f"created_ts: {item['created_ts']}\n")
            file.write(f"created: {item['created']}\n")
            file.write(f"content: {item['content']}\n")

def main():
    backup()

if __name__ == '__main__':
    main()
