import sys
import json

from final4.config import app
from final4.db_helper import getDb
from final4.models import league
from final4.models import country

from flask import render_template
from flask import request

# league views
@app.route('/leagues', methods=['DEL','GET', 'POST'])
def league_page():
    conn, cur = getDb()
    leagues = league.Leagues(conn, cur)
    countries = country.Countries(conn, cur)
    print('LEAGUES PAGE')
    if request.method == 'GET':
        l, total = leagues.get_leagues(5,0)
        c = countries.get_countries()
        return render_template('leagues.html', leaguetable=league.leaguetable, leagues=l, countries=c, total=total)
    elif request.method == 'POST':
        print('ADD LEAGUE')
        name = request.form['name']
        country_id = request.form['country']
        lg = league.League(name, country_id)
        leagues.add_league(lg)
        
        l, total = leagues.get_leagues(5,0)
        c = countries.get_countries()
        return render_template('leagues.html', leaguetable=league.leaguetable, leagues=l, countries=c, total=total)

    elif request.method == 'DEL':
        print ('DELETE REQUEST:LEAGUES PAGE')
        print (request.form)
        # concat json var with '[]' for calling array getted with request
        idlist = request.form.getlist('ids[]')
        print ('IDS: ', idlist)
        if idlist == []:
            try:
                idlist = [request.form['id']]
                print ('IDS: ', idlist)
            except:
                return json.dumps({'status':'OK', 'idlist':idlist})

        print ('IDS: ', idlist)
        print(json.dumps({'status':'OK', 'idlist':idlist}))
        for _id in idlist:
            print (_id)
            leagues.delete_league(_id)
        return json.dumps({'status':'OK', 'idlist':idlist})

@app.route('/leagues/g/<lid>', methods=['GET','POST'])
def league_from_id(lid):
    conn, cur = getDb()
    leagues = league.Leagues(conn, cur)
    countries = country.Countries(conn, cur)
    
    if request.method == 'GET':
        l= leagues.get_league(lid)
        if l:
            return json.dumps({'status':'OK', 'league':l.getAttrs()})
        else:
            return json.dumps({'status':'FAILED'})
    elif request.method == 'POST':
        print("POST METHOD REQUEST")
        lid = request.form['id']
        name = request.form['name']
        country_id = request.form['country']
        lg = league.League(name, country_id)
        leagues.update_league(lid, lg)

        l, total = leagues.get_leagues(5,0)
        c = countries.get_countries()
        return render_template('leagues.html', leaguetable=league.leaguetable, leagues=l, countries=c, total=total)


@app.route('/leagues/s/<key>', methods=['GET','POST'])
def search_league(key):
    conn, cur = getDb()
    leagues = league.Leagues(conn, cur)
    countries = country.Countries(conn, cur)

    result = leagues.get_leagues_by(key, 'name')
    c = countries.get_countries()
    return render_template('leagues.html', leaguetable=league.leaguetable, leagues=result, countries=c)
