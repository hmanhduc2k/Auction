from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class AuctionListing(models.Model):
    # User who posted the auction listing
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name="poster")
    # Title of the Auction listing
    auctionTitle = models.CharField(max_length=50)
    # Image of the bidded object
    image = models.URLField(blank=False)
    # Further details about the auction listing
    auctionDetails = models.TextField()
    # Current bid price
    currentBid = models.IntegerField()
    # Posting date of the auction listing
    listingDate = models.DateTimeField(auto_now_add=True)
    # Status of the auction listing
    isClosed = models.BooleanField(default=False)
    # Add category later
    category = models.ForeignKey('Category', on_delete=models.CASCADE, default=None)
    
    def __str__(self):
        return f"{self.auctionTitle} (listing date {self.listingDate})"

class Bidding(models.Model):
    # user who made the bid
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    # the auction being bidded
    auction = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, default=None)
    # user bid amount
    bidAmount = models.IntegerField()
    # bidding date
    bidDate = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"User {self.user} bids {self.bidAmount}"

class Comments(models.Model):
    # user who made the comments
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name="commenter")
    # the auction being commented on
    auction = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, default=None)
    # user comments
    comments = models.TextField()
    # comment date
    commentDate = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Commented by {self.user}"

class Category(models.Model):
    # name of the category
    categoryName = models.CharField(max_length=50)
    def __str__(self):
        return f"{self.categoryName}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, blank = False)
    listing = models.ForeignKey(AuctionListing, on_delete = models.CASCADE, blank = False)