from flask import url_for
teamtable = ['id', 'name', 'country_id', 'country']

class Team:
    def __init__(self, name, country_id, country=None, _id=None):
        self._id = _id
        self.name = name
        self.country_id = country_id
        self.country = country
        self.photo = url_for('static', filename='data/teams/'+name.lower()+'.png')
    def getAttrs(self):
        return (dict(zip(teamtable, (self._id, self.name, self.country_id, self.country))))

class Teams:
    def __init__(self, conn, cur):
        self.conn = conn
        self.cur = cur
        self.last_key = None

    def add_team(self, team):
        print("addteam ", team)
        query = """INSERT INTO teams (name, country_id) 
                                    values (%s,%s)""" 

        self.cur.execute(query, (team.name, team.country_id))
        self.conn.commit()

    def delete_team(self, _id):
        query = """DELETE FROM teams WHERE id=%s"""
        self.cur.execute(query, (_id,))
        self.conn.commit()

    def update_team(self, _id, new):
        print('update_team')
        query = """UPDATE teams SET name=%s, country_id=%s
                    WHERE id=%s"""
        self.cur.execute(query, (new.name, new.country_id, _id))
        self.conn.commit()

    def get_team(self,_id):
        query = """SELECT teams.id, teams.name, countries.id, countries.name
                        FROM teams,countries
                        WHERE teams.id=%s AND countries.id=teams.country_id
                        ORDER BY teams.name
                        """
        self.cur.execute(query, (_id,))
        t = self.cur.fetchone()
        if t:
            td = dict(zip(teamtable, t[:len(teamtable)]))
            team = Team(td['name'], td['country_id'], td['country'], td['id'])
            return team
        else:
            return None

    def get_teams(self, limit=100, offset=0):

        query = """SELECT count(teams.id)
                        FROM teams,countries WHERE countries.id=teams.country_id
                          """
        self.cur.execute(query)
        total = self.cur.fetchone()[0]

        query = """SELECT teams.id, teams.name, countries.id, countries.name 
                        FROM teams,countries WHERE countries.id=teams.country_id
                          ORDER BY teams.name LIMIT %s OFFSET %s"""
        self.cur.execute(query, (limit, offset))
        teams = self.cur.fetchall()
        teamlist = []
        for t in teams:
            td = dict(zip(teamtable, t))
            team = Team(td['name'], td['country_id'], td['country'],td['id'])
            teamlist.append(team)
        return teamlist, total

    def get_teams_by(self, attrib, search_key, limit=100, offset=0):
        skey = str(search_key)

        query = """SELECT count(teams.id)
                        FROM teams,countries WHERE teams.{attrib}=%s AND 
                            countries.id=teams.country_id""".format(attrib=attrib)
        self.cur.execute(query, (skey,))
        total = self.cur.fetchone()[0]

        query = """SELECT teams.id, teams.name, teams.country_id, countries.name
                        FROM teams,countries WHERE teams.{attrib}=%s AND 
                            countries.id=teams.country_id ORDER BY teams.name
                            LIMIT %s OFFSET %s""".format(attrib=attrib)
        self.cur.execute(query, (skey,limit, offset))
        teams = self.cur.fetchall()
        print('teams:', teams)
        teamlist = []
        for t in teams:
            td = dict(zip(teamtable, t))
            team = Team(td['name'], td['country_id'], td['country'],td['id'])
            teamlist.append(team)
        return teamlist, total

    def get_teams_search_by(self, attrib, search_key, limit=100, offset=0):
        skey = str(search_key) + '%'
        query = """SELECT count(teams.id)
                        FROM teams,countries WHERE teams.{attrib} LIKE %s AND 
                            countries.id=teams.country_id""".format(attrib=attrib)
        self.cur.execute(query, (skey,))
        total = self.cur.fetchone()[0]

        query = """SELECT teams.id, teams.name, teams.country_id, countries.name
                        FROM teams,countries WHERE teams.{attrib} LIKE %s AND 
                            countries.id=teams.country_id ORDER BY teams.name
                            LIMIT %s OFFSET %s""".format(attrib=attrib)
        self.cur.execute(query, (skey,limit, offset))
        teams = self.cur.fetchall()
        print('teams:', teams)
        teamlist = []
        for t in teams:
            td = dict(zip(teamtable, t))
            team = Team(td['name'], td['country_id'], td['country'],td['id'])
            teamlist.append(team)
        return teamlist, total

