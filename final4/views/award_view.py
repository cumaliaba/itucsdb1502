from flask import render_template

from final4.config import app
from final4.db_helper import getDb
from final4.models import award


# award views
@app.route('/awards')
def award_page():
    conn, cur = getDb()
    
    awards = award.Awards(conn, cur)
    awardlist = awards.get_awards()
    return render_template('awards.html', awardtable=award.awardtable, awards=awardlist)


