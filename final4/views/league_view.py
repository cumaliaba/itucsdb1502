from final4.config import app
from final4.db_helper import getDb
from final4.models import league

from flask import render_template

# league views
@app.route('/leagues')
def league_page():
    conn, cur = getDb()
    
    leagues = league.Leagues(conn, cur)
    l = leagues.get_leagues()
    return render_template('leagues.html', leaguetable=league.leaguetable, leagues=l)
