from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Organization, Account


class AccountInline(admin.StackedInline):
    model = Account
    can_delete = False
    verbose_name_plural = 'accounts'

class UserAdmin(BaseUserAdmin):
    inlines = (AccountInline, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Organization)
