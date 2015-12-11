scheduletable = ['id','team1_id','team1_name','team2_id','team2_name', 'season_id', 'season_year','league_id','league_name','date','saloon','score1','score2','state']

class Schedule:
    def __init__(self, team1_id, team2_id, season_id, league_id, date, saloon, score1=None, score2=None, state=False, team1_name=None,team2_name=None, season_year=None, league_name=None, _id=None):
     
        self._id = _id
        self.team1_id=team1_id
        self.team2_id=team2_id
        self.season_id = season_id
        self.league_id = league_id
        self.date = str(date)
        self.saloon = saloon
        self.score1 = score1
        self.score2 = score2
        self.state = state
        
        self.team1_name = team1_name
        self.team2_name = team2_name
        self.season_year = season_year
        self.league_name = league_name


    def getAttrs(self):
        return (dict(zip(scheduletable, (self._id,self.team1_id, self.team1_name, self.team2_id, self.team2_name,  self.season_id,  self.season_year, self.league_id, self.league_name, self.date, self.saloon, self.score1, self.score2, self.state))))

class Schedules:
    def __init__(self, conn, cur):
        self.conn = conn
        self.cur = cur
        self.last_key = None

    def add_schedule(self, schedule):
        query = """INSERT INTO schedules (team1_id, team2_id, season_id,league_id,date,saloon,score1,score2,state) 
                                    values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

        self.cur.execute(query, (schedule.team1_id, schedule.team2_id, schedule.season_id,schedule.league_id,schedule.date,schedule.saloon,schedule.score1,schedule.score2,schedule.state))
        self.conn.commit()

    def delete_schedule(self, _id):
        query = "DELETE FROM schedules WHERE id=%s"
        self.cur.execute(query, (_id,))
        self.conn.commit()

    def update_schedule(self, _id, new):
        '''
        new : schedule object
        '''
        query = """UPDATE schedules SET team1_id=%s,
                    team2_id=%s,season_id=%s,league_id=%s,date=%s, saloon=%s, score1=%s,score2=%s,state=%s WHERE id=%s"""

        self.cur.execute(query, (new.team1_id, new.team2_id, new.season_id,new.league_id,new.date,new.saloon,new.score1,new.score2,new.state, _id))
        self.conn.commit()

        
    def get_schedule(self,_id):
    
        query = """SELECT schedules.id, teams1.id, teams1.name, teams2.id, teams2.name, seasons.id, seasons.year, leagues.id, leagues.name, schedules.date, schedules.saloon, schedules.score1, schedules.score2,schedules.state 
                        FROM seasons,leagues, schedules
                        JOIN teams teams1 ON teams1.id=schedules.team1_id
                        JOIN teams teams2 ON teams2.id=schedules.team2_id
                        WHERE schedules.id=%s AND seasons.id=schedules.season_id AND leagues.id=schedules.league_id
                        """
        self.cur.execute(query, (_id,))
        l = self.cur.fetchone()

        if l:
            ld = dict(zip(scheduletable, l[:len(scheduletable)]))
            schedule = Schedule(ld['team1_id'],ld['team2_id'],ld['season_id'], ld['league_id'], ld['date'], ld['saloon'],ld['score1'],ld['score2'], ld['state'], team1_name=ld['team1_name'], team2_name=ld['team2_name'], season_year=ld['season_year'], league_name=ld['league_name'], _id=ld['id'])
            return schedule
        else:
            return None

    def get_schedules(self, limit=100, offset=0):

        query = """SELECT count(schedules.id)
                        FROM seasons,leagues,schedules 
                        JOIN teams teams1 ON teams1.id=schedules.team1_id
                        JOIN teams teams2 ON teams2.id=schedules.team2_id
                        WHERE seasons.id=schedules.season_id AND leagues.id=schedules.league_id
                          """
        self.cur.execute(query)
        total = self.cur.fetchone()[0]

        query = """SELECT schedules.id, teams1.id, teams1.name, teams2.id, teams2.name, seasons.id, seasons.year, leagues.id, leagues.name, schedules.date, schedules.saloon, schedules.score1, schedules.score2,schedules.state 
                        FROM seasons,leagues,schedules 
                        JOIN teams teams1 ON teams1.id=schedules.team1_id
                        JOIN teams teams2 ON teams2.id=schedules.team2_id
                        WHERE seasons.id=schedules.season_id AND leagues.id=schedules.league_id
			LIMIT %s OFFSET %s
                        """

        self.cur.execute(query, (limit, offset))
        schedules = self.cur.fetchall()
        schedulelist = []
        for l in schedules:
            ld = dict(zip(scheduletable, l))
            print(l)
            print('-----------------------------------')
            print(ld)
            schedule = Schedule(ld['team1_id'],ld['team2_id'],ld['season_id'], ld['league_id'], ld['date'], ld['saloon'],ld['score1'],ld['score2'], ld['state'], team1_name=ld['team1_name'], team2_name=ld['team2_name'], season_year=ld['season_year'], league_name=ld['league_name'], _id=ld['id'])
            schedulelist.append(schedule)
            
        return schedulelist, total

    def get_schedules_by(self, attrib, search_key, limit=100, offset=0):
        skey = str(search_key)

        # WARNING !!! SQL INJECTION?
        query = """SELECT count(schedules.id)
                        FROM seasons,leagues,schedules 
                        JOIN teams teams1 ON teams1.id=schedules.team1_id
                        JOIN teams teams2 ON teams2.id=schedules.team2_id
                         WHERE schedules.{attrib}=%s AND seasons.id=schedules.season_id AND leagues.id=schedules.league_id
                          """.format(attrib=attrib)
        self.cur.execute(query, (skey,))
        total = self.cur.fetchone()[0]

        # WARNING !!! SQL INJECTION?
        query = """SELECT schedules.id, teams1.id, teams1.name, teams2.id, teams2.name, seasons.id, seasons.year, leagues.id, leagues.name, schedules.date, schedules.saloon, schedules.score1, schedules.score2,schedules.state 
                        FROM seasons,leagues,schedules 
                        JOIN teams teams1 ON teams1.id=schedules.team1_id
                        JOIN teams teams2 ON teams2.id=schedules.team2_id
                        WHERE schedules.{attrib}=%s AND seasons.id=schedules.season_id AND leagues.id=schedules.league_id
                          LIMIT %s OFFSET %s
                        """.format(attrib=attrib)
        self.cur.execute(query, (skey,limit, offset))
        schedules = self.cur.fetchall()
        print('schedules:', schedules)
        schedulelist = []
        for l in schedules:
            ld = dict(zip(scheduletable, l))
            schedule = Schedule(ld['team1_id'],ld['team2_id'],ld['season_id'], ld['league_id'], ld['date'], ld['saloon'],ld['score1'],ld['score2'], ld['state'], team1_name=ld['team1_name'], team2_name=ld['team2_name'], season_year=ld['season_year'], league_name=ld['league_name'], _id=ld['id'])
            schedulelist.append(schedule)
        return schedulelist, total

    def get_schedules_search_by(self, attrib, search_key, limit=100, offset=0):
        # convert search key to special sql search syntax that means
        # all matches that starts with search_key
        # searches team1 attribute
        skey = str(search_key) + '%'
        
        # WARNING !!! SQL INJECTION?
        query = """SELECT count(schedules.id)
                        FROM seasons,leagues,schedules 
                        JOIN teams teams1 ON teams1.id=schedules.team1_id
                        JOIN teams teams2 ON teams2.id=schedules.team2_id
                         WHERE teams1.{attrib} LIKE %s AND seasons.id=schedules.season_id AND leagues.id=schedules.league_id
                          """.format(attrib=attrib)
        self.cur.execute(query, (skey,))
        total = self.cur.fetchone()[0]

        # WARNING !!! SQL INJECTION?
        query = """SELECT schedules.id, teams1.id, teams1.name, teams2.id, teams2.name, seasons.id, seasons.year, leagues.id, leagues.name, schedules.date, schedules.saloon, schedules.score1, schedules.score2,schedules.state 
                        FROM seasons,leagues,schedules 
                        JOIN teams teams1 ON teams1.id=schedules.team1_id
                        JOIN teams teams2 ON teams2.id=schedules.team2_id
                        WHERE teams1.{attrib} LIKE %s AND seasons.id=schedules.season_id AND leagues.id=schedules.league_id
                          LIMIT %s OFFSET %s
                        """.format(attrib=attrib)
        self.cur.execute(query, (skey,limit, offset))
        schedules = self.cur.fetchall()
        print('schedules:', schedules)
        schedulelist = []
        for l in schedules:
            ld = dict(zip(scheduletable, l))
            schedule = Schedule(ld['team1_id'],ld['team2_id'],ld['season_id'], ld['league_id'], ld['date'], ld['saloon'],ld['score1'],ld['score2'], ld['state'], team1_name=ld['team1_name'], team2_name=ld['team2_name'], season_year=ld['season_year'], league_name=ld['league_name'], _id=ld['id'])
            schedulelist.append(schedule)
        return schedulelist, total

