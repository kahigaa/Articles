from lib.db.seed import seed_database
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

def debug():
    seed_database()  # <-- Populate test data

    print("=== Debug Session ===")
    print("\nAuthors:")
    for i in range(1, 4):
        author = Author.find_by_id(i)
        if author:
            print(f"{author.id}: {author.name}")
        else:
            print(f"No author found with id {i}")

    print("\nMagazines:")
    for i in range(1, 4):
        magazine = Magazine.find_by_id(i)
        if magazine:
            print(f"{magazine.id}: {magazine.name} ({magazine.category})")
        else:
            print(f"No magazine found with id {i}")

    print("\nTesting relationships:")
    author = Author.find_by_name("John Doe")
    if author:
        print(f"\nArticles by {author.name}:")
        articles = author.articles()
        if articles:
            for article in articles:
                print(f"- {article.title}")
        else:
            print("No articles found for this author.")
    else:
        print("Author 'John Doe' not found")

if __name__ == '__main__':
    debug()

