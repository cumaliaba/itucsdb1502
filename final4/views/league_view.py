import sys
import json

from final4.config import app
from final4.db_helper import getDb
from final4.models import league
from final4.models import country

from flask import render_template
from flask import request
from flask import session

# league views

@app.route('/leagues', methods=['GET'])
def leagues_home():
    ''' This view page list all leagues in leagues table.
        This page doesn't allow editing.
    '''
    conn, cur = getDb()
    leagues = league.Leagues(conn, cur)
    countries = country.Countries(conn, cur)
    
    # limit, page and order args
    # required for each table page
    limit = int(request.args['limit']) if 'limit' in request.args else 10
    page = int(request.args['page']) if 'page' in request.args else 0
    offset = page*limit
    sortby = request.args['sortby'] if 'sortby' in request.args else 'name'
    order = request.args['order'] if 'order' in request.args else 'asc'
        
    sortby={'attr':'name', 'property':'asc'}
   
    # check search value
    if 'name' in request.args:
        search_name = request.args['name']
        l, total = leagues.get_leagues_search_by('name', search_name, limit=limit, offset=offset)
    else:
        l, total = leagues.get_leagues(limit=limit, offset=offset)
    return render_template('leagues_home.html', leaguetable=league.leaguetable, leagues=l, total=total, 
                limit=limit, page=page, sortby=sortby)

@app.route('/leagues/table', methods=['DEL','GET', 'POST'])
def league_page():
    if 'username' not in session:
        return render_template('error.html', err_code=401)

    conn, cur = getDb()
    leagues = league.Leagues(conn, cur)
    countries = country.Countries(conn, cur)
    print('LEAGUES PAGE')
    if request.method == 'GET':
        # handle GET request
        print ('GET REQUEST', request.args)
        limit = int(request.args['limit']) if 'limit' in request.args else 10
        page = int(request.args['page']) if 'page' in request.args else 0
        
        offset = page*limit
        print('page:',page,'limit',limit,'offset',offset)
        sortby = request.args['sortby'] if 'sortby' in request.args else 'name'
        order = request.args['order'] if 'order' in request.args else 'asc'
 
        l, total = leagues.get_leagues(limit, offset)
        c = countries.get_countries()
        sortby={'attr':'name', 'property':'asc'}
        return render_template('leagues.html', leaguetable=league.leaguetable, leagues=l, countries=c, total=total, 
                limit=limit, page=page, sortby=sortby)
    elif request.method == 'POST':
        # handle POST request
        print('ADD LEAGUE')
        name = request.form['name']
        country_id = request.form['country']
        limit = int(request.form['limit']) if 'limit' in request.form else 10
        page = int(request.form['page']) if 'page' in request.form else 0
        offset = page*limit
        sortby = request.form['sortby'] if 'sortby' in request.form else 'name'
        order = request.form['order'] if 'order' in request.form else 'asc'
        lg = league.League(name, country_id)
        leagues.add_league(lg)
        
        l, total = leagues.get_leagues(limit, offset)
        c = countries.get_countries()
        sortby={'attr':'name', 'property':'asc'}
        return render_template('leagues.html', leaguetable=league.leaguetable, leagues=l, countries=c, total=total, 
                                limit=limit, page=page, sortby=sortby)

    elif request.method == 'DEL':
        # handle DEL request
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
    if 'username' not in session:
        return render_template('error.html', err_code=401)
    conn, cur = getDb()
    leagues = league.Leagues(conn, cur)
    countries = country.Countries(conn, cur)
    
    if request.method == 'GET':
        # handle GET request
        l= leagues.get_league(lid)
        if l:
            return json.dumps({'status':'OK', 'league':l.getAttrs()})
        else:
            return json.dumps({'status':'FAILED'})
    elif request.method == 'POST':
        # handle POST request
        print("POST METHOD REQUEST")
        lid = request.form['id']
        name = request.form['name']
        country_id = request.form['country']
        # limit: number of result showing each page
        # offset: selectedpage x limit
        limit = int(request.form['limit']) if 'limit' in request.form else 10
        page = int(request.form['page']) if 'page' in request.form else 0
        offset = page*limit
        order = request.form['sortby'] if 'sortby' in request.form else 'name'
        order = request.form['order'] if 'order' in request.form else 'asc'
        lg = league.League(name, country_id)
        leagues.update_league(lid, lg)
        
        l, total = leagues.get_leagues(limit, offset)
        c = countries.get_countries()
        sortby={'attr':'name', 'property':'asc'}
        return render_template('leagues.html', leaguetable=league.leaguetable, leagues=l, countries=c, total=total, 
                                limit=limit, page=page, sortby=sortby)


@app.route('/leagues/s/<key>', methods=['GET','POST'])
def search_league(key):
    if 'username' not in session:
        return render_template('error.html', err_code=401)
    conn, cur = getDb()
    leagues = league.Leagues(conn, cur)
    countries = country.Countries(conn, cur)

    limit = int(request.args['limit']) if 'limit' in request.args else 10
    page = int(request.args['page']) if 'page' in request.args else 0

    sortby = request.args['sortby'] if 'sortby' in request.args else 'name'
    order = request.args['order'] if 'order' in request.args else 'asc'
    
    offset = page*limit

    result,total = leagues.get_leagues_search_by('name', key,  limit, offset)
    c = countries.get_countries()
    sortby={'attr':'name', 'property':'asc'}
    return render_template('leagues.html', leaguetable=league.leaguetable, leagues=result, countries=c, total=total, 
                            limit=limit, page=page, sortby=sortby)

@app.route('/leagues/league/<league_id>')
def view_league(league_id):
    conn, cur = getDb()

    leagues = league.Leagues(conn, cur)

    l = leagues.get_league(league_id)
    if l is None:
        # return not found error 
        return render_template('error.html', err_code=404)

    # else render country page with required args

    #teams = teams.Teams(conn, cur)
    #team_list, total = teams.get_teams_by('league_id', l.country_id)
    #team_dict = {'teams':team_list,
    #                'total': total
    #                }
    return render_template('league_page.html', league=l, 
            team_dict=None)
