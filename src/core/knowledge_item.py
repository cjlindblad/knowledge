class KnowledgeItem:
    def __init__(self, created='', title='', content='', category=''):
        self.created = created
        self.title = title
        self.content = content
        self.category = category

    def as_dict(self):
        dict = {
            'created': self.created,
            'title': self.title,
            'content': self.content,
            'category': self.category
        }

        return dict
