from flask import url_for

countrytable = ['id', 'name', 'code']

class Country:
    '''
    Country Object

    **flagpath** is url for country flag. The filename generated based on country code.

    :param name: country name
    :param code: ISO alpha-2 code
    '''
    def __init__(self, name, code, _id=None):
        self._id = _id
        self.name = name
        self.code = code
        self.flagpath = url_for('static', filename='data/flags/'+code.lower()+'.png')

    def getAttrs(self):
        '''returns attributes of the Country class as a dictionary. Keys are 
        taken from the countrytable and corresponding values are taken from 
        the Country object attributes.
        
        :returns: attributes of the Country object as a dictionary.
        :rtype: dict'''
        return (dict(zip(countrytable, (self._id, self.name, self.code))))

class Countries:
    '''the Countries object provides functions for database connections of *countries* table.
    
    :param conn: psycopg2 connection object
    :param cur: psycopg2 cursor object
    '''
    def __init__(self, conn, cur):
        self.conn = conn
        self.cur = cur
        self.last_key = None

    def add_country(self, country):
        '''inserts a new row to the *countries* table with values of the given country attributes.
        
        :param country: new Country object
        '''
        print("addcountry ", country)
        query = """INSERT INTO countries (name, code) 
                                    values (%s,%s)""" 

        self.cur.execute(query, (country.name, country.code))
        self.conn.commit()

    def delete_country(self, _id):
        '''deletes the row from the countries table whose id is given _id.

        :param _id: id of the row - int
        '''
        query = """DELETE FROM countries WHERE id=%s"""
        # variables should be in tuple object
        self.cur.execute(query, (_id,))
        self.conn.commit()

    def update_country(self, _id, new):
        '''Updates the row from the countries table whose id is given _id. 
        The new values is taken from given *new* Country object.

        :param _id: id of the row - int
        :param new: Country object with new values
        '''
        query = """UPDATE countries SET name=%s, code=%s
                    WHERE id=%s"""
        self.cur.execute(query, (new.name, new.code, _id))
        self.conn.commit()

    def get_country(self,_id):
        '''Returns :class:`final4.models.country.Country` object with values from
        the *countries* table IF there is a record has a given _id ELSE returns None.

        :param _id: id of the row - int
        :returns: country or None
        :rtype: :class:`final4.models.country.Country` object or None
        '''
        query = """SELECT * FROM countries WHERE id=%s"""
        self.cur.execute(query, (_id,))
        # c: country attributes array
        # cd: country dictionary
        c = self.cur.fetchone()
        if c:
            cd = dict(zip(countrytable, c))
            country = Country(cd['name'], cd['code'], cd['id'])
            return country
        else:
            return None

    def get_country_name(self, name):
        '''Returns :class:`final4.models.country.Country` object with values from
        the *countries* table IF there is a record has a given name ELSE returns None.

        :param name: country name - int
        :returns: country or None
        :rtype: :class:`final4.models.country.Country` object or None
        '''
        query = """SELECT * FROM countries WHERE name=%s"""
        self.cur.execute(query, (name,))
        # c: country attributes array
        # cd: country dictionary
        c = self.cur.fetchone()
        if c:
            cd = dict(zip(countrytable, c))
            country = Country(cd['name'], cd['code'], cd['id'])
            return country
        else:
            return None

    def get_countries(self, limit=100, offset=0):
        '''Returns result list and total number of results.
        Returning list is list of :class:`final4.models.country.Country` object. All objects
        filled up with values from the rows of the `countries` table.
        Also returns the total number of the result.
        
        :param limit: maximum number of the result
        :param offset: skip beginning of the result
        :returns: countrylist, total
        :rtype: list, int
        '''
        query = """SELECT count(countries.id) 
                    FROM countries 
                    """
        self.cur.execute(query)
        total = self.cur.fetchone()[0]

        query = """SELECT * 
                    FROM countries 
                    ORDER BY name 
                    LIMIT %s OFFSET %s"""
        self.cur.execute(query, (limit, offset))
        countries = self.cur.fetchall()
        countrylist = []
        for c in countries:
            cd = dict(zip(countrytable, c))
            print (cd)
            country = Country(cd['name'], cd['code'], cd['id'])
            countrylist.append(country)
        return countrylist, total

    def get_countries_by(self, attrib, key, limit=100, offset=0):
        '''Returns result list and total number of result.
        Returning list is list of  :class:`final4.models.country.Country` object. All objects
        filled up with values from the rows of the `countries` table. 
        
        The return list made up by **filtered results** with given parameters.
       
        :param limit: maximum number of the result
        :param offset: skip beginning of the result
        
        :returns: countrylist, total
        :rtype: list, int
        '''
        '''
        get countries from countries table which given 'var' attribute starts with given 'key' value
        '''
        skey = str(key) + '%'
        print(skey)
        query = """SELECT count(countries.id) 
                    FROM countries 
                    WHERE name LIKE %s 
                    """
        self.cur.execute(query, (skey,))
        total = self.cur.fetchone()[0]
        
        query = """SELECT * 
                    FROM countries 
                    WHERE name LIKE %s 
                    ORDER BY name
                    LIMIT %s OFFSET %s"""
        self.cur.execute(query, (skey, limit, offset))
        countries = self.cur.fetchall()
        print('countries:', countries)
        countrylist = []
        for c in countries:
            cd = dict(zip(countrytable, c))
            country = Country(cd['name'], cd['code'], cd['id'])
            countrylist.append(country)
        return countrylist, total

