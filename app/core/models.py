"""
Datbank mMdels.
"""
from django.db import models
from django.conf import settings

from django.contrib.auth import get_user_model

from django.contrib.auth.models import (
    AbstractBaseUser, 
    BaseUserManager, 
    PermissionsMixin
)

from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extrafields):
        """Erstellt, speichert und gibt als Rückgabewert User zurück."""

        user = self.model(
            email=self.normalize_email(email), 
            **extrafields
            )
        print('Hier usermanager')
        print(password)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extrafields):
        """Erstellt und gibt als Rückgabewert Superuser zurück."""
        extrafields.setdefault('is_active', True)
        extrafields.setdefault('is_staff', True)
        extrafields.setdefault('is_superuser', True)
        extrafields.setdefault('is_admin', True)

        user = self.create_user(
            email, 
            password, 
            **extrafields
        )
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    class Rolle(models.TextChoices):
        Admin = "Admin", 'Admin'
        Tutor = "Tutor", 'Tutor'
        Kursleiter = "Kursleiter", 'Kursleiter'
        Dozent = "Dozent", 'Dozent'

    base_user=Rolle.Admin

    rolle = models.CharField(("Rolle"), max_length=10, choices=Rolle.choices)
    email = models.EmailField(max_length=255, unique=True)
    vorname = models.CharField(max_length=255, blank=True)
    nachname = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)

    is_admin = models.BooleanField(default=False)
    is_dozent = models.BooleanField(default=False)
    is_kursleiter = models.BooleanField(default=False)
    is_tutor = models.BooleanField(default=False)

    objects = UserManager()

    class Meta:
        verbose_name_plural = "Benutzer"

    USERNAME_FIELD = 'email'

    # def has_perm(self , perm, obj = None):
    #     return self.is_admin
      
    # def has_module_perms(self , app_label):
    #     return True

    # def save(self, *args, **kwargs):
    #     print('user save draußen')
    #     if not self.pk:
    #         print('ich war hier user save drinnen')
    #         print(self.base_user)
    #         self.rolle = self.rolle
    #         # email senden verifizieren active auf True setzen und
    #         # passwort setzen
    #         return super().save(*args, **kwargs)




###################################


class Kurs(models.Model):
    """Kurse im System"""
    kurs = models.CharField(max_length=50, unique=True)
    beschreibung = models.TextField(blank=True)
    ref_id = models.CharField(max_length=100, unique=True)
    # dozent = models.ForeignKey(Dozent, on_delete=models.CASCADE, related_name='kurs')

    class Meta:
        verbose_name_plural = "Kurse"

    def __str__(self):
        return f"{self.kurs}"


class Blatt(models.Model):
    """Übungsblätter im System"""
    ass_name = models.CharField(max_length=200)
    ass_id = models.CharField(max_length=100, unique=True)
    kurs = models.ForeignKey(Kurs, on_delete=models.CASCADE, default=None)

    class Meta:
        verbose_name_plural = "Übungsblätter"

    def __str__(self):
        return f"{self.ass_name}"
    



###############################################


class TutorManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args , **kwargs)
        queryset = queryset.filter(rolle = User.Rolle.Admin)
        return queryset


class Tutor(User):
    base_role = User.Rolle.Tutor

    objects = TutorManager()

    class Meta:
        proxy = True
        verbose_name_plural = "Tutoren"

    def save(self , *args , **kwargs):
        self.base_user = User.Rolle.Tutor
        self.is_tutor = True
        return super().save(*args , **kwargs)


class TutorProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    kurs = models.ForeignKey(Kurs, on_delete=models.CASCADE,null=True, blank=True)
    tutor_id = models.CharField(max_length=100, null=True, blank=True,default=None)
    arbeitsstunden = models.FloatField(default=0)

    class Meta:
        verbose_name_plural = "Tutor Profil"

    def __str__(self):
        return f"{self.user.email}"


#####################################


class KursleiterManager(models.Manager):

    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(rolle=User.Rolle.Kursleiter)


class Kursleiter(User):
    base_role = User.Rolle.Kursleiter

    objects = KursleiterManager()

    class Meta:
        proxy = True
        verbose_name_plural = "Kursleiter"

    def save(self  , *args , **kwargs):
        self.base_user = User.Rolle.Kursleiter
        self.is_kursleiter = True
        return super().save(*args , **kwargs)


class KursleiterProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    kurs = models.ForeignKey(Kurs, on_delete=models.CASCADE,null=True, blank=True)

    class Meta:
        verbose_name_plural = "Kursleiter Profil"

    def __str__(self):
        return f"{self.user.email}"


#########################


class Dozent(User):
    base_user = User.Rolle.Dozent

    class Meta:
        proxy = True
        verbose_name_plural="Dozenten"


class DozentProfile(models.Model):
    class Titel(models.TextChoices):
        Prof = "Prof", 'Prof'
        Dr = "Dr", 'Dr'

    titel = models.CharField(("Titel"), max_length=10, choices=Titel.choices, default='Prof.')
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Dozent Profil"

        
 #############

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance=None, created=False, **kwargs):
    if created and instance.is_kursleiter == True:
        print("Kursleiterprofil und Token wurde erstellt")
        KursleiterProfile.objects.create(user=instance)
        Token.objects.create(user=instance)
    if created and instance.is_tutor == True:
        print("Tutorprofil und Token wurde erstellt")
        print(instance.email)
        TutorProfile.objects.create(user=instance)
        Token.objects.create(user=instance)
    if created and instance.is_dozent == True:
        print("Dozent Profil und Token wurde erstellt")
        DozentProfile.objects.create(user=instance)
        Token.objects.create(user=instance)




# @receiver(post_save, sender=Dozent)
# def create_dozent_profile(sender, instance, created, **kwargs):
#     if created and instance.rolle == "Dozent":
#         DozentProfile.objects.create(user=instance)


# @receiver(post_save, sender=Kursleiter)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created and instance.rolle == "Kursleiter":
#         KursleiterProfile.objects.create(user=instance)



# @receiver(post_save, sender=Tutor)
# def create_tutor_profile(sender, instance=None, created=False, **kwargs):
#     if created and instance.rolle == "Tutor":
#         print('ich bin hier post save tutor profile')
#         TutorProfile.objects.create(user=instance)


# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
#     if created and instance.is_tutor == True:
#         print("1")
#         TutorProfile.objects.create(instance=instance)
#     if created and instance.rolle == "Kursleiter":
#         print("2")
#         KursleiterProfile.objects.create(user=instance)
#     if created and instance.rolle == "Tutor":
#         print("3")
#         TutorProfile.objects.create(user=instance)
#     if created and instance.rolle == "Dozent":
#         print("4")
#         DozentProfile.objects.create(user=instance)