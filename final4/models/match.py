matchtable = ['id', 'schedule_id', 'T1_name', 'T2_name', 'T1_3PT', 'T1_2PT', 'T1_block', 'T1_reb', 'T1_rate', 'T2_3PT', 'T2_2PT', 'T2_block', 'T2_reb', 'T2_rate']

class Match:
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
        return (dict(zip(matchtable, (self._id, self.schedule_id, self.T1_name, self.T2_name, self.T1_3PT, self.T1_2PT, self.T1_block, self.T1_reb, self.T1_rate, self.T2_3PT, self.T2_2PT, self.T2_block, self.T2_reb, self.T2_rate))))

class Matches:
    def __init__(self, conn, cur):
        self.conn = conn
        self.cur = cur
        self.last_key = None
        
    def add_match(self, match):
        query = """INSERT INTO matches (schedule_id, T1_3PT, T1_2PT, T1_block, T1_reb, T1_rate, T2_3PT, T2_2PT, T2_block, T2_reb, T2_rate) 
                                    values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

        self.cur.execute(query, (match.schedule_id, match.T1_3PT, match.T1_2PT, match.T1_block, match.T1_reb, match.T1_rate, match.T2_3PT, match.T2_2PT, match.T2_block, match.T2_reb, match.T2_rate))
        self.conn.commit()

    def delete_match(self, _id):
        query = "DELETE FROM matches WHERE id=%s"
        self.cur.execute(query, (_id,))
        self.conn.commit()
        
    def update_match(self, _id, new):
        '''
        new : match object
        '''
        print('update_match')
        query = """UPDATE matches SET schedule_id=%s, T1_3PT=%s, T1_2PT=%s, T1_block=%s, T1_reb=%s, T1_rate=%s, T2_3PT=%s, T2_2PT=%s, T2_block=%s, T2_reb=%s, T2_rate=%s
                    WHERE id=%s"""
        self.cur.execute(query, (new.schedule_id, new.T1_3PT, new.T1_2PT, new.T1_block, new.T1_reb, new.T1_rate, new.T2_3PT, new.T2_2PT, new.T2_block, new.T2_reb, new.T2_rate, _id))
        self.conn.commit()

    def get_match(self,_id):
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
