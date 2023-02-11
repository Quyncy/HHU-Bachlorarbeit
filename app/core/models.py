"""
Datbank mMdels.
"""
from django.db import models

from django.conf import settings
from django.contrib.auth import get_user_model

from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)

from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework.authtoken.models import Token


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

    # base_user=Rolle.Admin

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

    def save(self, *args, **kwargs):
        if not self.id:
            print("models.py: usermanager save:")
            # print(self.base_user)
            # self.rolle = self.base_user
            # email senden verifizieren active auf True setzen und
            # passwort setzen
        return super().save(*args, **kwargs)


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
    kurs = models.ForeignKey(Kurs, on_delete=models.CASCADE, default=None, related_name="blatt")

    class Meta:
        verbose_name_plural = "Übungsblätter"

    def __str__(self):
        return f"{self.ass_name}"
    

##########################################

# class KursleiterManager(BaseUserManager):

#     def get_queryset(self, *args, **kwargs):
#         queryset = get_user_model().objects.filter(rolle = User.Rolle.Kursleiter)
#         return queryset


class Kursleiter(User):
    kurs = models.ForeignKey(Kurs, on_delete=models.CASCADE,null=True, blank=True, related_name="kursleiter")
    rolle = User.Rolle.Kursleiter

    class Meta:
        verbose_name_plural = "Kursleiter"



class KursleiterProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    kurs = models.ForeignKey(Kurs, on_delete=models.CASCADE,null=True, blank=True,related_name="kursleiterprofile")

    class Meta:
        verbose_name_plural = "Kursleiter Profil"

    def __str__(self):
        return f"{self.user.email}"


#########################


class Tutor(User):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    kurs = models.ForeignKey(Kurs, on_delete=models.CASCADE,null=True, blank=True,related_name="tutor")
    tutor_id = models.CharField(max_length=100, unique=True, null=True, blank=True,default=None)
    arbeitsstunden = models.FloatField(default=0)
    
    rolle = User.Rolle.Tutor

    class Meta:
        verbose_name_plural = "Tutoren"



class TutorProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    kurs = models.ForeignKey(Kurs, on_delete=models.CASCADE,null=True, blank=True, related_name="tutorprofile")
    tutor_id = models.CharField(max_length=100, unique=True, null=True, blank=True,default=None)
    arbeitsstunden = models.FloatField(default=0)

    class Meta:
        verbose_name_plural = "Tutor Profil"

    def __str__(self):
        return f"{self.user.email}"



#####################################



class Dozent(User):
    class Titel(models.TextChoices):
        Prof = "Prof", 'Prof'
        Dr = "Dr", 'Dr'

    titel = models.CharField(("Titel"), max_length=10, choices=Titel.choices, default='Prof.')
    rolle = User.Rolle.Dozent

    class Meta:
        verbose_name_plural = "Dozenten"
    


class DozentProfile(models.Model):
    class Titel(models.TextChoices):
        Prof = "Prof", 'Prof'
        Dr = "Dr", 'Dr'

    titel = models.CharField(("Titel"), max_length=10, choices=Titel.choices, default='Prof.')
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Dozent Profil"

        

 #############





@receiver(post_save, sender=User)
def create_profile(sender, instance=None, created=False, **kwargs):
    if created and instance.rolle == Kursleiter:
        print("Kursleiterprofil und Token wurde erstellt")
        # KursleiterProfile.objects.create(user=instance)
        Token.objects.create(user=instance)
    if created and instance.rolle == Tutor:
        print("Tutorprofil und Token wurde erstellt")
        # TutorProfile.objects.create(user=instance)
        Token.objects.create(user=instance)
    if created and instance.rolle == Dozent:
        print("Dozent Profil und Token wurde erstellt")
        # DozentProfile.objects.create(user=instance)
        Token.objects.create(user=instance)




@receiver(post_save, sender=Dozent)
def create_dozent_profile(sender, instance, created, **kwargs):
    if created and instance.rolle == "Dozent":
        # DozentProfile.objects.create(user=instance)
        Token.objects.create(user=instance)



@receiver(post_save, sender=Kursleiter)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.rolle == "Kursleiter":
        # KursleiterProfile.objects.create(user=instance)
        Token.objects.create(user=instance)



@receiver(post_save, sender=Tutor)
def create_tutor_profile(sender, instance=None, created=False, **kwargs):
    if created and instance.rolle == "Tutor":
        print('ich bin hier post save tutor profile')
        TutorProfile.objects.create(user=instance)
        Token.objects.create(user=instance)

