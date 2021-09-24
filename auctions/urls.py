from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createlisting", views.createListing, name="createlisting"),
    path("auctiondetails/<str:id>", views.auctionDetails, name="auctiondetails"),
    path("watchlist", views.watchList, name="watchlist"),
    path("add_watchlist/<str:id>", views.addWatchlist, name="add_watchlist"),
    path("remove_watchlist/<str:id>", views.removeWatchlist, name="remove_watchlist"),
    path("bidding/<str:id>", views.makeBidding, name="bidding"),
    path("close/<str:id>", views.closeListing, name="close"),
    path("comment/<str:id>", views.comment, name="comment"),
    path("category", views.category, name="category"),
    path("category/<str:name>", views.categoryName, name="category_name"),
    path("oldlisting", views.oldListing, name="oldlisting")
]
