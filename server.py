import datetime
import json
import os
import psycopg2
import re

from flask import Flask
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask.helpers import url_for


from models import user
from models import league

app = Flask(__name__)

# generate secret key
app.secret_key = os.urandom(32)

# DATABASE HELPER FUNCTIONS

def connectDb():
    '''
    open a database connection and return connection and cursor
    '''
    conn = psycopg2.connect(app.config['dsn'])
    cur = conn.cursor()

    return conn, cur

@app.teardown_appcontext
def closeDb(exception):
    print('CLOSECLOSECLOSECLOSE')
    if hasattr(g, 'psdb'):
        conn, cur = getDb()
        
        if 'username' in session:
            username = session['username']
            cur.execute("UPDATE users SET online=FALSE WHERE username='%s'" % username)
            conn.commit()

        cur.close() # close cursor object
        conn.close() # close database connection

def getDb():
    if not hasattr(g, 'psdb'):
        g.psdb = connectDb()
    return g.psdb

def get_elephantsql_dsn(vcap_services):
    """Returns the data source name for ElephantSQL."""
    parsed = json.loads(vcap_services)
    uri = parsed["elephantsql"][0]["credentials"]["uri"]
    match = re.match('postgres://(.*?):(.*?)@(.*?)(:(\d+))?/(.*)', uri)
    user, password, host, _, port, dbname = match.groups()
    dsn = """user='{}' password='{}' host='{}' port={}
        dbname='{}'""".format(user, password, host, port, dbname)
    return dsn

# HELPER FUNCS
def login_success(username, password):
    conn, cur = getDb()
    cur.execute("SELECT * FROM users WHERE username='%s' AND password='%s'" % (username, password) )
    user = cur.fetchone()

    if user:
        return True

    return False

def getCurrTimeStr():
    now = str(datetime.datetime.now())
    return now[:-7]

# PAGE ROUTES

@app.route('/')
def home():
    conn, cur = getDb()
    now = datetime.datetime.now()
    return render_template('home.html', current_time=now.ctime())

@app.route('/users')
def users():
    conn, cur = getDb()
    usr = user.Users(conn, cur)
    users = usr.get_users()

    if 'username' in session:
        g.role = 'admin'
    return render_template('users.html',users=users, error=None, usertable=user.usertable)

@app.route('/profile/<username>')
def profile(username):
    conn, cur = getDb()
    usr = user.Users(conn, cur)
    puser = usr.get_user(username)
    return render_template('profile.html', user=puser, usertable=user.usertable)

@app.route('/updateUser', methods=['POST'])
def updateUser():
    username = request.form['username']
    password = request.form['password']
    return json.dumps({'status':'OK','user':username,'pass':password})

@app.route('/admin', methods=['POST', 'GET'])
def admin():
    conn, cur = getDb()
    error = None
    roles = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if login_success(username, password):
            error = 'Logged in!'
            cur.execute("SELECT role, lastlogin FROM users WHERE username='%s';"%username)
            role,lastlogin = cur.fetchone()
            g.role = role
            g.lastlogin = lastlogin
            session['username'] = request.form['username']
            
            now = getCurrTimeStr()
            cur.execute("UPDATE users SET lastlogin='%s' WHERE username='%s'"%(now, username))
            cur.execute("UPDATE users SET online=TRUE WHERE username='%s'" % username)
            conn.commit()
        else:
            error = 'Invalid username or password!'

    if 'username' in session:
        username = session['username']
        cur.execute("SELECT role, lastlogin FROM users WHERE username='%s';"%username)
        role,lastlogin = cur.fetchone()
        g.role = role
        g.lastlogin = lastlogin
    
    return render_template('adminpanel.html', error=error, roles=roles)

@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        conn, cur = getDb()
        
        username = request.form['username']
        password = request.form['password']
        email = str(request.form['email'])
        role = request.form['role']
        regtime = getCurrTimeStr()
        lastlogin = regtime
        online = False

        usr = user.User(username, password, email, role, lastlogin, regtime, online)
        users = user.Users(conn, cur)
        users.add_user(usr)

        return redirect(url_for('admin'))


@app.route('/logout')
def logout():
    conn, cur = getDb()
    if 'username' in session:
        username = session['username']
        cur.execute("UPDATE users SET online=FALSE WHERE username='%s'" % username)
        conn.commit()
    g.role = 'guest'
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/count')
def counter_page():
    conn, cur = getDb()

    query = "UPDATE COUNTER SET N = N + 1"
    cur.execute(query)
    conn.commit()

    query = "SELECT N FROM COUNTER"
    cur.execute(query)
    (count,) = cur.fetchone()
    return "This page was accessed %d times." % count

# league views
@app.route('/leagues')
def league_page():
    conn, cur = getDb()
    
    leagues = league.Leagues(conn, cur)
    l = leagues.get_leagues()
    return render_template('leagues.html', leaguetable=league.leaguetable, leagues=l)

@app.route('/initdb')
def initialize_database():
    conn, cur = getDb()
    
    query = """DROP TABLE IF EXISTS COUNTER"""
    cur.execute(query)
    conn.commit()
    try:
        conn, cur = getDb()

        query = """CREATE TABLE COUNTER (N INTEGER)"""
        cur.execute(query)
    
        query = """INSERT INTO COUNTER (N) VALUES (0)"""
        cur.execute(query)

        # users table
        query = "DROP TABLE IF EXISTS users;"
        cur.execute(query)
        query = """CREATE TABLE users (id serial PRIMARY KEY, 
                               username varchar(32) UNIQUE NOT NULL,
                               password varchar(255) NOT NULL,
                               email varchar(255) UNIQUE NOT NULL,
                               role varchar(12) DEFAULT 'level1',
                               lastlogin varchar(26),
                               regtime varchar(26),
                               online boolean DEFAULT FALSE);
        """
        cur.execute(query)

        now = getCurrTimeStr()
        query = """INSERT INTO users 
                    (username, password, email, role, lastlogin, regtime, online)
                    values ('admin', '1234', 'admin@test.com', 'admin','%s', '%s', FALSE );""" % (now, now)
        cur.execute(query)

        # leagues table
        query = "DROP TABLE IF EXISTS leagues;"
        query = """CREATE TABLE leagues (id serial PRIMARY KEY, 
                               name varchar(32) NOT NULL,
                               country varchar(32));
        """
        cur.execute(query)

        conn.commit() # commit changes
    except:
        return 'CREATE TABLE ERROR'
    return redirect(url_for('home'))


# ERROR PAGES

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', err_code=404, error=error), 404



if __name__ == '__main__':
    VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
    if VCAP_APP_PORT is not None:
        port, debug = int(VCAP_APP_PORT), False
    else:
        port, debug = 5000, True

    VCAP_SERVICES = os.getenv('VCAP_SERVICES')
    if VCAP_SERVICES is not None:
        app.config['dsn'] = get_elephantsql_dsn(VCAP_SERVICES)
    else:
        app.config['dsn'] = """dbname=itucsdb host=localhost port=54321 user=vagrant password=vagrant"""

    app.run(host='0.0.0.0', port=port, debug=debug)
