import requests
import copy
from . import config


class AnonymousUser(object):

    def __init__(self):
        self.api_url = config.API_URL
    
    def get(self, *args, **kwargs):
        return requests.get(*self.update_args(args), **self.update_kwargs(kwargs))
    
    def post(self, *args, **kwargs):
        return requests.post(*self.update_args(args), **self.update_kwargs(kwargs))
    
    def put(self, *args, **kwargs):
        return requests.put(*self.update_args(args), **self.update_kwargs(kwargs))
    
    def update_args(self, args):
        args = list(args)
        if len(args) > 0:
            url = args[0]
            if not (url[0:4] == 'http' or url[0:2] == '//'):
                url = self.api_url + (url[0] == '/' and url or ('/' + url))
            args[0] = url
        return args
    
    def update_kwargs(self, kwargs):
        if 'headers' in kwargs:
            headers = kwargs['headers']
        else:
            headers = {}
            
        if hasattr(self, 'access_token') and self.access_token:
            headers['Authorization'] = headers.get('Authorization', 'Bearer:' + self.access_token)
        
        if headers:
            kwargs['headers'] = headers
        return kwargs
    
    def get_config(self, name):
        if hasattr(config, name):
            return copy.deepcopy(getattr(config, name))
        raise Exception('Non-existent config value: %s' % name)


class AuthenticatedUser(AnonymousUser):
    def __init__(self):
        AnonymousUser.__init__(self)
        self.access_token = config.AUTHENTICATED_USER_ACCESS_TOKEN

        
class BumblebeeAnonymousUser(AnonymousUser):
    def __init__(self):
        AnonymousUser.__init__(self)
        self.access_token = config.BUMBLEBEE_ANONYMOUS_USER_ACCESS_TOKEN


            
anonymous_user = AnonymousUser()
authenticated_user = AuthenticatedUser()
bumblebee_user = BumblebeeAnonymousUser()    