#testowanie
import unittest
#from manage_users import users_list
from db_run import DB
from models import User
from clcrypto import generate_salt, password_hash


class Test_1(unittest.TestCase):

    def setUp(self):
        print('password_hash')
        self.password = 'pass1234P'
        self.salt1 = 'vf33wWR'
        print(password_hash(self.password, salt=self.salt1))

    def test_salt(self):
        self.assertEqual(len(generate_salt()), 16)
        self.assertNotIn('?', generate_salt())
        self.assertNotIn(',', generate_salt())

    def pswd_hash_salt_none(self):
        self.assertGreater(len(password_hash(self.password)), 16)
        self.assertNotIn('?', password_hash(self.password))
        self.assertNotIn('.', password_hash(self.password))
        self.assertNotIn('=', password_hash(self.password))

    def pswd_hash_salt(self):
        self.assertGreater(len(password_hash(self.password, )), 16)
        self.assertNotIn('?', password_hash(self.password, salt=self.salt1))
        self.assertNotIn('-', password_hash(self.password, salt=self.salt1))
        self.assertNotIn(';', password_hash(self.password, salt=self.salt1))
        self.assertEqual(password_hash(self.password, salt=self.salt1)[0:4],'vf33')
        self.assertEqual(password_hash(self.password, salt=self.salt1)[9:13], 'aaaa')





if __name__ == '__main__':
    unittest.main()
