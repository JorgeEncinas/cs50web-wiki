from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("new_entry", views.new_entry, name="new_entry"),
    path("wiki/<str:title>", views.get_entry, name="get_entry"),
    path("random_entry", views.random_entry, name="random_entry"),
    path("search", views.search_entry, name="search_entry"),
    path("edit_entry", views.edit_entry, name="edit_entry")
]
