from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Categorys)
admin.site.register(Listing)
admin.site.register(Bids)
admin.site.register(Comments)
admin.site.register(Watchlist)