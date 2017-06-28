from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import Trip
from ..login_and_registration_app.models import User
import datetime

def get_time_now():
    return datetime.date.today()

# Create your views here.
def index(request):
    # User.objects.all().delete()
    # Trip.objects.all().delete()
    return render(request, 'travel_buddy_app/index.html')

def travel_dashboard(request):
    print "*"*42
    if not request.session.get('id'):
        messages.error(request, 'Access Denied. Log in first.')
        return redirect('/')
    user = User.objects.get(id=request.session.get('id'))
    # trips = user.trips.all().order_by('-created_at')
    trips = Trip.objects.filter(users__name=user).order_by('-created_at')
    other_trips = Trip.objects.all().exclude(creator=user)
    context = {
        'user': user,
        'trips': trips,
        'other_trips': other_trips,
    }
    print context
    return render(request, 'travel_buddy_app/travels.html', context)

def travel_add(request):
    if not request.session.get('id'):
        messages.error(request, 'Access Denied. Log in first.')
        return redirect('/')
    # user = User.objects.get(id=request.session.get('id'))
    # context = {
    #     'user': user,
    # }
    return render(request, 'travel_buddy_app/travel_add.html')

def travel_add_trip(request):
    # print "*"*42
    # print request.POST
    # print request.session['id']
    # print "*"*42
    if not request.session.get('id'):
        messages.error(request, 'Access Denied. Log in first.')
        return redirect('/travel_dashboard')
    results = Trip.objects.addTravelVal(request.POST)
    # print "*"*42
    # print results
    # print "*"*42
    if not results['error_message'] == []:
        for error in results['error_message']:
            messages.error(request, error)
        return redirect('/travel_dashboard')
    else:
        messages.success(request, 'Trip Successfuly Added.')
        # return redirect('books/'+str(results['book'].id))
        return redirect('/travel_dashboard')

def join_trip(request, id):
    trip = Trip.objects.get(id=id)
    print trip
    user = User.objects.get(id=request.session.get('id'))
    # trip.add(users=request.session['id'])
    trip.users.add(user)
    return redirect('/travel_dashboard')

def destination(request, id):
    user = User.objects.get(id=request.session.get('id'))
    trip = Trip.objects.get(id=id)
    other_users = trip.users.exclude(name=user.name)
    context = {
        'user': user,
        'trip': trip,
        'other_users': other_users
    }
    return render(request, 'travel_buddy_app/dest.html', context)

def logout(request):
    request.session.clear()
    messages.success(request, 'Logged Out')
    return redirect('/')

def home(request):
    return redirect('/travel_dashboard')
