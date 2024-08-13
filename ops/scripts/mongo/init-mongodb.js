db = db.getSiblingDB('fastshop');

db.createCollection('productReviews');
db.createCollection('productAnalytics');

db.productReviews.createIndex({ productId: 1 });
db.productAnalytics.createIndex({ productId: 1 });

db.productReviews.insertMany([
    { productId: 1, review: "Great product!", rating: 5 },
    { productId: 2, review: "Not bad.", rating: 3 }
]);

db.productAnalytics.insertMany([
    { productId: 1, views: 100, sales: 10 },
    { productId: 2, views: 150, sales: 20 }
]);
