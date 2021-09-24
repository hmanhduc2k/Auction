from auctions.models import AuctionListing, Bidding, Category, Comments, Watchlist
from django.contrib import admin

# Register your models here.
admin.site.register(AuctionListing)
admin.site.register(Bidding)
admin.site.register(Comments)
admin.site.register(Watchlist)
admin.site.register(Category)