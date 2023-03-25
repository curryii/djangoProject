from django.shortcuts import render
import json
from django.db.models import Q, QuerySet, Count, Avg, Max, Min
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import Projects
from interfaces.models import Interfaces
# Create your views here.
from django.views import View
from django.db import connection
from .serializers import InterfaceSerializer


# Create your views here.

class InterfaceView(View):
    def post(self, request):
        interface_data = json.loads(request.body)
        serializer_obj = InterfaceSerializer(data=interface_data)

        if not serializer_obj.is_valid():
            return JsonResponse(serializer_obj.errors, status=400)

        serializer_obj.save()
        return JsonResponse(serializer_obj.data, status=201)


class InterfaceViewId(View):
    def put(self, request, pk):
        pass
