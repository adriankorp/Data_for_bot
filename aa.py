import sqlite3

conn = sqlite3.connect('Message_data.db')
cur = conn.cursor()

conn.execute(f'''CREATE TABLE IF NOT EXISTS 'MESSAGES'
                (id INTEGER PRIMARY KEY ASC,
                  msg_id INT NOT NULL,
                  msg VARCHAR(255) NOT NULL
                    );''')
