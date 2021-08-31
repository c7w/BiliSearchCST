from django.http.response import HttpResponse
from django.shortcuts import render

# Create your views here.
def root(req):
    return render(req, "Base.html")