matchtable = ['id', 'schedule_id', 'T1_name', 'T2_name', 'T1_3PT', 'T1_2PT', 'T1_block', 'T1_reb', 'T1_rate', 'T2_3PT', 'T2_2PT', 'T2_block', 'T2_reb', 'T2_rate']

class Match:
    '''Match object'''
    def __init__(self, schedule_id, T1_3PT, T1_2PT, T1_block, T1_reb, T1_rate, T2_3PT, T2_2PT, T2_block, T2_reb, T2_rate, T1_name=None, T2_name=None, _id=None):
        self._id = _id
        self.schedule_id = schedule_id
        self.T1_3PT = T1_3PT
        self.T1_2PT = T1_2PT
        self.T1_block = T1_block
        self.T1_reb = T1_reb
        self.T1_rate = T1_rate
        self.T2_3PT = T2_3PT
        self.T2_2PT = T2_2PT
        self.T2_block = T2_block
        self.T2_reb = T2_reb
        self.T2_rate = T2_rate
        
        self.T1_name = T1_name
        self.T2_name = T2_name

    def getAttrs(self):
        '''returns attributes of the Match class as a dictionary. Keys are 
        taken from the matchtable and corresponding values are taken from 
        the Match object attributes.
        
        :returns: attributes of the Match object as a dictionary.
        :rtype: dict'''
        return (dict(zip(matchtable, (self._id, self.schedule_id, self.T1_name, self.T2_name, self.T1_3PT, self.T1_2PT, self.T1_block, self.T1_reb, self.T1_rate, self.T2_3PT, self.T2_2PT, self.T2_block, self.T2_reb, self.T2_rate))))

