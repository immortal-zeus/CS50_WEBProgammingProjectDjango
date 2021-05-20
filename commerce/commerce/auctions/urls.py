from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("category",views.cat, name="cat"),
    path("createlisting", views.createlisting, name="createlisting"),
    path("addcategory", views.addcategory, name="addcat"),
    path("activelisting", views.activelist, name="actlist"),
    path("listing", views.listing, name="listi"),
    path("addwatch", views.addwatchlist, name="addwatch"),
    path("removewatch", views.removewatchlist, name="removewatch"),
    path("watchlist",views.watchlist, name="watchlist"),
    path('closelisting', views.close_listing,name="closeL")
]
