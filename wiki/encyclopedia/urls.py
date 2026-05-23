from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"), 
    path("wiki/search", views.search_page, name="search-page"),
    path("wiki/newpage", views.create_newpage, name="create-page"),
    path("wiki/randompage", views.random_page, name="random-page"),
    path("wiki/<str:title>/editpage", views.edit_page, name='edit-page'),
    path("wiki/<str:title>", views.entry_page, name="entry-page"),
]
