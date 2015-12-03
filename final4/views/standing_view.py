import sys
import json

from final4.config import app
from final4.db_helper import getDb
from final4.models import standing

from flask import render_template
from flask import request

# standing views
@app.route('/standings', methods=['DEL','GET', 'POST', 'PUT'])
def standing_page():
    conn, cur = getDb()
    standings = standing.Standings(conn, cur)
    print('STANDINGS PAGE')
    if request.method == 'GET':
        l = standings.get_standings()
        return render_template('standings.html', standingtable=standing.standingtable, standings=l)
    elif request.method == 'POST':
        winning = request.form['winning']
        season_id = request.form['season_id']
        league_id=request.form['league_id']
        team_id = request.form['team_id']
        lg = standing.Standing(winning, season_id,league_id,team_id)
        standings.add_standing(lg)
        
        l = standings.get_standings()
        return render_template('standings.html', standingtable=standing.standingtable, standings=l)

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




@app.route('/standing/g/<lid>', methods=['GET','POST'])
def standing_from_id(lid):
    conn, cur = getDb()
    standings = standing.standings(conn, cur)
    
    if request.method == 'GET':
        l = standings.get_standing(lid)
        if l:
            return json.dumps({'status':'OK', 'standing':l.getAttrs()})
        else:
            return json.dumps({'status':'FAILED'})
    elif request.method == 'POST':
        print("PUT METHOD REQUEST")
        lid = request.form['id']
        winning = request.form['winning']
        season_id = request.form['season_id']
        league_id=request.form['league_id']
        team_id = request.form['team_id']
        print(lid, winning, season_id,league_id,team_id)
        lg = standing.Standing(winning, season_id,league_id,team_id)
        standings.update_standing(lid, lg)

        l = standings.get_standings()
        return render_template('standings.html', standingtable=standing.standingtable, standings=l)


