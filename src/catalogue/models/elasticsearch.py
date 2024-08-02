from elasticsearch_dsl import Document, Text, connections
from .category_index import CategoryIndex

connections.create_connection(hosts=['localhost'])

PRODUCT_INDEX = 'products_index'

class ProductIndex(Document):
    title = Text()
    description = Text()
    short_description = Text()

    class Index:
        name = PRODUCT_INDEX

def initialize_indices():
    if not CategoryIndex._index.exists():
        CategoryIndex.init()
    if not ProductIndex._index.exists():
        ProductIndex.init()
