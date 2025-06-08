from django.contrib import admin
from .models import MarketPost, MarketComment

# Register your models here.
admin.site.register(MarketPost)
admin.site.register(MarketComment)
