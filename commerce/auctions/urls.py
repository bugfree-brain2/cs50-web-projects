from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path('watchlists', views.watchlist_view, name="watchlists"),
    path('listing/<int:id>', views.page_view, name= "ind-page"),
    path("catagory/", views.catagory_view, name="catagory"), 
    path("catagory/<str:catagory_name>", views.catagory_view_list, name="catagory_list") 
]
