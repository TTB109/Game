from django.http import HttpResponse,HttpResponseRedirect,HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect,render,get_object_or_404

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#from django.urls import reverse, reverse_lazy
from .models import *
from .forms import *

# Create your views here.

def view_tfidf(request,id):

  return render(request,'adm/tfidf.html')

def view_(request):
  return render(request,'adm/index.html')

def view(request):
  return render(request,'adm/index.html')

