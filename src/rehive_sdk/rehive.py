from .api.client import Client
from .api.rehive_admin import RehiveAdmin
from .api.rehive_auth import RehiveAuth
from .api.rehive_util import RehiveUtil


class Rehive:

    def __init__(self, token=None, connection_pool_size=0):
        # API Classes
        # Leave token blank if logging in
        self.client = Client(token, connection_pool_size)
        self.admin = RehiveAdmin(self.client)
        self.auth = RehiveAuth(self.client)
        self.util = RehiveUtil(self.client)
