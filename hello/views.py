from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Flight, Passenger
from django.urls import reverse
import logging
# Create your views here.
logger = logging.getLogger(__name__)

def index(request):
    logger.error(request)
    # if not request.user.is_authenticated:
    #     return render(request,"hello/login.html", {"message": None})
    context = {
      "flights": Flight.objects.all()
    }
    logger.error(context)
    return render(request,"hello/index.html", context)

def login_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username = username, password = password)
    logger.error(username,password,user)
    if user is not None:
        login(request, user)
        context = {
          "flights": Flight.objects.all()
        }
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, 'hello/error.html', {"message": "Invalid credential."})

# def login_view(request):
#     username = request.POST.get('username')
#     password = request.POST.get('password')
#     user = authenticate(request, usename=username, password=password)
#     logger.error(username,password,user)
#     if user is not None:
#         login(requst,user)
#         context = {
#           "flights": Flight.objects.all()
#         }
#         return HttpResponseRedirect(reverse("index",context))
#     else:
#         return render(request,"hello/login.html", {"message": "Invalid credentials"})

def logout_view(request):
    logout(request)
    return render(request,"hello/login.html", {"message": "Logged out"})

def flight(request, flight_id):
    try:
        flight = Flight.objects.get(pk=flight_id)
    except Flight.DoesNotExist:
        raise Http404("Fligh does not exist")

    context = {
      "flight": flight,
      "passengers": flight.passengers.all(),
      "non_passengers": Passenger.objects.exclude(flights=flight).all()
    }
    return render(request,"hello/flight.html", context)

def book(request, flight_id):
    try:
        passenger_id = int(request.POST["passenger"])
        passenger = Passenger.objects.get(pk=passenger_id)
        flight = Flight.objects.get(pk=flight_id)
    except KeyError:
        return render(request,"hello/error.html",{"message": "No sellection."})
    except Flight.DoesNotExist:
        return render(request,"hello/error.html",{"message": "No flight."})
    except Passenger.DoesNotExist:
        return render(request,"hello/error.html",{"message": "No passenger."})

    passenger.flights.add(flight)
    return HttpResponseRedirect(reverse("flight", args=(flight_id)))
