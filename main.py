import argparse
import sys
from src.interface.main import main as interface_main
from src.core.knowledge_repository import KnowledgeRepository
from src.core.knowledge_item import KnowledgeItem


def main():
    parser = argparse.ArgumentParser(description='Knowledge repository')
    parser.add_argument(
        '-l',
        '--list',
        help='writes list of all knowledge to stdout',
        action='store_true'
    )
    parser.add_argument(
        '-a',
        '--add',
        help='adds knowledge',
        action='store_true'
    )
    args = parser.parse_args()

    if args.list:
        knowledge_repo = KnowledgeRepository()
        knowledge = knowledge_repo.list()
        for item in knowledge:
            sys.stdout.write(f'title: {item.title}\n')
            sys.stdout.write(f'category: {item.category}\n')
            sys.stdout.write(f'created: {item.created}\n')
            sys.stdout.write(f'content: {item.content}\n')
            sys.stdout.write('\n')
    elif args.add:
        item = KnowledgeItem()
        knowledge_repo = KnowledgeRepository()
        for line in sys.stdin:
            if item.title and item.category and item.created and item.content:
                knowledge_repo.add(item)
                item = KnowledgeItem()

            if 'title:' in line:
                item.title = line.replace('title: ', '').replace('\n', '')
            elif 'category:' in line:
                item.category = line.replace(
                    'category: ', '').replace('\n', '')
            elif 'created:' in line:
                item.created = line.replace('created: ', '').replace('\n', '')
            elif 'content:' in line:
                item.content = line.replace('content: ', '')
            else:
                item.content = item.content + line

    else:
        interface_main()
