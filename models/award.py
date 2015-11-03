awardtable = ['id', 'name', 'playerID', 'seasonID']

class Award:
    def __init__(self, name, playerid, seasonid, id=None):
        self.id = id
        self.name = name
        self.playerID = playerid
        self.seasonID = seasonid
        
class Awards:
    def __init__(self, conn, cur):
        self.conn = conn
        self.cur = cur
        self.last_key = None

    def add_award(self, award):
        query = """INSERT INTO awards (name, playerid, seasonid) 
                                    values ('%s','%s','%s','%s')""" % (award.id, award.name, award.playerID, award.seasonID)

        self.cur.execute(query)
        self.conn.commit()

    def delete_award(self, id):
        query = "DELETE FROM awards WHERE id='%s'" % id
        self.cur.execute(query)
        self.conn.commit()

    def update_award(self, award):
        query = """UPDATE awards SET name='%s', 
                    playerID='%s',seasonID='%s' WHERE id='%s'""" % (award.name, award.playerID, award.seasonID, award.id)

        self.cur.execute(query)
        self.conn.commit()

    def get_awards(self):
        query = "SELECT * FROM awards;"
        self.cur.execute(query)
        awards = self.cur.fetchall()
        awardl = []
        for a in awards:
            ad = dict(zip(awardtable, a))
            award = Award(ad['name'], ad['playerID'],ad['seasonID'], ad['id'])
            awardl.append(award)
   
        return awardl
