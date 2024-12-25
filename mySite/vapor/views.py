from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from .models import Game, Rating
from django.views.generic.edit import FormView
from django.views.generic import ListView, DetailView
from .forms import FeedbackForm,SearchForm


class GameListView(ListView):
    model = Game
    context_object_name = "games"
    template_name = 'index.html'
    queryset = Game.objects.all().order_by('name')




def game_list_api(request):

    query = request.GET.get('search','')
    games = Game.objects.all().values('name', 'img_url','slug')
    if query:
        games = games.filter(name__icontains=query)
    game_list = list(games)
    return JsonResponse(game_list, safe=False)  # Return as JSON

class GameView(View):
    template_name = 'game.html'
    form_class = FeedbackForm

    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        game = get_object_or_404(Game, slug=slug)
        form = self.form_class()
        return render(request, self.template_name, {'game': game, 'form': form})

    def post(self, request, *args, **kwargs):

        slug = kwargs.get('slug')
        game = get_object_or_404(Game, slug=slug)

        form = self.form_class(request.POST)

        if form.is_valid():

            rating = form.cleaned_data['rating']
            Rating.objects.create(game=game, rating=rating)

            return redirect(reverse('game-detail', kwargs={'slug': game.slug}))

        return render(request, self.template_name, {'game': game, 'form': form})
