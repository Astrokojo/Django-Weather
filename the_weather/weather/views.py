"""
views.py

This module handles the views for the weather application.

It provides two main views:
1. `index`: Displays weather information for cities and allows users to add new cities.
2. `delete_city`: Allows users to delete cities from the list.

Each view interacts with the OpenWeatherMap API to fetch current weather data for cities stored in the database.

Dependencies:
    - Django models and forms (City, CityForm)
    - requests (for making API calls)
    - render and redirect functions (for rendering templates and handling redirects)

"""

from django.shortcuts import render, redirect
from django.contrib import messages
import requests
from .models import City
from .forms import CityForm

# Create your views here.
def index(request):
    """
    The main view that displays the weather data for cities.

    - On GET: Fetches weather information for all cities stored in the database and renders them.
    - On POST: Processes the form submission to add a new city if it doesn't already exist in the database.

    Args:
        request: The HTTP request object, either GET or POST.

    Returns:
        A rendered HTML page showing the weather data and a form for adding new cities.
    """

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=c78fcf774624e553f52b2c0c4a9bf675'

    cities = City.objects.all() #return all the cities in the database

    if request.method == 'POST':
        form =CityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['name']
            if not City.objects.filter(name=new_city).exists():
                form.save()
            else:
                messages.warning(request, f"{new_city} already exists in the database")
                pass

    form = CityForm()

    weather_data = []

    for city in cities:

        city_weather = requests.get(url.format(city)).json()
        #request the API data and convert the JSON to Python data types

        weather = {
            'city' : city,
            'temperature' : city_weather['main']['temp'],
            'description' : city_weather['weather'][0]['description'],
            'icon' : city_weather['weather'][0]['icon']
        }

        weather_data.append(weather) # add the data for the current city into our list

    context = {'weather_data' : weather_data, 'form' : form}

    return render(request, 'weather/index.html', context) #returns the index.html template

def delete_city(request, city_name):
    """
    View to handle deleting a city from the database.

    Args:
        request: The HTTP request object.
        city_name: The name of the city to be deleted.

    Returns:
        A redirect to the 'index' view after the city is deleted.
    """

    City.objects.filter(name=city_name).delete()
    return redirect('index')
