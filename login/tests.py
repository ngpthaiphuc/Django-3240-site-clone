from django.test import TestCase
#from .models import User
from .models import Account as AccountModel
from .models import BaseLocation as BL
from .models import FriendRequest as FReq
from datetime import datetime

d1 = datetime(2015, 10, 9, 23, 55, 59, 342380)
d2 = datetime(2014, 10, 9, 23, 55, 59, 342380)


# Create your tests here.
class PagesTestCase(TestCase):
    # Check to make sure the homepage returns a successful HTTP request
    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    # Check to make sure the search page returns a successful HTTP request
    def test_search(self):
        response = self.client.get('/search')
        self.assertEqual(response.status_code, 200)

    # Checking secure admin route
    def test_secure_admin(self):
        response = self.client.get('/secure-admin')
        self.assertEqual(response.status_code, 404)

    # Checking default admin route
    def test_default_admin(self):
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 302)

    # Checking default pricing route
    def test_pricing(self):
        response = self.client.get('/pricing')
        self.assertEqual(response.status_code, 200)

    # Checking default hoosaroundme route
    def test_hoosaroundme(self):
        response = self.client.get('/hoosaroundme')
        self.assertEqual(response.status_code, 200)

    # Checking default login route
    def test_login_a(self):
        response = self.client.get('/logina')
        self.assertEqual(response.status_code, 200)

    # Checking non-existent id route
    def test_no_user(self):
        response = self.client.get('/0/')
        self.assertEqual(response.status_code, 404)


class FriendRequest(TestCase):
    # Checking that no-auth cannot send a friend request
    def test_no_friend_request(self):
        response = self.client.get('/friend_request/')
        self.assertEqual(response.status_code, 200)

    # Checking that no-auth cannot send a friend request
    def test_no_request_accept(self):
        response = self.client.get('/friend_request_accept/')
        self.assertEqual(response.status_code, 404)

    # Checking that no-auth cannot decline a friend request
    def test_no_request_decline(self):
        response = self.client.get('/friend_request_decline/')
        self.assertEqual(response.status_code, 404)

    # Checking that no-auth cannot decline a friend request
    def test_no_request_cancel(self):
        response = self.client.get('/friend_request_cancel/')
        self.assertEqual(response.status_code, 200)


# class UserTestCase(TestCase):
#     # Setting up the user model
#     def setUp(self):
#         User.objects.create(userId='123', userName='test', email='test@gmail.com', homeLocation='Charlottesville',
#                             friends=['321'])
#         User.objects.create(userId='321', userName='friend1', email='f1@gmail.com', homeLocation='Charlottesville',
#                             friends=['123'])
#
#     def test_userName(self):
#         test_user = User.objects.get(userId='123')
#         # field_label = test_user._meta.get_field('userName')
#         self.assertEqual(test_user.userName, 'test')
#
#     def test_email(self):
#         test_user = User.objects.get(userId='123')
#         self.assertEqual(test_user.email, 'test@gmail.com')
#
#     def test_homeLocation(self):
#         test_user = User.objects.get(userId='123')
#         self.assertEqual(test_user.homeLocation, 'Charlottesville')
#
#     def test_default_savedLocation(self):
#         test_user = User.objects.get(userId='123')
#         self.assertEqual(test_user.savedLocations, ['Home,70.2333,-36.1239'])
#
#     def test_friends(self):
#         test_user = User.objects.get(userId='123')
#         friend = User.objects.get(userId=test_user.friends[0])
#         self.assertEqual(friend.userName, 'friend1')
#         self.assertEqual(friend.email, 'f1@gmail.com')


