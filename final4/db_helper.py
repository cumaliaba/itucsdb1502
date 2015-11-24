from flask import g
from flask import session

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
    if hasattr(g, 'psdb'):
        conn, cur = getDb()
        
        cur.close() # close cursor object
        conn.close() # close database connection

def getDb():
    if not hasattr(g, 'psdb'):
        g.psdb = connectDb()
    return g.psdb


