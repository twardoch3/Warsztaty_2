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

class Test_2_DB_user(unittest.TestCase):

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


class Test_3_message_DB(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.db = DB()
        cls.connection = cls.db.connect_db()
        cls.ids = []
        cls.msg_id = []
        cls.unames = []
        with cls.db.db_cursor(cls.connection) as curs:
            for i in range(2):
                u = User()
                u.username = 'user' + ('').join(random.choices(ALPHABET, k=3))
                u.email = str(u.username) + '@email.com'
                u.hashed_password = {'password': ('').join(random.choices(ALPHABET, k=6)), 'salt': None}
                u.save_to_db(curs)
                cls.ids.append(u.load_user_by_username(curs, u.username).id)  #user ids
                cls.unames.append(u.username)
            cls.connection.commit()


    def setUp(self):
        self.message = Message()
        self.message.from_id = self.ids[0]
        self.message.to_id = self.ids[1]
        self.message.text = 'test message 1'
        # print(cls.message.id)
        #self.message.date

    def test_id(self):
        self.assertEqual(self.message.id, -1)

    def test_add_load_message(self):
        with self.db.db_cursor(self.connection) as curs:
             #add message
             save = self.message.save_to_db(curs)
             self.connection.commit()
             self.msg_id.append(self.message.id) # append zmienia zmienna klasowa cls.msg_id = []
             self.assertTrue(save)
             # load message by id
             loaded_message = self.message.load_message_by_id(curs, self.message.id)
             print(loaded_message.text)
             self.assertIsInstance(loaded_message, Message)
             self.assertEqual(loaded_message.text, self.message.text)
             self.assertEqual(loaded_message.from_id, self.message.from_id)
             self.assertEqual(loaded_message.to_id, self.message.to_id)


    def test_delete_message(self):
        with self.db.db_cursor(self.connection) as curs:
            loaded_message = self.message.load_message_by_id(curs, self.msg_id[0])
            self.assertIsInstance(loaded_message, Message)
            delete = loaded_message.delete(curs)
            self.connection.commit()
            self.assertTrue(delete)
            self.assertFalse(self.message.load_message_by_id(curs, self.message.id))


    def tearDown(self):
         del self.message


    @classmethod
    def tearDownClass(cls):
        with cls.db.db_cursor(cls.connection) as curs:
            for uname in cls.unames:
                user = User.load_user_by_username(curs, uname)
                user.delete(curs)
                cls.connection.commit()
        cls.connection.close()
        print(cls.connection)


class Test_3_all_messages_DB(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.db = DB()
        cls.connection = cls.db.connect_db()
        cls.u_ids = []
        cls.msg_id = []
        cls.unames = []
        with cls.db.db_cursor(cls.connection) as curs:
            #create temporary users
            for i in range(5):
                u = User()
                u.username = 'user' + ('').join(random.choices(ALPHABET, k=3))
                u.email = str(u.username) + '@email.com'
                u.hashed_password = {'password': ('').join(random.choices(ALPHABET, k=6)), 'salt': None}
                u.save_to_db(curs)
                cls.u_ids.append(u.load_user_by_username(curs, u.username).id)  #user ids
                cls.unames.append(u.username)
            cls.connection.commit()
            #create temporary messages
            for i in range(5):
                message = Message()
                message.from_id = random.choice(cls.u_ids)
                message.to_id = random.choice(cls.u_ids[1:])
                message.text = 'test message ' + ('').join(random.choices(ALPHABET, k=6))
                # print(cls.message.id)
                # self.message.date !
                save = message.save_to_db(curs)
                cls.connection.commit()
                cls.msg_id.append(message.id)  # append zmienia zmienna klasowa cls.msg_id = []
            # User 1 messages
            for i in range(5):
                message = Message()
                message.from_id = random.choice(cls.u_ids)
                message.to_id = cls.u_ids[0]
                message.text = 'test message ' + ('').join(random.choices(ALPHABET, k=6))
                # print(cls.message.id)
                # self.message.date !
                save = message.save_to_db(curs)
                cls.connection.commit()
                cls.msg_id.append(message.id)
            print(cls.msg_id)

    def setUp(self):
        self.message = Message()

    def test_load_all_messages(self):
        with self.db.db_cursor(self.connection) as curs:
            all_messages = self.message.load_all_messages(curs)
            self.assertIsInstance(all_messages, list)
            self.assertEqual(len(all_messages), 10)
            self.assertIn(all_messages[0].id, self.msg_id)
            self.assertIsInstance(all_messages[1], Message)
            self.assertIn(all_messages[5].id, self.msg_id)


    def test_load_all_messages_for_user(self):
        with self.db.db_cursor(self.connection) as curs:
            #User 1
            u1_messages = self.message.load_all_messages_for_user(curs, self.unames[0])
            self.assertIsInstance(u1_messages, list)
            self.assertEqual(len(u1_messages), 5)
            for i in range(len(u1_messages)):
                self.assertEqual(u1_messages[i].to_id, self.u_ids[0])


    def tearDown(self):
        del self.message

    @classmethod
    def tearDownClass(cls):
        #delete messages and users
        with cls.db.db_cursor(cls.connection) as curs:
            for uname in cls.unames:
                user = User.load_user_by_username(curs, uname)
                user.delete(curs)  #on delete cascade usuwa tez messages
                cls.connection.commit()
        cls.connection.close()
        print(cls.connection)



if __name__ == '__main__':
    unittest.main()




