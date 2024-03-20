from flask import Flask
import psycopg2

app = Flask(__name__)

conn = psycopg2.connect(
    host="postgres://root:xQRkPp71cXDUpUqY1uUXZPmF6kJm3KyT@dpg-cnt33af79t8c73abjj10-a.frankfurt-postgres.render.com/photos_ktzk",
    database="photos_ktzk",
    user="root",
    password="xQRkPp71cXDUpUqY1uUXZPmF6kJm3KyT")



def init_db():
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            email VARCHAR(255),
            password VARCHAR(255)
        )
    ''')
    conn.commit()
    cur.close()



@app.route('/')
def hello_world():
    init_db()
    return 'Hello, World!'

