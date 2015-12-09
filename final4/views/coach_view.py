import os
import json
import sys

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
        # handle GET request
        limit = int(request.args['limit']) if 'limit' in request.args else 10
        page = int(request.args['page']) if 'page' in request.args else 0
        
        offset = page*limit
        print('page:',page,'limit',limit,'offset',offset)
        sortby = request.args['sortby'] if 'sortby' in request.args else 'name'
        order = request.args['order'] if 'order' in request.args else 'asc'

        l, total_coaches = coaches.get_coaches()
        c = countries.get_countries()

        sortby={'attr':'name', 'property':'asc'}

        return render_template('coaches.html', coachtable=coach.coachtable, coaches=l, countries=c, total=total_coaches,
                limit=limit, page=page)
    elif request.method == 'POST':
        # handle POST request
        print('ADD coach')
        name = request.form['name']
        surname = request.form['surname']
        country_id = request.form['country']
        coach_img = request.files['file']

        limit = int(request.form['limit']) if 'limit' in request.form else 10
        page = int(request.form['page']) if 'page' in request.form else 0
        offset = page*limit
        order = request.form['sortby'] if 'sortby' in request.form else 'name'
        order = request.form['order'] if 'order' in request.form else 'asc'

        print(name, surname, coach_img)
        lg = coach.Coach(name, surname, country_id)
        # add coach to table and get id
        insert_id = coaches.add_coach(lg)
        
        # save image to path
        # image path should start with appname:
        #      real_save_path = 'final4' + <save_path>
        # because app runs in the upper folder.
        if coach_img:
            # get generated image path for new coach object
            save_path = lg.img_path(insert_id)
            coach_img.save(app.config['APP_FOLDER']+save_path)
    
        l, total_coaches = coaches.get_coaches()
        c = countries.get_countries()

        sortby={'attr':'name', 'property':'asc'}

        return render_template('coaches.html', coachtable=coach.coachtable, coaches=l, countries=c, total=total_coaches,
                limit=limit, page=page)

    elif request.method == 'DEL':
        # handle DEL request
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
        # handle GET request
        # return json object
        l= coaches.get_coach(lid)
        if l:
            return json.dumps({'status':'OK', 'coach':l.getAttrs()})
        else:
            return json.dumps({'status':'FAILED'})
    elif request.method == 'POST':
        # handle POST request
        # UPDATE item
        print("POST METHOD REQUEST")
        lid = request.form['id']
        name = request.form['name']
        surname = request.form['surname']
        country_id = request.form['country']
        coach_img = request.files['file']

        limit = int(request.form['limit']) if 'limit' in request.form else 10
        page = int(request.form['page']) if 'page' in request.form else 0
        offset = page*limit
        order = request.form['sortby'] if 'sortby' in request.form else 'name'
        order = request.form['order'] if 'order' in request.form else 'asc'

        lg = coach.Coach(name, surname, country_id)
        coaches.update_coach(lid, lg)
        
        # save image to path
        # image path should start with appname:
        #      real_save_path = 'final4' + <save_path>
        # because app runs in the upper folder.
        if coach_img:
            # get generated image path for new coach object
            save_path = lg.img_path(lid)
            coach_img.save(app.config['APP_FOLDER']+save_path)

        l, total_coaches = coaches.get_coaches()
        c = countries.get_countries()

        sortby={'attr':'name', 'property':'asc'}

        return render_template('coaches.html', coachtable=coach.coachtable, coaches=l, countries=c, total=total_coaches,
                limit=limit, page=page)


@app.route('/coaches/s/<key>', methods=['GET','POST'])
def search_coach(key):
    conn, cur = getDb()
    coaches = coach.Coaches(conn, cur)
    countries = country.Countries(conn, cur)

    l, total_coaches = coaches.get_coaches_search_by('name', key)
    c = countries.get_countries()
    
    limit = int(request.args['limit']) if 'limit' in request.args else 10
    page = int(request.args['page']) if 'page' in request.args else 0
    
    offset = page*limit
    print('page:',page,'limit',limit,'offset',offset)
    sortby = request.args['sortby'] if 'sortby' in request.args else 'name'
    order = request.args['order'] if 'order' in request.args else 'asc'

    sortby={'attr':'name', 'property':'asc'}

    return render_template('coaches.html', coachtable=coach.coachtable, coaches=l, countries=c, total=total_coaches,
            limit=limit, page=page)
