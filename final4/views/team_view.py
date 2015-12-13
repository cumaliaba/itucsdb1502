import os
import json
import sys

from final4.config import app
from final4.db_helper import getDb
from final4.models import team
from final4.models import country

from flask import render_template
from flask import request
@app.route('/teams', methods=['DEL','GET', 'POST'])
def team_page():
    conn, cur = getDb()
    teams = team.Teams(conn, cur)
    countries = country.Countries(conn, cur)
    print('teams PAGE')
    if request.method == 'GET':
        # handle GET request
        limit = int(request.args['limit']) if 'limit' in request.args else 10
        page = int(request.args['page']) if 'page' in request.args else 0
        
        offset = page*limit
        print('page:',page,'limit',limit,'offset',offset)
        sortby = request.args['sortby'] if 'sortby' in request.args else 'name'
        order = request.args['order'] if 'order' in request.args else 'asc'

        t, total_teams = teams.get_teams()
        c = countries.get_countries()

        sortby={'attr':'name', 'property':'asc'}

        return render_template('teams.html', teamtable=team.teamtable, teams=t, countries=c, total=total_teams,
                limit=limit, page=page)
    elif request.method == 'POST':
        print('ADD team')
        name = request.form['name']
        country_id = request.form['country']
        team_img = request.files['file']

        limit = int(request.form['limit']) if 'limit' in request.form else 10
        page = int(request.form['page']) if 'page' in request.form else 0
        offset = page*limit
        order = request.form['sortby'] if 'sortby' in request.form else 'name'
        order = request.form['order'] if 'order' in request.form else 'asc'

        print(name,team_img)
        tm = team.Team(name, country_id)
        insert_id = teams.add_team(tm)
        if team_img:
            save_path =tm.img_path(insert_id)
            team_img.save(app.config['APP_FOLDER']+save_path)
    
        t, total_teams = teams.get_teams()
        c = countries.get_countries()

        sortby={'attr':'name', 'property':'asc'}

        return render_template('teams.html', teamtable=team.teamtable, teams=t, countries=c, total=total_teams,
                limit=limit, page=page)

    elif request.method == 'DEL':
        print ('DELETE REQUEST:teams PAGE')
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
            teams.delete_team(_id)
        return json.dumps({'status':'OK', 'idlist':idlist})

@app.route('/teams/g/<lid>', methods=['GET','POST'])
def team_from_id(lid):
    conn, cur = getDb()
    teams = team.Teams(conn, cur)
    countries = country.Countries(conn, cur)
    
    if request.method == 'GET':
        t= teams.get_team(lid)
        if t:
            return json.dumps({'status':'OK', 'team':t.getAttrs()})
        else:
            return json.dumps({'status':'FAILED'})
    elif request.method == 'POST':
        print("POST METHOD REQUEST")
        lid = request.form['id']
        name = request.form['name']
        country_id = request.form['country']
        team_img = request.files['file']

        limit = int(request.form['limit']) if 'limit' in request.form else 10
        page = int(request.form['page']) if 'page' in request.form else 0
        offset = page*limit
        order = request.form['sortby'] if 'sortby' in request.form else 'name'
        order = request.form['order'] if 'order' in request.form else 'asc'

        tm = team.Team(name,country_id)
        teams.update_team(lid, tm)
       
        if team_img:
            save_path = tm.img_path(lid)
            team_img.save(app.config['APP_FOLDER']+save_path)

        t, total_teams = teams.get_teams()
        c = countries.get_countries()

        sortby={'attr':'name', 'property':'asc'}

        return render_template('teams.html', teamtable=team.teamtable, teams=t, countries=c, total=total_teams,
                limit=limit, page=page)


@app.route('/teams/s/<key>', methods=['GET','POST'])
def search_team(key):
    conn, cur = getDb()
    teams = team.Teams(conn, cur)
    countries = country.Countries(conn, cur)

    t, total_teams = teams.get_teams_search_by('name', key)
    c = countries.get_countries()
    
    limit = int(request.args['limit']) if 'limit' in request.args else 10
    page = int(request.args['page']) if 'page' in request.args else 0
    
    offset = page*limit
    print('page:',page,'limit',limit,'offset',offset)
    sortby = request.args['sortby'] if 'sortby' in request.args else 'name'
    order = request.args['order'] if 'order' in request.args else 'asc'

    sortby={'attr':'name', 'property':'asc'}

    return render_template('teams.html', teamtable=team.teamtable, teams=t, countries=c, total=total_teams,
            limit=limit, page=page)
