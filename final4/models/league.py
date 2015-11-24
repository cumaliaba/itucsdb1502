leaguetable = ['id', 'name', 'country']

class League:
    def __init__(self, name, country, _id=None):
        self._id = _id
        self.name = name
        self.country = country

    def getAttrs(self):
        return (dict(zip(leaguetable, (self._id, self.name, self.country))))

class Leagues:
    def __init__(self, conn, cur):
        self.conn = conn
        self.cur = cur
        self.last_key = None

    def add_league(self, league):
        print("addleague ", league)
        query = """INSERT INTO leagues (name, country) 
                                    values (%s,%s)""" 

        self.cur.execute(query, (league.name, league.country))
        self.conn.commit()

    def delete_league(self, _id):
        query = """DELETE FROM leagues WHERE id=%s"""
        # variables should be in tuple object
        self.cur.execute(query, (_id,))
        self.conn.commit()

    def update_league(self, _id, new):
        '''
        new : league object
        '''
        query = """UPDATE leagues SET name=%s, country=%s
                    WHERE id=%s"""
        self.cur.execute(query, (new.name, new.country, _id))
        self.conn.commit()

    def get_league(self,_id):
        query = """SELECT * FROM leagues WHERE id=%s"""
        self.cur.execute(query, (_id,))
        l = self.cur.fetchone()
        if l:
            ld = dict(zip(leaguetable, l))
            league = League(ld['name'], ld['country'], ld['id'])
            return league
        else:
            return None

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
