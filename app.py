from flask import Flask, render_template, request, session, redirect, url_for
import os
from werkzeug.utils import secure_filename
import psycopg2

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret'

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
    cur.execute('''
        CREATE TABLE IF NOT EXISTS photos (
            id SERIAL PRIMARY KEY,
            file_name VARCHAR(255),
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    conn.commit()
    cur.close()



@app.route('/')
def hello_world():
    # init_db()
    if 'user' in session:
        cur = conn.cursor()
        cur.execute('SELECT * FROM photos' )
        photos = cur.fetchall()
        cur.close()

        return render_template('index.html', user=session['user'], photos=photos)
    return redirect('/logIn')

@app.route('/upload', methods=['POST', 'GET'])
def uploadPhoto():
    if 'user' not in session:
        return redirect('/logIn')
    
    if request.method == 'POST':
        file = request.files['photo']
        filename = file.filename
        if filename == '':
            return redirect('/')
        filename = secure_filename(filename)
        
        user = session['user']
        if not os.path.exists(os.path.join('static/photos', str(user[0]))):
            os.makedirs(os.path.join('static/photos', str(user[0])))

        file.save(os.path.join('static/photos', str(user[0]), filename))
        cur = conn.cursor()
        cur.execute('INSERT INTO photos (file_name, user_id) VALUES (%s, %s)', (filename, user[0]))
        conn.commit()
        cur.close()

        return redirect('/')
    elif request.method == 'GET':
        return render_template('uploadPhoto.html')

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
        session['user'] = user
        cur.close()
        if user:
            return redirect('/')
        else:
            return render_template('logIn.html', error='Invalid username or password')
    elif request.method == 'GET':
        return render_template('logIn.html')


@app.route('/logOut', methods=['GET'])
def logOut():
    session.pop('user', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
    app.add_url_rule('/favicon.ico', redirect_to=url_for('static', filename='favicon.ico'))
    app.add_url_rule('/static/<path:filename>', endpoint='static', view_func=app.send_static_file)
