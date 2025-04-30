from django.shortcuts import render

# Create your views here.
def index(request):
    print('hi')
    return render(request, 'index-movemuz.html')