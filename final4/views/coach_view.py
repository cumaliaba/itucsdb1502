import sys
import json

from final4.config import app
from final4.db_helper import getDb
from final4.models import coach
from final4.models import country

from flask import render_template
from flask import request

# coach views
@app.route('/coaches', methods=['DEL','GET', 'POST'])
def coach_page():
    conn, cur = getDb()
    coaches = coach.Coaches(conn, cur)
    countries = country.Countries(conn, cur)
    print('coaches PAGE')
    if request.method == 'GET':
        l = coaches.get_coaches()
        c = countries.get_countries()
        return render_template('coaches.html', coachtable=coach.coachtable, coaches=l, countries=c)
    elif request.method == 'POST':
        print('ADD coach')
        name = request.form['name']
        surname = request.form['surname']
        country_id = request.form['country']
        lg = coach.Coach(name, surname, country_id)
        coaches.add_coach(lg)
        
        l = coaches.get_coaches()
        c = countries.get_countries()
        return render_template('coaches.html', coachtable=coach.coachtable, coaches=l, countries=c)

    elif request.method == 'DEL':
        print ('DELETE REQUEST:coaches PAGE')
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
            coaches.delete_coach(_id)
        return json.dumps({'status':'OK', 'idlist':idlist})

@app.route('/coaches/g/<lid>', methods=['GET','POST'])
def coach_from_id(lid):
    conn, cur = getDb()
    coaches = coach.Coaches(conn, cur)
    countries = country.Countries(conn, cur)
    
    if request.method == 'GET':
        l= coaches.get_coach(lid)
        if l:
            return json.dumps({'status':'OK', 'coach':l.getAttrs()})
        else:
            return json.dumps({'status':'FAILED'})
    elif request.method == 'POST':
        print("POST METHOD REQUEST")
        lid = request.form['id']
        name = request.form['name']
        surname = request.form['surname']
        country_id = request.form['country']
        lg = coach.Coach(name, surname, country_id)
        coaches.update_coach(lid, lg)

        l = coaches.get_coaches()
        c = countries.get_countries()
        return render_template('coaches.html', coachtable=coach.coachtable, coaches=l, countries=c)


@app.route('/coaches/s/<key>', methods=['GET','POST'])
def search_coach(key):
    conn, cur = getDb()
    coaches = coach.Coaches(conn, cur)
    countries = country.Countries(conn, cur)

    result = coaches.get_coaches_by(key, 'name')
    c = countries.get_countries()
    return render_template('coaches.html', coachtable=coach.coachtable, coaches=result, countries=c)
