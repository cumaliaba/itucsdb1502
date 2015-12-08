import sys
import json

from final4.config import app
from final4.db_helper import getDb
from final4.models import teamroster
from final4.models import team
from final4.models import player

from flask import render_template
from flask import request

# team views
@app.route('/teamrosters', methods=['DEL','GET', 'POST'])
def teamroster_page():
    conn, cur = getDb()
    teamrosters = teamroster.Teamrosters(conn, cur)
    teams=team.Teams(conn,cur)
    players=player.Players(conn,cur)
    print('TEAMROSTERS PAGE')
    if request.method == 'GET':
        print ('GET REQUEST', request.args)
        limit = int(request.args['limit']) if 'limit' in request.args else 10
        page = int(request.args['page']) if 'page' in request.args else 0
        
        offset = page*limit
        print('page:',page,'limit',limit,'offset',offset)
        orderby = request.args['orderby'] if 'orderby' in request.args else 'asc'
        tr, total = teamrosters.get_teamrosters(limit, offset)
        t = teams.get_teams()
        p=players.get_players()
        return render_template('teamrosters.html', teamrostertable=teamroster.teamrostertable, teamrosters=tr, teams=t,players=p, total=total, 
                                limit=limit, page=page)
    elif request.method == 'POST':
        print('ADD TEAMROSTER')
        team_id = request.form['team']
        player_id = request.form['player']
        limit = int(request.form['limit']) if 'limit' in request.form else 10
        page = int(request.form['page']) if 'page' in request.form else 0
        offset = page*limit
        orderby = request.form['orderby'] if 'orderby' in request.form else 'asc'
        trs = teamroster.Teamroster(team_id, player_id)
        teamrosters.add_teamroster(trs)
        
        tr, total = teamrosters.get_teamrosters(limit, offset)
        t = teams.get_teams()
        p=players.get_players()
        return render_template('teamrosters.html', teamrostertable=teamroster.teamrostertable, teams=t, players=p, total=total, 
                                limit=limit, page=page)

    elif request.method == 'DEL':
        print ('DELETE REQUEST:TEAMROSTERS PAGE')
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
            teams.delete_teamroster(_id)
        return json.dumps({'status':'OK', 'idlist':idlist})

@app.route('/teamrosters/g/<lid>', methods=['GET','POST'])
def teamroster_from_id(trid):
    conn, cur = getDb()
    teamrosters = teamroster.Teamrosters(conn, cur)
    teams=team.Teams(conn,cur)
    players=player.Players(conn,cur)
    if request.method == 'GET':
        tr= teamrosters.get_teamroster(trid)
        if tr:
            return json.dumps({'status':'OK', 'team':tr.getAttrs()})
        else:
            return json.dumps({'status':'FAILED'})
    elif request.method == 'POST':
        print("POST METHOD REQUEST")
        trid = request.form['id']
        team_id= request.form['team']
        player_id = request.form['player']
        # limit: number of result showing each page
        # offset: selectedpage x limit
        limit = int(request.form['limit']) if 'limit' in request.form else 10
        page = int(request.form['page']) if 'page' in request.form else 0
        offset = page*limit
        orderby = request.form['orderby'] if 'orderby' in request.form else 'asc'
        trs = teamroster.Teamroster(team_id, player_id)
        teamrosters.update_teamroster(trid, trs)
        
        tr, total = teamrosters.get_teamrosters(limit, offset)
        t = teams.get_teams()
        p=players.get_players()
        return render_template('teamrosters.html', teamrostertable=teamroster.teamrostertable, teamrosters=tr, teams=t,players=p, total=total, 
                                limit=limit, page=page)


@app.route('/teamrosters/s/<key>', methods=['GET','POST'])
def search_teamroster(key):
    conn, cur = getDb()
    teamrosters = teamroster.Teamrosters(conn, cur)
    coaches = coach.Coaches(conn, cur)
    teams=team.Teams(conn,cur)
    players=player.Players(conn,cur)
    limit = int(request.args['limit']) if 'limit' in request.args else 10
    page = int(request.args['page']) if 'page' in request.args else 0
    
    offset = page*limit

    result,total = teamrosters.get_teamrosters_by(key, 'name', limit, offset)
    t=teams.get_teams()
    p=players.get_players()
    return render_template('teamrosters.html', teamrostertable=teamroster.teamrostertable, teamrosters=result, teams=t,players=p, total=total, 
                            limit=limit, page=page)
