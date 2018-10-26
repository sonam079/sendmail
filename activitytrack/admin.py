from django.contrib import admin
from activitytrack.models import UserLoginActivity, UserTemplatesUploadActivity


# Register your models here.


# Register your models here.
class UserLoginActivityModelAdmin(admin.ModelAdmin):
    # for displaying more thing in admin page
    list_display = ['id', 'login_username', 'status', 'login_datetime']
    # for displaying link with another attribute
    list_display_links = ['login_username']
    # for list filter
    list_filter = ['status', 'login_datetime', 'user_agent_info']
    # setting search field
    search_fields = ['login_username', 'id']

    class Meta:
        model = UserLoginActivity


admin.site.register(UserLoginActivity, UserLoginActivityModelAdmin)


class UserTemplatesUploadActivityAdmin(admin.ModelAdmin):
    # for displaying more thing in admin page
    list_display = ['id', 'request_track_user_id', 'request_user_name', 'timestamp']
    # for displaying link with another attribute
    list_display_links = ['id']
    # for list filter
    list_filter = ['timestamp']
    # setting search field
    search_fields = ['request_user_name', 'request_track_user_id']

    class Meta:
        model = UserTemplatesUploadActivity


admin.site.register(UserTemplatesUploadActivity, UserTemplatesUploadActivityAdmin)
