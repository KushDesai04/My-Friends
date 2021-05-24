from flask import Flask, render_template, request
from config import Config
import sqlite3


app = Flask(__name__)
app.config.from_object(Config)

@app.context_processor
def context_processor():
    return dict(title = app.config['TITLE'])


# Reroute when a 404 error is found
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', page = 'WHAT DID YOU DO YOU IDIOT! GO BACK!'), 404


# Connect to database and execute query
def connect(query, val = tuple(''), single = False):
    conn = sqlite3.connect(app.config['DATABASE'])
    cur = conn.cursor()
    if val:
        cur.execute(query, val)
    else:
        cur.execute(query)
    result = cur.fetchone() if single else cur.fetchall()
    conn.close()
    return result


@app.route('/')
def home():
    friends = connect('SELECT * FROM Friend ORDER BY name ASC')
    return render_template('home.html', friends=friends)


@app.route('/friend/<int:id>', methods=['POST','GET'])
def friend(id):
    q = "SELECT * FROM Friend WHERE id = ?"
    val = (id, )
    friend = connect(q, val, single = True)
    print(friend)
    hidden = [""]

    if request.method == "POST":
      password = request.form['password']
      print(password)
      
      authentication = connect('SELECT password FROM Friend WHERE id = ?', (id,), single=True)
      print(authentication)
      if password == authentication[0]:
        hidden = connect('SELECT message from Friend WHERE id = ?', (id,), single=True)
        print(hidden)

    return render_template('friend.html', friend = friend, hidden = hidden[0])


if __name__ == '__main__':
    app.run(debug = app.config['DEBUG'], port = 8080, host = '0.0.0.0')
