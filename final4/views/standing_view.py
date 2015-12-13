import sys
import json

from final4.config import app
from final4.db_helper import getDb
from final4.models import standing
from final4.models import season
from final4.models import league
from final4.models import team

from flask import render_template
from flask import request
from flask import session

# standing views
@app.route('/standings', methods=['DEL','GET', 'POST'])
def standing_home():
    conn, cur = getDb()
    standings = standing.Standings(conn, cur)
    seasons = season.Seasons(conn, cur)
    leagues = league.Leagues(conn, cur)
    teams = team.Teams(conn, cur)
    print('STANDINGS PAGE')
    if request.method == 'GET':
        # handle GET request
        print ('GET REQUEST', request.args)
        limit = int(request.args['limit']) if 'limit' in request.args else 10
        page = int(request.args['page']) if 'page' in request.args else 0
        
        offset = page*limit
        print('page:',page,'limit',limit,'offset',offset)
        
        if 'name' in request.args:
            search_name = request.args['name']
            l, total = standings.get_standings_search_by('name', search_name, limit=limit, offset=offset)
        else:
            l, total = standings.get_standings(limit=limit, offset=offset)
    return render_template('standings_home.html', standingtable=standing.standingtable, standings=l, total=total, 
                limit=limit, page=page)
     
@app.route('/standings/table', methods=['DEL','GET', 'POST'])
def standing_page():
    if 'username' not in session:
        return render_template('error.html', err_code=401)
    
    conn, cur = getDb()
    standings = standing.Standings(conn, cur)
    seasons = season.Seasons(conn, cur)
    leagues = league.Leagues(conn, cur)
    teams = team.Teams(conn, cur)
    print('STANDINGS PAGE')
    if request.method == 'GET':
        # handle GET request
        print ('GET REQUEST', request.args)
        limit = int(request.args['limit']) if 'limit' in request.args else 10
        page = int(request.args['page']) if 'page' in request.args else 0
        
        offset = page*limit
        print('page:',page,'limit',limit,'offset',offset)
        
 
        standing_list, total = standings.get_standings(limit, offset)
        season_list = seasons.get_seasons()
        league_list,tk = leagues.get_leagues(100,0) # get list object
        team_list,tp = teams.get_teams(100,0)
        
        return render_template('standings.html', standingtable=standing.standingtable, 
			standings=standing_list, seasons=season_list, leagues=league_list, teams=team_list, 
			total=total, limit=limit, page=page)
    elif request.method == 'POST':
        print('ADD STANDING')
        season_id = request.form['season_year']
        league_id= request.form['league_name']
        team_id = request.form['team_name']
        limit = int(request.form['limit']) if 'limit' in request.form else 10
        page = int(request.form['page']) if 'page' in request.form else 0
        offset = page*limit
        
        standing_obj = standing.Standing(season_id, league_id, team_id)
        standings.add_standing(standing_obj)
        
        standing_list, total= standings.get_standings(limit,offset)
        season_list = seasons.get_seasons()
        league_list,tk = leagues.get_leagues(100,0)
        team_list,tp = teams.get_teams(100,0)
        
        return render_template('standings.html', standingtable=standing.standingtable, 
			standings=standing_list, seasons=season_list, leagues=league_list, teams=team_list, 
			total=total, limit=limit, page=page)

    elif request.method == 'DEL':
        # handle DEL request
        print ('DELETE REQUEST:STANDINGS PAGE')
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
            standings.delete_standing(_id) # delete object
        return json.dumps({'status':'OK', 'idlist':idlist})
 


@app.route('/standings/g/<standing_id>', methods=['GET','POST'])
def standing_from_id(standing_id):
    if 'username' not in session:
        return render_template('error.html', err_code=401)
        
    conn, cur = getDb()
    standings = standing.Standings(conn, cur)
    seasons=season.Seasons(conn,cur)
    leagues=league.Leagues(conn,cur)
    teams=team.Teams(conn,cur)
    
    if request.method == 'GET':
        l = standings.get_standing(standing_id)
        if l:
            return json.dumps({'status':'OK', 'standing':l.getAttrs()})
        else:
            return json.dumps({'status':'FAILED'})
    elif request.method == 'POST':
        print("POST METHOD REQUEST")
        lid = request.form['id']
        season_id = request.form['season_year']
        league_id= request.form['league_name']
        team_id = request.form['team_name']
        
        limit = int(request.form['limit']) if 'limit' in request.form else 10
        page = int(request.form['page']) if 'page' in request.form else 0
        offset = page*limit
        
        standing_obj = standing.Standing(season_id,league_id,team_id)
       
        standings.update_standing(lid,standing_obj)
        
        standing_list, total= standings.get_standings(limit,offset)
        season_list = seasons.get_seasons()
        league_list,tk = leagues.get_leagues(100,0)
        team_list,tp = teams.get_teams(100,0)
        
        return render_template('standings.html', standingtable=standing.standingtable, 
			standings=standing_list, seasons=season_list, leagues=league_list, teams=team_list, 
			total=total, limit=limit, page=page)

@app.route('/standings/s/<key>', methods=['GET','POST'])
def search_standing(key):
    if 'username' not in session:
        return render_template('error.html', err_code=401)    
    
    conn, cur = getDb()
    standings = standing.Standings(conn, cur)
    seasons=season.Seasons(conn,cur)
    leagues=league.Leagues(conn,cur)
    teams=team.Teams(conn,cur)

    limit = int(request.args['limit']) if 'limit' in request.args else 10
    page = int(request.args['page']) if 'page' in request.args else 0
    
    offset = page*limit
    
    standing_list,total = standings.get_standings_search_by('name', key,  limit, offset)
    season_list = seasons.get_seasons()
    league_list,tk = leagues.get_leagues(100,0)
    team_list,tp = teams.get_teams(100,0)
    
    return render_template('standings.html', standingtable=standing.standingtable, 
			standings=standing_list, seasons=season_list, leagues=league_list, teams=team_list, 
			total=total, limit=limit, page=page)
		
