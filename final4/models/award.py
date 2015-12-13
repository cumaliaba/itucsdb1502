awardtable = ['id', 'name']

class Award:
    def __init__(self, name, _id=None):
        self._id = _id
        self.name = name

    def getAttrs(self):
        return (dict(zip(awardtable, (self._id, self.name))))

        
class Awards:
    def __init__(self, conn, cur):
        self.conn = conn
        self.cur = cur
        self.last_key = None

    def add_award(self, award):
        query = """INSERT INTO awards (name) 
                                    values (%s)"""

        self.cur.execute(query, (award.name, ))
        self.conn.commit()

    def delete_award(self, _id):
        query = "DELETE FROM awards WHERE id=%s"
        self.cur.execute(query, (_id,))
        self.conn.commit()

    def update_award(self, _id, new):
        '''
        new : Award object
        '''
        query = """UPDATE awards SET name=%s WHERE id=%s"""

        self.cur.execute(query, (new.name, _id))
        self.conn.commit()

        
    def get_award(self,_id):
        query = """SELECT awards.id, awards.name 
                        FROM awards
                        WHERE awards.id=%s
                        """
        self.cur.execute(query, (_id,))
        l = self.cur.fetchone()
        if l:
            ld = dict(zip(awardtable, l[:len(awardtable)]))
            award = Award(ld['name'], _id=ld['id'])
            return award
        else:
            return None

    def get_awards(self, limit=100, offset=0):

        query = """SELECT count(awards.id)
                        FROM awards
                     """
        self.cur.execute(query)
        total = self.cur.fetchone()[0]

        query = """SELECT awards.id, awards.name
                        FROM awards
			ORDER BY awards.name ASC LIMIT %s OFFSET %s
                        """

        self.cur.execute(query, (limit, offset))
        awards = self.cur.fetchall()
        awardlist = []
        for l in awards:
            ld = dict(zip(awardtable, l))
            award = Award(ld['name'], _id=ld['id'])
            awardlist.append(award)
        return awardlist, total

    def get_awards_by(self, attrib, search_key, limit=100, offset=0):
        skey = str(search_key)

        # WARNING !!! SQL INJECTION?
        query = """SELECT count(awards.id)
                        FROM awards 
                        WHERE awards.{attrib}=%s
                        """.format(attrib=attrib)
        self.cur.execute(query, (skey,))
        total = self.cur.fetchone()[0]

        # WARNING !!! SQL INJECTION?
        query = """SELECT awards.id, awards.name
                        FROM awards
                        WHERE awards.{attrib}=%s
			ORDER BY awards.name ASC LIMIT %s OFFSET %s
                        """.format(attrib=attrib)
        self.cur.execute(query, (skey,limit, offset))
        awards = self.cur.fetchall()
        print('awards:', awards)
        awardlist = []
        for l in awards:
            ld = dict(zip(awardtable, a))
            award = Award(ld['name'], _id=ld['id'])
            awardlist.append(award)
        return awardlist, total

    def get_awards_search_by(self, attrib, search_key, limit=100, offset=0):
        # convert search key to special sql search syntax that means
        # all matches that starts with search_key
        skey = str(search_key) + '%'
        # WARNING !!! SQL INJECTION?
        query = """SELECT count(awards.id)
                        FROM awards
                        WHERE awards.{attrib} LIKE %s
                        """.format(attrib=attrib)
        self.cur.execute(query, (skey,))
        total = self.cur.fetchone()[0]

        # WARNING !!! SQL INJECTION?
        query = """SELECT awards.id, awards.name
                        FROM awards
                        WHERE awards.{attrib} LIKE %s
			ORDER BY awards.name ASC LIMIT %s OFFSET %s
                        """.format(attrib=attrib)
        self.cur.execute(query, (skey,limit, offset))
        awards = self.cur.fetchall()
        print('awards:', awards)
        awardlist = []
        for l in awards:
            ld = dict(zip(awardtable, l))
            award = Award(ld['name'], _id=ld['id'])
            awardlist.append(award)
        return awardlist, total

