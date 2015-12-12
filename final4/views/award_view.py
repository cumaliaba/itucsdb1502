import sys
import json

from final4.config import app
from final4.db_helper import getDb
from final4.models import award

from flask import render_template
from flask import request

# award views
@app.route('/awards', methods=['DEL','GET', 'POST'])
def award_page():
    conn, cur = getDb()
    awards = award.Awards(conn, cur)
    print('AWARDS PAGE')
    if request.method == 'GET':
        # handle GET request
        print ('GET REQUEST', request.args)
        limit = int(request.args['limit']) if 'limit' in request.args else 10
        page = int(request.args['page']) if 'page' in request.args else 0
        
        offset = page*limit
        print('page:',page,'limit',limit,'offset',offset)
        sortby = request.args['sortby'] if 'sortby' in request.args else 'name'
        order = request.args['order'] if 'order' in request.args else 'asc'
 
        award_list, total = awards.get_awards(limit, offset)
        sortby={'attr':'name', 'property':'asc'}
        return render_template('awards.html', awardtable=award.awardtable, 
                        awards=award_list,
			total=total, limit=limit, page=page, sortby=sortby)
    elif request.method == 'POST':
        # handle POST request
        print('ADD award')
        name = request.form['name']
        limit = int(request.form['limit']) if 'limit' in request.form else 10
        page = int(request.form['page']) if 'page' in request.form else 0
        offset = page*limit
        order = request.form['sortby'] if 'sortby' in request.form else 'name'
        order = request.form['order'] if 'order' in request.form else 'asc'
        award_obj = award.Award(name)
        awards.add_award(award_obj)
        
        award_list, total = awards.get_awards(limit, offset)
        sortby={'attr':'name', 'property':'asc'}
        return render_template('awards.html', awardtable=award.awardtable, 
                        awards=award_list,
			total=total, limit=limit, page=page, sortby=sortby)

    elif request.method == 'DEL':
        # handle DEL request
        print ('DELETE REQUEST:AWARDS PAGE')
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
            awards.delete_award(_id) # delete object
        return json.dumps({'status':'OK', 'idlist':idlist})

@app.route('/awards/g/<award_id>', methods=['GET','POST'])
def award_from_id(award_id):
    conn, cur = getDb()
    awards = award.Awards(conn, cur)
    
    if request.method == 'GET':
        # handle GET request
        award_obj= awards.get_award(award_id)
        if award_obj:
            return json.dumps({'status':'OK', 'award':award_obj.getAttrs()})
        else:
            return json.dumps({'status':'FAILED'})
    elif request.method == 'POST':
        # handle POST request
        print("POST METHOD REQUEST")
        award_id = request.form['id']
        name = request.form['name']
        # limit: number of result showing each page
        # offset: selectedpage x limit
        limit = int(request.form['limit']) if 'limit' in request.form else 10
        page = int(request.form['page']) if 'page' in request.form else 0
        offset = page*limit
        order = request.form['sortby'] if 'sortby' in request.form else 'name'
        order = request.form['order'] if 'order' in request.form else 'asc'
        award_obj = award.Award(name)
        awards.update_award(award_id, award_obj)
        
        award_list, total = awards.get_awards(limit, offset)
        sortby={'attr':'name', 'property':'asc'}
        return render_template('awards.html', awardtable=award.awardtable, 
			awards=award_list, 
			total=total, limit=limit, page=page, sortby=sortby)


@app.route('/awards/s/<key>', methods=['GET','POST'])
def search_award(key):
    conn, cur = getDb()
    awards = award.Awards(conn, cur)

    limit = int(request.args['limit']) if 'limit' in request.args else 10
    page = int(request.args['page']) if 'page' in request.args else 0

    sortby = request.args['sortby'] if 'sortby' in request.args else 'name'
    order = request.args['order'] if 'order' in request.args else 'asc'
    
    offset = page*limit

    award_list, total = awards.get_awards_search_by('name', key,  limit, offset)
    sortby={'attr':'name', 'property':'asc'}
    return render_template('awards.html', awardtable=award.awardtable, 
		awards=award_list,
		total=total, limit=limit, page=page, sortby=sortby)

@app.route('/awards/award/<award_id>')
def view_award(award_id):
    conn, cur = getDb()

    awards = award.Awards(conn, cur)

    l = awards.get_award(award_id)
    if l is None:
        # return not found error 
        return render_template('error.html', err_code=404)

    # else render country page with required args

    return render_template('award_page.html', award=l)
