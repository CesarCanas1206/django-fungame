from main.models import Page
from wowtbc.models import Game


class MainMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.pages = Page.objects.all()
        request.games = Game.objects.all()
        response = self.get_response(request)

        return response
