teamrostertable = ['id', 'team_id', 'player_id']

class Teamroster:
    def __init__(self, team_id, player_id, id=None):
        self.team_id=team_id
        self.player_id = player_id
        self.id=id
		
class Teamrosters:
    def __init__(self, conn, cur):
        self.conn = conn
        self.cur = cur
        self.last_key = None

    def add_teamroster(self, teamroster):
        query = """INSERT INTO teamrosters (team_id, player_id,id) 
                                    values ('%s','%s','%s')""" % teamroster.getAttrs()

        self.cur.execute(query)
        self.conn.commit()

    def delete_teamroster(self, team_id):
        query = "DELETE FROM teamrosters WHERE team_id='%s'" % team_id
        self.cur.execute(query)
        self.conn.commit()

    def update_teamroster(self, key, teamroster):
        args = teamroster.getAttrs() + (key,)
        query = """UPDATE teamrosters SET team_id='%s', player_id='%s', 
                    id='%s'""" % args

        self.cur.execute(query)
        self.conn.commit()

    def get_teamroster(self, team_id):
        query = "SELECT * FROM teamrosters WHERE team_id='%s'" % team_id
        self.cur.execute(query)
        tr = self.cur.fetchone()
        if tr:
            print (tr)
            trd = dict(zip(teamrostertable, trd)) # teamroster dict
            teamroster = Teamroster(trd['team_id'], trd['player_id'],trd['id'])
            print (teamroster.team_id)
	    print (teamroster.player_id)
            return teamroster
        return None

    def get_teamrosters(self):
        query = "SELECT * FROM teamrosters;"
        self.cur.execute(query)
        teamrosters = self.cur.fetchall()
        teamrosterlist = []
        for tr in teamrosters:
            trd = dict(zip(teamrostertable, tr))
            teamroster = Teamroster.fromDict(trd)
            teamrosterlist.append(teamroster)
            
        return teamrosterlist
