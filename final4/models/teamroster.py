teamrostertable = ['id', 'team_id', 'player_id','team','player']

class Teamrosters:
    def __init__(self, team_id, player_id, id=None,team=None,player=None):
        self.team_id=team_id
        self.player_id = player_id
        self.id=id
        self.team=team
        self.player=player

    def getAttrs(self):
        return (dict(zip(teamrostertable, (self._id, self.team_id, self.player_id, self.team,self.player))))

class Teamrosters:
    def __init__(self, conn, cur):
        self.conn = conn
        self.cur = cur
        self.last_key = None

    def add_teamroster(self, teamroster):
        print("addteamroster ", teamroster)
        query = """INSERT INTO teamrosters (team_id, player_id) 
                                    values (%s,%s)""" 

        self.cur.execute(query, (teamroster.team_id, teamroster.player_id))
        self.conn.commit()

    def delete_teamroster(self, _id):
        query = """DELETE FROM teamrosters WHERE id=%s"""
        self.cur.execute(query, (_id,))
        self.conn.commit()

    def update_teamroster(self, _id, new):
        print('update_teamroster')
        query = """UPDATE teamrosters SET team_id=%s, player_id=%s
                    WHERE id=%s"""
        self.cur.execute(query, (new.team_id, new.player_id, _id))
        self.conn.commit()

    def get_teamroster(self,_id):
        query = """SELECT teamrosters.id, teams.name, players.name
                        FROM teams,players
                        WHERE teamrosters.id=%s AND players.id=teamrosters.player_id AND teams.id=teamrosters.team_id
                        ORDER BY teamrosters.team_id
                        """
        self.cur.execute(query, (_id,))
        tr = self.cur.fetchone()
        if tr:
            trd = dict(zip(teamrostertable, tr[:len(teamrostertable)]))
            teamroster = Teamroster(trd['team_id'], trd['player_id'], trd['team'],trd['player'], trd['id'])
            return teamroster
        else:
            return None

    def get_teamrosters(self, limit, offset):

        query = """SELECT count(teamrosters.id)
                        FROM teamrosters
                                                  """
        self.cur.execute(query)
        total = self.cur.fetchone()[0]

       
        query = """SELECT count(teamrosters.id)
                        FROM teamrosters
                                                  """
        self.cur.execute(query, (limit, offset))
        teamrosters = self.cur.fetchall()
        teamlist = []
        for tr in teamrosters:
            trd = dict(zip(teamrostertable, tr))
            teamroster = Teamroster(trd['team_id'], trd['player_id'], trd['team'],trd['player'],trd['id'])
            teamteamrosterlist.append(teamroster)
        return teamteamrosterlist, total

    def get_teamrosters_by(self, key, var, limit, offset):
        skey = str(key) + '%'

        query = """SELECT count(teamrosters.id)
                      """
        self.cur.execute(query, (skey,))
        total = self.cur.fetchone()[0]

        query = """SELECT teams.id, teams.name, teams.coach_id, countries.name
                        FROM teams,countries WHERE teams.name LIKE %s AND 
                            countries.id=teams.coach_id ORDER BY teams.name
                            LIMIT %s OFFSET %s"""
        self.cur.execute(query, (skey,limit, offset))
        teams = self.cur.fetchall()
        print('teamrosters:', teamrosters)
        teamrosterlist = []
        for tr in teamrosters:
            trd = dict(zip(teamrostertable, tr))
            teamroster = Teamroster(trd['team_id'], trd['player_id'], trd['team'],trd['player'],trd['id'])
            teamrosterlist.append(teamroster)
        return teamrosterlist, total

