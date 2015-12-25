from flask import url_for

#: corresponding key values of the League class attributes
coachtable = ['id', 'name', 'surname', 'country_id', 'country']

class Coach:
    '''Coach object'''
    def __init__(self, name, surname, country_id, country=None, _id=None):
        self._id = _id
        self.name = name
        self.surname = surname
        self.country_id = country_id
        self.country = country
    
    def img_path(self, _id=None):
        '''returns the url of the image of the coach.
        The image url generated based on _id value.
        
        :returns: image url
        :rtype: string
        '''
        if _id==None and self._id==None:
            return url_for('static',filename='.') + 'data/img/coaches/not_available.png'
        if _id:
            return url_for('static',filename='.') + 'data/img/coaches/' + str(_id) + '.png'
        else:
            return url_for('static',filename='.') +'data/img/coaches/' + str(self._id) + '.png'

    def getAttrs(self):
        '''returns attributes of the Coach object as a dictionary. Keys are 
        taken from the *coachtable* and corresponding values are taken from 
        the Coach object attributes.
        
        :returns: attributes of the Coach object as a dictionary.
        :rtype: dict'''
        return (dict(zip(coachtable, (self._id, self.name, self.surname, self.country_id, self.country))))

class Coaches:
    '''the Coaches object provides functions for database connections of coaches table.
    
    :param conn: psycopg2 connection object
    :param cur: psycopg2 cursor object
    '''
    def __init__(self, conn, cur):
        self.conn = conn
        self.cur = cur
        self.last_key = None

    def add_coach(self, coach):
        '''inserts a new row to the coaches table with values of the given coach attributes.
        
        :param coach: new Coach object
        '''
        print("addcoach ", coach)
        query = """INSERT INTO coaches (name, surname, country_id) 
                                    values (%s,%s,%s) RETURNING id""" 

        self.cur.execute(query, (coach.name, coach.surname, coach.country_id))
        insert_id = self.cur.fetchone()[0]
        self.conn.commit()
        return insert_id

    def delete_coach(self, _id):
        '''deletes the row from the *coaches* table whose id is given *_id*.

        :param _id: id of the row - int
        '''
        query = """DELETE FROM coaches WHERE id=%s"""
        # variables should be in tuple object
        self.cur.execute(query, (_id,))
        self.conn.commit()

    def update_coach(self, _id, new):
        '''Updates the row from the *coaches* table whose id is given _id. 
        The new values is taken from given *new* Coach object.

        :param _id: id of the row - int
        :param new: Coach object with new values
        '''
        print('update_coach')
        query = """UPDATE coaches SET name=%s, surname=%s, country_id=%s
                    WHERE id=%s"""
        self.cur.execute(query, (new.name, new.surname, new.country_id, _id))
        self.conn.commit()

    def get_coach(self,_id):
        '''Returns :class:`final4.models.coach.Coach` object with values from
        the *coaches* table IF there is a record has a given _id ELSE returns None.

        :param _id: id of the row - int
        :returns: coach or None
        :rtype: :class:`final4.models.coach.Coach` object or None
        '''
        query = """SELECT coaches.id, coaches.name, coaches.surname, countries.id, countries.name
                        FROM coaches,countries
                        WHERE coaches.id=%s AND countries.id=coaches.country_id
                        ORDER BY coaches.name
                        """
        self.cur.execute(query, (_id,))
        l = self.cur.fetchone()
        if l:
            ld = dict(zip(coachtable, l[:len(coachtable)]))
            coach = Coach(ld['name'], ld['surname'], ld['country_id'], ld['country'], ld['id'])
            return coach
        else:
            return None

    def get_coaches(self, limit=100, offset=0):
        '''Returns result list and total number of results.
        Returning list is list of :class:`final4.models.coach.Coach` object. All objects
        filled up with values from the rows of the *coaches* table.
        Also returns the total number of the result.
        
        :param limit: maximum number of the result
        :param offset: skip beginning of the result
        :returns: coachlist, total
        :rtype: list, int
        '''
        query = """SELECT count(coaches.id)
                        FROM coaches,countries WHERE countries.id=coaches.country_id
                          """
        self.cur.execute(query)
        total = self.cur.fetchone()[0]

        query = """SELECT coaches.id, coaches.name, coaches.surname, countries.id, countries.name 
                        FROM coaches,countries WHERE countries.id=coaches.country_id
                          ORDER BY coaches.name LIMIT %s OFFSET %s"""
        self.cur.execute(query, (limit, offset))
        coaches = self.cur.fetchall()
        coachlist = []
        for l in coaches:
            ld = dict(zip(coachtable, l))
            coach = Coach(ld['name'], ld['surname'], ld['country_id'], ld['country'],ld['id'])
            coachlist.append(coach)
        return coachlist, total

    def get_coaches_by(self, attrib, search_key, limit=100, offset=0):
        '''Returns result list and total number of result.
        Returning list is list of  :class:`final4.models.coach.Coach` object. All objects
        filled up with values from the rows of the *coaches* table. 
        
        The return list made up by **filtered results** with given parameters.
       
        :param limit: maximum number of the result
        :param offset: skip beginning of the result
        
        :returns: coachlist, total
        :rtype: list, int
        '''
        skey = str(search_key)
        
        query = """SELECT count(coaches.id)
                        FROM coaches,countries WHERE coaches.{attrib}=%s AND 
                            countries.id=coaches.country_id""".format(attrib=attrib)
        self.cur.execute(query, (skey,))
        total = self.cur.fetchone()[0]
        
        query = """SELECT coaches.id, coaches.name, coaches.surname, coaches.country_id, countries.name
                        FROM coaches,countries WHERE coaches.{attrib}=%s AND 
                            countries.id=coaches.country_id ORDER BY coaches.name 
                            LIMIT %s OFFSET %s""".format(attrib=attrib)
        self.cur.execute(query, (skey, limit, offset))
        coaches = self.cur.fetchall()
        print('coaches:', coaches)
        coachlist = []
        for l in coaches:
            ld = dict(zip(coachtable, l))
            coach = Coach(ld['name'], ld['surname'], ld['country_id'], ld['country'],ld['id'])
            coachlist.append(coach)
        return coachlist, total

    def get_coaches_search_by(self, attrib, search_key, limit=100, offset=0):
        '''Returns result list and total number of result.
        Returning list is list of  :class:`final4.models.coach.Coach` object. All objects
        filled up with values from the rows of the *coaches* table. 
        
        The return list made up by **filtered results** with given parameters.
       
        :param limit: maximum number of the result
        :param offset: skip beginning of the result
        
        :returns: coachlist, total
        :rtype: list, int
        '''
        skey = str(search_key) + '%'
        
        query = """SELECT count(coaches.id)
                        FROM coaches,countries WHERE coaches.{attrib} LIKE %s AND 
                            countries.id=coaches.country_id""".format(attrib=attrib)
        self.cur.execute(query, (skey,))
        total = self.cur.fetchone()[0]
        
        query = """SELECT coaches.id, coaches.name, coaches.surname, coaches.country_id, countries.name
                        FROM coaches,countries WHERE coaches.{attrib} LIKE %s AND 
                            countries.id=coaches.country_id ORDER BY coaches.name 
                            LIMIT %s OFFSET %s""".format(attrib=attrib)
        self.cur.execute(query, (skey, limit, offset))
        coaches = self.cur.fetchall()
        print('coaches:', coaches)
        coachlist = []
        for l in coaches:
            ld = dict(zip(coachtable, l))
            coach = Coach(ld['name'], ld['surname'], ld['country_id'], ld['country'],ld['id'])
            coachlist.append(coach)
        return coachlist, total

