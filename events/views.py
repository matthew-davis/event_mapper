from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Event
from .serializers import *
import datetime

@api_view(['GET', 'POST'])
def events_list(request):
    if request.method == 'GET':
        data = []
        nextPage = 1
        previousPage = 1
        events = Event.objects.all().order_by('-EventDate')
        page = request.GET.get('page', 1)
        paginator = Paginator(events, 25)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)

        serializer = EventSerializer(data,context={'request': request} ,many=True)
        if data.has_next():
            nextPage = data.next_page_number()
        if data.has_previous():
            previousPage = data.previous_page_number()

        return Response({'data': serializer.data , 'count': paginator.count, 'numpages' : paginator.num_pages, 'nextlink': '/api/events/?page=' + str(nextPage), 'prevlink': '/api/events/?page=' + str(previousPage)})

    elif request.method == 'POST':
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def events_detail(request, pk):
    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = EventSerializer(event,context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = EventSerializer(event, data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def event_map(request, date):

    currenttime = datetime.datetime.now() - datetime.timedelta(minutes=15)
    orangefilter = currenttime - datetime.timedelta(seconds=1)
    bluefilter = currenttime.day

    try:
        #two fetches
        orangeevents = Event.objects.values('DataMapCountry').filter(EventDate__range=[orangefilter, currenttime]).exclude(DataMapCountry='').annotate(dcount=Count('DataMapCountry'))
        blueevents = Event.objects.values('DataMapCountry').filter(EventDate__day=bluefilter).exclude(DataMapCountry='').annotate(dcount=Count('DataMapCountry'))

        orangeeventmap = []
        blueeventmap = []

        # two set up of data
        for dict in orangeevents:
            orangeeventmap.append(list(dict.values()))

        for dict in blueevents:
            blueeventmap.append(list(dict.values()))

    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response({ 'blue': blueeventmap, 'orange': orangeeventmap })
