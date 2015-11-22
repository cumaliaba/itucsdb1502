playertable = ['id', 'name', 'country', 'age', 'playing_position']

class Player:
    def __init__(self, name, country, age,playing_position, id=None):
        self.name = name
        self.country = country
        self.age = age
        self.playing_position = playing_position
        self.id=id
		
class Players:
    def __init__(self, conn, cur):
        self.conn = conn
        self.cur = cur
        self.last_key = None

    def add_player(self, player):
        query = """INSERT INTO players (name, country, age,playing_position,id) 
                                    values ('%s','%s','%s','%s','%s')""" % player.getAttrs()

        self.cur.execute(query)
        self.conn.commit()

    def delete_player(self, name):
        query = "DELETE FROM players WHERE name='%s'" % name
        self.cur.execute(query)
        self.conn.commit()

    def update_player(self, key, player):
        args = player.getAttrs() + (key,)
        query = """UPDATE players SET name='%s', country='%s', 
                    age='%s',playing_position='%s',id='%s'""" % args

        self.cur.execute(query)
        self.conn.commit()

    def get_player(self, name):
        query = "SELECT * FROM players WHERE name='%s'" % name
        self.cur.execute(query)
        p = self.cur.fetchone()
        if p:
            print (p)
            pd = dict(zip(playertable, p)) # player dict
            player = Player(pd['name'], pd['country'], pd['age'], pd['playing_position'],pd['id'])
            print (player.age)
            return player
        return None

    def get_players(self):
        query = "SELECT * FROM players;"
        self.cur.execute(query)
        players = self.cur.fetchall()
        playerlist = []
        for p in players:
            pd = dict(zip(playertable, p))
            player = Player.fromDict(pd)
            playerlist.append(player)
            
        return playerlist
