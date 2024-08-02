from elasticsearch_dsl import Document, Text

class CategoryIndex(Document):
    title = Text()
    description = Text()

    class Index:
        name = 'categories_index'
