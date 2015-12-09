import sys
import json

from final4.config import app
from final4.db_helper import getDb
from final4.models import standing
from final4.models import season

from flask import render_template
from flask import request

# standing views
@app.route('/standings', methods=['DEL','GET', 'POST'])
def standing_page():
    conn, cur = getDb()
    standings = standing.Standings(conn, cur)
    season = season.Seasons(conn, cur)
    print('STANDINGS PAGE')
    if request.method == 'GET':
        l, total = standings.get_standings(5,0)
        c = seasons.get_seasons()
        return render_template('standings.html', standingtable=standing.standingtable, standings=l, seasons=c, total=total)
    elif request.method == 'POST':
        print('ADD STANDING')
        season_id = request.form['season']
        league_id=request.form['league_id']
        team_id = request.form['team_id']
        lg = standing.Standing(season_id,league_id,team_id)
        standings.add_standing(lg)
        
        l, total = standings.get_standings(5,0)
        c = seasons.get_seasons()
        return render_template('standings.html', standingtable=standing.standingtable, standings=l, seasons=c, total=total)

    elif request.method == 'DEL':
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
            standings.delete_standing(_id)
        return json.dumps({'status':'OK', 'idlist':idlist})
        '''
        try:
            for _id in idlist:
                print (_id)
                standings.delete_standing(_id)
            return json.dumps({'status':'OK', 'idlist':idlist})
        except:
            error = sys.exc_info()[0]
            return json.dumps({'status':'FAILED', 'error':error})
        '''
        #return render_template('standing.html', standingtable=standing.standingtable, standings=l)




@app.route('/standings/g/<lid>', methods=['GET','POST'])
def standing_from_id(lid):
    conn, cur = getDb()
    standings = standing.Standings(conn, cur)
    seasons=seasons.Seasons(conn,cur)
    
    if request.method == 'GET':
        l = standings.get_standing(lid)
        if l:
            return json.dumps({'status':'OK', 'standing':l.getAttrs()})
        else:
            return json.dumps({'status':'FAILED'})
    elif request.method == 'POST':
        print("POST METHOD REQUEST")
        lid = request.form['id']
        season_id = request.form['season']
        league_id=request.form['league_id']
        team_id = request.form['team_id']
        lg = standing.Standing(season_id,league_id,team_id)
        standings.update_standing(lid, lg)

        l, total = standings.get_standings(5,0)
        c = seasons.get_seasons()
        l = standings.get_standings()
        return render_template('standings.html', standingtable=standing.standingtable, standings=l, seasons=c, total=total)

@app.route('/standings/s/<key>', methods=['GET','POST'])
def search_standing(key):
    conn, cur = getDb()
    standings = standing.Standings(conn, cur)
    seasons = season.Seasons(conn, cur)

    result = standings.get_standings_by(key, 'league_id')
    c = seasons.get_seasons()
    return render_template('standings.html', standingtable=standing.standingtable, standings=l, seasons=c, total=total)
