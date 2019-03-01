import unittest
from models import User
from db_run import DB


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
        cls.user = None
        cls.db = None






if __name__ == '__main__':
    unittest.main()


# u1 = User()
# u1.hashed_password = {'password': 'pas23', 'salt': 'er445'}
