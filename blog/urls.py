from django.urls import path
from . import views

app_name = "blog"
urlpatterns = [
    path("", views.archive, name="archive"),
    path("<slug:slug>/", views.post, name="post"),
]
