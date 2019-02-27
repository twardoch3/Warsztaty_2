#testowanie
import unittest
#from manage_users import users_list
from db_run import DB
from models import User
from clcrypto import generate_salt, password_hash, check_password


class Test_1(unittest.TestCase):

    def setUp(self):
        self.password = 'lk9kiuy$yui'
        self.salt1 = 'vf33wWR'
        self.salt2 = 'vf33wWRdsdsdsdswewdel45453433ertrteterwee'
        #print(password_hash(self.password, salt=self.salt2))

    def test_salt(self):
        self.assertEqual(len(generate_salt()), 16)
        self.assertNotIn('?', generate_salt())
        self.assertNotIn(',', generate_salt())

    def test_pswd_hash_salt_none(self):
        self.assertEqual(len(password_hash(self.password)), 16 + 64)
        self.assertNotIn('?', password_hash(self.password))
        self.assertNotIn('.', password_hash(self.password))
        self.assertNotIn('=', password_hash(self.password))

    def test_pswd_hash_salt_lt_16(self):
        self.assertEqual(len(password_hash(self.password, )), 16 + 64)
        self.assertNotIn('?', password_hash(self.password, salt=self.salt1))
        self.assertNotIn('-', password_hash(self.password, salt=self.salt1))
        self.assertNotIn(';', password_hash(self.password, salt=self.salt1))
        self.assertEqual(password_hash(self.password, salt=self.salt1)[0:4],'vf33')
        self.assertEqual(password_hash(self.password, salt=self.salt1)[9:16], 'aaaaaaa')

    def test_pswd_hash_salt_gt_16(self):
        l = len(self.salt2)
        self.assertEqual(len(password_hash(self.password, )), 16 + 64)
        self.assertNotIn('?', password_hash(self.password, salt=self.salt2))
        self.assertNotIn('-', password_hash(self.password, salt=self.salt2))
        self.assertNotIn(';', password_hash(self.password, salt=self.salt2))
        self.assertEqual(password_hash(self.password, salt=self.salt2)[10:15],self.salt2[10:15])
        self.assertNotEqual(password_hash(self.password, salt=self.salt2)[16:l], self.salt2[16:l])

    def test_pswd_check(self):
        self.assertFalse(check_password('pass1234', 'a3ed5ed2bc5fe39ceac31aa989f7008e'))
        self.assertTrue(check_password('pass1','666777DEFGaa88990f5bd282ac89105f24e6ba85e1eb4c3ed417aecd5d223fc753a9d3ab6ec87178'))

    def test_exceptions(self):
        with self.assertRaises(Exception):
            password_hash()
        with self.assertRaises(Exception):
            check_password()



if __name__ == '__main__':
    unittest.main()
