from django.contrib import admin
from .models import AuctionList, bids, Comments, User, watchlist

admin.site.register(AuctionList)
admin.site.register(bids)
admin.site.register(Comments)
admin.site.register(watchlist)
# Register your models here.
