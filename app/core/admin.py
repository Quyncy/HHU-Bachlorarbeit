from django.contrib import admin
from core.models import *

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group
from django.utils.translation import gettext_lazy as _

# from .forms import KursForm, BlattForm, CostumUserCreationForm, CustomUserChangeForm
from .forms import *

from guardian.admin import GuardedModelAdmin
from guardian.shortcuts import get_objects_for_user


# class ReadOnlyAdminMixin:

#     def has_add_permission(self, request):
#         return False

#     def has_change_permission(self, request, obj=None):
#         #
#         #
#         #
#         if request.user.has_perm('kurs.change_kurs'):
#             return False
#         else:
#             return False

#     def has_delete_permission(self, request, obj=None):
#         return False

#     def has_view_permission(self, request, obj=None):
#         return False



class Custom_Disable_Perm(GuardedModelAdmin):

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser

        if not is_superuser:
            #form.base_fields['rolle'].disabled = False
            form.base_fields['is_staff'].disabled = True
            form.base_fields['is_admin'].disabled = True
            form.base_fields['is_superuser'].disabled = True
            form.base_fields['is_kursleiter'].disabled = True
            form.base_fields['user_permissions'].disabled = True
            form.base_fields['groups'].disabled = True
        return form


# class Custom_User_Perm(GuardedModelAdmin):

#     def has_module_permission(self, request):
#         if super().has_module_permission(request):
#             return True
#         return self.get_model_objects(request).exists()

#     def get_queryset(self, request):
#         if request.user.is_superuser:
#             return super().get_queryset(request)
#         data = self.get_model_objects(request)
#         print('Data: ')
#         print(data)
#         return data

#     def get_model_objects(self, request, action=None, klass=None):
#         # options um meta daten zu erhalten
#         opts = self.opts
#         actions = [action] if action else ['view','edit','delete']
#         klass = klass if klass else opts.model
#         model_name = klass._meta.model_name
#         print("-----------------------------")
#         print("OPTS: ") # core.user
#         print(opts)
#         print("KLASS: ")  # Model KlASSE <class 'core.models.Kurs'>
#         print(klass)
#         print("Model_name: ")   # kurs
#         print(model_name)
#         print("actions: ")  # ['view', 'edit', 'delete']
#         print(actions)
#         return get_objects_for_user(user=request.user, perms=[f'{perm}_{model_name}' for perm in actions], klass=klass, any_perm=True)

#     def has_permission(self, request, obj, action):
#         opts = self.opts
#         code_name = f'{action}_{opts.model_name}'
#         print('----------- Codename:  -------------')
#         print(code_name)
#         if obj:
#             return request.user.has_perm(f'{opts.app_label}.{code_name}', obj)
#         else:
#             return self.get_model_objects(request).exists()

#     def has_view_permission(self, request, obj=None):
#         return self.has_permission(request, obj, 'view')

#     def has_change_permission(self, request, obj=None):
#         return self.has_permission(request, obj, 'change')

#     def has_delete_permission(self, request, obj=None):
#         return self.has_permission(request, obj, 'delete')






@admin.register(User)
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






