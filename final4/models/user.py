usertable = ['id', 'username', 'password', 'email', 'role', 'lastlogin', 'regtime', 'online']

class User:
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
        return cls(ud['username'], ud['password'], ud['email'], ud['role'], ud['lastlogin'], ud['regtime'], ud['online'])

    def getAttrs(self):
        return (self.username, self.password, self.email, self.role,
                self.lastlogin, self.regtime, self.online)

class Users:
    def __init__(self, conn, cur):
        self.conn = conn
        self.cur = cur
        self.last_key = None

    def add_user(self, user):
        query = """INSERT INTO users (username, password, email, role,
                                    lastlogin, regtime, online) 
                                    values (%s,%s,%s,%s,%s,%s,%s);"""

        self.cur.execute(query, user.getAttrs())
        self.conn.commit()

    def delete_user(self, username):
        query = "DELETE FROM users WHERE username=%s;"
        self.cur.execute(query, (username,))
        self.conn.commit()

    def update_user(self, key, user):
        args = user.getAttrs() + (key,)
        query = """UPDATE users SET username=%s, password=%s, 
                    email=%s,role=%s, lastlogin=%s, regtime=%s, 
                    online%s WHERE id=%s;"""

        self.cur.execute(query, args)
        self.conn.commit()

    def get_user(self, username):
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
