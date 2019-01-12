from app import app, db
from datetime import datetime, timedelta
import unittest

from app.models import User, Post

class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u = User(username="Dhriti")
        u.set_password("Dhriti")
        self.assertFalse(u.check_password("noname"))
        self.assertTrue(u.check_password("Dhriti"))

    def test_follow(self):
        u1 = User(username="raju", email="raju@noname.org")
        u2 = User(username="kallappa", email="kallappa@noname.org")
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(u2.followed.all(), [])

        u1.follow(u2)
        db.session.commit()
        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 1)
        self.assertEqual(u1.followed.first().username, "kallappa")
        self.assertEqual(u2.followers.count(), 1)
        self.assertEqual(u2.followers.first().username, "raju")

        u1.unfollow(u2)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 0)
        self.assertEqual(u2.followers.count(), 0)

    def test_follow_posts(self):

        u1 = User(username="A1", email="a1@example.com")
        u2 = User(username="A2", email="a2@example.com")

        db.session.add_all([u1,u2])

        now = datetime.utcnow()
        p1 = Post(body="Post from A1", author=u1,
                    timestamp= now+timedelta(seconds=1))
        p2 = Post(body="Post from A2", author=u2,
                    timestamp= now+timedelta(seconds=2))

        u1.follow(u2)
        db.session.commit()

        self.assertEqual(u1.followed_posts().all(), [p2,p1])




if __name__ == "__main__":
    unittest.main(verbosity=2)
