"""
Database models.
"""
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Erstellt, speichert und gibt als Rückgabewert User zurück."""
        user = self.model(
            email=self.normalize_email(email), 
            **extra_fields
            )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Erstellt und gibt als Rückgabewert Superuser zurück."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    class Rolle(models.TextChoices):
        Admin = "Admin", 'Admin'
        Tutor = "Tutor", 'Tutor'
        Kursleiter = "Kursleiter", 'Kursleiter'
        Dozent = "Dozent", 'Dozent'

    base_user = Rolle.Admin

    rolle = models.CharField(("Rolle"), max_length=10, choices=Rolle.choices)
    email = models.EmailField(max_length=255, unique=True)
    vorname = models.CharField(max_length=255, blank=True)
    nachname = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    class Meta:
        verbose_name_plural = "Benutzer"

    USERNAME_FIELD = 'email'

    def save(self, *args, **kwargs):
        ##
        ###!!!!!!!!!
        # !!!!!!! base_user soll nur gespeichert werden, wenn es von dozent, kursleiter oder tutor gespeichert wird.
        if not self.id:
            self.rolle = self.base_user
            # email senden verifizieren active auf True setzen und
            # passwort setzen
        return super().save(*args, **kwargs)


###################################


class Kurs(models.Model):
    """Kurse im System"""
    kurs_name = models.CharField(max_length=50, unique=True)
    beschreibung = models.TextField(blank=True)
    ref_id = models.CharField(max_length=100)
    # dozent = models.ForeignKey(Dozent, on_delete=models.CASCADE, related_name='kurs')

    class Meta:
        verbose_name_plural = "Kurse"

    def __str__(self):
        return f"{self.kurs_name}"


class Blatt(models.Model):
    """Übungsblätter im System"""
    ass_name = models.CharField(max_length=200)
    ass_id = models.CharField(max_length=100, unique=True)
    kurs = models.ForeignKey(Kurs, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Übungsblätter"


###############################################


class TutorManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(rolle=User.Rolle.Tutor)


class Tutor(User):

    base_role = User.Rolle.Tutor

    Tutor = TutorManager()

    class Meta:
        proxy = True
        verbose_name_plural = "Tutoren"



@receiver(post_save, sender=Tutor)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.rolle == "Tutor":
        TutorProfile.objects.create(user=instance)


class TutorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tutor_id = models.IntegerField(null=True, blank=True)
    arbeitsstunden = models.FloatField(default=0)

    class Meta:
        verbose_name_plural = "Tutor Profil"

    def __str__(self):
        return f"{self.user.vorname} {self.user.nachname}"


#####################################



class KursleiterManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(rolle=User.Rolle.Kursleiter)


class Kursleiter(User):

    base_role = User.Rolle.Kursleiter

    Kursleiter = KursleiterManager()

    class Meta:
        proxy = True
        verbose_name_plural = "Kursleiter"



class KursleiterProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Kursleiter_id = models.IntegerField(null=True, blank=True)
    kurs = models.ForeignKey(Kurs, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Kursleiter Profil"

    def __str__(self):
        return f"{self.user.vorname} {self.user.nachname}"


@receiver(post_save, sender=Kursleiter)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.rolle == "Kursleiter":
        KursleiterProfile.objects.create(user=instance)


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

    titel = models.CharField(("Rolle"), max_length=10, choices=Titel.choices, default='Prof.')
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Dozent Profil"


@receiver(post_save, sender=Dozent)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.rolle == "Dozent":
        DozentProfile.objects.create(user=instance)




