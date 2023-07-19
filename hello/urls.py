from django.urls import path

from .views import users

app_name = "hello"
urlpatterns = [
    path("", view=users, name="users"),
]
