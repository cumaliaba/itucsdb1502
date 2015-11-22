from flask import g
from final4.config import app
import psycopg2

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


