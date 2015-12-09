import datetime
import json
import os
import psycopg2
import re
import sys

from flask import g
from flask import redirect
from flask import render_template
from flask.helpers import url_for
from flask import send_from_directory


from final4.config import app

from final4 import db_helper as db

from final4.helper import getCurrTimeStr

from final4.views import login_view
from final4.views import league_view
from final4.views import player_view
from final4.views import award_view
from final4.views import stat_view
from final4.views import country_view
from final4.views import coach_view

from final4.views import team_view
from final4.views import teamroster_view

from final4.views import season_view
from final4.views import standing_view
#from final4.views import schedule_view
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

@app.route('/data/flags/<path:fn>')
def flag_folder(fn):
    return send_from_directory('static', fn)

@app.route('/initdb')
def initialize_database():
    conn, cur = db.getDb()
    
    try:
        conn, cur = db.getDb()

        drop_tables()
        # users table
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


        # countries table
        query = """CREATE TABLE countries (id serial PRIMARY KEY, 
                               name varchar(65) NOT NULL,
                               code varchar(2) NOT NULL);
        """
        cur.execute(query)


        # leagues table
        query = """CREATE TABLE leagues (id serial PRIMARY KEY, 
                               name varchar(255) NOT NULL,
                               country_id integer references countries(id) );
        """
        cur.execute(query)

        # players table
        query = """CREATE TABLE players (id serial PRIMARY KEY, 
                               name varchar(32) NOT NULL,
                               surname varchar(32) NOT NULL,
                               age varchar(3),
                               pp  varchar(32),
                               country_id integer references countries(id));
        """
        cur.execute(query)

        #seasons table

        query="""CREATE TABLE seasons ( id serial PRIMARY KEY, 
					year varchar(9));"""
        cur.execute(query)
    
        # awards table
        query = """CREATE TABLE awards (id serial PRIMARY KEY, 
                               name varchar(32) NOT NULL,
                               player_id integer references players(id), season_id integer references seasons(id));
        """
        cur.execute(query)


        # coaches table
        query = """CREATE TABLE coaches (id serial PRIMARY KEY, 
                               name varchar(32) NOT NULL, 
                               surname varchar(32) NOT NULL,
                               country_id integer REFERENCES countries(id));
        """
        cur.execute(query)

        # teams table
        query = """CREATE TABLE teams (id serial PRIMARY KEY, 
                               name varchar(255) NOT NULL,
                               country_id integer references countries(id) );
        """
        cur.execute(query)
	    # teamrosters table
        query = """CREATE TABLE teamrosters (id serial PRIMARY KEY, 
                               team_id integer REFERENCES teams(id),
                               player_id integer REFERENCES players(id));
"        """



        
        # standings table
        query="""CREATE TABLE standings ( id serial PRIMARY KEY, 
			      	season_id integer REFERENCES seasons(id),
			      	league_id integer REFERENCES leagues(id), 
				team_id integer REFERENCES teams(id));"""

        cur.execute(query)
        
        # schedules table
        # query=CREATE TABLE schedules (id serial PRIMARY KEY,
        #                      team1 integer REFERENCES teams(id),
        #                     team2 integer REFERENCES teams(id),
        #                   date varchar(65));"""
        
        # DO NOT ADD ANYTHING AFTER THIS LINE
        conn.commit() # commit changes
    except:
        print(sys.exc_info())
        conn.rollback()
        return 'create table error'
    return redirect(url_for('home'))


def drop_tables():
    conn, cur = db.getDb()
    
    query = "DROP TABLE IF EXISTS standings;"
    cur.execute(query)   
    
    query = "DROP TABLE IF EXISTS awards;"
    cur.execute(query)
    
    query = "DROP TABLE IF EXISTS teamrosters;"
    cur.execute(query)
    
    query = "DROP TABLE IF EXISTS teams;"
    cur.execute(query)

    query = "DROP TABLE IF EXISTS coaches;"
    cur.execute(query)

    query="DROP TABLE IF EXISTS seasons;"
    cur.execute(query)
    
    #query="DROP TABLE IF EXISTS schedules;"
    #cur.execute(query)

    query = "DROP TABLE IF EXISTS players;"
    cur.execute(query)

    query = "DROP TABLE IF EXISTS leagues;"
    cur.execute(query)

    query = "DROP TABLE IF EXISTS countries;"
    cur.execute(query)

    query = "DROP TABLE IF EXISTS users;"
    cur.execute(query)
 




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
