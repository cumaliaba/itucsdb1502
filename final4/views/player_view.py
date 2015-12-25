import os
import json
import sys

from final4.config import app
from final4.db_helper import getDb
from final4.models import player
from final4.models import country

from flask import render_template
from flask import request

@app.route('/players', methods=['DEL','GET', 'POST'])
def player_page():
    conn, cur = getDb()
    players = player.Players(conn, cur)
    countries = country.Countries(conn, cur)
    print('players PAGE')
    if request.method == 'GET':
        limit = int(request.args['limit']) if 'limit' in request.args else 10
        page = int(request.args['page']) if 'page' in request.args else 0
        
        offset = page*limit
        print('page:',page,'limit',limit,'offset',offset)
        sortby = request.args['sortby'] if 'sortby' in request.args else 'name'
        order = request.args['order'] if 'order' in request.args else 'asc'

        p, total_players = players.get_players()
        c,total_countries = countries.get_countries()

        sortby={'attr':'name', 'property':'asc'}

        return render_template('players.html', playertable=player.playertable, players=p, countries=c, total=total_players,
                limit=limit, page=page)
    elif request.method == 'POST':
        print('ADD player')
        name = request.form['name']
        surname = request.form['surname']
        age=request.form['age']
        pp=request.form['pp']
        country_id = request.form['country']
        player_img = request.files['file']

        limit = int(request.form['limit']) if 'limit' in request.form else 10
        page = int(request.form['page']) if 'page' in request.form else 0
        offset = page*limit
        order = request.form['sortby'] if 'sortby' in request.form else 'name'
        order = request.form['order'] if 'order' in request.form else 'asc'

        print(name, surname, player_img)
        pl = player.Player(name, surname,age,pp,country_id)
        insert_id = players.add_player(pl)
        if player_img:
            save_path = pl.img_path(insert_id)
            player_img.save(app.config['APP_FOLDER']+save_path)
    
        p, total_players = players.get_players()
        c,total_countries = countries.get_countries()

        sortby={'attr':'name', 'property':'asc'}

        return render_template('players.html', playertable=player.playertable, players=p, countries=c, total=total_players,
                limit=limit, page=page)

    elif request.method == 'DEL':
        print ('DELETE REQUEST:players PAGE')
        print (request.form)
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

@app.route('/players/g/<pid>', methods=['GET','POST'])
def player_from_id(pid):
    conn, cur = getDb()
    players = player.Players(conn, cur)
    countries = country.Countries(conn, cur)
    
    if request.method == 'GET':
        p= players.get_player(pid)
        if p:
            return json.dumps({'status':'OK', 'player':p.getAttrs()})
        else:
            return json.dumps({'status':'FAILED'})
    elif request.method == 'POST':
        print("POST METHOD REQUEST")
        pid = request.form['id']
        name = request.form['name']
        surname = request.form['surname']
        age=request.form['age']
        pp=request.form['pp']
        country_id = request.form['country']
        player_img = request.files['file']

        limit = int(request.form['limit']) if 'limit' in request.form else 10
        page = int(request.form['page']) if 'page' in request.form else 0
        offset = page*limit
        order = request.form['sortby'] if 'sortby' in request.form else 'name'
        order = request.form['order'] if 'order' in request.form else 'asc'

        pl = player.Player(name, surname,age,pp, country_id)
        players.update_player(pid, pl)
        
        if player_img:
            save_path = pl.img_path(pid)
            player_img.save(app.config['APP_FOLDER']+save_path)

        p, total_players = players.get_players()
        c,total_countries = countries.get_countries()

        sortby={'attr':'name', 'property':'asc'}

        return render_template('players.html', playertable=player.playertable, players=p, countries=c, total=total_players,
                limit=limit, page=page)


@app.route('/players/s/<key>', methods=['GET','POST'])
def search_player(key):
    conn, cur = getDb()
    players = player.Players(conn, cur)
    countries = country.Countries(conn, cur)

    p, total_players = players.get_players_search_by('name', key)
    c,total_countries = countries.get_countries()
    
    limit = int(request.args['limit']) if 'limit' in request.args else 10
    page = int(request.args['page']) if 'page' in request.args else 0
    
    offset = page*limit
    print('page:',page,'limit',limit,'offset',offset)
    sortby = request.args['sortby'] if 'sortby' in request.args else 'name'
    order = request.args['order'] if 'order' in request.args else 'asc'

    sortby={'attr':'name', 'property':'asc'}

    return render_template('players.html', playertable=player.playertable, players=p, countries=c, total=total_players,
        limit=limit, page=page)
