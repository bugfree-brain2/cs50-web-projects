from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import User, AuctionList,  bids, Comments, watchlist


catagories = ["Fashion", "Electronics", "Property", "Toys", "Tech", "Cosmetics", "Furniture"]
def index(request):
    auction_list = AuctionList.objects.all()
    auction = list(auction_list)[::-1]
    for items in auction:
        top_bid = bids.objects.filter(products=items.id).order_by('-bid_price').first()
        items.auction_winner = top_bid.user if top_bid else None 
    return render(request, "auctions/index.html", 
            {
            "auction" : auction,
            }
        )

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

def create(request):
    if request.method == 'POST':
        title = request.POST["title"]
        description = request.POST["description"]
        image = request.POST["image-url"]
        bid  = request.POST["bid"]
        catagory = request.POST['catagory']
        auction_list = AuctionList.objects.create(
        title = title,
        description = description, 
        image = image, 
        start_bid = bid,
        owners = request.user,
        catagory = catagory
            )
        return redirect("ind-page", 
            id = auction_list.id, 
        )
    return render(request, "creating_and_listing/create.html", {
        "catagories" : catagories
    })
    

def page_view(request, id):
    auction_list  = AuctionList.objects.get(id=id)
    winners = bids.objects.filter(products=auction_list.id).order_by('-bid_price').first()
    winner = winners.user if winners else None
    request.session["winner"] = winner.id if winner else None
    comments_filt = Comments.objects.filter(product_page=auction_list)
    watchlist_ids = []
    user_watchlist = None
    if request.user.is_authenticated:
        user_watchlist, _ = watchlist.objects.get_or_create(user = request.user)
        watchlist_ids = user_watchlist.watch_list.values_list('id', flat=True)
    if request.method == "POST":
        auction_status = request.POST.get("auctions_status")
        if auction_status == "end-auction":
            auction_list.active = False
            auction_list.save()
        watchlist_feature = request.POST.get("watchlist-button")
        watchlist_delete = request.POST.get("watchlist-button-delete")
        if watchlist_feature:
           user_watchlist.watch_list.add(auction_list)
        if watchlist_delete:
            user_watchlist.watch_list.remove(auction_list.id)

        auction_bid = request.POST.get("bid")
        if auction_bid != None:
            if float(auction_bid) >= auction_list.start_bid:
                heighest_bid = bids.objects.filter(products=auction_list).order_by('-bid_price').first()
                if heighest_bid is None or float(heighest_bid.bid_price) < float(auction_bid):
                    auction_bids = bids.objects.create(
                    user = request.user,
                    products = auction_list,
                    bid_price = auction_bid
            )
                else:
                    return render(request, "creating_and_listing/list_page.html", {
                'auction' : auction_list, 
                'wrong_bid' : "The bid ammount is already placed it you have to place higher bid", 
                'watchlists': watchlist_ids,
                'comments' : comments_filt
                    })
            else:
                return render(request, "creating_and_listing/list_page.html", {
                'auction' : auction_list, 
                'wrong_bid' : "the ammount should be heigher than the starter bid ammount", 
                'watchlists': watchlist_ids,
                'comments' : comments_filt
        })
        auction_comment = request.POST.get('comment-submit')
        if auction_comment == "comment-input": 
            comment_val = request.POST.get('comment')
            Comments.objects.create(
            user = request.user,
            comment = comment_val,
            product_page = auction_list
        )
    return render(request, "creating_and_listing/list_page.html", {
        'auction' : auction_list, 
        'auction_winner' : winner,
        'watchlists': watchlist_ids,
        'comments' :  comments_filt
    })
   
def watchlist_view(request):
    watchlists = watchlist.objects.get(user=request.user.id)
    return render(request, 'creating_and_listing/watchlist.html', {
        'watchlists' : watchlists.watch_list.all()
    })

def catagory_view(request):
    return render(request, 'creating_and_listing\catagory_listing.html', {
        'catagories' : catagories
    })
def catagory_view_list(request, catagory_name):
    catagory = AuctionList.objects.filter(catagory=catagory_name)
    return render(request, 'creating_and_listing\catagory_listing_2.html', {
        'catagories' : catagory
    })
