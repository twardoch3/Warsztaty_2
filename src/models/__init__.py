from clcrypto import password_hash, generate_salt


class User:
    __id = None
    username = None
    __hashed_password = None
    email = None

    def __init__(self):
        self.__id = -1
        self.username = ""
        self.email = ""
        self.__hashed_password = ""

    @property
    def id(self):
        return self.__id

    @property
    def hashed_password(self):
        return self.__hashed_password

    @hashed_password.setter
    def hashed_password(self, dict_pass_salt):
        self.__hashed_password = password_hash(dict_pass_salt["password"], dict_pass_salt["salt"])

    def save_to_db(self, cursor):
        if self.__id == -1:
            sql = """INSERT INTO users(username, email, hashed_password)
            VALUES (%s, %s, %s) RETURNING id;"""
            values = (self.username, self.email, self.hashed_password)
            cursor.execute(sql, values)
            self.__id = cursor.fetchone()['id']
            return True
        else:
            sql = """UPDATE Users SET hashed_password=%s
            WHERE username=%s"""
            values = (self.hashed_password, self.username)
            cursor.execute(sql, values)
            return True

    @staticmethod
    def load_user_by_username(cursor, username):
        sql = "SELECT id, username, email, hashed_password FROM users WHERE username=%s"
        cursor.execute(sql, (username,))
        data = cursor.fetchone()
        if data:
            loaded_user = User()
            loaded_user.__id = data['id']
            loaded_user.username = data['username']
            loaded_user.email = data['email']
            loaded_user.__hashed_password = data['hashed_password']
            return loaded_user
        else:
            return None

    @staticmethod
    def load_all_users(cursor):
        sql = "SELECT id, username, email, hashed_password FROM Users"

        ret = []
        cursor.execute(sql)
        for row in cursor.fetchall():
            loaded_user = User()
            loaded_user.__id = row['id']  # jestesmy w srodku klasy dlatego to jest mozliwe
            loaded_user.username = row['username']
            loaded_user.email = row['email']
            loaded_user.__hashed_password = row['hashed_password']
            ret.append(loaded_user)
        return ret

    def delete(self, cursor):
        sql = "DELETE FROM Users WHERE id=%s"
        cursor.execute(sql, (self.__id,))
        self.__id = -1
        return True


class Message:
    __id = None
    from_id = None
    to_id = None
    text = None
    creation_date = None

    def __init__(self):
        self.__id = -1
        self.from_id = None
        self.to_id = None
        self.text = ""
        self.creation_date = None

    @property
    def id(self):
        return self.__id

    @staticmethod
    def load_message_by_id(cursor, message_id):
        sql = "SELECT id, from_id, to_id, text, creation_date FROM Message where id=%s"
        cursor.execute(sql, (message_id,))
        data = cursor.fetchone()
        if data:
            loaded_message = Message()
            loaded_message.__id = data['id']
            loaded_message.from_id = data['from_id']
            loaded_message.to_id = data['to_id']
            loaded_message.text = data['text']
            loaded_message.creation_date = data['creation_date']
            return loaded_message
        else:
            return None

    @staticmethod
    def load_all_messages_for_user(cursor, username):
        sql = """SELECT message.id, from_id, to_id, text, creation_date, u1.username as sender, u2.username as receiver FROM Message
                 inner join users u1 on u1.id=message.from_id inner join users u2 on u2.id=message.to_id
                 where u2.username=%s order by creation_date DESC; """

        cursor.execute(sql, (username,))
        ret = []
        for row in cursor.fetchall():
            loaded_message = Message()
            loaded_message.__id = row['id']  # jestesmy w srodku klasy dlatego to jest mozliwe
            loaded_message.from_id = row['from_id']
            loaded_message.to_id = row['to_id']
            loaded_message.text = row['text']
            loaded_message.creation_date = row['creation_date']
            loaded_message.sender = row['sender']  # nowy dynamiczny atrybut

            ret.append(loaded_message)
        return ret

    @staticmethod
    def load_all_messages(cursor):
        sql = "SELECT * FROM Message order by creation_date DESC; "
        ret = []
        cursor.execute(sql)
        for row in cursor.fetchall():
            loaded_message = Message()
            loaded_message.__id = row['id']
            loaded_message.from_id = row['from_id']
            loaded_message.to_id = row['to_id']
            loaded_message.text = row['text']
            loaded_message.creation_date = row['creation_date']
            ret.append(loaded_message)
        return ret

    def save_to_db(self, cursor):
        if self.__id == -1:
            sql = """INSERT INTO message(from_id, to_id, text, creation_date)
                     VALUES (%s, %s, %s, now()) RETURNING id;"""
            values = (self.from_id, self.to_id, self.text)
            cursor.execute(sql, values)
            self.__id = cursor.fetchone()['id']
            return True

    # delete receiver messages
    def delete(self, cursor):
        sql = "DELETE FROM Message WHERE id=%s"
        cursor.execute(sql, (self.__id,))
        self.__id = -1
        return True
