from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article
from lib.db.connection import get_connection

def seed_database():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM articles")
    cursor.execute("DELETE FROM authors")
    cursor.execute("DELETE FROM magazines")
    conn.commit()
    conn.close()

    authors = [
        Author.create("John Doe"),
        Author.create("Jane Smith"),
        Author.create("Bob Johnson")
    ]

    magazines = [
        Magazine.create("Tech Today", "Technology"),
        Magazine.create("Science Weekly", "Science"),
        Magazine.create("Business Insights", "Business")
    ]

    articles = [
        {"title": "Python Programming", "author": 0, "magazine": 0},
        {"title": "Machine Learning", "author": 0, "magazine": 0},
        {"title": "Quantum Physics", "author": 1, "magazine": 1},
        {"title": "Neuroscience", "author": 1, "magazine": 1},
        {"title": "Stock Market", "author": 2, "magazine": 2},
        {"title": "Startup Funding", "author": 2, "magazine": 2}
    ]

    for article in articles:
        Article.create(
            article['title'],
            authors[article['author']].id,
            magazines[article['magazine']].id
        )