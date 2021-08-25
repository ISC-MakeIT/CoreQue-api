import json
from django import http
from django.http.response import HttpResponsePermanentRedirect, JsonResponse
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
 
def specialMeaningNo(requst):
    data = {
            "id":"1",
            "first_name":"Steven",
            "last_name":"Thompson",
            "email":"sthompson0@spotify.com",
            "gender":"Male",
            "ip_address":"129.167.217.82"
        }
    return JsonResponse(data=data)
