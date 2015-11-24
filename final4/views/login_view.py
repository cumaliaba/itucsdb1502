import json
import sys

from flask import abort
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask.helpers import url_for


from final4.config import app
from final4.db_helper import getDb
from final4.helper import login_success, getCurrTimeStr

from final4.models import user

from psycopg2 import IntegrityError

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
    if 'username' not in session:
        return abort(403)
    
    conn, cur = getDb()

    username = request.form['username']
    if session['username'] != username:
        return abort(403)

    password = request.form['password']
    passwordnew = request.form['passwordnew']

    users = user.Users(conn, cur)
    muser = users.get_user(username)
    if password == muser.password:
        muser.password = passwordnew
        try:
            users.update_user(username, muser)
            return json.dumps({'status':'OK','user':username,'pass':passwordnew})
        except:
            error = sys.exc_info()[0]
            return json.dumps({'status':'FAILED','error':error})
    else:
        error = "The password you entered is wrong!"
        return json.dumps({'status':'FAILED', 'error':error})

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
        try:
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
        except IntegrityError:
            conn.rollback()
            roles=None
            error = "This username already registered."
            return render_template('adminpanel.html', error=error, roles=roles)
        else:
            conn.rollback()
            error = sys.exc_info()[0]
            roles=None
            return render_template('adminpanel.html', error=error, roles=roles)


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


