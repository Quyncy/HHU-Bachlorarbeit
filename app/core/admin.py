from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from core.models import *

# # User-View
# class UserAdminConfig(UserAdmin):
#     list_display = ('id', 'email', 'vorname', 'nachname', 'role', 'date_published', 'date_modified', )
#     list_filter = ('role',)
#     ordering = ('email',)

#     fieldsets = (
#         (None, {'fields':('email', 'vorname', 'nachname', 'role', )}),
#         ('Permissions', {
#             'fields': (
#                 'groups',
#                 ),
#         }),
#     )

#     add_fieldsets = (
#         (None, {
#             'classes': ('wide'),
#             'fields': ('email', 'vorname', 'nachname','groups', 'role', 'password1', 'password2', )
#         }),
#     )


# # Teacher-View
# class KursleiterView(UserAdmin):
#     list_display = ('email', 'vorname', 'nachname',  'role', 'kurs_name',)
#     list_filter = ('kurs_name',)
#     ordering = ('email', )

#     fieldsets = (
#         (None, {'fields':('vorname', 'nachname', 'email', 'role', 'kurs_name', )}),
#     )

#     add_fieldsets = (
#         (None, {
#             'classes': ('wide'),
#             'fields': ('email', 'vorname', 'nachname', 'role', 'kurs_name', 'password1', 'password2', )
#         }),
#     )


# class TutorView(UserAdmin):
#     list_display = ('email', 'vorname', 'nachname', 'tutor_id', 'role', 'kurs_name', 'arbeitsstunden', )
#     list_filter = ('email', 'vorname', 'nachname', )
#     ordering = ('email', )

#     fieldsets = (
#         (None, {'fields':('email', 'vorname', 'nachname', 'role', 'tutor_id', 'kurs_name', 'arbeitsstunden',)}),
#     )

#     add_fieldsets = (
#         (None, {
#             'classes': ('wide'),
#             'fields': ('email', 'vorname', 'nachname','role', 'tutor_id', 'kurs_name', 'arbeitsstunden', 'password1', 'password2', )
#         }),
#     )


# class KursView(admin.ModelAdmin):
#     list_display = ('kurs_name', 'dozent',)

# class ProfileView(admin.ModelAdmin):
#     list_display = ('email')


admin.site.register(User) # UserConfigAdmin

admin.site.register(Dozent)
admin.site.register(DozentProfile)

admin.site.register(Kursleiter) # , KursleiterView
admin.site.register(KursleiterProfile)

admin.site.register(Tutor) # , TutorView
admin.site.register(TutorProfile)

admin.site.register(Kurs) # , KursView
admin.site.register(Blatt)
