standingtable = ['id', 'season_id','league_id','team_id','season']

class Standing:
    def __init__(self, season_id,league_id,team_id, _id=None):
        self._id = _id
        self.season_id = season_id
        self.league_id = league_id
        self.team_id = team_id
        self.season =season
        

    def getAttrs(self):
        return (dict(zip(standingtable, (self._id, self.season_id,self.league_id,self.team_id,self.season))))

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
        print('update_league')
        query = """UPDATE standings SET season_id=%s,league_id=%s,team_id=%s
                    WHERE id=%s"""
        self.cur.execute(query, (new.season_id,new.league_id,new.team_id, _id))
        self.conn.commit()

    def get_standing(self,_id):
        query = """SELECT standings.id, standings.league_id,standings.team_id, seasons.id, seasons.year
                        FROM standings,seasons 
                        WHERE standings.id=%s AND seasons.id=standings.seasons_id
                        ORDER BY standings.league_id
                        """   
                        
        self.cur.execute(query, (_id,))
        l = self.cur.fetchone()
        if l:
            ld = dict(zip(standingtable, l))
            standing = Standing(ld['season_id'], ld['league_id'], ld['team_id'],ld['season'], ld['id'])
            return standing
        else:
            return None

    def get_standings(self):
        query="""SELECT count(standings.id)
                        FROM standings,seasons WHERE seasons.id=standings.season_id
                          """
        self.cur.execute(query)
        total = self.cur.fetchone()[0]
        
        query="""SELECT standings.id,standings.league_id,standings.team_id
                        FROM standings, seasons WHERE seasons.id=standings.seasons_id
                          ORDER BY standings.league_id LIMIT %s OFFSET %s"""
        self.cur.execute(query, (limit, offset))
        standings = self.cur.fetchall()
        standinglist = []
        for l in standings:
            ld = dict(zip(standingtable, l))
            standing = Standing(ld['season_id'], ld['league_id'], ld['team_id'], ld['season'],ld['id'])
            standinglist.append(standing)
        return standinglist
        
    def get_standings_by(self, key, var):
        skey = str(key) + '%'
        query = """SELECT standings.id, standings.season_id, standings.league_id, standings.team_id,seasons.year
                        FROM standings,seasons WHERE stadings.league_id LIKE %s AND  
                            season.id=standings.season_id ORDER BY standings.league_id"""
        self.cur.execute(query, (skey,))
        standings = self.cur.fetchall()
        print('standings:', standings)
        standinglist = []
        for l in standings:
            ld = dict(zip(standingtable, l))
            standing = Standing(ld['season_id'], ld['league_id'], ld['team_id'], ld['season'],ld['id'])
            standinglist.append(standing)
        return standinglist
