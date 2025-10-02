from elasticsearch_dsl import (
    AsyncDocument as Document,
    Text,
    connections,
)


PRODUCT_INDEX = 'products_index'
CATEGORY_INDEX = 'categories_index'


class ProductIndex(Document):
    title = Text()
    description = Text()
    short_description = Text()

    class Index:
        name = PRODUCT_INDEX

class CategoryIndex(Document):
    title = Text()
    description = Text()

    class Index:
        name = 'categories_index'