class KursleiterView(UserAdmin):
    # add_form = CostumUserCreationForm
    # form = CustomUserChangeForm
    model = Kursleiter

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(email=request.user.email)
            
    list_display = ("email", "rolle","is_staff", "is_active", "is_superuser", "is_admin", "is_tutor", "is_kursleiter",)
    list_filter = ("email", "is_staff", "is_active", "is_superuser","is_admin", "is_tutor", "is_kursleiter",)
    fieldsets = (
        (None, {"fields": ("email", "rolle", "password")}), 
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
                "email","rolle",  "password1", "password2", "is_staff", 
                "is_active",  "is_superuser","is_admin", "is_tutor", "is_kursleiter", "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)
admin.site.register(Kursleiter, KursleiterView)






class DozentView(UserAdmin):
    # add_form = CostumUserCreationForm
    # form = CustomUserChangeForm
    model = Dozent

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(email=request.user.email)
            
    list_display = ("email", "rolle","is_staff", "is_active",)
    list_filter = ("email", "is_staff", "is_active", "is_dozent")
    fieldsets = (
        (None, {"fields": ("email", "rolle", "password")}), 
        ("Permissions", {"fields": 
            ("is_staff", 
            "is_active", 
            "is_dozent",  
            "groups", 
            "user_permissions")}
        ),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "rolle",  "password1", "password2", "is_staff", 
                "is_active",  "is_dozent", "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)
admin.site.register(Dozent, DozentView)







class TutorView(UserAdmin, Custom_Disable_Perm):
    # add_form = CostumUserCreationForm
    # form = CustomUserChangeForm

    model = Tutor

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(email=request.user.email)


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
                "email", "tutor_id", "kurs","rolle", "arbeitsstunden", "password1", "password2", "is_staff", 
                "is_active",  "is_superuser","is_admin", "is_tutor", "is_kursleiter", "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)
admin.site.register(Tutor, TutorView)
# @admin.register(Tutor)
# class TutorAdmin(GuardedModelAdmin):
#     form = TutorForm
#     list_display = ('vorname', 'nachname', 'tutor_id', 'kurs',)
#     list_odering = ('tutor_id',)

#     def has_module_permission(self, request) -> bool:
#         if super().has_module_permission(request):
#             return super().has_module_permission(request)

#     def get_queryset(self, request):
#         if request.user.is_superuser:
#             return super().get_queryset(request)
#         data = self.get_model_objects(request)
#         return data

#     def get_model_objects(self, request, action=None, klass=None):
#         opts = self.opts
#         actions = [actions] if action else ['view', 'edit', 'delete']
#         klass = klass if klass else opts.model
#         model_name = klass._meta.model_name
#         # print("OPTS: ")
#         # print(opts)
#         # print("KLASS: ")
#         # print(klass)
#         # print("Model_name: ")
#         # print(model_name)
#         # print("actions: ")
#         # print(actions)
#         return get_objects_for_user(user=request.user, perms=[f"{perm}_{model_name}" for perm in actions], klass=klass,any_perm=True)

#     def has_permissions(self, request, obj, action):
#         opts = self.opts
#         code_name = f'{action}_{opts.model_name}'
#         print(code_name)
#         if obj:
#             return request.user.has_perm(f'{opts.app_label}.{code_name}', obj)
#         else:
#             return self.get_model_objects(request).exists()

#     def has_add_permission(self, request=None) -> bool:
#         return self.has_add_permission(request)

#     def has_change_permission(self, request, obj=None) -> bool:
#         return self.has_change_permission(request, obj)

#     def has_delete_permission(self, request, obj=None) -> bool:
#         return self.has_delete_permission(request, obj)
    






# admin.site.register(Kurs, KursView)
@admin.register(Kurs)
class KursAdmin(admin.ModelAdmin):
    form = KursForm
    list_display = ('kurs', 'beschreibung','ref_id',)






class BlattAdmin(admin.ModelAdmin):
    form = BlattForm

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(kurs=request.user.kurs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "car":
            kwargs["queryset"] = Blatt.objects.filter(tutor_id=request.user.tutor_id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    fieldsets = (
        ('Bereich 1', {
            'fields': ('kurs', 'ass_name'), 
            'description': "Das hier ist der Übungsblätter Bereich",
        }),
        ('Bereich 2', {
            'fields': ('ass_id',)
        }),
    )

#admin.site.register(Blatt, BlattAdmin)
@admin.register(Blatt)
class Blatt_Admin(admin.ModelAdmin):
    model = Blatt
    list_display = ('ass_name', 'kurs', )

    # def get_queryset(self, request):
    #     qs = super().get_queryset(request)
    #     if request.user.is_superuser():
    #         return qs
    #     return qs.filter(kurs=request.user.kurs)





admin.site.register(BlattKorrektur)





