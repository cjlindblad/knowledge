class KnowledgeItem:
    def __init__(self, id=None, created='', title='', content='', category=''):
        self.id = id
        self.created = created
        self.title = title
        self.content = content
        self.category = category

    @property
    def valid(self):
        return (self.created != ''
                and self.title != ''
                and self.content != '')
