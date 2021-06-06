from django.contrib import admin

# Register your models here.
from .models import Category,Comment,Country,Post,Reply,FundingComment

admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Country)
admin.site.register(Reply)
admin.site.register(Post)
admin.site.register(FundingComment)