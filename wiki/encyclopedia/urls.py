from django.urls import path

from . import views

app_name = "wiki"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entries, name="entries"),
    path("search", views.search, name="search"),
    path("new", views.newPage, name="newPage"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("rand", views.rand, name="rand"),
]
