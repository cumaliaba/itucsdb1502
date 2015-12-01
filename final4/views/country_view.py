import sys
import json

from final4.config import app
from final4.db_helper import getDb
from final4.models import country

from flask import render_template
from flask import request

# country views
@app.route('/countries', methods=['DEL','GET', 'POST'])
def country_page():
    conn, cur = getDb()
    countries = country.Countries(conn, cur)
    print('countries PAGE')
    if request.method == 'GET':
        c = countries.get_countries()
        return render_template('countries.html', countrytable=country.countrytable, countries=c)
    elif request.method == 'POST':
        name = request.form['name']
        code = request.form['code']
        ct = country.Country(name, code)
        countries.add_country(ct)
        
        c = countries.get_countries()
        return render_template('countries.html', countrytable=country.countrytable, countries=c)

    elif request.method == 'DEL':
        print ('DELETE REQUEST:countries PAGE')
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
            countries.delete_country(_id)
        return json.dumps({'status':'OK', 'idlist':idlist})

@app.route('/countries/g/<cid>', methods=['GET','POST'])
def country_from_id(cid):
    conn, cur = getDb()
    countries = country.Countries(conn, cur)
    
    if request.method == 'GET':
        c = countries.get_country(cid)
        if c:
            return json.dumps({'status':'OK', 'country':c.getAttrs()})
        else:
            return json.dumps({'status':'FAILED'})
    elif request.method == 'POST':
        print("PUT METHOD REQUEST")
        lid = request.form['id']
        name = request.form['name']
        code = request.form['code']
        ct = country.Country(name, code)
        countries.update_country(cid, ct)

        c = countries.get_countries()
        return render_template('countries.html', countrytable=country.countrytable, countries=c)


@app.route('/countries/s/<key>', methods=['GET','POST'])
def search_country(key):
    conn, cur = getDb()
    countries = country.Countries(conn, cur)
    result = countries.get_countries_by(key, 'name')
    return render_template('countries.html', countrytable=country.countrytable, countries=result)
