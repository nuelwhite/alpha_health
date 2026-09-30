from django.http import HttpResponsePermanentRedirect
from .models import Redirect


class RedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if response.status_code == 404:
            try:
                redirect = Redirect.objects.get(old_path=request.path)
                return HttpResponsePermanentRedirect(redirect.new_path)
            except Redirect.DoesNotExist:
                pass

        return response