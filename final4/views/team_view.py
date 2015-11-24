from flask import render_template

from final4.config import app
from final4.db_helper import getDb
from final4.models import team

# team views
@app.route('/teams')
def player_page():
    conn, cur = getDb()
    
    teams = teams.Teams(conn, cur)
    teamlist = teams.get_players()
    return render_template('teams.html', teamtable=team.teamtable, teams=teamlist)


