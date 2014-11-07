from django.shortcuts import render

# Create your views here.
def game_index(request):
    return render(request, "Games/game_index.html")