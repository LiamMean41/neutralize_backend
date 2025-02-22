import sqlite3

def init_db():
    # Connect to the database (or create it if it doesn't exist)
    conn = sqlite3.connect('neutralize.db')
    cursor = conn.cursor()

    # Create a sample table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sample_table (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            value REAL
        )
    ''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")