standingtable = ['id', 'season_id','season_year','league_id','league_name','team_id','team_name']

class Standing:
    def __init__(self, season_id,league_id,team_id, season_year=None, league_name=None, team_name=None, _id=None):
        self._id = _id
        self.season_id = season_id
        self.season_year = season_year
        self.league_id = league_id
        self.league_name = league_name
        self.team_id = team_id
        self.team_name = team_name
        

    def getAttrs(self):
        return (dict(zip(standingtable, (self._id, self.season_id,self.season_year,self.league_id,self.league_name,self.team_id,self.team_name))))

class Standings:
    def __init__(self, conn, cur):
        self.conn = conn
        self.cur = cur
        self.last_key = None

    def add_standing(self, standing):
        print("addstanding ", standing)
        query = """INSERT INTO standings (season_id,league_id,team_id) 
                                    values (%s,%s,%s)""" 

        self.cur.execute(query, (standing.season_id,standing.league_id,standing.team_id))
        self.conn.commit()

    def delete_standing(self, _id):
        query = """DELETE FROM standings WHERE id=%s"""
        # variables should be in tuple object
        self.cur.execute(query, (_id,))
        self.conn.commit()

    def update_standing(self, _id, new):
        '''
        new : standing object
        '''
        #print('update_league')
        query = """UPDATE standings SET season_id=%s,league_id=%s,team_id=%s WHERE id=%s"""
        self.cur.execute(query, (new.season_id,new.league_id,new.team_id, _id))
        self.conn.commit()

    def get_standing(self,_id):
        query = """SELECT standings.id, seasons.id, seasons.year, leagues.id, leagues.name, teams.id, teams.name
                        FROM standings,seasons,leagues,teams 
                        WHERE standings.id=%s AND seasons.id=standings.season_id AND leagues.id=standings.league_id AND teams.id=standings.team_id"""   
                        
        self.cur.execute(query, (_id,))
        l = self.cur.fetchone()
        if l:
            ld = dict(zip(standingtable, l[:len(standingtable)]))
            standing = Standing(ld['season_id'], ld['league_id'], ld['team_id'], _id=ld['id'], league_name=ld['league_name'],team_name=ld['team_name'],season_year=ld['season_year'])
            return standing
        else:
            return None

    def get_standings(self,limit=100, offset=0):
    
        query="""SELECT count(standings.id)
                        FROM standings,seasons,leagues,teams WHERE standings.season_id=seasons.id AND standings.league_id=leagues.id AND standings.team_id=teams.id
          """
        self.cur.execute(query)
        total = self.cur.fetchone()[0]
        
        query="""SELECT standings.id, seasons.id,seasons.year,leagues.id,leagues.name,teams.id,teams.name
                        FROM standings, seasons,leagues,teams WHERE seasons.id=standings.season_id AND leagues.id=standings.league_id AND teams.id=standings.team_id
                          LIMIT %s OFFSET %s"""
        self.cur.execute(query, (limit, offset))
        standings = self.cur.fetchall()
        standinglist = []
        for l in standings:
            ld = dict(zip(standingtable, l))
            standing = Standing(ld['season_id'], ld['league_id'], ld['team_id'], _id=ld['id'], league_name=ld['league_name'],team_name=ld['team_name'],season_year=ld['season_year'])
            standinglist.append(standing)
        return standinglist,total
        
    def get_standings_by(self, attrib, search_key, limit=100, offset=0):
        skey = str(search_key)
        
        query = """SELECT count(standings.id)
                        FROM standings,leagues,teams,seasons WHERE standings.season_id=seasons.id AND standings.league_id = leagues.id AND standings.team_id = teams.id """.format(attrib=attrib)
                        
        self.cur.execute(query, (skey,))
        total = self.cur.fetchone()[0]
        
        query = """SELECT standings.id, seasons.id, seasons.year, leagues.id,leagues.name, teams.id, teams.name 
                        FROM standings,leagues,teams,seasons
                        WHERE standings.{attrib}=%s AND standings.season_id=seasons.id AND standings.league_id = leagues.id AND standings.team_id = teams.id
			LIMIT %s OFFSET %s""".format(attrib=attrib)
        self.cur.execute(query, (skey,limit, offset))
        standings= self.cur.fetchall()
        print('standings:',standings)
        standinglist = []
        for l in standings:
            ld = dict(zip(standingtable, l))
            standing = Standing(ld['season_id'], ld['league_id'], ld['team_id'], _id=ld['id'], league_name=ld['league_name'],team_name=ld['team_name'],season_year=ld['season_year'])
            standinglist.append(standing)
        return standinglist, total
      
    def get_standings_search_by(self, attrib, search_key, limit=100, offset=0):
      
        skey = str(search_key) + '%'
      
        query = """SELECT count(standings.id)
                  FROM standings,leagues,teams,seasons
                        WHERE leagues.name LIKE %s AND standings.season_id=seasons.id AND standings.league_id = leagues.id AND standings.team_id = teams.id
                          """
      
        self.cur.execute(query, (skey,))
        total = self.cur.fetchone()[0]
      
        query = """SELECT standings.id, seasons.id, seasons.year, leagues.id,leagues.name, teams.id, teams.name 
                        FROM standings,leagues,teams,seasons
                        WHERE leagues.name LIKE %s AND standings.season_id=seasons.id AND standings.league_id = leagues.id AND standings.team_id = teams.id LIMIT %s OFFSET %s
                  """
        self.cur.execute(query, (skey,limit, offset))
        standings = self.cur.fetchall()
        print('standings:',standings)
        standinglist = []
        for l in standings:
            ld = dict(zip(standingtable, l))
            standing = Standing(ld['season_id'], ld['league_id'], ld['team_id'], _id=ld['id'], league_name=ld['league_name'],team_name=ld['team_name'],season_year=ld['season_year'])
            standinglist.append(standing)
        return standinglist, total
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
        
        
