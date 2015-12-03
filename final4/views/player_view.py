import sys
import json

from final4.config import app
from final4.db_helper import getDb
from final4.models import player

from flask import render_template
from flask import request

# player views
@app.route('/players', methods=['DEL','GET', 'POST', 'PUT'])
def player_page():
    conn, cur = getDb()
    players = player.Players(conn, cur)
    print('PLAYERS PAGE')
    if request.method == 'GET':
        p = players.get_players()
        return render_template('players.html', playertable=player.playertable, players=p)
    elif request.method == 'POST':
        name = request.form['name']
        country = request.form['country']
        age = request.form['age']
        playing_position = request.form['playing_position']
        pl = player.Player(name, country,age,playing_position)
        players.add_player(pl)
        
        p = players.get_player()
        return render_template('players.html', playertable=player.playertable, platers=p)

    elif request.method == 'DEL':
        print ('DELETE REQUEST:PLAYERS PAGE')
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
            players.delete_player(_id)
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
        #return render_template('players.html', playertable=player.playertable, players=p)




@app.route('/players/<pid>', methods=['GET','POST'])
def player_from_id(pid):
    conn, cur = getDb()
    players = player.Players(conn, cur)
    
    if request.method == 'GET':
        p = players.get_player(pid)
        if p:
            return json.dumps({'status':'OK', 'player':p.getAttrs()})
        else:
            return json.dumps({'status':'FAILED'})
    elif request.method == 'POST':
        print("PUT METHOD REQUEST")
        pid = request.form['id']
        name = request.form['name']
        country = request.form['country']
        age = request.form['age']
        playing_position = request.form['playing_position']
        print(pid, name, country)
        pl = player.Player(name, country,age,playing_position)
        players.update_player(pid, pl)

        p = players.get_players()
        return render_template('players.html', playertable=player.playertable, players=p)


