leaguetable = ['id', 'name', 'country_id', 'country']

class League:
    def __init__(self, name, country_id, country=None, _id=None):
        self._id = _id
        self.name = name
        self.country_id = country_id
        self.country = country

    def getAttrs(self):
        return (dict(zip(leaguetable, (self._id, self.name, self.country_id, self.country))))

class Leagues:
    def __init__(self, conn, cur):
        self.conn = conn
        self.cur = cur
        self.last_key = None

    def add_league(self, league):
        print("addleague ", league)
        query = """INSERT INTO leagues (name, country_id) 
                                    values (%s,%s)""" 

        self.cur.execute(query, (league.name, league.country_id))
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
        print('update_league')
        query = """UPDATE leagues SET name=%s, country_id=%s
                    WHERE id=%s"""
        self.cur.execute(query, (new.name, new.country_id, _id))
        self.conn.commit()

    def get_league(self,_id):
        query = """SELECT leagues.id, leagues.name, countries.id, countries.name
                        FROM leagues,countries
                        WHERE leagues.id=%s AND countries.id=leagues.country_id
                        ORDER BY leagues.name
                        """
        self.cur.execute(query, (_id,))
        l = self.cur.fetchone()
        if l:
            ld = dict(zip(leaguetable, l[:len(leaguetable)]))
            league = League(ld['name'], ld['country_id'], ld['country'], ld['id'])
            return league
        else:
            return None

    def get_leagues(self):
        query = """SELECT leagues.id, leagues.name, countries.id, countries.name 
                        FROM leagues,countries WHERE countries.id=leagues.country_id
                          ORDER BY leagues.name"""
        self.cur.execute(query)
        leagues = self.cur.fetchall()
        leaguelist = []
        for l in leagues:
            ld = dict(zip(leaguetable, l))
            league = League(ld['name'], ld['country_id'], ld['country'],ld['id'])
            leaguelist.append(league)
        return leaguelist

    def get_leagues_by(self, key, var):
        skey = str(key) + '%'
        query = """SELECT leagues.id, leagues.name, leagues.country_id, countries.name
                        FROM leagues,countries WHERE leagues.name LIKE %s AND 
                            countries.id=leagues.country_id ORDER BY leagues.name"""
        self.cur.execute(query, (skey,))
        leagues = self.cur.fetchall()
        print('leagues:', leagues)
        leaguelist = []
        for l in leagues:
            ld = dict(zip(leaguetable, l))
            league = League(ld['name'], ld['country_id'], ld['country'],ld['id'])
            leaguelist.append(league)
        return leaguelist

