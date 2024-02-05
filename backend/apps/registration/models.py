from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    MALE = 1
    FEMALE = 2
    OTHER = 3
    GENDERS = CHOICES = (
        (MALE, "Male"),
        (FEMALE, "Female"),
        (OTHER, "Other"),
    )

    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    birth_date = models.DateField(verbose_name="Birth date", blank=True, null=True)
    gender = models.PositiveSmallIntegerField(
        verbose_name="Gender",
        choices=GENDERS,
        blank=True,
        null=True,
    )

    class Meta:
        app_label = "registration"


class Interest(models.Model):
    name = models.CharField(verbose_name="Name", max_length=255)
    users = models.ManyToManyField(User, related_name="interests")

    class Meta:
        app_label = "registration"
