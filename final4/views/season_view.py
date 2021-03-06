import sys
import json

from final4.config import app
from final4.db_helper import getDb
from final4.models import season

from flask import render_template
from flask import request
from flask import session

# season views
@app.route('/seasons', methods=['DEL','GET', 'POST', 'PUT'])
def seasons_home():
    conn, cur = getDb()
    seasons = season.Seasons(conn, cur)
    print('SEASONS PAGE')
    if request.method == 'GET':
        if 'name' in request.args:
            search_name = request.args['name']
            l = seasons.get_seasons_by(search_name, 'name')
            #l = seasons.get_seasons_search_by('name', search_name)
        else:
            l = seasons.get_seasons()
        
        return render_template('seasons_home.html', seasontable=season.seasontable, seasons=l)
        
        
@app.route('/seasons/table', methods=['DEL','GET', 'POST', 'PUT'])
def season_page():
    if 'username' not in session:
        return render_template('error.html', err_code=401)
        
    conn, cur = getDb()
    seasons = season.Seasons(conn, cur)
    print('SEASONS PAGE')
    if request.method == 'GET':
        l = seasons.get_seasons()
        print('HEYHEY',l)
        return render_template('seasons.html', seasontable=season.seasontable, seasons=l)
    elif request.method == 'POST':
        year = request.form['year']
        
        lg = season.Season(year)
        seasons.add_season(lg)
        
        l = seasons.get_seasons()
        return render_template('seasons.html', seasontable=season.seasontable, seasons=l)

    elif request.method == 'DEL':
        print ('DELETE REQUEST:SEASONS PAGE')
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
            seasons.delete_season(_id)
        return json.dumps({'status':'OK', 'idlist':idlist})


@app.route('/seasons/g/<lid>', methods=['GET','POST'])
def season_from_id(lid):
    if 'username' not in session:
        return render_template('error.html', err_code=401)    
    
    conn, cur = getDb()
    seasons = season.Seasons(conn, cur)
    
    if request.method == 'GET':
        l = seasons.get_season(lid)
        if l:
            return json.dumps({'status':'OK', 'season':l.getAttrs()})
        else:
            return json.dumps({'status':'FAILED'})
    elif request.method == 'POST':
        print("PUT METHOD REQUEST")
        lid = request.form['id']
        year = request.form['year']
        
        lg = season.Season(year)
        seasons.update_season(lid, lg)

        l = seasons.get_seasons()
        return render_template('seasons.html', seasontable=season.seasontable, seasons=l)
        
@app.route('/seasons/s/<key>', methods=['GET','POST'])
def search_season(key):
    if 'username' not in session:
        return render_template('error.html', err_code=401)
        
    conn, cur = getDb()
    seasons = season.Seasons(conn, cur)
    result = seasons.get_seasons_by(key, 'name')
    return render_template('seasons.html', seasontable=season.seasontable, seasons=result)


