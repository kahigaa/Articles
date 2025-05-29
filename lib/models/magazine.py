from lib.db.connection import get_connection

class Magazine:
    def __init__(self, name, category, id=None):
        self.id = id
        self.name = name
        self.category = category

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        if self.id:
            cursor.execute("UPDATE magazines SET name = ?, category = ? WHERE id = ?", 
                         (self.name, self.category, self.id))
        else:
            cursor.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", 
                         (self.name, self.category))
            self.id = cursor.lastrowid
        conn.commit()
        conn.close()

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(row['name'], row['category'], row['id'])
        return None
    
def contributors(self):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT authors.* FROM authors
        JOIN articles ON authors.id = articles.author_id
        WHERE articles.magazine_id = ?
    """, (self.id,))
    rows = cursor.fetchall()
    conn.close()
    from lib.models.author import Author
    return [Author(row['name'], row['id']) for row in rows]

@classmethod
def top_publisher(cls):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT magazines.*, COUNT(articles.id) as article_count
        FROM magazines
        LEFT JOIN articles ON magazines.id = articles.magazine_id
        GROUP BY magazines.id
        ORDER BY article_count DESC
        LIMIT 1
    """)
    row = cursor.fetchone()
    conn.close()
    if row:
        return cls(row['name'], row['category'], row['id'])
    return None    

    