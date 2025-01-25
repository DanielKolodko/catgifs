import sqlite3
import os

# Path to the folder containing GIFs
gifs_folder = "static/gifs"

# SQLite database file name (ensure this matches your Flask app's DATABASE_URL)
db_path = "database.db"

# Connect to the SQLite database (it will create the database if it doesn't exist)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create the "gifs" table to store GIF URLs (if it doesn't already exist)
cursor.execute("""
CREATE TABLE IF NOT EXISTS gifs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT NOT NULL
)
""")

# Clear existing GIF data (optional, useful for testing)
cursor.execute("DELETE FROM gifs")

# Insert GIF URLs into the database
if os.path.exists(gifs_folder):
    gif_files = [f for f in os.listdir(gifs_folder) if f.endswith('.gif')]
    for gif in gif_files:
        url = f"/static/gifs/{gif}"  # Relative URL for Flask
        cursor.execute("INSERT INTO gifs (url) VALUES (?)", (url,))
        print(f"Inserted: {gif} -> {url}")
else:
    print(f"Gifs folder not found: {gifs_folder}")

# Commit the changes and close the connection
conn.commit()
conn.close()
print("Database and GIFs setup completed!")
