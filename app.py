from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)

conn = psycopg2.connect(
    host="dpg-cnt33af79t8c73abjj10-a.frankfurt-postgres.render.com",
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
    cur.execute('INSERT INTO users (name, email, password) VALUES (%s, %s, %s)', ('admin', 'admin@admin.com', 'admin'))
    cur.close()



@app.route('/')
def hello_world():
    init_db()
    return 'Hello, World!'


@app.route('/logIn', methods=['POST', 'GET'])
def logIn():
    print(request.method)
    if request.method == 'POST':
        name = request.form['username']
        password = request.form['password']
        cur = conn.cursor()
        print(name)
        print(password)
        cur.execute('SELECT * FROM users WHERE name = %s AND password = %s', (name, password))
        user = cur.fetchone()
        cur.close()
        if user:
            return 'Logged in'
        else:
            return 'Invalid credentials'
    elif request.method == 'GET':
        return render_template('logIn.html')


if __name__ == '__main__':
    app.run(debug=True)
