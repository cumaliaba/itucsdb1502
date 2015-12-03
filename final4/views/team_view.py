import sys
import json

from final4.config import app
from final4.db_helper import getDb
from final4.models import team

from flask import render_template
from flask import request

# team views
@app.route('/teams', methods=['DEL','GET', 'POST', 'PUT'])
def team_page():
    conn, cur = getDb()
    teams = team.Teams(conn, cur)
    print('TEAMS PAGE')
    if request.method == 'GET':
        t = teams.get_teams()
        return render_template('teams.html', teamtable=team.teamtable, teams=t)
    elif request.method == 'POST':
        name = request.form['name']
        coach_id = request.form['coach_id']
        tm = team.Team(name, coach_id)
        teams.add_team(tm)
        
        t = teams.get_teams()
        return render_template('teams.html', teamtable=team.teamtable, teams=t)

    elif request.method == 'DEL':
        print ('DELETE REQUEST:TEAMS PAGE')
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
            teams.delete_team(_id)
        return json.dumps({'status':'OK', 'idlist':idlist})
        '''
        try:
            for _id in idlist:
                print (_id)
                leagues.delete_league(_id)
            return json.dumps({'status':'OK', 'idlist':idlist})
        except:
            error = sys.exc_info()[0]
            return json.dumps({'status':'FAILED', 'error':error})
        '''
        #return render_template('teams.html', teamtable=team.teamtable, teams=t)




@app.route('/teams/<tid>', methods=['GET','POST'])
def team_from_id(tid):
    conn, cur = getDb()
    teams = team.Teams(conn, cur)
    
    if request.method == 'GET':
        t = teams.get_team(tid)
        if t:
            return json.dumps({'status':'OK', 'team':t.getAttrs()})
        else:
            return json.dumps({'status':'FAILED'})
    elif request.method == 'POST':
        print("PUT METHOD REQUEST")
        tid = request.form['id']
        name = request.form['name']
        coach_id = request.form['coach_id']
        print(tid, name, coach_id)
        tm = tm.Team(name, coach_id)
        teams.update_team(tid, tm)

        t = teams.get_teams()
        return render_template('teams.html', teamtable=team.teamtable, teams=t)


