from django.shortcuts import render
from .functions import multiplicate_by_5
from django.contrib.auth.decorators import login_required
from .forms import PredApiForm
from django.http import HttpResponseRedirect
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import os
import json


@login_required
def form_page(request):
        url = 'http://fastapi_sba:8000/predict'

        headers = {
        'Accepts': 'application/json',
        }

        session = Session()
        session.headers.update(headers)

        # if this is a POST request we need to process the form data
        if request.method == "POST":
            # create a form instance and populate it with data from the request:
            form = PredApiForm(request.POST)
            # check whether it's valid:
            if form.is_valid():
                try :
                    data_input = json.dumps(form.cleaned_data)
                    response = session.post(url, data=data_input)
                    data = response.json()
                    print(data)
                    form.save(prediction=data.get('prediction'))
                    return render(request, "main/form_page.html", context = {"form": form, 'data': data})
                except (ConnectionError, Timeout, TooManyRedirects, KeyError) as e:
                    return render(request, "main/form_page.html", context = {"form": form, 'error': e})
        else:
            form = PredApiForm()

        return render(request, "main/form_page.html", context = {"form": form})

# Create your views here.
def home_page(request):
    return render(request, 'main/home_page.html')

def about_page(request):
    return render(request, 'main/about_page.html')

@login_required
def special_page(request):
    return render(request, "main/special_page.html")

