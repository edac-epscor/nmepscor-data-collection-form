from models import UserProfile, InvestigatorProfile

from django.contrib import admin
# Register your models here.


class UserProfileAdmin(admin.ModelAdmin):
    model = UserProfile
    can_delete = False
    verbose_name_plural = "User Admin"
    readonly_fields = ['user']

    # Monkey patch gettrs to retrieve foreign key
    def get_username(self, obj):
        return obj.user.username

    def get_first(self, obj):
        return obj.user.first_name

    def get_last(self, obj):
        return obj.user.last_name

    def has_add_permission(self, request):
        return False
        # No add button, this is hooked

    get_username.short_description = 'User Name'
    get_first.short_description = 'First Name'
    get_last.short_description = 'Last Name'

    list_display = [
        'get_username',
        'get_first',
        'get_last',
    ]


class InvestigatorProfileAdmin(admin.ModelAdmin):
    model = InvestigatorProfile
    verbose_name_plural = "My PIs"

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(InvestigatorProfile, InvestigatorProfileAdmin)
