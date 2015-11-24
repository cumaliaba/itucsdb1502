from flask import render_template

from final4.config import app
from final4.db_helper import getDb
from final4.models import player

# player views
@app.route('/players')
def player_page():
    conn, cur = getDb()
    
    players = player.Players(conn, cur)
    playerlist = players.get_players()
    return render_template('players.html', playertable=player.playertable, players=playerlist)


