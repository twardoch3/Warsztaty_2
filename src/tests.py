#testowanie
import unittest
#from manage_users import users_list
from db_run import DB
from models import User
from clcrypto import generate_salt, password_hash


class Test_1(unittest.TestCase):

    def setUp(self):
        print('password_hash')
        self.password = 'lk9kiuy$yui'
        self.salt1 = 'vf33wWR'
        self.salt2 = 'vf33wWRdsdsdsdswewdel45453433ertrteterwee'
        #print(password_hash(self.password, salt=self.salt2))

    def test_salt(self):
        self.assertEqual(len(generate_salt()), 16)
        self.assertNotIn('?', generate_salt())
        self.assertNotIn(',', generate_salt())

    def pswd_hash_salt_none(self):
        self.assertEqual(len(password_hash(self.password)), 16 + 64)
        self.assertNotIn('?', password_hash(self.password))
        self.assertNotIn('.', password_hash(self.password))
        self.assertNotIn('=', password_hash(self.password))

    def pswd_hash_salt_lt_16(self):
        self.assertEqual(len(password_hash(self.password, )), 16 + 64)
        self.assertNotIn('?', password_hash(self.password, salt=self.salt1))
        self.assertNotIn('-', password_hash(self.password, salt=self.salt1))
        self.assertNotIn(';', password_hash(self.password, salt=self.salt1))
        self.assertEqual(password_hash(self.password, salt=self.salt1)[0:4],'vf33')
        self.assertEqual(password_hash(self.password, salt=self.salt1)[9:13], 'aaaa')

    def pswd_hash_salt_gt_16(self):
        self.assertEqual(len(password_hash(self.password, )), 16 + 64)
        self.assertNotIn('?', password_hash(self.password, salt=self.salt2))
        self.assertNotIn('-', password_hash(self.password, salt=self.salt2))
        self.assertNotIn(';', password_hash(self.password, salt=self.salt2))
        self.assertEqual(password_hash(self.password, salt=self.salt1)[15],self.salt2[15])
        self.assertNotEqual(password_hash(self.password, salt=self.salt1)[17:29], self.salt2[17:21] )


if __name__ == '__main__':
    unittest.main()
