teamrostertable = ['id', 'player_id','player','team_id','team']

class Teamroster:
    def __init__(self, player_id,team_id, player=None, team=None, _id=None):
        self._id = _id
        self.player_id = player_id
        self.player = player
        self.team_id = team_id
        self.team = team
        

    def getAttrs(self):
        return (dict(zip(teamrostertable, (self._id, self.player_id,self.player,self.team_id,self.team))))

class Teamrosters:
    def __init__(self, conn, cur):
        self.conn = conn
        self.cur = cur
        self.last_key = None

    def add_teamroster(self, teamroster):
        print("addteamroster ", teamroster)
        query = """INSERT INTO teamrosters (player_id,team_id) 
                                    values (%s,%s)""" 

        self.cur.execute(query, (teamroster.player_id,teamroster.team_id))
        self.conn.commit()

    def delete_teamroster(self, _id):
        query = """DELETE FROM teamrosters WHERE id=%s"""
        self.cur.execute(query, (_id,))
        self.conn.commit()

    def update_teamroster(self, _id, new):
        query = """UPDATE teamrosters SET player_id=%s,team_id=%s WHERE id=%s"""
        self.cur.execute(query, (new.player_id,new.team_id, _id))
        self.conn.commit()

    def get_teamroster(self,_id):
        query = """SELECT teamrosters.id, players.id, players.name,teams.id, teams.name
                        FROM teamrosters,players,teams 
                        WHERE teamrosters.id=%s AND players.id=teamrosters.player_id AND teams.id=teamrosters.team_id"""   
                        
        self.cur.execute(query, (_id,))
        tr = self.cur.fetchone()
        if tr:
            trd = dict(zip(teamrostertable, tr[:len(teamrostertable)]))
            teamroster = Teamroster(trd['player_id'],trd['team_id'], _id=trd['id'],team=trd['team'],player=trd['player'])
            return teamroster
        else:
            return None

    def get_teamrosters(self,limit=100, offset=0):
    
        query="""SELECT count(teamrosters.id)
                        FROM teamrosters,players,teams WHERE teamrosters.player_id=players.id AND teamrosters.team_id=teams.id
          """
        self.cur.execute(query)
        total = self.cur.fetchone()[0]
        
        query="""SELECT teamrosters.id, players.id,players.name,teams.id,teams.name
                        FROM teamrosters, players,teams WHERE players.id=teamrosters.player_id AND teams.id=teamrosters.team_id
                          LIMIT %s OFFSET %s"""
        self.cur.execute(query, (limit, offset))
        teamrosters = self.cur.fetchall()
        teamrosterlist = []
        for tr in teamrosters:
            trd = dict(zip(teamrostertable, tr))
            teamroster = Teamroster(trd['player_id'],trd['team_id'], _id=trd['id'], team=trd['team'],player=trd['player'])
            teamrosterlist.append(teamroster)
        return teamrosterlist,total
        
    def get_teamrosters_by(self, attrib, search_key, limit=100, offset=0):
        skey = str(search_key)
        
        query = """SELECT count(teamrosters.id)
                        FROM teamrosters,teams,players WHERE teamrosters.player_id=players.id AND teamrosters.team_id = teams.id """.format(attrib=attrib)
                        
        self.cur.execute(query, (skey,))
        total = self.cur.fetchone()[0]
        
        query = """SELECT teamrosters.id, players.id, players.name, teams.id, teams.name 
                        FROM teamrosters,teams,players
                        WHERE teamrosters.{attrib}=%s AND teamrosters.player_id=players.id AND teamrosters.team_id = teams.id
			LIMIT %s OFFSET %s""".format(attrib=attrib)
        self.cur.execute(query, (skey,limit, offset))
        teamrosters= self.cur.fetchall()
        print('teamrosters:',teamrosters)
        teamrosterlist = []
        for tr in teamrosters:
            trd = dict(zip(teamrostertable, tr))
            teamroster = Teamroster(trd['player_id'], trd['team_id'], _id=trd['id'], team=trd['team'],player=trd['player'])
            teamrosterlist.append(teamroster)
        return teamrosterlist, total
      
    def get_teamrosters_search_by(self, attrib, search_key, limit=100, offset=0):
      
        skey = str(search_key) + '%'
      
        query = """SELECT count(teamrosters.id)
                  FROM teamrosters,teams,players
                        WHERE players.name LIKE %s AND teamrosters.player_id=players.id AND teamrosters.team_id = teams.id
                          """
      
        self.cur.execute(query, (skey,))
        total = self.cur.fetchone()[0]
      
        query = """SELECT teamrosters.id, players.id, players.name, teams.id, teams.name 
                        FROM teamrosters,teams,players
                        WHERE players.name LIKE %s AND teamrosters.player_id=players.id AND teamrosters.team_id = teams.id LIMIT %s OFFSET %s
                  """
        self.cur.execute(query, (skey,limit, offset))
        teamrosters = self.cur.fetchall()
        print('teamrosters:',teamrosters)
        teamrosterlist = []
        for tr in teamrosters:
            trd = dict(zip(teamrostertable, tr))
            teamroster = Teamroster(trd['player_id'], trd['team_id'], _id=trd['id'], team=trd['team'],player=trd['player'])
            teamrosterlist.append(teamroster)
        return teamrosterlist, total
      
      
