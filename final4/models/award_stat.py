award_stattable = ['id', 'award_id', 'award_name', 'player_id', 'player_name', 'player_surname', 'season_id', 'season_year']

class AwardStat:
    '''Awartstat object'''
    def __init__(self, award_id, player_id, season_id, 
            award_name=None, player_name=None, player_surname=None, 
            season_year=None, _id=None):
        self._id = _id
        self.award_id = award_id
        self.award_name = award_name
        self.player_id = player_id
        self.player_name = player_name
        self.player_surname = player_surname
        self.season_id = season_id
        self.season_year = season_year

    def getAttrs(self):
        '''returns attributes of the Awardstat class as a dictionary. Keys are 
        taken from the awardstattable and corresponding values are taken from 
        the Awardstat object attributes.
        
        :returns: attributes of the Awardstat object as a dictionary.
        :rtype: dict'''
        return (dict(zip(award_stattable, (self._id, self.award_id, self.award_name, self.player_id, 
            self.player_name, self.player_surname, self.season_id, self.season_year))))

        
class AwardStats:
    '''the Awardstats object provides functions for database connections of awardstats table.
    
    :param conn: psycopg2 connection object
    :param cur: psycopg2 cursor object
    '''
    def __init__(self, conn, cur):
        self.conn = conn
        self.cur = cur
        self.last_key = None

    def add_award_stat(self, award_stat):
        '''inserts a new row to the awardstats table with values of the given awardstat attributes.
        
        :param awardstat: new Awardstat object
        '''
        query = """INSERT INTO award_stats (award_id, player_id, season_id) 
                                    values (%s,%s,%s)"""

        self.cur.execute(query, (award_stat.award_id, award_stat.player_id, award_stat.season_id))
        self.conn.commit()

    def delete_award_stat(self, _id):
        '''deletes the row from the awardstats table whose id is given _id.

        :param _id: id of the row - int
        '''
        query = "DELETE FROM award_stats WHERE id=%s"
        self.cur.execute(query, (_id,))
        self.conn.commit()

    def update_award_stat(self, _id, new):
        '''Updates the row from the awardstats table whose id is given _id. 
        The new values is taken from given *new* Awardstat object.

        :param _id: id of the row - int
        :param new: Awardstat object with new values
        '''
        query = """UPDATE award_stats SET award_id=%s, 
                    player_id=%s, season_id=%s WHERE id=%s"""

        self.cur.execute(query, (new.award_id, new.player_id, new.season_id, _id))
        self.conn.commit()

        
    def get_award_stat(self,_id):
        '''Returns :class:`final4.models.awardstat.Awardstat` object with values from
        the awardstats table IF there is a record has a given _id ELSE returns None.

        :param _id: id of the row - int
        :returns: awardstat or None
        :rtype: :class:`final4.models.awardstat.Awardstat` object or None
        '''
        query = """SELECT award_stats.id, 
                          awards.id, awards.name, 
                          players.id, players.name, players.surname, 
                          seasons.id, seasons.year
                        FROM award_stats, awards, players, seasons
                        WHERE 
                            award_stats.id=%s AND 
                            awards.id=award_stats.award_id AND 
                            players.id=award_stats.player_id AND 
                            seasons.id=award_stats.season_id
                        """
        self.cur.execute(query, (_id,))
        l = self.cur.fetchone()
        if l:
            ld = dict(zip(award_stattable, l[:len(award_stattable)]))
            award_stat = AwardStat(ld['award_id'], ld['player_id'], ld['season_id'],
			    _id=ld['id'], award_name=ld['award_name'], player_name=ld['player_name'],
			    player_surname=ld['player_surname'], season_year=ld['season_year'])
            return award_stat
        else:
            return None

    def get_award_stats(self, limit=100, offset=0):
        '''Returns result list and total number of results.
        Returning list is list of :class:`final4.models.awardstat.Awardstat` object. All objects
        filled up with values from the rows of the awardstats table.
        Also returns the total number of the result.
        
        :param limit: maximum number of the result
        :param offset: skip beginning of the result
        :returns: awardstatlist, total
        :rtype: list, int
        '''

        query = """SELECT count(award_stats.id)
                        FROM award_stats, awards, players, seasons 
                        WHERE 
                            awards.id=award_stats.award_id AND
                            award_stats.player_id=players.id AND
                            award_stats.season_id=seasons.id
                          """
        self.cur.execute(query)
        total = self.cur.fetchone()[0]

        query = """SELECT award_stats.id, 
                          awards.id, awards.name, 
                          players.id, players.name, players.surname, 
                          seasons.id, seasons.year 
                        FROM award_stats, awards, players, seasons
                        WHERE 
                            awards.id=award_stats.award_id AND
                            award_stats.player_id=players.id AND
                            award_stats.season_id=seasons.id
			ORDER BY awards.name ASC LIMIT %s OFFSET %s
                        """

        self.cur.execute(query, (limit, offset))
        award_stats = self.cur.fetchall()
        award_statlist = []
        for l in award_stats:
            ld = dict(zip(award_stattable, l))
            award_stat = AwardStat(ld['award_id'], ld['player_id'], ld['season_id'],
			    _id=ld['id'], award_name=ld['award_name'], player_name=ld['player_name'],
			    player_surname=ld['player_surname'], season_year=ld['season_year'])
            award_statlist.append(award_stat)
        return award_statlist, total

    def get_award_stats_by(self, attrib, search_key, limit=100, offset=0):
        '''Returns result list and total number of result.
        Returning list is list of  :class:`final4.models.awardstat.Awardstat` object. All objects
        filled up with values from the rows of the awardstats table. 
        
        The return list made up by **filtered results** with given parameters.
       
        :param limit: maximum number of the result
        :param offset: skip beginning of the result
        
        :returns: awardstatlist, total
        :rtype: list, int
        '''
        skey = str(search_key)

        # WARNING !!! SQL INJECTION?
        query = """SELECT count(award_stats.id)
                        FROM award_stats, awards, players, seasons 
                        WHERE 
                            awards.{attrib}=%s AND 
                            awards.id=award_stats.award_id AND
                            award_stats.player_id=players.id AND 
                            award_stats.season_id=seasons.id
                          """.format(attrib=attrib)
        self.cur.execute(query, (skey,))
        total = self.cur.fetchone()[0]

        # WARNING !!! SQL INJECTION?
        query = """SELECT award_stats.id, 
                          awards.id, awards.name, 
                          players.id, players.name, players.surname, 
                          seasons.id, seasons.year 
                        FROM award_stats, awards, players, seasons
                        WHERE 
                            awards.{attrib}=%s AND 
                            awards.id=award_stats.award_id AND
                            players.id=award_stats.player_id AND
                            seasons.id=award_stats.season_id
			ORDER BY awards.name ASC LIMIT %s OFFSET %s
                        """.format(attrib=attrib)
        self.cur.execute(query, (skey,limit, offset))
        award_stats = self.cur.fetchall()
        award_statslist = []
        for l in award_stats:
            ld = dict(zip(award_stattable, a))
            award_stat = AwardStat(ld['award_id'], ld['player_id'], ld['season_id'],
			    _id=ld['id'], award_name=ld['award_name'], player_name=ld['player_name'],
			    player_surname=ld['player_surname'], season_year=ld['season_year'])
            award_statslist.append(award_stat)
        return award_statslist, total

    def get_award_stats_search_by(self, attrib, search_key, limit=100, offset=0):
        '''Returns result list and total number of result.
        Returning list is list of  :class:`final4.models.awardstat.Awardstat` object. All objects
        filled up with values from the rows of the awardstats table. 
        
        The return list made up by **filtered results** with given parameters.
       
        :param limit: maximum number of the result
        :param offset: skip beginning of the result
        
        :returns: awardstatlist, total
        :rtype: list, int
        '''
        # convert search key to special sql search syntax that means
        # all matches that starts with search_key
        skey = str(search_key) + '%'
        # WARNING !!! SQL INJECTION?
        query = """SELECT count(award_stats.id)
                        FROM award_stats, awards, players, seasons 
                        WHERE 
                            awards.{attrib} LIKE %s AND
                            awards.id=award_stats.award_id AND
                            players.id=award_stats.player_id AND
                            seasons.id=award_stats.season_id
                          """.format(attrib=attrib)
        self.cur.execute(query, (skey,))
        total = self.cur.fetchone()[0]

        # WARNING !!! SQL INJECTION?
        query = """SELECT award_stats.id,
                          awards.id, awards.name, 
                          players.id, players.name, players.surname, 
                          seasons.id, seasons.year 
                        FROM award_stats, awards, players, seasons
                        WHERE 
                            awards.{attrib} LIKE %s AND
                            awards.id=award_stats.award_id AND
                            players.id=award_stats.player_id AND 
                            seasons.id=award_stats.season_id
			ORDER BY awards.name ASC LIMIT %s OFFSET %s
                        """.format(attrib=attrib)
        self.cur.execute(query, (skey,limit, offset))
        award_stats = self.cur.fetchall()
        award_statslist = []
        for l in award_stats:
            ld = dict(zip(award_stattable, l))
            award_stat = AwardStat(ld['award_id'], ld['player_id'], ld['season_id'],
			    _id=ld['id'], award_name=ld['award_name'], player_name=ld['player_name'],
			    player_surname=ld['player_surname'], season_year=ld['season_year'])
            award_statslist.append(award_stat)
        return award_statslist, total

