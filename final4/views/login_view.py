import datetime
import json
import sys

from flask import abort
from flask import flash
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


@app.route('/signin')
def signin():
    '''Routing function for signin page.'''
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
    
    return render_template('signin.html')

@app.route('/users')
def users():
    '''Routing function for users page.'''
    conn, cur = getDb()
    usr = user.Users(conn, cur)
    users = usr.get_users()

    if 'username' in session:
        g.role = 'admin'
    return render_template('users.html',users=users, error=None, usertable=user.usertable)

@app.route('/profile/<username>')
def profile(username):
    '''Routing function for user profile page.
    Renders *templates/profile.html* for user which has given username.

    :param username: username string
    '''
    conn, cur = getDb()
    usr = user.Users(conn, cur)
    puser = usr.get_user(username)
    return render_template('profile.html', user=puser, usertable=user.usertable)

@app.route('/updateUser', methods=['POST'])
def updateUser():
    '''Routing function for updating user. This url allows only POST request.
    
    Updates the user which attributes recieved from *request.form* and returns the JSON object.
    
    :returns: status and error
    :rtype: JSON object
    '''
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
    '''Routing function for admin page. 
    This page allows *POST* and *GET* requests.
    
    *GET request:* If the user signed in adminpanel page is rendered. 
    Otherwise signin page is rendered.

    *POST request:* Checks the request.form values for registered 
    users. If the values are valid it adds user to the session and 
    renders the adminpanel. Otherwise error message is flashed.
    '''
    conn, cur = getDb()
    error = None
    roles = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if login_success(username, password):
            error = 'Logged in!'
            query = "SELECT role, lastlogin FROM users WHERE username=%s"
            cur.execute(query, (username,))
            role,lastlogin = cur.fetchone()
            g.role = role
            g.lastlogin = lastlogin
            session['username'] = request.form['username']
            
            now = getCurrTimeStr()
            query = "UPDATE users SET lastlogin=%s WHERE username=%s"
            cur.execute(query, (now, username))
            query = "UPDATE users SET online=TRUE WHERE username=%s" 
            cur.execute(query, (username,))
            conn.commit()
        else:
            error = 'Invalid username or password!'

    if 'username' in session:
        username = session['username']
        query = "SELECT role, lastlogin FROM users WHERE username=%s"
        cur.execute(query, (username,))
        role,lastlogin = cur.fetchone()
        g.role = role
        g.lastlogin = lastlogin
    else:
        flash('Wrong username or password')
        return render_template('signin.html')

    return render_template('adminpanel.html', error=error, roles=roles)

@app.route('/signup', methods=['POST'])
def signup():
    '''Routing function for signup page. 
    
    It allows only *POST* request.
    If the valid values are gotten from the request.form then new user is created and inserted 
    to the db.
    '''
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
    '''Routing function for logout page.
    
    When this page called if there is a user logged in, then the user removed from the session.
    
    After all it redirects to the home page.
    '''
    conn, cur = getDb()
    if 'username' in session:
        username = session['username']
        query = "UPDATE users SET online=FALSE WHERE username=%s"
        cur.execute(query, (username,))
        conn.commit()
    g.role = 'guest'
    session.pop('username', None)
    return redirect(url_for('home'))


