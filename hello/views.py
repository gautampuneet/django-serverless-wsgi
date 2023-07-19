import json
from django.shortcuts import render
from django.http import Http404, HttpResponse

from hello.models import UserProfileModel
from django.core import serializers


def users(request):
    if request.method == 'GET':
        data = UserProfileModel.objects.all()
        return render(request, 'user_view.html', {'users': data})
    elif request.method == 'POST':
        body = json.loads(request.body)
        data = UserProfileModel(
            name=body.get("name"),
            email=body.get("email")
        )
        data.save()
        data = serializers.serialize('json', [data, ])
        return HttpResponse(data, content_type='application/json')
    else:
        return Http404("HTTP Method not allowed")

