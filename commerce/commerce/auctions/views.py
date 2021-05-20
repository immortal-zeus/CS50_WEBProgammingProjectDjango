from django.contrib.auth import authenticate, login, logout , decorators
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import *

# --- logins of users -------
# thejain : 000
# newuser1 : 111
#--------------------------------------

class listing_form(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['Title' , 'Textdes' , 'Category','StartingBid','Imagelink']
        labels = {
            'TextDes': 'Description',
            'Imagelink': 'Image-Link',
            'StartingBid': 'Starting- Price/Bid'
        }


class AddCategory_form(forms.ModelForm):
    class Meta:
        model = Categorys
        fields = '__all__'
        labels = {
            'Categoryname' : 'Add Category'
        }


class Bids_forms(forms.ModelForm):
    class Meta:
        model = Bids
        fields = ['Bid']
        labels = {
            'Bid': 'Offer / Bid'
        }


class Comments_form(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['Text']
        labels = {
            'Text': 'Comment'
        }


def index(request):
    return render(request, "auctions/index.html",{
        "all_cat": Categorys.objects.all(),
        "all_list":Listing.objects.all()
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

def cat(request):
    return render(request, "auctions/Category.html",{
        "all_cat": Categorys.objects.all()
    })

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


@decorators.login_required
def createlisting(request):
    if request.method == "POST":
        form_lis = listing_form(request.POST , request.FILES)
        if form_lis.is_valid():
            Listing = form_lis.save(commit= False)
            Listing.Luser = request.user
            Listing.save()
            return render(request, "auctions/createlisting.html", {
                "form_listing": listing_form(),
                "list_save": True
            })
        else:
            return render(request, "auctions/createlisting.html", {
                "form_listing": form_lis,
                "list_save": False
            })
    else:

        return render(request, "auctions/createlisting.html", {
            "form_listing" : listing_form(),
            "list_save": False
        })


@decorators.login_required
def addcategory(request):
    if request.method == "POST":
        form_cat = AddCategory_form(request.POST)
        if form_cat.is_valid():
            form_cat.save()
            return createlisting(request)
        else:
            return render(request, "auctions/addcat.html", {
                "form_cat": form_cat
            })
    else:
        return render(request, "auctions/addcat.html" ,{
            "form_cat": AddCategory_form()
        })



def activelist(request):
    cat_id = request.GET.get('idcat',None)
    if cat_id is None:
        list_all = Listing.objects.all()
        return render(request, "auctions/index.html", {
            "all_list": list_all,
            "all_cat": Categorys.objects.all()
        })
    else:
        list_all = Listing.objects.filter(Category=cat_id)

        return render(request, "auctions/index.html",{
            "all_list" : list_all,
            "all_cat": Categorys.objects.all()
        })

@decorators.login_required
def listing(request):
    list_id = request.GET.get('idlisti',None)
    Com = Comments.objects.filter(ListingItem = Listing.objects.get(pk=list_id))
    watch = Watchlist.objects.filter(ListingItem = Listing.objects.get(pk=list_id) , Wuser = request.user, )
    if  list_id is None:
        return index(request)
    else:
        listi = Listing.objects.get(pk=list_id)

        try:
            bb = Bids.objects.get(Listing_b=listi, Bid=listi.CurrentBid).Buser
        except Bids.DoesNotExist:
            bb= None

        if request.method == "POST":
            if "Comments" in request.POST:
                form_comment = Comments_form(request.POST, request.FILES)
                if form_comment.is_valid():
                    Comment = form_comment.save(commit=False)
                    Comment.Cuser = request.user
                    Comment.ListingItem = listi
                    Comment.save()

            else:
                from_bid = Bids_forms(request.POST, request.FILES)
                if from_bid.is_valid():
                    Bi = from_bid.save(commit=False)
                    if listi.CurrentBid is None:
                        if Bi.Bid > listi.StartingBid :
                            Bi.Buser = request.user
                            listi.CurrentBid = Bi.Bid
                            Bi.Listing_b = listi
                            listi.save()
                            Bi.save()
                        else:
                            return render(request, "auctions/listing.html", {
                                "listing": listi,
                                "bid": from_bid,
                                "Flag": True,
                                "com": Com,
                                "Watch": watch,
                                "bideer": bb
                            })

                    else:
                        if Bi.Bid > listi.CurrentBid:
                            Bi.Buser = request.user
                            listi.CurrentBid = Bi.Bid
                            Bi.Listing_b = listi
                            listi.save()
                            Bi.save()
                        else:
                            return render(request, "auctions/listing.html", {
                                "listing": listi,
                                "bid": from_bid,
                                "Flag": True,
                                "com": Com,
                                "Watch": watch,
                                "bideer": bb
                            })


        return render(request,"auctions/listing.html",{
            "listing":listi,
            "bid": Bids_forms(),
            "com": Com,
            "Com": Comments_form(),
            "Watch": watch,
            "bideer": bb
        })


def addwatchlist(request):
    list_id = request.GET.get('idlisti', None)
    user = request.user
    listing1 = Listing.objects.get(pk=list_id)
    try:
        w = Watchlist.objects.get(ListingItem = listing1, Wuser = user)
    except Watchlist.DoesNotExist:
        Watch = Watchlist(ListingItem = listing1, Wuser = user)
        Watch.save()
    return listing(request)

def removewatchlist(request):
    list_id = request.GET.get('idlisti', None)
    user = request.user
    listing1 = Listing.objects.get(pk=list_id)
    try:
        w = Watchlist.objects.get(ListingItem = listing1, Wuser = user)
        w.delete()
    except Watchlist.DoesNotExist:
        pass

    return listing(request)

def watchlist(request):
    return render(request, "auctions/watchlist.html", {
        "all_list": Watchlist.objects.filter(Wuser = request.user),
    })

def close_listing(request):
    list_id = request.GET.get('idlisti', None)
    listi = Listing.objects.get(pk=list_id)
    listi.open = False
    listi.save()
    return listing(request)


