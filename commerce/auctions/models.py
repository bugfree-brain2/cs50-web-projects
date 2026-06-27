from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class AuctionList(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField()
    image = models.CharField()
    start_bid = models.DecimalField(max_digits=10, decimal_places=2)
    active = models.BooleanField(default=True)
    catagory = models.CharField(default="")
    owners = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.title} | {self.description} | {self.image} | {self.start_bid} | {self.catagory} "
class bids(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ForeignKey(AuctionList, on_delete=models.CASCADE)
    bid_price = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return f"{self.user} | {self.products} | {self.bid_price}"
class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField()
    product_page = models.ForeignKey(AuctionList, on_delete=models.CASCADE)
class watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    watch_list = models.ManyToManyField(AuctionList)
    def __str__(self):
        return f"{self.user} | {self.watch_list}"