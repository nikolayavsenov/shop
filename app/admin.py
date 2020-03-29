from django.contrib import admin
from .models import *
from rest_framework.authtoken.admin import TokenAdmin

admin.site.register(Goods)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Cart)
TokenAdmin.raw_id_fields = ['user']
