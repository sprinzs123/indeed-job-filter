from django.shortcuts import render
from .models import Product

def index(request):
    items = Product.objects.all()
    return render(request, 'store/index.html', {'items': items})