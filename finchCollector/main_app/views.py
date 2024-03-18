from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from .models import Finch, Toy, Photo 
from .forms import FeedingForm
import boto3
import uuid

S3_BASE_URL = 'https://s3.us-east-2.amazonaws.com/'
BUCKET = "finchcollector24"

# Create your views here.
def home(request):
    return render (request, 'home.html')

def about(request): 
    return render(request, 'about.html')

def finchs_index(request):
    finchs = Finch.objects.all()
    return render(request, 'finchs/index.html', { 'finchs': finchs })

def finchs_details(request, finch_id):
    finch = Finch.objects.get(id=finch_id)
    feeding_form = FeedingForm()
    toys_finch_doesent_have = Toy.objects.exclude(id__in = finch.toys.all().values_list('id'))
    return render(request, 'finchs/detail.html', {
        'finch': finch, 'feeding_form': feeding_form,
        'toys': toys_finch_doesent_have
    })

def add_feeding(request, finch_id):
    form = FeedingForm(request.POST)
    if form.is_valid():
        new_feeding = form.save(commit=False)
        new_feeding.finch_id = finch_id
        new_feeding.save()
    return redirect('detail', finch_id=finch_id)

def assoc_toy(request, finch_id, toy_id):
    Finch.objects.get(id=finch_id).toys.add(toy_id)
    return redirect('detail', finch_id=finch_id)

def assoc_toy_delete(request, finch_id, toy_id):
    Finch.objects.get(id=finch_id).toys.remove(toy_id)
    return redirect('detail', finch_id=finch_id)

def add_photo(request, finch_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            photo = Photo(url=url, finch_id=finch_id)
            photo.save()
        except Exception as error:
            print('An Error has occured in s3:')
            print(error)

    return redirect("detail", finch_id=finch_id)
class FinchCreate(CreateView):
    model = Finch
    fields = ['name', 'breed', 'description', 'age']
    success_url = '/finchs/'

class FinchUpdate(UpdateView):
    model = Finch
    fields = ['breed', 'description', 'age']

class FinchDelete(DeleteView):
    model = Finch
    success_url = '/finchs/'

class ToyList(ListView):
    model = Toy
    template_name = 'toys/index.html'

class ToyDetail(DetailView):
    model = Toy
    template_name = 'toys/detail.html'
class ToyCreate(CreateView):
    model = Toy
    fields = ['name', 'color']

class ToyUpdate(UpdateView):
    model = Toy
    fields = ['name', 'color']

class ToyDelete(DeleteView):
    model = Toy
    success_url = '/toys/'
