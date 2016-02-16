"""
Base class for all tests
"""
import unittest
from ..user_roles import AnonymousUser, AuthenticatedUser,\
    BumblebeeAnonymousUser


class TestBase(unittest.TestCase):
    """
    Base class for all tests
    """
    def setUp(self):
        """
        Generic setup
        """
        self.anonymous_user = AnonymousUser()
        self.authenticated_user = AuthenticatedUser()
        self.bumblebee_user = BumblebeeAnonymousUser()

