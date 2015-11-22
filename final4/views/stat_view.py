from flask import render_template

from final4.config import app
from final4.db_helper import getDb

@app.route('/stats')
def stats():
    return "Stats page will be here"


