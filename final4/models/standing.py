standingtable = ['id', 'winning', 'season_id','league_id','team_id']

class Standing:
    def __init__(self, winning, season_id,league_id,team_id, _id=None):
        self._id = _id
        self.winning = winning
        self.season_id = season_id
        self.league_id = league_id
        self.team_id = team_id
        

    def getAttrs(self):
        return (dict(zip(standingtable, (self._id, self.winning, self.season_id,self.league_id,self.team_id))))

class Standings:
    def __init__(self, conn, cur):
        self.conn = conn
        self.cur = cur
        self.last_key = None

    def add_standing(self, standing):
        print("addstanding ", standing)
        query = """INSERT INTO standings (winning,season_id,league_id,team_id) 
                                    values (%s,%s,%s,%s)""" 

        self.cur.execute(query, (standing.winning, standing.season_id,standing.league_id,standing.team_id))
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
        query = """UPDATE standings SET winning=%s, season_id=%s,league_id=%s,team_id=%s
                    WHERE id=%s"""
        self.cur.execute(query, (new.winning, new.season_id,new.league_id,new.team_id, _id))
        self.conn.commit()

    def get_standing(self,_id):
        query = """SELECT * FROM standings WHERE id=%s"""
        self.cur.execute(query, (_id,))
        l = self.cur.fetchone()
        if l:
            ld = dict(zip(standingtable, l))
            standing = Standing(ld['winning'], ld['season_id'],ld['league_id'],ld['team_id'], ld['id'])
            return standing
        else:
            return None

    def get_standings(self):
        query = "SELECT * FROM standings;"
        self.cur.execute(query)
        standings = self.cur.fetchall()
        standinglist = []
        for l in standings:
            ld = dict(zip(standingtable, l))
            standing = Standing(ld['winning'], ld['season_id'], ld['league_id'], ld['team_id'], ld['id'])
            standinglist.append(standing)
        return standinglist
