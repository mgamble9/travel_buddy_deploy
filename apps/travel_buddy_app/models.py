from __future__ import unicode_literals
from django.db import models
from ..login_and_registration_app.models import User
import datetime

def get_time_now():
    # return datetime.datetime.now().strftime('(%Y/%m/%d)')
    # return datetime.datetime.now().strptime('(%Y/%m/%d)')
    # return datetime.date.today()
    return datetime.datetime.today()

# Create your models here.
class TripManager(models.Manager):
    def addTravelVal(self, postData):
        context = {
            'error_message' : [],
            # 'success_message' : []
        }

        # print postData['travel_start']
        # print postData['travel_end']
        first_date= datetime.datetime.strptime(str(postData['travel_start']),'%Y-%m-%d')
        second_date= datetime.datetime.strptime(str(postData['travel_end']),'%Y-%m-%d')
        # print first_date
        # print second_date
        date_now = get_time_now()
        # print date_now
        if date_now > first_date:
            context['error_message'].append(
                'ERROR: Trip starting date of trip can\'t be less than today\'s date!')

        if date_now > second_date:
            context['error_message'].append(
                'ERROR: Trip ending date of trip can\'t be less than today\'s date!')

        if first_date == second_date:
            context['error_message'].append(
                'ERROR: Start and end dates of the trip can\'t be the same!')

        if first_date > second_date:
            context['error_message'].append(
                'ERROR: Start date can\'t later then end date!')

        # results = {'status': True, 'errors': []}
        if not postData['destination'] or len(postData['destination']) < 1:
            context['error_message'].append(
                'ERROR: Please enter Destination (must be at least 3 characters!)')
        if not postData['description'] or len(postData['destination']) < 1:
            context['error_message'].append(
                'ERROR: Please enter a travel plan.')



        # try:
        if context['error_message'] == []:
            # print "*"*42
            # print postData['creator']
            # print "*"*42
            user = User.objects.get(id=postData['creator'])
            # trip = Trip.objects.get(destination=postData['destination'])

            trip = Trip.objects.create(
                description=postData['description'],
                destination=postData['destination'],
                creator=user,
                travel_date_from=postData['travel_start'],
                travel_date_to=postData['travel_end'],
            )

            # print "*"*3
            # print trip
            # print "*"*3
            trip.save()
            trip.users.add(user)

            # review.books.add(book)
            # review.users.add(user)

        # except IntegrityError as e:
        # except:
        #     results['status'] = False
        #     results['errors'].append('fail')

        return context



DEFAULT_CREATOR = 1
class Trip(models.Model):
    description = models.TextField(blank=False, null=False)
    destination = models.CharField(max_length=1)
    travel_date_from = models.DateTimeField()
    travel_date_to = models.DateTimeField()
    creator = models.ForeignKey(User, related_name="creator_trips", default=DEFAULT_CREATOR)
    users = models.ManyToManyField(User, related_name="trips")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()

    def __str__(self):
        return str(self.destination)
