import sys
import json

from final4.config import app
from final4.db_helper import getDb
from final4.models import country
from final4.models import league
from final4.models import coach

from flask import render_template
from flask import request
from flask import session

# country views

@app.route('/countries', methods=['GET'])
def countries_home():
    ''' Routing function for countries-home page. 
    
    This view page lists all countries in countries table.
    This page doesn't allow editing.
    '''

    conn, cur = getDb()
    countries = country.Countries(conn, cur)
    print('countries PAGE for normal user')
        
    # limit, page and order args
    # required for each table page if pagination used !
    limit = int(request.args['limit']) if 'limit' in request.args else 10
    page = int(request.args['page']) if 'page' in request.args else 0
    offset = page*limit
    sortby = request.args['sortby'] if 'sortby' in request.args else 'name'
    order = request.args['order'] if 'order' in request.args else 'asc'
        
    # check search value
    if 'name' in request.args:
        search_name = request.args['name']
        c, total = countries.get_countries_by('name', search_name, limit=limit, offset=offset)
    else:
        c, total = countries.get_countries(limit=limit, offset=offset)
    
    return render_template('countries_home.html', countrytable=country.countrytable,
            countries=c, total=total, limit=limit, page=page, sortby=sortby)


@app.route('/countries/table', methods=['DEL','GET', 'POST'])
def country_page():
    '''Routing function for country-table page. 

    This page has session control. see *session controlled pages*

    This page lists countries and allows adding, deleting, and updating on them.
    '''
    if 'username' not in session:
        return render_template('error.html', err_code=401)
    
    conn, cur = getDb()
    countries = country.Countries(conn, cur)
    print('countries PAGE for admin')
    if request.method == 'GET':
        # handle GET request

        # limit, page and order args
        # required for each table page if pagination used !
        limit = int(request.args['limit']) if 'limit' in request.args else 10
        page = int(request.args['page']) if 'page' in request.args else 0
        offset = page*limit
        sortby = request.args['sortby'] if 'sortby' in request.args else 'name'
        order = request.args['order'] if 'order' in request.args else 'asc'

        c, total = countries.get_countries(limit, offset)
        return render_template('countries.html', countrytable=country.countrytable,
            countries=c, total=total, limit=limit, page=page, sortby=sortby)

    elif request.method == 'POST':
        # handle POST request
        name = request.form['name']
        code = request.form['code']
        
        limit = int(request.form['limit']) if 'limit' in request.form else 10
        page = int(request.form['page']) if 'page' in request.form else 0
        offset = page*limit
        sortby = request.form['sortby'] if 'sortby' in request.form else 'name'
        order = request.form['order'] if 'order' in request.form else 'asc'
        
        ct = country.Country(name, code)
        countries.add_country(ct)
        
        c, total = countries.get_countries(limit, offset)
        return render_template('countries.html', countrytable=country.countrytable,
            countries=c, total=total, limit=limit, page=page, sortby=sortby)

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
    '''Routing function for getting country from its id.
    
    *GET request* returns JSON object.

    *POST request* updates country which has id equal to the *cid* with the 
    values recieved from the request.form. After all it renders countries.html

    :param cid: id of the country, int
    '''
    if 'username' not in session:
        return render_template('error.html', err_code=401)
    
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
        
        # get new country args
        lid = request.form['id']
        name = request.form['name']
        code = request.form['code']
        ct = country.Country(name, code) # create country object with new values
        countries.update_country(cid, ct) # update selected country
       
        # get pagination args
        limit = int(request.form['limit']) if 'limit' in request.form else 10
        page = int(request.form['page']) if 'page' in request.form else 0
        offset = page*limit
        sortby = request.form['sortby'] if 'sortby' in request.form else 'name'
        order = request.form['order'] if 'order' in request.form else 'asc'

        c, total = countries.get_countries(limit, offset)
        return render_template('countries.html', countrytable=country.countrytable,
            countries=c, total=total, limit=limit, page=page, sortby=sortby)

@app.route('/countries/s/<key>', methods=['GET','POST'])
def search_country(key):
    '''Routing function for search country by its name.

    *GET request* renders the countries.html with leagues comes from the search result.
    '''
    if 'username' not in session:
        return render_template('error.html', err_code=401)
    
    conn, cur = getDb()
    countries = country.Countries(conn, cur)

    # get pagination args
    limit = int(request.form['limit']) if 'limit' in request.form else 10
    page = int(request.form['page']) if 'page' in request.form else 0
    offset = page*limit
    sortby = request.form['sortby'] if 'sortby' in request.form else 'name'
    order = request.form['order'] if 'order' in request.form else 'asc'

    result = countries.get_countries_by(key, 'name', limit, offset)
    return render_template('countries.html', countrytable=country.countrytable,
        countries=c, total=total, limit=limit, page=page, sortby=sortby)

@app.route('/countries/country/<country_name>')
def view_country(country_name):
    '''Routing function for country info page.

    This view renders the country_page.html with the general information and 
    related table statistics for given country.

    :param country_name: name of the country, string
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
