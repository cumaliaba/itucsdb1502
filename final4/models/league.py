leaguetable = ['id', 'name', 'country']

class League:
    def __init__(self, name, country, _id=None):
        self.name = name
        self.country = country

class Leagues:
    def __init__(self, conn, cur):
        self.conn = conn
        self.cur = cur
        self.last_key = None

    def add_league(self, league):
        query = """INSERT INTO leagues (name, country) 
                                    values (%s,%s)""" 

        self.cur.execute(query, (league.name, league.country))
        self.conn.commit()

    def delete_league(self, league):
        query = "DELETE FROM leagues WHERE name=%s and country=%s" 
        self.cur.execute(query, (league.name,league.country))
        self.conn.commit()

    def update_league(self, old, new):
        '''
        old and new are league objects
        '''
        query = """UPDATE leagues SET name=%s, country=%s, 
                    WHERE name=%s and country=%s"""
        self.cur.execute(query, (new.name, new.country, old.name, old.country))
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
