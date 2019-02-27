import unittest
from models import User


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






if __name__ == '__main__':
    unittest.main()


# u1 = User()
# u1.hashed_password = {'password': 'pas23', 'salt': 'er445'}
