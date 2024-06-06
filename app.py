from flask import Flask, render_template, request, redirect,url_for, jsonify
import sqlite3
import json
import base64

app = Flask(__name__)

def create_table():
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                (id INTEGER PRIMARY KEY,
                 name TEXT,
                 age INTEGER,
                 bio TEXT,
                 gender TEXT,
                 address TEXT,
                 contact TEXT,
                 photo BLOB)''')
    conn.commit()
    conn.close()


@app.route('/')
def start():
    return render_template('start.html')



@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    age = request.form['age']
    bio = request.form['bio']

    gender = request.form['gender']
    address = request.form['address']
    contact = request.form['contact']

    photo = request.files['photo'].read()

    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute('INSERT INTO users (name, age, bio, gender, address, contact, photo) VALUES (?, ?, ?, ?, ?, ?, ?)', (name, age, bio, gender, address, contact, photo))
    conn.commit()
    conn.close()

    return redirect(url_for('get_user',name=name))






@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        data = {
            'email': email,
            'password': password
        }

        with open('users.txt', 'r') as file:
            for line in file:
                data1 = json.loads(line)
                if data1['email'] == email:
                    return redirect(url_for('get_user',name=email))
        return redirect(url_for('register'))

    return render_template('login.html')

@app.route('/sign',methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        data = {
            'name': name,
            'email': email,
            'password': password
        }

        with open('users.txt', 'a') as file:
            json.dump(data, file)
            file.write('\n')
        return redirect(url_for('get_user',name=email))
    return render_template('signup.html')

@app.route('/user/<email>')
def user_details(email):
    # Read user data from the "users.txt" file and display on user details page
    with open('users.txt', 'r') as file:
        for line in file:
            data = json.loads(line) 
            if data['email'] == email:
                return f"Name: {data['name']}<br>Email: {data['email']}<br>Password: {data['password']}"
    return "User not found"


@app.route('/users/<name>', methods=['GET','POST'])
def get_user(name):
    a = name
    data={
        'name':name
    }
    with open('temp.txt', 'w') as file:
            json.dump(data, file)
            file.write('\n')
    try:    
        conn = sqlite3.connect('user_data.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE name=?", (name,))
        user_data = c.fetchone()
        conn.close()
        if user_data:
            user_dict = {
                'id': user_data[0],
                'name': user_data[1],
                'age': user_data[2],
                'bio': user_data[3],
                'gender': user_data[4],
                
                'contact': user_data[6],
                'address': user_data[5],

                'photo': base64.b64encode(user_data[7]).decode('utf-8')
            }
            return render_template('user.html', user=user_dict,kk=name)
        else:
            return render_template('index.html', error='User not found')
        
        if request.method =='POST':
           return redirect(url_for(viewlogin))
        return render_template('user.html',user=user_dict)
    except sqlite3.OperationalError as e:
        return render_template('error.html', error=str(e))


@app.route('/view2/<name>')
def view2(name):
    user_dict= []
    conn = sqlite3.connect('user_data.db')
    # name = "kr$"  # replace with the name of the currently logged-in user
    c = conn.cursor()
    # c.execute('SELECT * FROM details WHERE name=? ', (name))
    # name = c.fetchone()
    c.execute('SELECT * FROM users WHERE name <> ? AND name NOT IN (SELECT DISTINCT name FROM swipes WHERE user = ?)', (name, name))
    rows = c.fetchall()
    if rows:
            for row in rows:
                user_dict.append(
                    {
                    'id': row[0],
                    'name': row[1],
                    'age': row[2],
                    'bio': row[3],
                    'photo': base64.b64encode(row[7]).decode('utf-8')
                    }
                
                )
            
    conn.close()
    return render_template('view2.html', users= user_dict,name=name)


@app.route('/viewlogin',methods=['GET', 'POST'])
def viewlogin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        data = {
            'email': email,
            'password': password
        }  
        return redirect(url_for('view2',name=data['email']))
    return render_template('viewlogin.html')




def create_table2():
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS swipes
                (id INTEGER PRIMARY KEY,
                 name TEXT,
                 swipe_direction TEXT,
              user TEXT)''')
    conn.commit()
    conn.close()


def create_table3():
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS matched
                (
                 name TEXT,
                 user TEXT)''')
    conn.commit()
    conn.close()

@app.route('/swipe_left', methods=['POST'])
def swipe_left():
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    name1 = request.args.get('name')
    name2 = request.args.get('user')
    c.execute('INSERT INTO swipes (name, user, swipe_direction) VALUES (?, ?, ?)',(name1, name2, "left"))
    conn.commit()
    conn.close
    return redirect(url_for('view2',name=name2))


@app.route('/swipe_right', methods=['POST'])
def swipe_right():
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()

    name1 = request.args.get('name')
    name2 = request.args.get('user')
    # conn.commit()
    # check for match
    c.execute('SELECT * FROM swipes WHERE name = ? AND user = ? AND swipe_direction = ?',
              (name2, name1, "right"))
    match = c.fetchone()
    if match:
        # delete matching swipes from table
        c.execute('INSERT INTO matched (name, user) VALUES (?, ?)',
                  (name1, name2))

        c.execute('DELETE FROM swipes WHERE name = ? AND user = ? AND swipe_direction = ?',
                  (name2, name1, "right"))
        c.execute('DELETE FROM swipes WHERE name = ? AND user = ? AND swipe_direction = ?',
                  (name1, name2, "right"))
        conn.commit()
        conn.close()

        return redirect(url_for('view2',name=name2))
    else:
        c.execute('INSERT INTO swipes (name, user, swipe_direction) VALUES (?, ?, ?)',
                  (name1, name2, "right"))
        conn.commit()
        conn.close()
        return redirect(url_for('view2',name=name2))

@app.route('/viewmatch',methods=['GET', 'POST'])
def viewmatch():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        data = {
            'email': email,
            'password': password
        }  
        return redirect(url_for('matched',name=data['email']))
    return render_template('viewmatch.html')

@app.route('/match/<name>')
def matched(name):
    user_dict=[]
    conn = sqlite3.connect('user_data.db')

    # name = "kr$"  # replace with the name of the currently logged-in user
    c = conn.cursor()
    # c.execute('SELECT * FROM details WHERE name=? ', (name))
    # name = c.fetchone()
    c.execute('SELECT u.* FROM users u INNER JOIN matched m ON u.name = m.user OR u.name = m.name WHERE m.name = ? OR m.user = ? ', (name, name))

    rows = c.fetchall()
    
    if rows:
            for row in rows:
                user_dict.append(
                    {
                    'id': row[0],
                    'name': row[1],
                    'age': row[2],
                    'bio': row[3],
                    'photo': base64.b64encode(row[7]).decode('utf-8')
                    }
                
                )
            
    conn.close()
    return render_template('match.html', users= user_dict,name=name)

# app = Flask(__name__)v
def get_user(id):
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE id=?', (id,))
    user = c.fetchone()
    conn.close()
    return user

@app.route('/users/<int:id>')
def user_profile(id):
    user = get_user(id)
    if user:
        return render_template('profile.html', user=user)
    else:
        return 'User not found'

if __name__ == '__main__':
    create_table2()
    create_table()
    create_table3()
    app.run(port=3001,debug=True)   
    