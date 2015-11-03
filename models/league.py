leaguetable = ['id', 'name', 'country']

class League:
    def __init__(self, name, country, _id=None):
        self._id = _id
        self.name = name
        self.country = country

class Leagues:
    def __init__(self, conn, cur):
        self.conn = conn
        self.cur = cur
        self.last_key = None

    def add_league(self, league):
        query = """INSERT INTO leagues (name, country) 
                                    values ('%s','%s')""" % (league.name, league.country)

        self.cur.execute(query)
        self.conn.commit()

    def delete_league(self, _id):
        query = "DELETE FROM leagues WHERE id='%s'" % _id
        self.cur.execute(query)
        self.conn.commit()

    def update_league(self, league):
        query = """UPDATE leagues SET name='%s', country='%s', 
                    WHERE id='%s'""" % (league.name, league.country, league._id)

        self.cur.execute(query)
        self.conn.commit()

    def get_leagues(self):
        query = "SELECT * FROM leagues;"
        self.cur.execute(query)
        leagues = self.cur.fetchall()
        leaguelist = []
        for l in leagues:
            ld = dict(zip(leaguetable, l))
            league = League(ld['name'], ld['country'],ld['id'])
            leaguelist.append(league)
        return leaguelist
