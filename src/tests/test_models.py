import unittest
from models import User



class Test_2(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user = User()

    def test_id(self):
        self.assertEqual(self.user.id, -1)




if __name__ == '__main__':
    unittest.main()


# u1 = User()
# u1.hashed_password = {'password': 'pas23', 'salt': 'er445'}
