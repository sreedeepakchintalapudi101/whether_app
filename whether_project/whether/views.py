import requests
from django.shortcuts import render
from .models import WeatherSearch
from .forms import CityForm

API_KEY = "bfa99dedd19cccf5ec15dff710cc7aab"  # Replace with your API key

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&appid={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def weather_view(request):
    form = CityForm()
    weather_data = None
    history = WeatherSearch.objects.order_by('-date')[:5]  # Show last 5 searches

    if request.method == "POST":
        form = CityForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data["city"]
            data = get_weather(city)
            if data:
                weather_data = {
                    "city": city,
                    "temperature": data["list"][0]["main"]["temp"],
                    "description": data["list"][0]["weather"][0]["description"],
                    "forecast": data["list"][:5],  # Get 5-day forecast
                }
                WeatherSearch.objects.create(
                    city=city,
                    temperature=weather_data["temperature"],
                    description=weather_data["description"],
                )
    
    return render(request, "weather.html", {"form": form, "weather": weather_data, "history": history})