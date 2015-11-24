import datetime
import json
import os
import psycopg2
import re


from flask import redirect
from flask import render_template
from flask.helpers import url_for


from final4.config import app

from final4 import db_helper as db

from final4.helper import getCurrTimeStr

from final4.views import login_view
from final4.views import league_view
from final4.views import player_view
from final4.views import award_view
from final4.views import stat_view
from final4.views import season_view
from final4.views import standing_view

def get_elephantsql_dsn(vcap_services):
    """Returns the data source name for ElephantSQL."""
    parsed = json.loads(vcap_services)
    uri = parsed["elephantsql"][0]["credentials"]["uri"]
    match = re.match('postgres://(.*?):(.*?)@(.*?)(:(\d+))?/(.*)', uri)
    user, password, host, _, port, dbname = match.groups()
    dsn = """user='{}' password='{}' host='{}' port={}
        dbname='{}'""".format(user, password, host, port, dbname)
    return dsn

# PAGE ROUTES

@app.route('/')
def home():
    conn, cur = db.getDb()
    now = datetime.datetime.now()
    return render_template('home.html', current_time=now.ctime())

@app.route('/initdb')
def initialize_database():
    conn, cur = db.getDb()
    
    try:
        conn, cur = db.getDb()

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

        #seasons table
        query="DROP TABLE IF EXISTS seasons;"
        cur.execute(query)

        query="""CREATE TABLE SEASONS ( id serial PRIMARY KEY, 
					year INTEGER);"""
        cur.execute(query)
        
        # standings table
        query = "DROP TABLE IF EXISTS standings;"
        cur.execute(query)

        query="""CREATE TABLE standings (id serial PRIMARY KEY,
                                winning varchar(80), 
				season_id integer, 
			      	league_id integer, 
				team_id integer);"""

        cur.execute(query)


        # coaches table
        query = "DROP TABLE IF EXISTS coaches;"
        cur.execute(query)

        query = """CREATE TABLE coaches (id serial PRIMARY KEY, 
                               name varchar(32) NOT NULL, surname varchar(32) NOT NULL,
                               nationality varchar(32), 
                               playerid integer, seasonid integer);
        """
        cur.execute(query)

        # teams table

        query = "DROP TABLE IF EXISTS teams;"
        cur.execute(query)

        query = """CREATE TABLE teams (id serial PRIMARY KEY, 
                               name varchar(32) NOT NULL,
                               coach_id integer REFERENCES coaches(id));
        """
        cur.execute(query)
        
	# teamrosters table
        query = "DROP TABLE IF EXISTS teamrosters;"
        cur.execute(query)

        query = """CREATE TABLE teamrosters (id serial PRIMARY KEY, 
                               team_id integer REFERENCES teams(id),
                               player_id integer REFERENCES players(id));
        """


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
