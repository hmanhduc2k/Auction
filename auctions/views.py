from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.forms import ModelForm
from django.contrib.auth.decorators import login_required
from django import forms

from .models import AuctionListing, User, Bidding, Comments, Watchlist, Category


def index(request):
    active_listings = []
    all_listings = AuctionListing.objects.all()
    for listing in all_listings:
        if listing.isClosed is False:
            active_listings.append(listing)
    return render(request, "auctions/index.html", {
        "title": "All active listings available:",
        "listings": active_listings,
        "is_watchlist_remove": True,
        "is_index": True
    })

def oldListing(request):
    closed_listing = []
    all_listings = AuctionListing.objects.all()
    for listing in all_listings:
        if listing.isClosed is True:
            closed_listing.append(listing)
    return render(request, "auctions/index.html", {
        "title": "Closed listings:",
        "listings": closed_listing,
        "is_watchlist_remove": True
    })


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

class ListingForm(forms.ModelForm):
    class Meta:
        model = AuctionListing
        fields = ['auctionTitle', 'image', 'currentBid', 'auctionDetails', 'category']
        widgets = {
            'auctionTitle': forms.TextInput(attrs={'class': 'form-control', 'aria-label': 'Title'}),
            'image': forms.TextInput(attrs={'class': 'form-control'}),
            'currentBid': forms.NumberInput(attrs={'class': 'form-control'}),
            'auctionDetails': forms.Textarea(attrs={'class': 'form-control'}),
            'category': forms.Select(choices=Category.objects.all(), attrs={'class' : 'form-control'})
        }
        labels = {
            'auctionTitle': 'Title of the new Auction',
            'image': 'Image URL',
            'currentBid': "Starting bid",
            'auctionDetails': 'Details about the Auction',
            'category': 'Select a Category'
        }

def createListing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST)
        if form.is_valid:
            listing = form.save(commit=False)
            listing.user = request.user
            listing.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/createlisting.html", {
            'form': ListingForm()
        })

def watchList(request):
    all_match = []
    watchList = Watchlist.objects.filter(user=request.user)
    for i in watchList:
        if not i.listing.isClosed:
            all_match.append(i.listing)
    return render(request, "auctions/index.html", {
        "title": "Your watch list:",
        "listings": all_match,
        "is_watchlist_remove": False
    })

@login_required(login_url='login')
def addWatchlist(request, id):
    user = request.user
    listing = AuctionListing.objects.get(id=id)
    test = Watchlist.objects.filter(user=user, listing=listing).first()
    if test is None:
        new_listing = Watchlist(user=user, listing=listing)
        new_listing.save()
    return HttpResponseRedirect(reverse('watchlist'))

def removeWatchlist(request, id):
    user = request.user
    listing = AuctionListing.objects.get(id=id)
    curr = Watchlist.objects.filter(user=user, listing=listing)
    curr.delete()
    watchList = Watchlist.objects.filter(user=user)
    return HttpResponseRedirect(reverse('watchlist'))

def makeBidding(request, id):
    try:
        listing = AuctionListing.objects.get(id=id)
    except:
        return HttpResponseRedirect("index")
    if request.method == 'POST':
        new_price = request.POST.get('currentBid', None)
        user = request.user
        new_bid = Bidding(user=user, bidAmount=new_price, auction=listing)
        new_bid.save()
        listing.currentBid = new_price
        listing.save()
        old_bid = Bidding.objects.filter(auction=listing).exclude(bidAmount=new_price)
        old_bid.delete()
    return HttpResponseRedirect(reverse('auctiondetails', args=id))

@login_required(login_url='login')
def auctionDetails(request, id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    try:
        listing = AuctionListing.objects.get(id=id)
    except:
        return render(request, "auctions/error.html", {
            "message": "There is no listing associated"
        })
    commentList = Comments.objects.filter(auction=listing)
    latestBid = Bidding.objects.filter(auction=listing).first()
    return render(request, "auctions/auctiondetails.html", {
        "listing": listing,
        "user": request.user, 
        "commentList": commentList,
        "bidder": latestBid,
        "min_bid": listing.currentBid + 1
    })

def closeListing(request, id):
    listing = AuctionListing.objects.get(id=id)
    listing.isClosed = True
    listing.save()
    commentList = Comments.objects.filter(auction=listing)
    latestBid = Bidding.objects.filter(auction=listing).first()
    return render(request, "auctions/auctiondetails.html", {
        "listing": listing,
        "user": request.user, 
        "commentList": commentList,
        "bidder": latestBid
    })

def comment(request, id):
    if request.method == "POST":
        comments = request.POST['content']
        listing = AuctionListing.objects.get(id = id)
        newComment = Comments(user=request.user, auction=listing, comments=comments)
        newComment.save()
    return HttpResponseRedirect(reverse('auctiondetails', args=id))

@login_required(login_url='login')
def category(request):
    return render(request, "auctions/category.html", {
        "title": "View listings by categories",
        "categories": Category.objects.all()
    })

@login_required(login_url='login')
def categoryName(request, name):
    category = Category.objects.filter(categoryName=name).first()
    if category is None:
        return render(request, "auctions/error.html", {
            "message": "I'm sorry, but there is no listing with category" + name
        })
    else:
        listings = AuctionListing.objects.filter(category=category, isClosed=False)
        return render(request, "auctions/index.html", {
            "title": "Listings with category " + name + " are:",
            "listings": listings,
            "is_watchlist_remove": True
        })