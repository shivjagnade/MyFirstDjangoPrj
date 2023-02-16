from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.template import context

# Create your views here.
def test(request):
    return render(request, 'test.html')