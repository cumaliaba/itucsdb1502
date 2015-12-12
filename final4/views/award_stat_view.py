import sys
import json

from final4.config import app
from final4.db_helper import getDb
from final4.models import award_stat
from final4.models import award
from final4.models import player
from final4.models import season

from flask import render_template
from flask import request

# award views
@app.route('/award_stats', methods=['DEL','GET', 'POST'])
def award_stat_page():
    conn, cur = getDb()
    award_stats = award_stat.AwardStats(conn, cur)
    awards = award.Awards(conn, cur)
    players = player.Players(conn, cur)
    seasons = season.Seasons(conn, cur)
    print('AWARD STATS PAGE')
    if request.method == 'GET':
        # handle GET request
        print ('GET REQUEST', request.args)
        limit = int(request.args['limit']) if 'limit' in request.args else 10
        page = int(request.args['page']) if 'page' in request.args else 0
        
        offset = page*limit
        print('page:',page,'limit',limit,'offset',offset)
        sortby = request.args['sortby'] if 'sortby' in request.args else 'name'
        order = request.args['order'] if 'order' in request.args else 'asc'
 
        award_stat_list, total = award_stats.get_award_stats(limit, offset)
        print(award_stat_list[0].getAttrs())
        award_list, ta = awards.get_awards(limit, offset)
        player_list,tp = players.get_players(100,0) # get list object
        season_list = seasons.get_seasons() # get list object
        sortby={'attr':'name', 'property':'asc'}
        return render_template('award_stats.html', award_stattable=award_stat.award_stattable, 
			award_stats=award_stat_list, awards=award_list, seasons=season_list, players=player_list, 
			total=total, limit=limit, page=page, sortby=sortby)
    elif request.method == 'POST':
        # handle POST request
        print('ADD award')
        award_id = request.form['award_name']
        player_id = request.form['player_name']
        season_id = request.form['season_year']
        limit = int(request.form['limit']) if 'limit' in request.form else 10
        page = int(request.form['page']) if 'page' in request.form else 0
        offset = page*limit
        order = request.form['sortby'] if 'sortby' in request.form else 'name'
        order = request.form['order'] if 'order' in request.form else 'asc'
        
        award_stat_obj = award_stat.AwardStat(award_id, player_id, season_id)
        award_stats.add_award_stat(award_stat_obj)
        
        award_stat_list, total = award_stats.get_award_stats(limit, offset)
        award_list, ta = awards.get_awards(limit, offset)
        player_list,tp = players.get_players(100,0) # get list object
        season_list = seasons.get_seasons() # get list object
        sortby={'attr':'name', 'property':'asc'}
        return render_template('award_stats.html', award_stattable=award_stat.award_stattable, 
			award_stats=award_stat_list, awards=award_list, seasons=season_list, players=player_list, 
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
            award_stats.delete_award_stat(_id) # delete object
        return json.dumps({'status':'OK', 'idlist':idlist})

@app.route('/award_stats/g/<award_stat_id>', methods=['GET','POST'])
def award_stat_from_id(award_stat_id):
    conn, cur = getDb()
    award_stats = award_stat.AwardStats(conn, cur)
    awards = award.Awards(conn, cur)
    players = player.Players(conn, cur)
    seasons = season.Seasons(conn, cur)
    
    if request.method == 'GET':
        # handle GET request
        award_stat_obj= award_stats.get_award_stat(award_stat_id)
        if award_stat_obj:
            return json.dumps({'status':'OK', 'award_stat':award_stat_obj.getAttrs()})
        else:
            return json.dumps({'status':'FAILED'})
    elif request.method == 'POST':
        # handle POST request
        print("POST METHOD REQUEST")
        award_stat_id = request.form['id']
        award_id = request.form['award_name']
        player_id = request.form['player_name']
        season_id = request.form['season_year']
        # limit: number of result showing each page
        # offset: selectedpage x limit
        limit = int(request.form['limit']) if 'limit' in request.form else 10
        page = int(request.form['page']) if 'page' in request.form else 0
        offset = page*limit
        order = request.form['sortby'] if 'sortby' in request.form else 'name'
        order = request.form['order'] if 'order' in request.form else 'asc'
        award_stat_obj = award_stat.AwardStat(award_id, player_id, season_id)
        award_stats.update_award_stat(award_stat_id, award_stat_obj)
        
        award_stat_list, total = award_stats.get_award_stats(limit, offset)
        award_list, ta = awards.get_awards(limit, offset)
        player_list,tp = players.get_players(100,0) # get list object
        season_list = seasons.get_seasons() # get list object
        sortby={'attr':'name', 'property':'asc'}
        return render_template('award_stats.html', award_stattable=award_stat.award_stattable, 
			award_stats=award_stat_list, awards=award_list, seasons=season_list, players=player_list, 
			total=total, limit=limit, page=page, sortby=sortby)
        

@app.route('/award_stats/s/<key>', methods=['GET','POST'])
def search_award_stat(key):
    conn, cur = getDb()
    award_stats = award_stat.AwardStats(conn, cur)
    awards = award.Awards(conn, cur)
    players = player.Players(conn, cur)
    seasons = season.Seasons(conn, cur)

    limit = int(request.args['limit']) if 'limit' in request.args else 10
    page = int(request.args['page']) if 'page' in request.args else 0

    sortby = request.args['sortby'] if 'sortby' in request.args else 'name'
    order = request.args['order'] if 'order' in request.args else 'asc'
    
    offset = page*limit
    
    award_stat_list, total = award_stats.get_award_stats(limit, offset)
    award_list, ta = awards.get_awards(limit, offset)
    player_list,tp = players.get_players(100,0) # get list object
    season_list = seasons.get_seasons() # get list object
    sortby={'attr':'name', 'property':'asc'}
    return render_template('award_stats.html', award_stattable=award_stat.award_stattable, 
                    award_stats=award_stat_list, awards=award_list, seasons=season_list, players=player_list, 
                    total=total, limit=limit, page=page, sortby=sortby)

@app.route('/award_stats/award_stat/<award_stat_id>')
def view_award_stat(award_stat_id):
    conn, cur = getDb()

    award_stats = award_stat.AwardStats(conn, cur)
    #awards = award.Awards(conn, cur)
    #players = player.Players(conn, cur)
    #seasons = season.Seasons(conn, cur)

    l = award_stats.get_award_stat(award_stat_id)
    if l is None:
        # return not found error 
        return render_template('error.html', err_code=404)

    # else render country page with required args

    return render_template('award_stat_page.html', award=l)
