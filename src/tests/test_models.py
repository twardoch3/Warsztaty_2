import unittest
from models import User, Message
from db_run import DB
from clcrypto import ALPHABET
import random


class Test_2(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user = User()

    def test_id(self):
        self.assertEqual(self.user.id, -1)

    def test_pwd_hash(self):
        hash1 = 'er445aaaaaaaaaaa2e15685bc7def4f2aa8da56e7a5e47f62a9d636fa8ea175abf9eb13c427bf336'
        self.user.hashed_password = {'password': 'pas23', 'salt': 'er445'}
        self.assertEqual(self.user.hashed_password, hash1)
        hash2 = '666777DEFGaa88990f5bd282ac89105f24e6ba85e1eb4c3ed417aecd5d223fc753a9d3ab6ec87178'
        self.user.hashed_password = {'password': 'pass1', 'salt': hash2[:16]}
        self.assertEqual(self.user.hashed_password, hash2)

    @classmethod
    def tearDownClass(cls):
        cls.user = None

class Test_2_DB(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user = User()
        cls.user.username = 'userA111'
        cls.user.email = 'user11@gmail.com'
        cls.user.hashed_password = {'password': 'pas23', 'salt': 'er445'}
        cls.db = DB()


    def test_user_db(self):
        connection = self.db.connect_db()
        with self.db.db_cursor(connection) as curs:
            #save
            save = self.user.save_to_db(curs)
            self.assertTrue(save)
            #load
            loaded_user = self.user.load_user_by_username(curs, self.user.username)
            self.assertTrue(loaded_user)
            self.assertEqual(loaded_user.username, self.user.username)
            self.assertEqual(loaded_user.email, self.user.email)
            #self.assertEqual(loaded_user.hashed_password, self.user.hashed_password)
            self.assertNotEqual(loaded_user.id, -1)
            #update
            loaded_user.hashed_password = {'password': 'xxx123', 'salt': None}
            #print(loaded_user.hashed_password)
            self.assertTrue(loaded_user.save_to_db(curs))  #update/change password
            self.assertEqual(loaded_user.hashed_password, (User.load_user_by_username(curs, loaded_user.username)).hashed_password)
            #delete
            self.assertTrue(loaded_user.delete(curs))
            self.assertFalse(User.load_user_by_username(curs, loaded_user.username))

        connection.commit()
        connection.close()

    @classmethod
    def tearDownClass(cls):
        del cls.user
        del cls.db


class Test_2_DB_all_users(unittest.TestCase):

    def setUp(self):
        self.db = DB()
        self.connection = self.db.connect_db()
        with self.db.db_cursor(self.connection) as curs:
            for i in range(10):
                self.u = User()
                self.u.username = 'user' + ('').join(random.choices(ALPHABET, k=3))
                self.u.email = str(self.u.username) + '@email.com'
                self.u.hashed_password = {'password': ('').join(random.choices(ALPHABET, k=6)), 'salt': None}
                #save
                save = self.u.save_to_db(curs)
            self.connection.commit()


    def test_load_all_users(self):
        with self.db.db_cursor(self.connection) as curs:
            all_users = User.load_all_users(curs)
            self.assertTrue(len(all_users), 10)
            self.assertIsInstance(all_users, list)
            self.assertIsInstance(all_users[1], User)
            self.assertIsInstance(all_users[6], User)
            self.assertIsInstance(all_users[9], User)


    def tearDown(self):
        with self.db.db_cursor(self.connection) as curs:
            all_users = User.load_all_users(curs)
            for u in all_users:
                u.delete(curs)
                self.connection.commit()

        self.connection.close()
        print(self.connection)


class Test_3_message(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.db = DB()
        cls.connection = cls.db.connect_db()
        cls.ids = []
        with cls.db.db_cursor(cls.connection) as curs:
            for i in range(2):
                u = User()
                u.username = 'user' + ('').join(random.choices(ALPHABET, k=3))
                u.email = str(u.username) + '@email.com'
                u.hashed_password = {'password': ('').join(random.choices(ALPHABET, k=6)), 'salt': None}
                u.save_to_db(curs)
                cls.ids.append(u.load_user_by_username(curs, u.username).id)  #user ids
            cls.connection.commit()

    def setUp(self):
        self.message = Message()
        self.message.from_id = self.ids[0]
        self.message.to_id = self.ids[1]
        self.message.text = 'test message 1'
        #self.message.date

    def test_id(self):
        self.assertEqual(self.message.id, -1)

    def test_add_message(self):
        with self.db.db_cursor(self.connection) as curs:
             save = self.message.save_to_db(curs)
             self.connection.commit()
        self.assertTrue(save)
        print(self.connection)

    def tearDown(self):
        del self.message


    #def test_delete_message
    #def test_load_message_by_id

    @classmethod
    def tearDownClass(cls):
        #usunac message i users
        cls.connection.close()
        #poprawic




if __name__ == '__main__':
    unittest.main()