class Matches:
    '''the Matches object provides functions for database connections of matches table.
    
    :param conn: psycopg2 connection object
    :param cur: psycopg2 cursor object
    '''
    def __init__(self, conn, cur):
        self.conn = conn
        self.cur = cur
        self.last_key = None
        
    def add_match(self, match):
        '''inserts a new row to the matches table with values of the given match attributes.
        
        :param match: new Match object
        '''
        query = """INSERT INTO matches (schedule_id, T1_3PT, T1_2PT, T1_block, T1_reb, T1_rate, T2_3PT, T2_2PT, T2_block, T2_reb, T2_rate) 
                                    values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

        self.cur.execute(query, (match.schedule_id, match.T1_3PT, match.T1_2PT, match.T1_block, match.T1_reb, match.T1_rate, match.T2_3PT, match.T2_2PT, match.T2_block, match.T2_reb, match.T2_rate))
        self.conn.commit()

    def delete_match(self, _id):
        '''deletes the row from the matches table whose id is given _id.

        :param _id: id of the row - int
        '''
        query = "DELETE FROM matches WHERE id=%s"
        self.cur.execute(query, (_id,))
        self.conn.commit()
        
    def update_match(self, _id, new):
        '''Updates the row from the matches table whose id is given _id. 
        The new values is taken from given *new* Match object.

        :param _id: id of the row - int
        :param new: Match object with new values
        '''
        print('update_match')
        query = """UPDATE matches SET schedule_id=%s, T1_3PT=%s, T1_2PT=%s, T1_block=%s, T1_reb=%s, T1_rate=%s, T2_3PT=%s, T2_2PT=%s, T2_block=%s, T2_reb=%s, T2_rate=%s
                    WHERE id=%s"""
        self.cur.execute(query, (new.schedule_id, new.T1_3PT, new.T1_2PT, new.T1_block, new.T1_reb, new.T1_rate, new.T2_3PT, new.T2_2PT, new.T2_block, new.T2_reb, new.T2_rate, _id))
        self.conn.commit()

    def get_match(self,_id):
        '''Returns :class:`final4.models.match.Match` object with values from
        the matches table IF there is a record has a given _id ELSE returns None.

        :param _id: id of the row - int
        :returns: match or None
        :rtype: :class:`final4.models.match.Match` object or None
        '''
        query = """SELECT matches.id,
                          schedules.id,
                          teams1.name, teams2.name,
                          T1_3PT, T1_2PT, T1_block, T1_reb, T1_rate,
                          T2_3PT, T2_2PT, T2_block, T2_reb, T2_rate
                        FROM matches, schedules
                        JOIN teams teams1 ON teams1.id=schedules.team1_id
                        JOIN teams teams2 ON teams2.id=schedules.team2_id
                        WHERE matches.id=%s AND schedules.id=matches.schedule_id"""
        self.cur.execute(query, (_id,))
        l = self.cur.fetchone()
        if l:
            ld = dict(zip(matchtable, l[:len(matchtable)]))
            match = Match(ld['schedule_id'], ld['T1_3PT'], ld['T1_2PT'], ld['T1_block'], ld['T1_reb'], ld['T1_rate'], ld['T2_3PT'], ld['T2_2PT'], ld['T2_block'], ld['T2_reb'], ld['T2_rate'], T1_name=ld['T1_name'], T2_name=ld['T2_name'], _id=ld['id'])
            return match
        else:
            return None
            
    def get_matches(self, limit=100, offset=0):
        '''Returns result list and total number of results.
        Returning list is list of :class:`final4.models.match.Match` object. All objects
        filled up with values from the rows of the matches table.
        Also returns the total number of the result.
        
        :param limit: maximum number of the result
        :param offset: skip beginning of the result
        :returns: matchlist, total
        :rtype: list, int
        '''

        query = """SELECT count(matches.id)
                        FROM matches, schedules
                        WHERE schedules.id=matches.schedule_id
                          """
        self.cur.execute(query)
        total = self.cur.fetchone()[0]
        
        query = """SELECT matches.id,
                          schedules.id,
                          teams1.name, teams2.name,
                          T1_3PT, T1_2PT, T1_block, T1_reb, T1_rate,
                          T2_3PT, T2_2PT, T2_block, T2_reb, T2_rate
                        FROM matches, schedules
                        JOIN teams teams1 ON teams1.id=schedules.team1_id
                        JOIN teams teams2 ON teams2.id=schedules.team2_id
                        WHERE schedules.id=matches.schedule_id"""

        self.cur.execute(query, (limit, offset))
        matches = self.cur.fetchall()
        matchlist = []
        for l in matches:
            ld = dict(zip(matchtable, l))
            match = Match(ld['schedule_id'], ld['T1_3PT'], ld['T1_2PT'], ld['T1_block'], ld['T1_reb'], ld['T1_rate'], ld['T2_3PT'], ld['T2_2PT'], ld['T2_block'], ld['T2_reb'], ld['T2_rate'], T1_name=ld['T1_name'], T2_name=ld['T2_name'], _id=ld['id'])
            matchlist.append(match)
        return matchlist, total

    def get_matches_by(self, attrib, search_key, limit=100, offset=0):
        '''Returns result list and total number of result.
        Returning list is list of  :class:`final4.models.match.Match` object. All objects
        filled up with values from the rows of the matches table. 
        
        The return list made up by **filtered results** with given parameters.
       
        :param limit: maximum number of the result
        :param offset: skip beginning of the result
        
        :returns: matchlist, total
        :rtype: list, int
        '''
        skey = str(search_key)

        # WARNING !!! SQL INJECTION?
        query = """SELECT count(matches.id)
                        FROM matches, schedules
                        WHERE matches.{attrib}=%s AND schedules.id=matches.schedule_id""".format(attrib=attrib)
        self.cur.execute(query, (skey,))
        total = self.cur.fetchone()[0]

        # WARNING !!! SQL INJECTION?
        query = """SELECT matches.id,
                          schedules.id,
                          teams1.name, teams2.name,
                          T1_3PT, T1_2PT, T1_block, T1_reb, T1_rate,
                          T2_3PT, T2_2PT, T2_block, T2_reb, T2_rate
                        FROM matches, schedules
                        JOIN teams teams1 ON teams1.id=schedules.team1_id
                        JOIN teams teams2 ON teams2.id=schedules.team2_id
                        WHERE leagues.{attrib}=%s AND schedules.id=matches.schedule_id""".format(attrib=attrib)
        self.cur.execute(query, (skey,limit, offset))
        matches = self.cur.fetchall()
        print('matches:', matches)
        matchlist = []
        for l in matches:
            ld = dict(zip(matchtable, l))
            match = Match(ld['schedule_id'], ld['T1_3PT'], ld['T1_2PT'], ld['T1_block'], ld['T1_reb'], ld['T1_rate'], ld['T2_3PT'], ld['T2_2PT'], ld['T2_block'], ld['T2_reb'], ld['T2_rate'], T1_name=ld['T1_name'], T2_name=ld['T2_name'], _id=ld['id'])
            matchlist.append(match)
        return matchlist, total

    def get_matches_search_by(self, attrib, search_key, limit=100, offset=0):
        '''Returns result list and total number of result.
        Returning list is list of  :class:`final4.models.match.Match` object. All objects
        filled up with values from the rows of the matches table. 
        
        The return list made up by **filtered results** with given parameters.
       
        :param limit: maximum number of the result
        :param offset: skip beginning of the result
        
        :returns: matchlist, total
        :rtype: list, int
        '''
    
        skey = str(search_key) + '%'

        # WARNING !!! SQL INJECTION?
        query = """SELECT count(matches.id)
                        FROM matches, schedules
                        WHERE matches.{attrib}=%s AND schedules.id=matches.schedule_id""".format(attrib=attrib)
        self.cur.execute(query, (skey,))
        total = self.cur.fetchone()[0]

        # WARNING !!! SQL INJECTION?
        query = """SELECT matches.id,
                          schedules.id,
                          teams1.name, teams2.name,
                          T1_3PT, T1_2PT, T1_block, T1_reb, T1_rate,
                          T2_3PT, T2_2PT, T2_block, T2_reb, T2_rate
                        FROM matches, schedules
                        JOIN teams teams1 ON teams1.id=schedules.team1_id
                        JOIN teams teams2 ON teams2.id=schedules.team2_id
                        WHERE leagues.{attrib}=%s AND schedules.id=matches.schedule_id""".format(attrib=attrib)
        self.cur.execute(query, (skey,limit, offset))
        matches = self.cur.fetchall()
        print('matches:', matches)
        matchlist = []
        for l in matches:
            ld = dict(zip(matchtable, l))
            match = Match(ld['schedule_id'], ld['T1_3PT'], ld['T1_2PT'], ld['T1_block'], ld['T1_reb'], ld['T1_rate'], ld['T2_3PT'], ld['T2_2PT'], ld['T2_block'], ld['T2_reb'], ld['T2_rate'], T1_name=ld['T1_name'], T2_name=ld['T2_name'], _id=ld['id'])
            matchlist.append(match)
        return matchlist, total
