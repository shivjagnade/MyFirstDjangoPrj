from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.template import context

# Create your views here.
def test1(request):
    return render(request, 'test1.html')