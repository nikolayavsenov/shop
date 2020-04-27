from django.contrib import admin
from .models import *

admin.site.register(Goods)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Cart)
admin.site.register(PromoCode)
admin.site.register(FavoriteGood)
admin.site.register(GoodsInCart)
admin.site.register(Order)