awardtable = ['id', 'name']

class Award:
    '''Award object'''
    def __init__(self, name, _id=None):
        self._id = _id
        self.name = name

    def getAttrs(self):
        '''returns attributes of the Award class as a dictionary. Keys are 
        taken from the awardtable and corresponding values are taken from 
        the Award object attributes.
        
        :returns: attributes of the Award object as a dictionary.
        :rtype: dict'''
        return (dict(zip(awardtable, (self._id, self.name))))

        
class Awards:
    '''the Awards object provides functions for database connections of awards table.
    
    :param conn: psycopg2 connection object
    :param cur: psycopg2 cursor object
    '''
    def __init__(self, conn, cur):
        self.conn = conn
        self.cur = cur
        self.last_key = None

    def add_award(self, award):
        '''inserts a new row to the awards table with values of the given award attributes.
        
        :param award: new Award object
        '''
        query = """INSERT INTO awards (name) 
                                    values (%s)"""

        self.cur.execute(query, (award.name, ))
        self.conn.commit()

    def delete_award(self, _id):
        '''deletes the row from the awards table whose id is given _id.

        :param _id: id of the row - int
        '''
        query = "DELETE FROM awards WHERE id=%s"
        self.cur.execute(query, (_id,))
        self.conn.commit()

    def update_award(self, _id, new):
        '''Updates the row from the awards table whose id is given _id. 
        The new values is taken from given *new* Award object.

        :param _id: id of the row - int
        :param new: Award object with new values
        '''
        query = """UPDATE awards SET name=%s WHERE id=%s"""

        self.cur.execute(query, (new.name, _id))
        self.conn.commit()

        
    def get_award(self,_id):
        '''Returns :class:`final4.models.award.Award` object with values from
        the awards table IF there is a record has a given _id ELSE returns None.

        :param _id: id of the row - int
        :returns: award or None
        :rtype: :class:`final4.models.award.Award` object or None
        '''
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
        '''Returns result list and total number of results.
        Returning list is list of :class:`final4.models.award.Award` object. All objects
        filled up with values from the rows of the awards table.
        Also returns the total number of the result.
        
        :param limit: maximum number of the result
        :param offset: skip beginning of the result
        :returns: awardlist, total
        :rtype: list, int
        '''

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
        '''Returns result list and total number of result.
        Returning list is list of  :class:`final4.models.award.Award` object. All objects
        filled up with values from the rows of the awards table. 
        
        The return list made up by **filtered results** with given parameters.
       
        :param limit: maximum number of the result
        :param offset: skip beginning of the result
        
        :returns: awardlist, total
        :rtype: list, int
        '''
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
        '''Returns result list and total number of result.
        Returning list is list of  :class:`final4.models.award.Award` object. All objects
        filled up with values from the rows of the awards table. 
        
        The return list made up by **filtered results** with given parameters.
       
        :param limit: maximum number of the result
        :param offset: skip beginning of the result
        
        :returns: awardlist, total
        :rtype: list, int
        '''
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

