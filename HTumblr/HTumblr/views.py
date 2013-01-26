from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
 
def main_page(request):
    return render(request, 'index.html')
 
def logout_page(request):
    """
    Log users out and re-direct them to the main page.
    """
    logout(request)
    return HttpResponseRedirect('/')