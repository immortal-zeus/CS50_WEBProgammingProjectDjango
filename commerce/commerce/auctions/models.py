from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    pass


class Categorys(models.Model):
    Categoryname = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.Categoryname}"

class Listing(models.Model):
    Title = models.CharField(max_length=50)
    Textdes = models.CharField(null=True , max_length=150)
    Category = models.ForeignKey(Categorys, on_delete=models.CASCADE, related_name="Similar")
    Imagelink = models.URLField(blank=True)
    time = models.DateTimeField(default=timezone.now)
    Luser =models.ForeignKey(User, on_delete=models.PROTECT, related_name="Creator")
    StartingBid = models.FloatField()
    CurrentBid = models.FloatField(blank=True, null=True)
    open = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.Title} : {self.Textdes} : {self.Category} : {self.StartingBid}"


class Comments(models.Model):
    Text = models.CharField(max_length=256)
    ListingItem = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="all_comments")
    Cuser = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.Cuser} : {self.Text}"

class Bids(models.Model):
    Listing_b = models.ForeignKey(Listing, on_delete=models.CASCADE)
    Bid = models.FloatField()
    Buser = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.Buser} : {self.Bid}"

class Watchlist(models.Model):
    ListingItem = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="WatchItem")
    Wuser = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.Wuser} : {self.ListingItem}"
