from django.shortcuts import render
from django.views.decorators.cache import cache_page


@cache_page(5)
def main_page(request):
	return render(request, "index.html")
# Create your views here.
