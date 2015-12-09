import sys
import json

from final4.config import app
from final4.db_helper import getDb
from final4.models import country
from final4.models import league
from final4.models import coach

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

@app.route('/countries/country/<country_name>')
def view_country(country_name):
    '''
    country_arg (string): <country_name>

    This view presents the general information and 
    related table statistics for given country.
    '''
    conn, cur = getDb()
    countries = country.Countries(conn, cur)

    c = countries.get_country_name(country_name)
    if c is None:
        # return not found error 
        return render_template('error.html', err_code=404)

    # else render country page with required args
    leagues = league.Leagues(conn, cur)

    league_list, total = leagues.get_leagues_by('country_id', c._id)
    league_dict = {'leagues':league_list,
                    'total': total
                    }

    coaches = coach.Coaches(conn, cur)
    coach_list, total = coaches.get_coaches_by('country_id', c._id)
    coaches_dict = {'coaches':coach_list,
                    'total': total
                    }

    return render_template('country_page.html', country=c, 
            league_dict=league_dict, player_dict=None, coach_dict=coaches_dict)
