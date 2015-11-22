import datetime
import json
import os
import psycopg2
import re


from flask import abort
from flask import Flask
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask.helpers import url_for


from final4.config import app

from final4 import db_helper as db

from final4.models import user
from final4.models import league
from final4.models import player
from final4.models import award

from final4.views import league_view


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
    conn, cur = db.getDb()
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
    conn, cur = db.getDb()
    now = datetime.datetime.now()
    return render_template('home.html', current_time=now.ctime())

@app.route('/users')
def users():
    conn, cur = db.getDb()
    usr = user.Users(conn, cur)
    users = usr.get_users()

    if 'username' in session:
        g.role = 'admin'
    return render_template('users.html',users=users, error=None, usertable=user.usertable)

@app.route('/profile/<username>')
def profile(username):
    conn, cur = db.getDb()
    usr = user.Users(conn, cur)
    puser = usr.get_user(username)
    return render_template('profile.html', user=puser, usertable=user.usertable)

@app.route('/updateUser', methods=['POST'])
def updateUser():
    if 'username' not in session:
        return abort(403)
    
    username = request.form['username']
    if session['username'] != username:
        return abort(403)

    password = request.form['password']
    passwordnew = request.form['passwordnew']

    #email = request.form['email']
    return json.dumps({'status':'OK','user':username,'pass':password})


@app.route('/admin', methods=['POST', 'GET'])
def admin():
    conn, cur = db.getDb()
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
        conn, cur = db.getDb()
        
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
    conn, cur = db.getDb()
    if 'username' in session:
        username = session['username']
        cur.execute("UPDATE users SET online=FALSE WHERE username='%s'" % username)
        conn.commit()
    g.role = 'guest'
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/count')
def counter_page():
    conn, cur = db.getDb()

    query = "UPDATE COUNTER SET N = N + 1"
    cur.execute(query)
    conn.commit()

    query = "SELECT N FROM COUNTER"
    cur.execute(query)
    (count,) = cur.fetchone()
    return "This page was accessed %d times." % count

# player views
@app.route('/players')
def player_page():
    conn, cur = db.getDb()
    
    players = player.Players(conn, cur)
    playerlist = players.get_players()
    return render_template('players.html', playertable=player.playertable, players=playerlist)

# award views
@app.route('/awards')
def award_page():
    conn, cur = db.getDb()
    
    awards = award.Awards(conn, cur)
    awardlist = awards.get_awards()
    return render_template('awards.html', awardtable=award.awardtable, awards=awardlist)

@app.route('/stats')
def stats():
    return "Stats page will be here"

@app.route('/initdb')
def initialize_database():
    conn, cur = db.getDb()
    
    query = """DROP TABLE IF EXISTS COUNTER"""
    cur.execute(query)
    conn.commit()
    try:
        conn, cur = db.getDb()

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
        cur.execute(query)

        query = """CREATE TABLE leagues (id serial PRIMARY KEY, 
                               name varchar(32) NOT NULL,
                               country varchar(32));
        """
        cur.execute(query)

        # players table
        query = "DROP TABLE IF EXISTS players;"
        cur.execute(query)

        query = """CREATE TABLE players (id serial PRIMARY KEY, 
                               name varchar(32) NOT NULL,
                               country varchar(32), age varchar(3), playing_position varchar(32));
        """
        cur.execute(query)

    
        # awards table
        query = "DROP TABLE IF EXISTS awards;"
        cur.execute(query)

        query = """CREATE TABLE awards (id serial PRIMARY KEY, 
                               name varchar(32) NOT NULL,
                               playerid integer, seasonid integer);
        """
        cur.execute(query)

        conn.commit() # commit changes
    
    except:
        conn.rollback()
        return 'create table error'
    return redirect(url_for('home'))


# ERROR PAGES

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', err_code=404, error=error), 404



def run_app():
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
