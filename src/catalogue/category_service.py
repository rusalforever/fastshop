import redis
from .models.elasticsearch import CategoryIndex
from .models.database import Category

class CategoryService:
    def __init__(self, redis_client):
        self.redis_client = redis_client

    def update_category_index(self):
        categories = Category.query.all()
        for category in categories:
            doc = CategoryIndex(meta={'id': category.id}, title=category.title, description=category.description)
            doc.save()
        self.redis_client.set('category_index_status', 'completed')

    def get_index_status(self):
        return self.redis_client.get('category_index_status')
