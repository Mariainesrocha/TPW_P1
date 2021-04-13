from django.shortcuts import render


# Create your views here.
def home(request):
    return render(request, 'home.html')

def topseller(request):
    return render(request, 'TopSeller.html')

def newarrival(request):
    return render(request, 'NewArrival.html')