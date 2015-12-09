awardtable = ['id', 'name', 'player_id', 'player_name', 'player_surname', 'season_id', 'season_year']

class Award:
    def __init__(self, name, player_id, season_id, player_name=None, player_surname=None, season_year=None, _id=None):
        self._id = _id
        self.name = name
        self.player_id = player_id
        self.player_name = player_name
        self.player_surname = player_surname
        self.season_id = season_id
        self.season_year = season_year

    def getAttrs(self):
        return (dict(zip(awardtable, (self._id, self.name, self.player_id, 
            self.player_name, self.player_surname, self.season_id, self.season_year))))

        
class Awards:
    def __init__(self, conn, cur):
        self.conn = conn
        self.cur = cur
        self.last_key = None

    def add_award(self, award):
        query = """INSERT INTO awards (name, player_id, season_id) 
                                    values (%s,%s,%s)"""

        self.cur.execute(query, (award.name, award.player_id, award.season_id))
        self.conn.commit()

    def delete_award(self, _id):
        query = "DELETE FROM awards WHERE id=%s"
        self.cur.execute(query, (_id,))
        self.conn.commit()

    def update_award(self, _id, new):
        '''
        new : Award object
        '''
        query = """UPDATE awards SET name=%s, 
                    player_id=%s, season_id=%s WHERE id=%s"""

        self.cur.execute(query, (new.name, new.player_id, new.season_id, _id))
        self.conn.commit()

        
    def get_award(self,_id):
        query = """SELECT awards.id, awards.name, players.id, players.name, players.surname, seasons.id, seasons.year 
                        FROM awards, players, seasons
                        WHERE awards.id=%s AND players.id=awards.player_id AND seasons.id=awards.season_id
                        """
        self.cur.execute(query, (_id,))
        l = self.cur.fetchone()
        if l:
            ld = dict(zip(awardtable, l[:len(awardtable)]))
            award = Award(ld['name'], ld['player_id'], ld['season_id'],
			    _id=ld['id'], player_name=ld['player_name'],
			    player_surname=ld['player_surname'], season_year=ld['season_year'])
            return award
        else:
            return None

    def get_awards(self, limit=100, offset=0):

        query = """SELECT count(awards.id)
                        FROM awards, players, seasons WHERE awards.player_id=players.id
			AND awards.season_id=seasons.id
                          """
        self.cur.execute(query)
        total = self.cur.fetchone()[0]

        query = """SELECT awards.id, awards.name, players.id, players.name, players.surname, seasons.id, seasons.year 
                        FROM awards, players, seasons
                        WHERE players.id=awards.player_id AND seasons.id=awards.season_id
			ORDER BY awards.name ASC LIMIT %s OFFSET %s
                        """

        self.cur.execute(query, (limit, offset))
        awards = self.cur.fetchall()
        awardlist = []
        for l in awards:
            ld = dict(zip(awardtable, l))
            award = Award(ld['name'], ld['player_id'], ld['season_id'],
			    _id=ld['id'], player_name=ld['player_name'],
			    player_surname=ld['player_surname'], season_year=ld['season_year'])
            awardlist.append(award)
        return awardlist, total

    def get_awards_by(self, attrib, search_key, limit=100, offset=0):
        skey = str(search_key)

        # WARNING !!! SQL INJECTION?
        query = """SELECT count(awards.id)
                        FROM awards, players, seasons WHERE awards.{attrib}=%s AND awards.player_id=players.id
			AND awards.season_id=seasons.id
                          """.format(attrib=attrib)
        self.cur.execute(query, (skey,))
        total = self.cur.fetchone()[0]

        # WARNING !!! SQL INJECTION?
        query = """SELECT awards.id, awards.name, players.id, players.name, players.surname, seasons.id, seasons.year 
                        FROM awards, players, seasons
                        WHERE awards.{attrib}=%s AND players.id=awards.player_id AND seasons.id=awards.season_id
			ORDER BY awards.name ASC LIMIT %s OFFSET %s
                        """.format(attrib=attrib)
        self.cur.execute(query, (skey,limit, offset))
        awards = self.cur.fetchall()
        print('awards:', awards)
        awardlist = []
        for l in awards:
            ld = dict(zip(awardtable, a))
            award = Award(ld['name'], ld['player_id'], ld['season_id'],
			    _id=ld['id'], player_name=ld['player_name'],
			    player_surname=ld['player_surname'], season_year=ld['season_year'])
            awardlist.append(award)
        return awardlist, total

    def get_awards_search_by(self, attrib, search_key, limit=100, offset=0):
        # convert search key to special sql search syntax that means
        # all matches that starts with search_key
        skey = str(search_key) + '%'
        print('CCCCCCCCCCCC', skey)
        # WARNING !!! SQL INJECTION?
        query = """SELECT count(awards.id)
                        FROM awards, players, seasons WHERE awards.{attrib} LIKE %s AND awards.player_id=players.id
			AND awards.season_id=seasons.id
                          """.format(attrib=attrib)
        self.cur.execute(query, (skey,))
        total = self.cur.fetchone()[0]

        # WARNING !!! SQL INJECTION?
        query = """SELECT awards.id, awards.name, players.id, players.name, players.surname, seasons.id, seasons.year 
                        FROM awards, players, seasons
                        WHERE awards.{attrib} LIKE %s AND players.id=awards.player_id AND seasons.id=awards.season_id
			ORDER BY awards.name ASC LIMIT %s OFFSET %s
                        """.format(attrib=attrib)
        self.cur.execute(query, (skey,limit, offset))
        awards = self.cur.fetchall()
        print('awards:', awards)
        awardlist = []
        for l in awards:
            ld = dict(zip(awardtable, l))
            award = Award(ld['name'], ld['player_id'], ld['season_id'],
			    _id=ld['id'], player_name=ld['player_name'],
			    player_surname=ld['player_surname'], season_year=ld['season_year'])
            awardlist.append(award)
        return awardlist, total

