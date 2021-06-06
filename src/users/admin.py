from django.contrib import admin
from .models import NewUser
from django.contrib.auth.admin import UserAdmin
# Register your models here.


class UserAdminConfig(UserAdmin):
    search_fields = ('email','user_name',)
    ordering = ('-start_date',)
    list_filter = ('is_superuser','is_staff','is_investor')
    list_display = ('email','user_name','is_superuser','is_staff','is_investor')
    fieldsets = (
        (None, {'fields': ('email','user_name','first_name')}),
        ('Permissions',{'fields': ('is_superuser','is_staff','is_investor')}),
        ('Company Fields',{'fields': ('company_name','company_code','company_site')})
    )
    add_fieldsets = (
        ( None,{
            'classes':('wide',),
            'fields':('email','user_name','first_name','last_name','password1','password2','is_investor','is_staff','company_name','company_code','company_site')}
        ),
    )

admin.site.register(NewUser,UserAdminConfig)