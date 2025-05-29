import os
import sqlite3
import pytest

from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article
from lib.db.connection import get_connection

def setup_function():
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.executescript("""
        DROP TABLE IF EXISTS articles;
        DROP TABLE IF EXISTS authors;
        DROP TABLE IF EXISTS magazines;

        CREATE TABLE authors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        );

        CREATE TABLE magazines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL
        );

        CREATE TABLE articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author_id INTEGER,
            magazine_id INTEGER,
            FOREIGN KEY (author_id) REFERENCES authors(id),
            FOREIGN KEY (magazine_id) REFERENCES magazines(id)
        );
    """)
    conn.commit()

    # Seed test data
    author = Author.create("John Doe")
    magazine = Magazine.create("Tech Weekly", "Technology")
    Article.create("AI Advances", author.id, magazine.id)
    conn.close()


def test_author_creation():
    author = Author.find_by_name("John Doe")
    assert author is not None
    assert author.name == "John Doe"


def test_author_articles_relationship():
    author = Author.find_by_name("John Doe")
    assert author is not None
    articles = author.articles()
    assert any(article.title == "AI Advances" for article in articles)


def test_find_by_id():
    magazine = Magazine.find_by_id(1)
    assert magazine is not None
    assert magazine.name == "Tech Weekly"


def test_article_creation():
    author = Author.find_by_name("John Doe")
    magazine = Magazine.find_by_id(1)
    assert author is not None
    assert magazine is not None
    article = Article.create("New AI Trends", author.id, magazine.id)
    assert article.title == "New AI Trends"


def test_magazine_articles():
    magazine = Magazine.find_by_id(1)
    assert magazine is not None
    articles = magazine.articles()
    assert any(article.title == "AI Advances" for article in articles)
