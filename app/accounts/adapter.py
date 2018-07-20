from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter

class CustomAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
        path = "/"
        return path.format(username=request.user.username)

    def get_logout_redirect_url(self, request):
         path = "/app/accounts/login/"
         return path.format(username=request.user.username)

