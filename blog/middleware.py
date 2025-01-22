from django.urls import reverse
from django.shortcuts import redirect
class RedirectAuthenticatedUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.user.is_authenticated:
            path_to_redirect = [reverse('login'), reverse('register')]

            if request.path in path_to_redirect:
                return redirect('/')

        response = self.get_response(request)
        return response

class RestrictUnauthenticatedUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        restricted_path = [reverse('dashboard')]
        if not request.user.is_authenticated and request.path in restricted_path:
            return redirect(reverse('login'))

        response = self.get_response(request)
        return response

