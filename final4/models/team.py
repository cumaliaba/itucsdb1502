teamtable = ['id', 'name', 'coach_id', 'coach']

class Team:
    def __init__(self, name, coach_id, coach=None, _id=None):
        self._id = _id
        self.name = name
        self.coach_id = coach_id
        self.coach = coach

    def getAttrs(self):
        return (dict(zip(teamtable, (self._id, self.name, self.coach_id, self.coach))))

class Teams:
    def __init__(self, conn, cur):
        self.conn = conn
        self.cur = cur
        self.last_key = None

    def add_team(self, team):
        print("addteam ", team)
        query = """INSERT INTO teams (name, coach_id) 
                                    values (%s,%s)""" 

        self.cur.execute(query, (team.name, team.coach_id))
        self.conn.commit()

    def delete_team(self, _id):
        query = """DELETE FROM teams WHERE id=%s"""
        # variables should be in tuple object
        self.cur.execute(query, (_id,))
        self.conn.commit()

    def update_team(self, _id, new):
        '''
        new : team object
        '''
        print('update_team')
        query = """UPDATE teams SET name=%s, coach_id=%s
                    WHERE id=%s"""
        self.cur.execute(query, (new.name, new.coach_id, _id))
        self.conn.commit()

    def get_team(self,_id):
        query = """SELECT teams.id, teams.name, countries.id, countries.name
                        FROM teams,countries
                        WHERE teams.id=%s AND countries.id=teams.coach_id
                        ORDER BY teams.name
                        """
        self.cur.execute(query, (_id,))
        l = self.cur.fetchone()
        if l:
            ld = dict(zip(teamtable, l[:len(teamtable)]))
            team = Team(ld['name'], ld['coach_id'], ld['coach'], ld['id'])
            return team
        else:
            return None

    def get_teams(self, limit, offset):

        query = """SELECT count(teams.id)
                        FROM teams,countries WHERE countries.id=teams.coach_id
                          """
        self.cur.execute(query)
        total = self.cur.fetchone()[0]

        query = """SELECT teams.id, teams.name, countries.id, countries.name 
                        FROM teams,countries WHERE countries.id=teams.coach_id
                          ORDER BY teams.name LIMIT %s OFFSET %s"""
        self.cur.execute(query, (limit, offset))
        teams = self.cur.fetchall()
        teamlist = []
        for l in teams:
            ld = dict(zip(teamtable, l))
            team = Team(ld['name'], ld['coach_id'], ld['coach'],ld['id'])
            teamlist.append(team)
        return teamlist, total

    def get_teams_by(self, key, var, limit, offset):
        skey = str(key) + '%'

        query = """SELECT count(teams.id)
                        FROM teams,countries WHERE teams.name LIKE %s AND 
                            countries.id=teams.coach_id"""
        self.cur.execute(query, (skey,))
        total = self.cur.fetchone()[0]

        query = """SELECT teams.id, teams.name, teams.coach_id, countries.name
                        FROM teams,countries WHERE teams.name LIKE %s AND 
                            countries.id=teams.coach_id ORDER BY teams.name
                            LIMIT %s OFFSET %s"""
        self.cur.execute(query, (skey,limit, offset))
        teams = self.cur.fetchall()
        print('teams:', teams)
        teamlist = []
        for l in teams:
            ld = dict(zip(teamtable, l))
            team = Team(ld['name'], ld['coach_id'], ld['coach'],ld['id'])
            teamlist.append(team)
        return teamlist, total

