teamtable = ['id', 'name', 'coach_id']

class Team:
    def __init__(self, name, coach_id, id=None):
        self.name = name
        self.coach_id = coach_id
        self.id=id
		
class Teams:
    def __init__(self, conn, cur):
        self.conn = conn
        self.cur = cur
        self.last_key = None

    def add_team(self, team):
        query = """INSERT INTO teams (name, coach_id,id) 
                                    values ('%s','%s','%s')""" % team.getAttrs()

        self.cur.execute(query)
        self.conn.commit()

    def delete_team(self, name):
        query = "DELETE FROM teams WHERE name='%s'" % name
        self.cur.execute(query)
        self.conn.commit()

    def update_team(self, key, team):
        args = team.getAttrs() + (key,)
        query = """UPDATE teams SET name='%s', coach_id='%s', 
                    id='%s'""" % args

        self.cur.execute(query)
        self.conn.commit()

    def get_team(self, name):
        query = "SELECT * FROM teams WHERE name='%s'" % name
        self.cur.execute(query)
        t = self.cur.fetchone()
        if t:
            print (t)
            td = dict(zip(teamtable, t)) # team dict
            team = Team(td['name'], td['coach_id'],td['id'])
            print (team.age)
            return team
        return None

    def get_teams(self):
        query = "SELECT * FROM teams;"
        self.cur.execute(query)
        teams = self.cur.fetchall()
        teamlist = []
        for t in Teams:
            td = dict(zip(teamtable, t))
            team = Team.fromDict(td)
            teamlist.append(team)
        return teamlist
