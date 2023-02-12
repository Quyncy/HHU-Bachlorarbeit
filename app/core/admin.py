from django.contrib import admin
from core.models import *
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .forms import CostumUserCreationForm, CustomUserChangeForm


class CostumUserAdmin(UserAdmin):
    # add_form = CostumUserCreationForm
    # form = CustomUserChangeForm

    model = User

    list_display = ("email", "rolle","is_staff", "is_active", "is_superuser", "is_admin", "is_tutor", "is_kursleiter",)

    list_filter = ("email", "is_staff", "is_active", "is_superuser","is_admin", "is_tutor", "is_kursleiter",)
    
    fieldsets = (
        (None, {"fields": ("rolle","email", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser", "is_admin", "is_tutor", "is_kursleiter", 
        "groups", "user_permissions")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2", "rolle", "is_staff", "is_active",  "is_superuser","is_admin", "is_tutor", "is_kursleiter", "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)

# User-View
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


class KursleiterView(UserAdmin):
    # add_form = CostumUserCreationForm
    # form = CustomUserChangeForm
    model = Kursleiter
    
    list_display = ("email",  "kurs", "rolle","is_staff", "is_active", "is_superuser", "is_admin", "is_tutor", "is_kursleiter",)
    list_filter = ("email", "is_staff", "is_active", "is_superuser","is_admin", "is_tutor", "is_kursleiter",)
    fieldsets = (
        (None, {"fields": ("email",  "kurs", "rolle", "password")}), 
        ("Permissions", {"fields": 
            ("is_staff", 
            "is_active", 
            "is_superuser", 
            "is_admin", 
            "is_tutor", 
            "is_kursleiter", 
            "groups", 
            "user_permissions")}
        ),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email","kurs","rolle",  "password1", "password2", "is_staff", 
                "is_active",  "is_superuser","is_admin", "is_tutor", "is_kursleiter", "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


class TutorView(UserAdmin):
    # add_form = CostumUserCreationForm
    # form = CustomUserChangeForm

    model = Tutor

    list_display = ("email",  "tutor_id", "rolle", "kurs", "arbeitsstunden", "is_staff", "is_active", "is_superuser", "is_admin", "is_tutor", "is_kursleiter",)
    list_filter = ("email", "is_staff", "is_active", "is_superuser","is_admin", "is_tutor", "is_kursleiter",)
    
    fieldsets = (
        (None, 
            {"fields": 
                ("email",   "tutor_id", "rolle", "kurs", "arbeitsstunden",  "password")}), 
        ("Permissions", 
            {"fields": 
                ("is_staff", "is_active", "is_superuser", "is_admin", "is_tutor", "is_kursleiter", "groups", "user_permissions")
            }
        ),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "tutor_id", "kurs","rolle", "kurs", "arbeitsstunden", "password1", "password2", "is_staff", 
                "is_active",  "is_superuser","is_admin", "is_tutor", "is_kursleiter", "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)

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


admin.site.register(User, CostumUserAdmin) # UserConfigAdmin

admin.site.register(Dozent)
# admin.site.register(DozentProfile)

admin.site.register(Kursleiter, KursleiterView) # , KursleiterView
# admin.site.register(KursleiterProfile)

admin.site.register(Tutor, TutorView) # , TutorView
# admin.site.register(TutorProfile)

admin.site.register(Kurs) # , KursView
admin.site.register(Blatt)
