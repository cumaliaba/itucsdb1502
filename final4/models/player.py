playertable = ['id', 'name', 'country', 'age', 'playing_position']

class Player:
    def __init__(self, name, country, age,playing_position, _id=None):
        self._id=_id
        self.name = name
        self.country = country
        self.age = age
        self.playing_position = playing_position
        

    def getAttrs(self):
        return (dict(zip(playertable, (self._id, self.name, self.country,self.age,self.playing_position))))		
class Players:
    def __init__(self, conn, cur):
        self.conn = conn
        self.cur = cur
        self.last_key = None

    def add_player(self, player):
        print("addplayer",player)
        query = """INSERT INTO players (name, country,age,playing_position) 
                                    values (%s,%s,%s,%s)"""

        self.cur.execute(query,(player.name,player.country,player.age,player.playing_position))
        self.conn.commit()

    def delete_player(self, _id):
        query = "DELETE FROM players WHERE id=%s"""
        self.cur.execute(query,(_id,))
        self.conn.commit()

    def update_player(self, _id, new_player):
        query = """UPDATE players SET name='%s', country='%s', 
                    age='%s',playing_position='%s', WHERE id=%s"""

        self.cur.execute(query,(new_player.name,new_player.country,new_player.age,new_player.playing_position,_id))
        self.conn.commit()

    def get_player(self, _id):
        query = "SELECT * FROM players WHERE id=%s" 
        self.cur.execute(query,(_id,))
        p = self.cur.fetchone()
        if p:
            print (p)
            pd = dict(zip(playertable, p)) # player dict
            player = Player(pd['name'], pd['country'], pd['age'], pd['playing_position'],pd['id'])
            return player
        return None

    def get_players(self):
        query = "SELECT * FROM players ;"
        self.cur.execute(query)
        players = self.cur.fetchall()
        playerlist = []
        for p in players:
            pd = dict(zip(playertable, p))
            player = Player.fromDict(pd)
            playerlist.append(player)
            
        return playerlist
