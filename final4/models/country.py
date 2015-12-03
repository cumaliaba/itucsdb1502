from flask import url_for

countrytable = ['id', 'name', 'code']

class Country:
    def __init__(self, name, code, _id=None):
        '''
        Constructor function for country object,
        params:
            name: country name
            code: ISO alpha-3 code
        '''
        self._id = _id
        self.name = name
        self.code = code
        self.flagpath = url_for('static', filename='data/flags/'+code+'.PNG')

    def getAttrs(self):
        return (dict(zip(countrytable, (self._id, self.name, self.code))))

class Countries:
    def __init__(self, conn, cur):
        self.conn = conn
        self.cur = cur
        self.last_key = None

    def add_country(self, country):
        print("addcountry ", country)
        query = """INSERT INTO countries (name, code) 
                                    values (%s,%s)""" 

        self.cur.execute(query, (country.name, country.code))
        self.conn.commit()

    def delete_country(self, _id):
        query = """DELETE FROM countries WHERE id=%s"""
        # variables should be in tuple object
        self.cur.execute(query, (_id,))
        self.conn.commit()

    def update_country(self, _id, new):
        '''
        new : country object
        '''
        query = """UPDATE countries SET name=%s, code=%s
                    WHERE id=%s"""
        self.cur.execute(query, (new.name, new.code, _id))
        self.conn.commit()

    def get_country(self,_id):
        query = """SELECT * FROM countries WHERE id=%s ORDER BY name"""
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

    def get_countries(self):
        query = "SELECT * FROM countries ORDER BY name"
        self.cur.execute(query)
        countries = self.cur.fetchall()
        countrylist = []
        for c in countries:
            cd = dict(zip(countrytable, c))
            print (cd)
            country = Country(cd['name'], cd['code'], cd['id'])
            countrylist.append(country)
        return countrylist

    def get_countries_by(self, key, var):
        '''
        get countries from DB which given 'var' attribute starts with given 'key' value
        '''
        skey = str(key) + '%'
        query = "SELECT * FROM countries WHERE name LIKE %s ORDER BY name";
        self.cur.execute(query, (skey,))
        countries = self.cur.fetchall()
        print('countries:', countries)
        countrylist = []
        for c in countries:
            cd = dict(zip(countrytable, c))
            country = Country(cd['name'], cd['code'], cd['id'])
            countrylist.append(country)
        return countrylist

