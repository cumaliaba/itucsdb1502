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
        print ('GET REQUEST', request.args)
        limit = int(request.args['limit']) if 'limit' in request.args else 10
        page = int(request.args['page']) if 'page' in request.args else 0
        
        offset = page*limit
        print('page:',page,'limit',limit,'offset',offset)
        orderby = request.args['orderby'] if 'orderby' in request.args else 'asc'
        l, total = leagues.get_leagues(limit, offset)
        c = countries.get_countries()
        return render_template('leagues.html', leaguetable=league.leaguetable, leagues=l, countries=c, total=total, 
                                limit=limit, page=page)
    elif request.method == 'POST':
        print('ADD LEAGUE')
        name = request.form['name']
        country_id = request.form['country']
        limit = int(request.form['limit']) if 'limit' in request.form else 10
        page = int(request.form['page']) if 'page' in request.form else 0
        offset = page*limit
        orderby = request.form['orderby'] if 'orderby' in request.form else 'asc'
        lg = league.League(name, country_id)
        leagues.add_league(lg)
        
        l, total = leagues.get_leagues(limit, offset)
        c = countries.get_countries()
        return render_template('leagues.html', leaguetable=league.leaguetable, leagues=l, countries=c, total=total, 
                                limit=limit, page=page)

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
        # limit: number of result showing each page
        # offset: selectedpage x limit
        limit = int(request.form['limit']) if 'limit' in request.form else 10
        page = int(request.form['page']) if 'page' in request.form else 0
        offset = page*limit
        orderby = request.form['orderby'] if 'orderby' in request.form else 'asc'
        lg = league.League(name, country_id)
        leagues.update_league(lid, lg)
        
        l, total = leagues.get_leagues(limit, offset)
        c = countries.get_countries()
        return render_template('leagues.html', leaguetable=league.leaguetable, leagues=l, countries=c, total=total, 
                                limit=limit, page=page)


@app.route('/leagues/s/<key>', methods=['GET','POST'])
def search_league(key):
    conn, cur = getDb()
    leagues = league.Leagues(conn, cur)
    countries = country.Countries(conn, cur)

    limit = int(request.args['limit']) if 'limit' in request.args else 10
    page = int(request.args['page']) if 'page' in request.args else 0
    
    offset = page*limit

    result,total = leagues.get_leagues_by(key, 'name', limit, offset)
    c = countries.get_countries()
    return render_template('leagues.html', leaguetable=league.leaguetable, leagues=result, countries=c, total=total, 
                            limit=limit, page=page)
