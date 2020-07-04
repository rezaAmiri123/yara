from django.contrib import admin

from users.models import User, City, TimeZone, UserAccess


class UserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'is_active', 'is_admin')
    list_filter = ('is_active', 'is_admin')


class TimeZoneAdmin(admin.ModelAdmin):
    list_display = ('name',)


class CityAdmin(admin.ModelAdmin):
    list_display = ('city',)


class UserAccessAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type')
    list_filter = ('user_type',)


admin.site.register(UserAccess, UserAccessAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(TimeZone, TimeZoneAdmin)
