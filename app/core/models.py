"""
Datbankmodel.
"""
from django.db import models
from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.contrib.auth.hashers import make_password
from django.dispatch import receiver
from django.db.models.signals import post_save

# from guardian.shortcuts import assign_perm
# from rest_framework.authtoken.models import Token


class UserManager(BaseUserManager):
    """Manager für Benutzer."""

    def create_user(self, email, password, **extrafields):
        """
        Erstellt Benutzer mit email und gehashtes Passwort
        """
        if not email:
            raise ValueError('The given email must be set')

        user = self.model(
            email=self.normalize_email(email), 
            **extrafields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    # def create_user(self, email, password=None, **extra_fields):
    #     extra_fields.setdefault('is_superuser', False)
    #     return self._create_user(email, password, **extra_fields)

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
    """Benutzer in dem System."""
    class Rolle(models.TextChoices):
        Admin = "Admin", 'Admin'
        Tutor = "Tutor", 'Tutor'
        Kursleiter = "Kursleiter", 'Kursleiter'
        Dozent = "Dozent", 'Dozent'

    # base_user=Rolle.Admin

    rolle = models.CharField(("Rolle"), max_length=10, choices=Rolle.choices, default=Rolle.Admin)
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

    USERNAME_FIELD = 'email'

    # def save(self, *args, **kwargs):
    #     if not self.pk:
    #         print("models.py: usermanager save:")
    #         print()
    #         # print(self.base_user)
    #         # self.rolle = self.base_user
    #         # email senden verifizieren active auf True setzen und
    #         # passwort setzen
    #     return super().save(*args, **kwargs)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def set_password(self, password):
        self.password = make_password(password)




class Kursleiter(User):
    """ 
    Kursleiter im System
    """
    rolle = User.Rolle.Kursleiter

    class Meta:
        verbose_name_plural = "Kursleiter"

    def __str__(self):
        return f"{self.email}"



class Dozent(User):
    """ 
    Dozent im System
    """
    class Titel(models.TextChoices):
        Prof = "Prof", 'Prof'
        Dr = "Dr", 'Dr'

    titel = models.CharField(("Titel"), max_length=10, choices=Titel.choices, default='Prof.')
    rolle = User.Rolle.Dozent

    class Meta:
        verbose_name_plural = "Dozenten"



class Kurs(models.Model):
    """
    Kurse im System
    """
    kurs = models.CharField(max_length=50, unique=True)
    beschreibung = models.TextField()
    # dozent = models.OneToOneField(Dozent, on_delete=models.CASCADE, related_name='kurs_dozent')
    ref_id = models.CharField(max_length=100, unique=True)  # ref ID 1223794
    kursleiter = models.OneToOneField(Kursleiter, on_delete=models.CASCADE, related_name='kurs_kursleiter')

    class Meta:
        verbose_name_plural = "Kurse"

    def __str__(self):
        return f"{self.kurs}"



class Tutor(User):
    """ 
    Tutor im System
    """
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    kurs = models.ForeignKey(Kurs, on_delete=models.CASCADE,null=True, blank=True,related_name='tutor')
    tutor_id = models.CharField(max_length=100, unique=True, null=True, blank=True,default=None)
    arbeitsstunden = models.FloatField(default=0)
    
    rolle = User.Rolle.Tutor

    class Meta:
        verbose_name_plural = "Tutoren"



class Blatt(models.Model):
    """
    Übungsblätter der Studenten im System
    """
    kurs = models.ForeignKey(Kurs, on_delete=models.CASCADE, default=None, related_name="blatt")
    ass_name = models.CharField(max_length=200, help_text='Name des Übungsblatts')
    ass_id = models.CharField(max_length=100, unique=True)
    tutor_id = models.ForeignKey(User, on_delete=models.CASCADE)
    student = models.CharField(max_length=200)
    korrektur_notiz = models.TextField()

    class Meta:
        verbose_name_plural = "Übungsblätter"

    # def __str__(self):
    #     return f"{self.ass_name}"
    

class BlattKorrektur(models.Model):
    """
    Übungsblatt Status im System
    """
    ass_id = models.ForeignKey(Blatt, on_delete=models.CASCADE)
    tutor_id = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    total_points = models.FloatField(default=0) 




##########################################

# class KursleiterManager(BaseUserManager):

#     def get_queryset(self, *args, **kwargs):
#         queryset = get_user_model().objects.filter(rolle = User.Rolle.Kursleiter)
#         return queryset


#####################################


# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_dozent_profile(sender, instance, created, **kwargs):
#     if created:
#         # DozentProfile.objects.create(user=instance)
#         Token.objects.create(user=instance)



# @receiver(post_save, sender=Kursleiter)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created and instance.rolle == "Kursleiter":
#         # KursleiterProfile.objects.create(user=instance)
#         Token.objects.create(user=instance)



# @receiver(post_save, sender=Tutor)
# def create_tutor_profile(sender, instance=None, created=False, **kwargs):
#     if created and instance.rolle == "Tutor":
#         print('ich bin hier post save tutor profile')
#         # TutorProfile.objects.create(user=instance)
#         Token.objects.create(user=instance)


# @receiver(post_save, sender=Dozent)
# def create_dozent_profile(sender, instance, created, **kwargs):
#     if created and instance.rolle == "Dozent":
#         # DozentProfile.objects.create(user=instance)
#         Token.objects.create(user=instance)


####################################


# @receiver(post_save, sender=get_user_model())
# def create_profile(sender, instance=None, created=False, **kwargs):
#     if created and instance.rolle == 'Kursleiter':
#         print("Kursleiterprofil und Token wurde erstellt")
#         # KursleiterProfile.objects.create(user=instance)
#         Kursleiter.objects.create(email=instance.email)
#         Token.objects.create(user=instance)
#     if created and instance.rolle == 'Tutor':
#         print("Tutorprofil und Token wurde erstellt")
#         # TutorProfile.objects.create(user=instance)
#         Tutor.objects.create(user=instance)
#         Token.objects.create(user=instance)
#     if created and instance.rolle == 'Dozent':
#         print("Dozent Profil und Token wurde erstellt")
#         # DozentProfile.objects.create(user=instance)
#         Dozent.objects.create(user=instance)
#         Token.objects.create(user=instance)
