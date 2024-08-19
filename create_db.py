import sqlite3
import csv

# Connect to SQLite database (creates it if it doesn't exist)
conn = sqlite3.connect('countries.db')
c = conn.cursor()

# Create table
c.execute('''
    CREATE TABLE IF NOT EXISTS pays (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL
    )
''')

# Read CSV and insert country names into the table
with open('pays_data.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        c.execute('INSERT INTO pays (nom) VALUES (?)', (row['Nom du pays'],))

# Commit and close
conn.commit()
conn.close()
