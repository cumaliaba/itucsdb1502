import sys
import json

from final4.config import app
from final4.db_helper import getDb
from final4.models import league

from flask import render_template
from flask import request

# league views
@app.route('/leagues', methods=['DEL','GET', 'POST', 'PUT'])
def league_page():
    conn, cur = getDb()
    leagues = league.Leagues(conn, cur)
    print('LEAGUES PAGE')
    if request.method == 'GET':
        l = leagues.get_leagues()
        return render_template('leagues.html', leaguetable=league.leaguetable, leagues=l)
    elif request.method == 'POST':
        name = request.form['name']
        country = request.form['country']
        lg = league.League(name, country)
        leagues.add_league(lg)
        
        l = leagues.get_leagues()
        return render_template('leagues.html', leaguetable=league.leaguetable, leagues=l)

    elif request.method == 'DEL':
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
        #return render_template('leagues.html', leaguetable=league.leaguetable, leagues=l)




@app.route('/leagues/<lid>', methods=['GET','POST'])
def league_from_id(lid):
    conn, cur = getDb()
    leagues = league.Leagues(conn, cur)
    
    if request.method == 'GET':
        l = leagues.get_league(lid)
        if l:
            return json.dumps({'status':'OK', 'league':l.getAttrs()})
        else:
            return json.dumps({'status':'FAILED'})
    elif request.method == 'POST':
        print("PUT METHOD REQUEST")
        lid = request.form['id']
        name = request.form['name']
        country = request.form['country']
        print(lid, name, country)
        lg = league.League(name, country)
        leagues.update_league(lid, lg)

        l = leagues.get_leagues()
        return render_template('leagues.html', leaguetable=league.leaguetable, leagues=l)


