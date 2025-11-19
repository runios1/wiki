from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("search", views.search, name="search"),
    path("createNew", views.createNew, name="createNew"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("randomPage",views.randomPage,name="randomPage"),
]