class FriendRequestAccount(TestCase):
    def setUp(self):
        AccountModel.objects.create(username='testfr', email='testfr@gmail.com', )
        AccountModel.objects.create(username='friend1fr', email='f1fr@gmail.com', )

    def test_FReq(self):
        test_user1 = AccountModel.objects.get(email='testfr@gmail.com')
        test_user2 = AccountModel.objects.get(email='f1fr@gmail.com')
        test_freq = FReq.objects.create(receiver_id=test_user1.id, sender_id=test_user2.id)
        self.assertEqual(test_freq.is_active, True)

    def test_FReq_sender(self):
        test_user1 = AccountModel.objects.get(email='testfr@gmail.com')
        test_user2 = AccountModel.objects.get(email='f1fr@gmail.com')
        test_freq = FReq.objects.create(receiver_id=test_user1.id, sender_id=test_user2.id)
        self.assertEqual(test_freq.sender, test_user2)

    def test_FReq_receiver(self):
        test_user1 = AccountModel.objects.get(email='testfr@gmail.com')
        test_user2 = AccountModel.objects.get(email='f1fr@gmail.com')
        test_freq = FReq.objects.create(receiver_id=test_user1.id, sender_id=test_user2.id)
        self.assertEqual(test_freq.receiver, test_user1)

    def test_FReq_cancel(self):
        test_user1 = AccountModel.objects.get(email='testfr@gmail.com')
        test_user2 = AccountModel.objects.get(email='f1fr@gmail.com')
        test_freq = FReq.objects.create(receiver_id=test_user1.id, sender_id=test_user2.id)
        test_freq.cancel()
        self.assertEqual(test_freq.is_active, False)

    def test_FReq_decline(self):
        test_user1 = AccountModel.objects.get(email='testfr@gmail.com')
        test_user2 = AccountModel.objects.get(email='f1fr@gmail.com')
        test_freq = FReq.objects.create(receiver_id=test_user1.id, sender_id=test_user2.id)
        test_freq.decline()
        self.assertEqual(test_freq.is_active, False)

    def test_FReq_cname(self):
        test_user1 = AccountModel.objects.get(email='testfr@gmail.com')
        test_user2 = AccountModel.objects.get(email='f1fr@gmail.com')
        test_freq = FReq.objects.create(receiver_id=test_user1.id, sender_id=test_user2.id)
        self.assertEqual(test_freq.get_cname, "FriendRequest")


class Account(TestCase):
    # Setting up the user model
    def setUp(self):
        AccountModel.objects.create(username='test', email='test@gmail.com', )
        AccountModel.objects.create(username='friend1', email='f1@gmail.com', )

    def test_userName(self):
        test_user = AccountModel.objects.get(email='test@gmail.com')
        # field_label = test_user._meta.get_field('userName')
        self.assertEqual(test_user.username, 'test')

    def test_email(self):
        test_user = AccountModel.objects.get(email='test@gmail.com')
        self.assertEqual(test_user.email, 'test@gmail.com')

    def test_default_savedLocation(self):
        test_user = AccountModel.objects.get(email='test@gmail.com')
        self.assertEqual(test_user.savedLocations[0], 'Home,70.233,-36.1239')


class AccountDefaults(TestCase):
    # Setting up the user model
    def setUp(self):
        AccountModel.objects.create(username='test', email='test@gmail.com', )
        AccountModel.objects.create(username='friend1', email='f1@gmail.com', )

    def test_defaultis_admin(self):
        test_user = AccountModel.objects.get(email='test@gmail.com')
        # field_label = test_user._meta.get_field('userName')
        self.assertEqual(test_user.is_admin, False)

    def test_default_is_admin(self):
        test_user = AccountModel.objects.get(email='test@gmail.com')
        self.assertEqual(test_user.is_active, True)

    def test_default_is_staff(self):
        test_user = AccountModel.objects.get(email='test@gmail.com')
        self.assertEqual(test_user.is_staff, False)

    def test_default_is_superuser(self):
        test_user = AccountModel.objects.get(email='test@gmail.com')
        self.assertEqual(test_user.is_superuser, False)

    def test_default_hide_email(self):
        test_user = AccountModel.objects.get(email='test@gmail.com')
        self.assertEqual(test_user.hide_email, True)


class BaseLocation(TestCase):
    # Setting up the user model
    def setUp(self):
        d1 = datetime(2015, 10, 9, 23, 55, 59, 342380)
        d2 = datetime(2014, 10, 9, 23, 55, 59, 342380)
        BL.objects.create(date_added=d1)
        BL.objects.create(date_added=d2)

    def test_bl_long(self):
        test_bl = BL.objects.get(date_added=d1)
        self.assertEqual(test_bl.longitude, 0.0)

    def test_bl_lat(self):
        test_bl = BL.objects.get(date_added=d1)
        self.assertEqual(test_bl.latitude, 0.0)

    def test_bl_locname(self):
        test_bl = BL.objects.get(date_added=d1)
        self.assertEqual(test_bl.loc_name, '')