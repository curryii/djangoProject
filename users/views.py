from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .serializers import RegisterModelSerializer
from django.contrib.auth.models import User
from rest_framework import generics

# Create your views here.

"""
class UserView(
               generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterModelSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)"""


class UserView(mixins.CreateModelMixin,
               viewsets.GenericViewSet):
    """"""


class UsernameIsExistedView(APIView):

    def get(self, request, username):
        count = User.objects.filter(username=username).count()
        return Response({'username': username, 'count': count})


class EmailIsExistedView(APIView):

    def get(self, request, email):
        count = User.objects.filter(email=email).count()
        return Response({'username': email, 'count': count})
