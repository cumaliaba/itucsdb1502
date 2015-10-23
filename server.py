import datetime
import json
import os
import psycopg2
import re

from flask import Flask
from flask import redirect
from flask import render_template
from flask.helpers import url_for


app = Flask(__name__)


def get_sqldb_dsn(vcap_services):
    """Returns the data source name for IBM SQL DB."""
    parsed = json.loads(vcap_services)
    credentials = parsed["sqldb"][0]["credentials"]
    user = credentials["username"]
    password = credentials["password"]
    host = credentials["hostname"]
    port = credentials["port"]
    dbname = credentials["db"]
    dsn = """DATABASE={};HOSTNAME={};PORT={};UID={};PWD={};""".format(dbname, host, port, user, password)
    return dsn


@app.route('/')
def home_page():
    now = datetime.datetime.now()
    return render_template('home.html', current_time=now.ctime())


@app.route('/initdb')
def initialize_database():
    try:
        conn = psycopg2.connect(app.config['dsn'])
        cur = conn.cursor()
        query = """DROP TABLE IF EXISTS COUNTER"""
        cur.execute(query)
        conn.commit()
        cur.close()
        conn.close()
    except:
        return 'DROP TABLE ERROR'
    try:
        conn = psycopg2.connect(app.config['dsn'])
        cur = conn.cursor()
        query = """CREATE TABLE COUNTER (N INTEGER)"""
        cur.execute(query)
    
        query = """INSERT INTO COUNTER (N) VALUES (0)"""
        cur.execute(query)
        conn.commit()
        cur.close()
        conn.close()
    except:
        return 'CREATE TABLE ERROR'
    return redirect(url_for('home_page'))


@app.route('/count')
def counter_page():
    print (app.config['dsn'])
    conn = psycopg2.connect(app.config['dsn'])
    cur = conn.cursor() # get cursor

    query = "UPDATE COUNTER SET N = N + 1"
    cur.execute(query)
    conn.commit()

    query = "SELECT N FROM COUNTER"
    cur.execute(query)
    (count,) = cur.fetchone()
    return "This page was accessed %d times." % count


if __name__ == '__main__':
    VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
    if VCAP_APP_PORT is not None:
        port, debug = int(VCAP_APP_PORT), False
    else:
        port, debug = 5000, True

    VCAP_SERVICES = os.getenv('VCAP_SERVICES')
    if VCAP_SERVICES is not None:
        app.config['dsn'] = get_sqldb_dsn(VCAP_SERVICES)
    else:
        app.config['dsn'] = """dbname=itucsdb host=localhost port=54321 user=vagrant password=vagrant"""

    app.run(host='0.0.0.0', port=port, debug=debug)
