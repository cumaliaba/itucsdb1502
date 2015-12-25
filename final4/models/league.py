#: corresponding key values of the League class attributes
leaguetable = ['id', 'name', 'country_id', 'country']

class League:
    '''League object'''
    def __init__(self, name, country_id, country=None, _id=None):
        self._id = _id
        self.name = name
        self.country_id = country_id
        self.country = country

    def getAttrs(self):
        '''returns attributes of the League class as a dictionary. Keys are 
        taken from the leaguetable and corresponding values are taken from 
        the League object attributes.
        
        :returns: attributes of the League object as a dictionary.
        :rtype: dict'''
        return (dict(zip(leaguetable, (self._id, self.name, self.country_id, self.country))))

class Leagues:
    '''the Leagues object provides functions for database connections of leagues table.
    
    :param conn: psycopg2 connection object
    :param cur: psycopg2 cursor object
    '''
    def __init__(self, conn, cur):
        self.conn = conn
        self.cur = cur
        self.last_key = None

    def add_league(self, league):
        '''inserts a new row to the leagues table with values of the given league attributes.
        
        :param league: new League object
        '''
        print("addleague ", league)
        query = """INSERT INTO leagues (name, country_id) 
                                    values (%s,%s)""" 

        self.cur.execute(query, (league.name, league.country_id))
        self.conn.commit()

    def delete_league(self, _id):
        '''deletes the row from the leagues table whose id is given _id.

        :param _id: id of the row - int
        '''
        query = """DELETE FROM leagues WHERE id=%s"""
        # variables should be in tuple object
        self.cur.execute(query, (_id,))
        self.conn.commit()

    def update_league(self, _id, new):
        '''Updates the row from the leagues table whose id is given _id. 
        The new values is taken from given *new* League object.

        :param _id: id of the row - int
        :param new: League object with new values
        '''
        print('update_league')
        query = """UPDATE leagues SET name=%s, country_id=%s
                    WHERE id=%s"""
        self.cur.execute(query, (new.name, new.country_id, _id))
        self.conn.commit()

    def get_league(self,_id):
        '''Returns :class:`final4.models.league.League` object with values from
        the leagues table IF there is a record has a given _id ELSE returns None.

        :param _id: id of the row - int
        :returns: league or None
        :rtype: :class:`final4.models.league.League` object or None
        '''
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

    def get_leagues(self, limit=100, offset=0):
        '''Returns result list and total number of results.
        Returning list is list of :class:`final4.models.league.League` object. All objects
        filled up with values from the rows of the leagues table.
        Also returns the total number of the result.
        
        :param limit: maximum number of the result
        :param offset: skip beginning of the result
        :returns: leaguelist, total
        :rtype: list, int
        '''

        query = """SELECT count(leagues.id)
                        FROM leagues,countries WHERE countries.id=leagues.country_id
                          """
        self.cur.execute(query)
        total = self.cur.fetchone()[0]

        query = """SELECT leagues.id, leagues.name, countries.id, countries.name 
                        FROM leagues,countries WHERE countries.id=leagues.country_id
                          ORDER BY leagues.name ASC LIMIT %s OFFSET %s"""
        self.cur.execute(query, (limit, offset))
        leagues = self.cur.fetchall()
        leaguelist = []
        for l in leagues:
            ld = dict(zip(leaguetable, l))
            league = League(ld['name'], ld['country_id'], ld['country'],ld['id'])
            leaguelist.append(league)
        return leaguelist, total

    def get_leagues_by(self, attrib, search_key, limit=100, offset=0):
        '''Returns result list and total number of result.
        Returning list is list of  :class:`final4.models.league.League` object. All objects
        filled up with values from the rows of the leagues table. 
        
        The return list made up by **filtered results** with given parameters.
       
        :param limit: maximum number of the result
        :param offset: skip beginning of the result
        
        :returns: leaguelist, total
        :rtype: list, int
        '''
        skey = str(search_key)

        # WARNING !!! SQL INJECTION?
        query = """SELECT count(leagues.id)
                        FROM leagues,countries WHERE leagues.{attrib}=%s AND 
                            countries.id=leagues.country_id""".format(attrib=attrib)
        self.cur.execute(query, (skey,))
        total = self.cur.fetchone()[0]

        # WARNING !!! SQL INJECTION?
        query = """SELECT leagues.id, leagues.name, leagues.country_id, countries.name
                        FROM leagues,countries WHERE leagues.{attrib}=%s AND 
                            countries.id=leagues.country_id ORDER BY leagues.name
                            LIMIT %s OFFSET %s""".format(attrib=attrib)
        self.cur.execute(query, (skey,limit, offset))
        leagues = self.cur.fetchall()
        print('leagues:', leagues)
        leaguelist = []
        for l in leagues:
            ld = dict(zip(leaguetable, l))
            league = League(ld['name'], ld['country_id'], ld['country'],ld['id'])
            leaguelist.append(league)
        return leaguelist, total

    def get_leagues_search_by(self, attrib, search_key, limit=100, offset=0):
        '''Returns result list and total number of result.
        Returning list is list of  :class:`final4.models.league.League` object. All objects
        filled up with values from the rows of the leagues table. 
        
        The return list made up by **filtered results** with given parameters.
       
        :param limit: maximum number of the result
        :param offset: skip beginning of the result
        
        :returns: leaguelist, total
        :rtype: list, int
        '''
        # convert search key to special sql search syntax that means
        # all matches that starts with search_key
        skey = str(search_key) + '%'

        # WARNING !!! SQL INJECTION?
        query = """SELECT count(leagues.id)
                        FROM leagues,countries WHERE leagues.{attrib} LIKE %s AND 
                            countries.id=leagues.country_id""".format(attrib=attrib)
        self.cur.execute(query, (skey,))
        total = self.cur.fetchone()[0]

        # WARNING !!! SQL INJECTION?
        query = """SELECT leagues.id, leagues.name, leagues.country_id, countries.name
                        FROM leagues,countries WHERE leagues.{attrib} LIKE %s AND 
                            countries.id=leagues.country_id ORDER BY leagues.name
                            LIMIT %s OFFSET %s""".format(attrib=attrib)
        self.cur.execute(query, (skey,limit, offset))
        leagues = self.cur.fetchall()
        print('leagues:', leagues)
        leaguelist = []
        for l in leagues:
            ld = dict(zip(leaguetable, l))
            league = League(ld['name'], ld['country_id'], ld['country'],ld['id'])
            leaguelist.append(league)
        return leaguelist, total

