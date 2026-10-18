from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import responses


@api_view
def accounts(request):
    return responses('hi')

# Create your views here.
