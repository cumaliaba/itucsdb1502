#: corresponding key values of the User class attributes
usertable = ['id', 'username', 'password', 'email', 'role', 'lastlogin', 'regtime', 'online'] 

class User:
    '''User object'''
    def __init__(self, username, password, email, role='admin', 
            lastlogin=None, regtime=None, online=False):
        self.username = username
        self.password = password
        self.email = email
        self.role = role
        self.lastlogin = lastlogin
        self.regtime = regtime
        self.online = online

    @classmethod
    def fromDict(cls, ud):
        '''creates a new User object from given dictionary'''
        return cls(ud['username'], ud['password'], ud['email'], ud['role'], ud['lastlogin'], ud['regtime'], ud['online'])

    def getAttrs(self):
        '''returns all attributes of the User object as a tuple'''
        return (self.username, self.password, self.email, self.role,
                self.lastlogin, self.regtime, self.online)

class Users:
    '''the Users object provides functions for database connections of users table.
    
    :param conn: psycopg2 connection object
    :param cur: psycopg2 cursor object
    '''
    def __init__(self, conn, cur):
        self.conn = conn
        self.cur = cur
        self.last_key = None

    def add_user(self, user):
        '''inserts a new row to the users table with values of the given user attributes.

        :param user: new User object
        '''
        query = """INSERT INTO users (username, password, email, role,
                                    lastlogin, regtime, online) 
                                    values (%s,%s,%s,%s,%s,%s,%s);"""

        self.cur.execute(query, user.getAttrs())
        self.conn.commit()

    def delete_user(self, username):
        '''deletes the row from the users table whose username is given as parameter.

        :param username: username string
        '''
        query = "DELETE FROM users WHERE username=%s;"
        self.cur.execute(query, (username,))
        self.conn.commit()

    def update_user(self, username, user):
        '''updates the row from the users table whose username is given **username**. 
        The new values is taken from given **user**.

        :param username: username string
        :param user: User object with new values
        '''
        args = user.getAttrs() + (username,)
        query = """UPDATE users SET username=%s, password=%s, 
                    email=%s,role=%s, lastlogin=%s, regtime=%s, 
                    online=%s WHERE username=%s;"""

        self.cur.execute(query, args)
        self.conn.commit()

    def get_user(self, username):
        '''returns :class:`final4.models.user.User` object with values from the users table IF there is a record has a given username ELSE returns None.

        :param username: username string
        :returns: user or None
        :rtype: :class:`final4.models.user.User` object or None
        '''
        query = "SELECT * FROM users WHERE username=%s;"
        self.cur.execute(query, (username,))
        u = self.cur.fetchone()
        if u:
            print (u)
            ud = dict(zip(usertable, u)) # user dict
            user = User.fromDict(ud)
            print (user.email)
            return user
        return None

    def get_users(self):
        '''returns list of :class:`final4.models.user.User` object. All objects filled up with values from the rows of the users table.

        :returns: userlist
        :rtype: list
        '''
        query = "SELECT * FROM users;"
        self.cur.execute(query)
        users = self.cur.fetchall()
        userlist = []
        print (users)
        for u in users:
            print(u)
            ud = dict(zip(usertable, u))
            user = User.fromDict(ud)
            userlist.append(user)
            print (userlist)
        return userlist
